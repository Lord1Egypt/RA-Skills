"""
Authentication module for OlaXBT Nexus API.
Handles wallet-based authentication and JWT token management.
"""

import os
import json
import time
import logging
from typing import Optional, Dict, Any
from dataclasses import dataclass, field

import requests
from web3 import Web3
from web3.auto import w3

from .exceptions import (
    AuthenticationError,
    WalletError,
    TokenError,
    ValidationError,
    RateLimitError,
)
from .security import (
    SecurityConfig,
    TokenEncryptor,
    validate_wallet_address,
    validate_private_key,
    sanitize_error_message,
    generate_request_id,
)

logger = logging.getLogger(__name__)


def _jwt_placeholder_id(token: str) -> str:
    """Return a short placeholder for rate limiting when using JWT (no wallet in skill)."""
    if not token or len(token) < 8:
        return "jwt"
    return f"jwt:{token[-8:]}"  # last 8 chars only, no secret


@dataclass
class AuthState:
    """Authentication state container."""
    
    jwt_token: Optional[str] = None
    token_expiry: Optional[float] = None
    wallet_address: Optional[str] = None
    last_auth_time: Optional[float] = None
    auth_count: int = 0


class NexusAuth:
    """Handle authentication with OlaXBT Nexus API."""
    
    def __init__(
        self,
        wallet_address: str,
        private_key: str,
        auth_url: str,
        security_config: SecurityConfig,
    ):
        """
        Initialize authentication client.
        
        Args:
            wallet_address: Ethereum wallet address
            private_key: Ethereum private key
            auth_url: Authentication API URL
            security_config: Security configuration
            
        Raises:
            ValidationError: If credentials are invalid
        """
        # Validate inputs
        if not validate_wallet_address(wallet_address):
            raise ValidationError(
                f"Invalid wallet address format: {wallet_address[:20]}..."
            )
        
        if not validate_private_key(private_key):
            raise ValidationError(
                "Invalid private key format. Should be 0x + 64 hex characters"
            )
        
        # Store credentials
        self.wallet_address = wallet_address
        self.private_key = private_key
        self.auth_url = auth_url.rstrip("/")
        self.security_config = security_config
        
        # Initialize state
        self.state = AuthState(wallet_address=wallet_address)
        
        # Initialize encryption if enabled
        self.encryptor = None
        if security_config.encrypt_jwt and security_config.encryption_key:
            self.encryptor = TokenEncryptor(security_config.encryption_key)
        
        # Initialize Web3
        try:
            self.web3 = Web3()
        except Exception as e:
            raise WalletError(f"Failed to initialize Web3: {str(e)}")
        
        logger.info(f"Auth client initialized for wallet: {wallet_address[:10]}...")
    
    def authenticate(self) -> str:
        """
        Authenticate with the Nexus API and get JWT token.
        
        Returns:
            JWT token string
            
        Raises:
            AuthenticationError: If authentication fails
            RateLimitError: If rate limit is exceeded
        """
        # Check if we have a valid token
        if self._is_token_valid():
            logger.debug("Using cached JWT token")
            return self.state.jwt_token
        
        try:
            # Step 1: Get auth message (nonce)
            auth_message = self._get_auth_message()
            
            # Step 2: Sign message with wallet
            signature = self._sign_message(auth_message)
            
            # Step 3: Get JWT token
            jwt_token = self._get_jwt_token(auth_message, signature)
            
            # Step 4: Store token securely
            self._store_token(jwt_token)
            
            # Update state
            self.state.last_auth_time = time.time()
            self.state.auth_count += 1
            
            logger.info(f"Authentication successful for {self.wallet_address[:10]}...")
            return jwt_token
            
        except RateLimitError:
            raise
        except Exception as e:
            error_msg = sanitize_error_message(str(e))
            logger.error(f"Authentication failed: {error_msg}")
            raise AuthenticationError(f"Authentication failed: {error_msg}")
    
    def _get_auth_message(self) -> str:
        """
        Get authentication message (nonce) from API.
        
        Returns:
            Authentication message to sign
            
        Raises:
            AuthenticationError: If API request fails
        """
        endpoint = f"{self.auth_url}/auth/message"
        
        try:
            response = requests.post(
                endpoint,
                json={"address": self.wallet_address},
                timeout=self.security_config.timeout,
            )
            
            if response.status_code == 429:
                raise RateLimitError("Rate limit exceeded for auth message")
            
            response.raise_for_status()
            data = response.json()
            
            if not data.get("success"):
                raise AuthenticationError(
                    f"Failed to get auth message: {data.get('message', 'Unknown error')}"
                )
            
            return data["message"]
            
        except requests.exceptions.RequestException as e:
            raise AuthenticationError(f"Network error: {str(e)}")
    
    def _sign_message(self, message: str) -> str:
        """
        Sign message with Ethereum wallet.
        
        Args:
            message: Message to sign
            
        Returns:
            Hex-encoded signature
            
        Raises:
            WalletError: If signing fails
        """
        try:
            # Use personal_sign (EIP-191)
            signed = w3.eth.account.sign_message(
                text=message,
                private_key=self.private_key,
            )
            
            return signed.signature.hex()
            
        except Exception as e:
            raise WalletError(f"Failed to sign message: {str(e)}")
    
    def _get_jwt_token(self, auth_message: str, signature: str) -> str:
        """
        Exchange signature for JWT token.
        
        Args:
            auth_message: Original auth message
            signature: Signed message
            
        Returns:
            JWT token
            
        Raises:
            AuthenticationError: If token exchange fails
        """
        endpoint = f"{self.auth_url}/auth/wallet"
        
        try:
            # Extract nonce from message (simplified)
            import re
            nonce_match = re.search(r"Nonce:\s*([^\n]+)", auth_message)
            nonce = nonce_match.group(1).strip() if nonce_match else ""
            
            response = requests.post(
                endpoint,
                json={
                    "address": self.wallet_address,
                    "message": auth_message,
                    "signature": signature,
                    "nonce": nonce,
                },
                timeout=self.security_config.timeout,
            )
            
            if response.status_code == 429:
                raise RateLimitError("Rate limit exceeded for token exchange")
            
            response.raise_for_status()
            data = response.json()
            
            if not data.get("success"):
                raise AuthenticationError(
                    f"Failed to get JWT: {data.get('message', 'Unknown error')}"
                )
            
            return data["token"]
            
        except requests.exceptions.RequestException as e:
            raise AuthenticationError(f"Network error: {str(e)}")
    
    def _store_token(self, token: str) -> None:
        """
        Store JWT token securely.
        
        Args:
            token: JWT token to store
        """
        if self.encryptor:
            encrypted_token = self.encryptor.encrypt(token)
            self.state.jwt_token = encrypted_token
        else:
            self.state.jwt_token = token
        
        # Set expiry time
        self.state.token_expiry = time.time() + self.security_config.jwt_ttl
        
        logger.debug("JWT token stored securely")
    
    def _get_decrypted_token(self) -> Optional[str]:
        """
        Get decrypted JWT token.
        
        Returns:
            Decrypted JWT token or None
        """
        if not self.state.jwt_token:
            return None
        
        if self.encryptor:
            try:
                return self.encryptor.decrypt(self.state.jwt_token)
            except TokenError:
                logger.warning("Failed to decrypt token, clearing cache")
                self.clear_token()
                return None
        
        return self.state.jwt_token
    
    def _is_token_valid(self) -> bool:
        """
        Check if current JWT token is valid.
        
        Returns:
            True if token is valid and not expired
        """
        if not self.state.jwt_token or not self.state.token_expiry:
            return False
        
        # Check expiry
        if time.time() >= self.state.token_expiry:
            logger.debug("JWT token expired")
            return False
        
        # Try to decrypt if encrypted
        token = self._get_decrypted_token()
        if not token:
            return False
        
        # Basic JWT validation (check format)
        parts = token.split(".")
        if len(parts) != 3:
            logger.warning("Invalid JWT format")
            return False
        
        return True
    
    def get_token(self) -> str:
        """
        Get valid JWT token, refreshing if necessary.
        
        Returns:
            Valid JWT token
            
        Raises:
            AuthenticationError: If no valid token and authentication fails
        """
        if self._is_token_valid():
            return self._get_decrypted_token()
        
        # Token invalid or expired, re-authenticate
        return self.authenticate()
    
    def clear_token(self) -> None:
        """Clear stored JWT token."""
        self.state.jwt_token = None
        self.state.token_expiry = None
        logger.debug("JWT token cleared")
    
    def get_auth_headers(self) -> Dict[str, str]:
        """
        Get authentication headers for API requests.
        
        Returns:
            Dictionary with Authorization header
            
        Raises:
            AuthenticationError: If authentication fails
        """
        token = self.get_token()
        return {
            "Authorization": f"Bearer {token}",
            "X-Request-ID": generate_request_id(),
            "X-Wallet-Address": self.wallet_address,
        }
    
    def get_credits_balance(self) -> Dict[str, Any]:
        """
        Get current credits balance.
        
        Returns:
            Dictionary with credits information
            
        Raises:
            AuthenticationError: If API request fails
        """
        endpoint = f"{self.auth_url}/credits/balance"
        
        try:
            headers = self.get_auth_headers()
            
            response = requests.get(
                endpoint,
                headers=headers,
                timeout=self.security_config.timeout,
            )
            
            if response.status_code == 429:
                raise RateLimitError("Rate limit exceeded for credits check")
            
            response.raise_for_status()
            data = response.json()
            
            if not data.get("success"):
                raise AuthenticationError(
                    f"Failed to get credits balance: {data.get('message', 'Unknown error')}"
                )
            
            return data
            
        except requests.exceptions.RequestException as e:
            raise AuthenticationError(f"Network error: {str(e)}")


class NexusAuthJWT:
    """
    JWT-only authentication for Nexus API.
    Uses a pre-obtained JWT (e.g. from the auth flow in the Nexus Skills API spec).
    The skill does not handle private keys; obtain the JWT outside the skill.
    """

    def __init__(
        self,
        jwt_token: str,
        auth_url: str,
        security_config: SecurityConfig,
        wallet_address: Optional[str] = None,
    ):
        self._jwt = jwt_token.strip()
        if not self._jwt:
            raise ValidationError("NEXUS_JWT must be a non-empty JWT string.")
        parts = self._jwt.split(".")
        if len(parts) != 3:
            raise ValidationError("NEXUS_JWT must be a valid JWT (three parts).")
        self.auth_url = auth_url.rstrip("/")
        self.security_config = security_config
        self.wallet_address = wallet_address or _jwt_placeholder_id(self._jwt)
        self.state = AuthState(jwt_token=self._jwt, wallet_address=self.wallet_address)
        self.state.token_expiry = time.time() + security_config.jwt_ttl
        logger.info("Auth client initialized with JWT (no private key in skill).")

    def authenticate(self) -> str:
        return self.get_token()

    def get_token(self) -> str:
        return self._jwt

    def clear_token(self) -> None:
        pass  # JWT is provided by env; nothing to clear in skill

    def get_auth_headers(self) -> Dict[str, str]:
        return {
            "Authorization": f"Bearer {self._jwt}",
            "X-Request-ID": generate_request_id(),
            "X-Wallet-Address": self.wallet_address,
        }

    def get_credits_balance(self) -> Dict[str, Any]:
        endpoint = f"{self.auth_url}/credits/balance"
        try:
            headers = self.get_auth_headers()
            response = requests.get(
                endpoint,
                headers=headers,
                timeout=self.security_config.timeout,
            )
            if response.status_code == 429:
                raise RateLimitError("Rate limit exceeded for credits check")
            response.raise_for_status()
            data = response.json()
            if not data.get("success"):
                raise AuthenticationError(
                    f"Failed to get credits balance: {data.get('message', 'Unknown error')}"
                )
            return data
        except requests.exceptions.RequestException as e:
            raise AuthenticationError(f"Network error: {str(e)}")