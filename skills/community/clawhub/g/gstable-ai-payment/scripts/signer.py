"""
EIP-712 Signing utilities using eth-account
"""

from eth_account import Account
from eth_account.messages import encode_typed_data

from config import get_config
from eip712 import (
    get_eip712_domain,
    PAYMENT_SESSION_CREATION_TYPES,
    PREPARE_PAYMENT_TYPES,
    PaymentSessionCreationAuthorizationMessage,
    PreparePaymentAuthorizationMessage,
)

_account_instance = None


def get_account() -> Account:
    """
    Get or create account instance from private key in environment
    
    Returns:
        Account: eth-account Account instance
    """
    global _account_instance
    if _account_instance is None:
        config = get_config()
        _account_instance = Account.from_key(config.wallet_private_key)
    return _account_instance


def get_wallet_address() -> str:
    """
    Get the wallet address
    
    Returns:
        str: Wallet address
    """
    return get_account().address


def sign_create_session_message(
    auth_msg: PaymentSessionCreationAuthorizationMessage,
    chain_id: int | str
) -> str:
    """
    Sign a PaymentSessionCreationAuthorization message
    
    Args:
        auth_msg: Authorization message
        chain_id: Chain ID
        
    Returns:
        str: Signature
    """
    account = get_account()
    domain = get_eip712_domain(chain_id)
    
    # Build full typed data
    typed_data = {
        "types": {
            "EIP712Domain": [
                {"name": "name", "type": "string"},
                {"name": "version", "type": "string"},
                {"name": "chainId", "type": "uint256"},
            ],
            **PAYMENT_SESSION_CREATION_TYPES,
        },
        "primaryType": "PaymentSessionCreationAuthorization",
        "domain": domain,
        "message": auth_msg.to_signable_message(),
    }
    
    signable = encode_typed_data(full_message=typed_data)
    signed = account.sign_message(signable)
    
    return "0x" + signed.signature.hex()


def sign_prepare_payment_message(
    auth_msg: PreparePaymentAuthorizationMessage,
    chain_id: int | str
) -> str:
    """
    Sign a PreparePaymentAuthorization message
    
    Args:
        auth_msg: Authorization message
        chain_id: Chain ID
        
    Returns:
        str: Signature
    """
    account = get_account()
    domain = get_eip712_domain(chain_id)
    
    # Build full typed data
    typed_data = {
        "types": {
            "EIP712Domain": [
                {"name": "name", "type": "string"},
                {"name": "version", "type": "string"},
                {"name": "chainId", "type": "uint256"},
            ],
            **PREPARE_PAYMENT_TYPES,
        },
        "primaryType": "PreparePaymentAuthorization",
        "domain": domain,
        "message": auth_msg.to_signable_message(),
    }
    
    signable = encode_typed_data(full_message=typed_data)
    signed = account.sign_message(signable)
    
    return "0x" + signed.signature.hex()
