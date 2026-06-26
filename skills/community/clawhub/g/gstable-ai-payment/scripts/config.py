"""
Configuration management for GStable AI Payment Skill
Reads from environment variables
"""

import os
from dataclasses import dataclass
from typing import Optional

_config_instance: Optional["Config"] = None


@dataclass
class Config:
    """Configuration for GStable AI Payment"""
    wallet_private_key: str
    api_base_url: str
    default_payer_email: str
    rpc_urls: dict  # chain_id -> rpc_url


# Default RPC URLs
DEFAULT_RPC_URLS = {
    "137": "https://polygon-bor.publicnode.com",
    "1": "https://eth.llamarpc.com",
    "42161": "https://arb1.arbitrum.io/rpc",
    "8453": "https://mainnet.base.org",
}

CHAIN_ID_TO_ENV_NAME = {
    "137": "POLYGON",
    "1": "ETHEREUM",
    "42161": "ARBITRUM",
    "8453": "BASE",
}


def load_config() -> Config:
    """
    Load configuration from environment variables
    
    Returns:
        Config: Configuration object
        
    Raises:
        ValueError: If required environment variables are not set
    """
    wallet_private_key = os.environ.get("WALLET_PRIVATE_KEY")
    
    if not wallet_private_key:
        raise ValueError(
            "WALLET_PRIVATE_KEY environment variable is required. "
            "Please set it to your wallet private key (0x... format)."
        )
    
    # Validate private key format
    if not wallet_private_key.startswith("0x") or len(wallet_private_key) != 66:
        raise ValueError(
            "WALLET_PRIVATE_KEY must be a valid hex string starting with 0x (66 characters total)."
        )
    
    rpc_urls = {**DEFAULT_RPC_URLS}

    # Preferred format: chain-name based RPC env vars, e.g. RPC_URL_POLYGON
    for chain_id, chain_name in CHAIN_ID_TO_ENV_NAME.items():
        env_key = f"RPC_URL_{chain_name}"
        if os.environ.get(env_key):
            rpc_urls[chain_id] = os.environ[env_key]

    # Backward compatibility: allow numeric env vars, e.g. RPC_URL_137
    for chain_id in CHAIN_ID_TO_ENV_NAME.keys():
        legacy_env_key = f"RPC_URL_{chain_id}"
        if os.environ.get(legacy_env_key):
            rpc_urls[chain_id] = os.environ[legacy_env_key]

    return Config(
        wallet_private_key=wallet_private_key,
        api_base_url=os.environ.get("GSTABLE_API_BASE_URL", "https://aipay.gstable.io/api/v1"),
        default_payer_email=os.environ.get("DEFAULT_PAYER_EMAIL", "ai-agent@example.com"),
        rpc_urls=rpc_urls,
    )


def get_config() -> Config:
    """
    Get or create singleton config instance
    
    Returns:
        Config: Configuration object
    """
    global _config_instance
    if _config_instance is None:
        _config_instance = load_config()
    return _config_instance
