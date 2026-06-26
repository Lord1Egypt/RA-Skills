"""
EIP-712 Message Construction Helpers
"""

import secrets
import time
from dataclasses import dataclass
from typing import Any


def generate_nonce() -> str:
    """
    Generate a random 32-byte nonce for authorization
    
    Returns:
        str: Hex string starting with 0x
    """
    return "0x" + secrets.token_hex(32)


def generate_expires_at(duration_seconds: int = 3600) -> str:
    """
    Generate expiration timestamp
    
    Args:
        duration_seconds: Duration in seconds (default: 1 hour)
        
    Returns:
        str: Unix timestamp as string
    """
    return str(int(time.time()) + duration_seconds)


def get_eip712_domain(chain_id: int | str) -> dict[str, Any]:
    """
    EIP-712 Domain for GStable AI Payment
    
    Args:
        chain_id: Chain ID
        
    Returns:
        dict: EIP-712 domain object
    """
    return {
        "name": "aipay.gstable.io",
        "version": "1",
        "chainId": int(chain_id),
    }


# EIP-712 Types for PaymentSessionCreationAuthorization
PAYMENT_SESSION_CREATION_TYPES = {
    "PaymentSessionCreationAuthorization": [
        {"name": "purpose", "type": "string"},
        {"name": "linkId", "type": "string"},
        {"name": "linkVersion", "type": "string"},
        {"name": "merchantId", "type": "string"},
        {"name": "payer", "type": "address"},
        {"name": "paymentChainId", "type": "uint256"},
        {"name": "paymentToken", "type": "address"},
        {"name": "amount", "type": "uint256"},
        {"name": "authorizationNonce", "type": "bytes32"},
        {"name": "authorizationExpiresAt", "type": "uint256"},
    ]
}

# EIP-712 Types for PreparePaymentAuthorization
PREPARE_PAYMENT_TYPES = {
    "PreparePaymentAuthorization": [
        {"name": "purpose", "type": "string"},
        {"name": "sessionId", "type": "string"},
        {"name": "merchantId", "type": "string"},
        {"name": "paymentChainId", "type": "uint256"},
        {"name": "paymentToken", "type": "address"},
        {"name": "payer", "type": "address"},
        {"name": "payerEmail", "type": "string"},
        {"name": "authorizationNonce", "type": "bytes32"},
        {"name": "authorizationExpiresAt", "type": "uint256"},
    ]
}


@dataclass
class PaymentSessionCreationAuthorizationMessage:
    """Helper class for constructing PaymentSessionCreationAuthorization messages"""
    
    link_id: str
    link_version: str
    merchant_id: str
    payer: str
    payment_chain_id: int
    payment_token: str
    amount: int
    authorization_nonce: str
    authorization_expires_at: int
    
    @property
    def purpose(self) -> str:
        return "create_payment_session"
    
    def to_message(self) -> dict[str, Any]:
        """
        Convert to message dict for API
        
        Returns:
            dict: Message object
        """
        return {
            "purpose": self.purpose,
            "linkId": self.link_id,
            "linkVersion": self.link_version,
            "merchantId": self.merchant_id,
            "payer": self.payer,
            "paymentChainId": str(self.payment_chain_id),
            "paymentToken": self.payment_token,
            "amount": str(self.amount),
            "authorizationNonce": self.authorization_nonce,
            "authorizationExpiresAt": str(self.authorization_expires_at),
        }
    
    def to_signable_message(self) -> dict[str, Any]:
        """
        Convert to signable message for EIP-712
        
        Returns:
            dict: Signable message object with correct types
        """
        return {
            "purpose": self.purpose,
            "linkId": self.link_id,
            "linkVersion": self.link_version,
            "merchantId": self.merchant_id,
            "payer": self.payer,
            "paymentChainId": self.payment_chain_id,
            "paymentToken": self.payment_token,
            "amount": self.amount,
            "authorizationNonce": bytes.fromhex(self.authorization_nonce[2:]),
            "authorizationExpiresAt": self.authorization_expires_at,
        }


@dataclass
class PreparePaymentAuthorizationMessage:
    """Helper class for constructing PreparePaymentAuthorization messages"""
    
    session_id: str
    merchant_id: str
    payer: str
    payer_email: str
    payment_chain_id: int
    payment_token: str
    authorization_nonce: str
    authorization_expires_at: int
    
    @property
    def purpose(self) -> str:
        return "prepare_payment"
    
    def to_message(self) -> dict[str, Any]:
        """
        Convert to message dict for API
        
        Returns:
            dict: Message object
        """
        return {
            "purpose": self.purpose,
            "sessionId": self.session_id,
            "merchantId": self.merchant_id,
            "payer": self.payer,
            "payerEmail": self.payer_email,
            "paymentChainId": str(self.payment_chain_id),
            "paymentToken": self.payment_token,
            "authorizationNonce": self.authorization_nonce,
            "authorizationExpiresAt": str(self.authorization_expires_at),
        }
    
    def to_signable_message(self) -> dict[str, Any]:
        """
        Convert to signable message for EIP-712
        
        Returns:
            dict: Signable message object with correct types
        """
        return {
            "purpose": self.purpose,
            "sessionId": self.session_id,
            "merchantId": self.merchant_id,
            "paymentChainId": self.payment_chain_id,
            "paymentToken": self.payment_token,
            "payer": self.payer,
            "payerEmail": self.payer_email,
            "authorizationNonce": bytes.fromhex(self.authorization_nonce[2:]),
            "authorizationExpiresAt": self.authorization_expires_at,
        }
