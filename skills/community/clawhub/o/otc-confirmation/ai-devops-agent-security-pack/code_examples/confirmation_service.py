"""
OTC Confirmation Service — HMAC-Bound Implementation

A production-grade confirmation service that binds codes to specific operations
using HMAC, stores only hashes (never plaintext), and enforces single-use semantics.

Usage:
    service = ConfirmationService(secret_key="your-secret-key")
    
    # Generate a bound confirmation code
    code, token = service.generate(
        operation_type="send_email",
        parameters={"to": "alice@example.com", "subject": "Hello"}
    )
    # → Send `code` to human via secure channel (email)
    # → Store `token` for verification
    
    # Verify the code
    result = service.verify(
        user_code="cf-x7m2",
        token=token,
        operation_type="send_email",
        parameters={"to": "alice@example.com", "subject": "Hello"}
    )
    # → result.verified == True/False

Requirements:
    Python 3.10+
    No external dependencies (stdlib only)
"""

import hashlib
import hmac
import json
import os
import secrets
import string
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional


# =============================================================
# Configuration
# =============================================================

@dataclass
class OTCConfig:
    """Configuration for the confirmation service."""
    code_length: int = 4                    # Characters after "cf-" prefix
    code_charset: str = string.ascii_lowercase + string.digits  # a-z0-9
    code_prefix: str = "cf-"
    expiry_seconds: int = 600               # 10 minutes
    max_attempts: int = 5                   # Before lockout
    lockout_seconds: int = 300              # 5 minutes
    state_dir: Optional[str] = None         # Auto-detect if None
    
    def __post_init__(self):
        if self.state_dir is None:
            tmpdir = os.environ.get("TMPDIR", "/tmp")
            self.state_dir = os.path.join(tmpdir, f"otc_state_{os.getuid()}")


# =============================================================
# Data Models
# =============================================================

@dataclass
class PendingConfirmation:
    """A pending confirmation waiting for user verification."""
    code_hash: str              # SHA-256 of the code (never store plaintext)
    operation_hash: str         # SHA-256 of operation_type + parameters
    binding: str                # HMAC(secret, code + operation_hash)
    created_at: float           # Unix timestamp
    expires_at: float           # Unix timestamp
    attempts: int = 0           # Failed verification attempts
    session_id: str = ""        # Session that created this confirmation


@dataclass
class VerificationResult:
    """Result of a verification attempt."""
    verified: bool
    reason: str
    attempts_remaining: int = 0
    locked_until: Optional[float] = None


# =============================================================
# Confirmation Service
# =============================================================

class ConfirmationService:
    """HMAC-bound one-time confirmation service.
    
    Security properties:
    1. Codes are never stored in plaintext (only SHA-256 hashes)
    2. Codes are bound to specific operations via HMAC
    3. Codes are single-use (consumed on successful verification)
    4. Brute-force protection via attempt limiting and lockout
    5. Automatic expiry (default 10 minutes)
    """
    
    def __init__(self, secret_key: str, config: Optional[OTCConfig] = None):
        self.secret_key = secret_key
        self.config = config or OTCConfig()
        self._pending: dict[str, PendingConfirmation] = {}
        self._lockouts: dict[str, float] = {}  # session_id -> locked_until
        
        # Ensure state directory exists with restrictive permissions
        state_path = Path(self.config.state_dir)
        state_path.mkdir(mode=0o700, parents=True, exist_ok=True)
    
    def generate(
        self, 
        operation_type: str, 
        parameters: dict,
        session_id: str = ""
    ) -> tuple[str, str]:
        """Generate a confirmation code bound to an operation.
        
        Args:
            operation_type: Type of operation (e.g., "send_email", "deploy")
            parameters: Operation parameters (used for binding)
            session_id: Session identifier for rate limiting
            
        Returns:
            (code, token) — Send code to human, keep token for verification
            
        Raises:
            RateLimitError: If session is locked out
        """
        # Check lockout
        if session_id in self._lockouts:
            if time.time() < self._lockouts[session_id]:
                remaining = int(self._lockouts[session_id] - time.time())
                raise RateLimitError(
                    f"Session locked out. Try again in {remaining} seconds."
                )
            del self._lockouts[session_id]
        
        # Generate random code
        code = self.config.code_prefix + ''.join(
            secrets.choice(self.config.code_charset) 
            for _ in range(self.config.code_length)
        )
        
        # Compute hashes
        code_hash = self._hash(code.lower())
        operation_hash = self._hash_operation(operation_type, parameters)
        
        # Create HMAC binding: proves this code was generated for this operation
        binding = hmac.new(
            self.secret_key.encode(),
            f"{code_hash}:{operation_hash}".encode(),
            hashlib.sha256
        ).hexdigest()
        
        # Generate token (public identifier for this pending confirmation)
        token = secrets.token_hex(16)
        
        # Store pending confirmation (never stores plaintext code)
        now = time.time()
        self._pending[token] = PendingConfirmation(
            code_hash=code_hash,
            operation_hash=operation_hash,
            binding=binding,
            created_at=now,
            expires_at=now + self.config.expiry_seconds,
            session_id=session_id,
        )
        
        # Also write to state file for shell script compatibility
        self._write_state_file(code, token)
        
        return code, token
    
    def verify(
        self,
        user_code: str,
        token: str,
        operation_type: str,
        parameters: dict,
    ) -> VerificationResult:
        """Verify a user-provided code against a pending confirmation.
        
        Args:
            user_code: Code entered by the user
            token: Token from generate()
            operation_type: Must match the original operation
            parameters: Must match the original parameters
            
        Returns:
            VerificationResult with verified=True/False
        """
        # Check if token exists
        if token not in self._pending:
            return VerificationResult(
                verified=False,
                reason="No pending confirmation found for this token"
            )
        
        pending = self._pending[token]
        
        # Check expiry
        if time.time() > pending.expires_at:
            del self._pending[token]
            self._cleanup_state_file(token)
            return VerificationResult(
                verified=False,
                reason="Confirmation code has expired"
            )
        
        # Check lockout
        if pending.session_id in self._lockouts:
            if time.time() < self._lockouts[pending.session_id]:
                remaining = int(self._lockouts[pending.session_id] - time.time())
                return VerificationResult(
                    verified=False,
                    reason=f"Too many failed attempts. Locked for {remaining}s",
                    locked_until=self._lockouts[pending.session_id]
                )
        
        # Verify operation binding (prevents cross-operation replay)
        operation_hash = self._hash_operation(operation_type, parameters)
        if operation_hash != pending.operation_hash:
            return VerificationResult(
                verified=False,
                reason="Operation mismatch — code was generated for a different operation"
            )
        
        # Verify code
        user_code_hash = self._hash(user_code.strip().lower())
        
        if not hmac.compare_digest(user_code_hash, pending.code_hash):
            # Wrong code — increment attempts
            pending.attempts += 1
            remaining = self.config.max_attempts - pending.attempts
            
            if remaining <= 0:
                # Lockout
                self._lockouts[pending.session_id] = (
                    time.time() + self.config.lockout_seconds
                )
                del self._pending[token]
                self._cleanup_state_file(token)
                return VerificationResult(
                    verified=False,
                    reason="Maximum attempts exceeded. Session locked.",
                    attempts_remaining=0,
                    locked_until=self._lockouts[pending.session_id]
                )
            
            return VerificationResult(
                verified=False,
                reason="Incorrect code",
                attempts_remaining=remaining
            )
        
        # Verify HMAC binding
        expected_binding = hmac.new(
            self.secret_key.encode(),
            f"{user_code_hash}:{operation_hash}".encode(),
            hashlib.sha256
        ).hexdigest()
        
        if not hmac.compare_digest(expected_binding, pending.binding):
            # This shouldn't happen unless the secret key changed
            del self._pending[token]
            return VerificationResult(
                verified=False,
                reason="Binding verification failed (internal error)"
            )
        
        # Success — consume the code (single-use)
        del self._pending[token]
        self._cleanup_state_file(token)
        
        return VerificationResult(
            verified=True,
            reason="Confirmed"
        )
    
    # --- Internal helpers ---
    
    def _hash(self, value: str) -> str:
        return hashlib.sha256(value.encode()).hexdigest()
    
    def _hash_operation(self, operation_type: str, parameters: dict) -> str:
        canonical = f"{operation_type}:{json.dumps(parameters, sort_keys=True)}"
        return hashlib.sha256(canonical.encode()).hexdigest()
    
    def _write_state_file(self, code: str, token: str):
        """Write code to state file for shell script compatibility."""
        state_path = Path(self.config.state_dir) / "pending"
        state_path.write_text(code)
        os.chmod(state_path, 0o600)
    
    def _cleanup_state_file(self, token: str):
        """Remove state file after consumption."""
        state_path = Path(self.config.state_dir) / "pending"
        if state_path.exists():
            state_path.unlink()


# =============================================================
# Exceptions
# =============================================================

class RateLimitError(Exception):
    """Raised when rate limit / lockout is active."""
    pass


# =============================================================
# Example Usage
# =============================================================

if __name__ == "__main__":
    # Initialize with a secret key (use a proper secret in production)
    service = ConfirmationService(
        secret_key=os.environ.get("OTC_SECRET_KEY", "dev-secret-change-me")
    )
    
    # Simulate: Agent wants to send an email
    operation = {
        "type": "send_email",
        "params": {"to": "alice@example.com", "subject": "Deploy notification"}
    }
    
    print(f"Operation: {operation['type']}")
    print(f"Parameters: {operation['params']}")
    
    # Generate code
    code, token = service.generate(
        operation_type=operation["type"],
        parameters=operation["params"],
        session_id="session_main"
    )
    
    print(f"\n[SECURE CHANNEL] Code sent to user: {code}")
    print(f"[INTERNAL] Token for verification: {token[:16]}...")
    
    # Simulate: User enters the code
    user_input = code  # In real life, user types this from email
    
    result = service.verify(
        user_code=user_input,
        token=token,
        operation_type=operation["type"],
        parameters=operation["params"]
    )
    
    print(f"\nVerification result: {'✅ CONFIRMED' if result.verified else '❌ DENIED'}")
    print(f"Reason: {result.reason}")
    
    # Try to reuse the same code (should fail — single use)
    print("\n--- Attempting code reuse ---")
    result2 = service.verify(
        user_code=user_input,
        token=token,
        operation_type=operation["type"],
        parameters=operation["params"]
    )
    print(f"Reuse result: {'✅ CONFIRMED' if result2.verified else '❌ DENIED'}")
    print(f"Reason: {result2.reason}")
