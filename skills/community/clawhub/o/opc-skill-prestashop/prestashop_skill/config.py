import os
import re

class PrestaShopConfig:
    """
    Configuration manager for PrestaShop Web Services integration.
    """
    def __init__(self, shop_url: str = None, api_key: str = None, timeout: int = 10, cache_ttl_seconds: int = 300):
        self.shop_url = (shop_url or os.getenv("PRESTASHOP_SHOP_URL", "")).rstrip("/")
        self.api_key = api_key or os.getenv("PRESTASHOP_API_KEY", "")
        self.timeout = int(os.getenv("PRESTASHOP_TIMEOUT", str(timeout)))
        self.cache_ttl_seconds = int(os.getenv("PRESTASHOP_CACHE_TTL", str(cache_ttl_seconds)))

    def validate(self):
        """Validates configuration parameters."""
        if not self.shop_url:
            raise ValueError("PrestaShop Shop URL is required. Set PRESTASHOP_SHOP_URL environment variable or pass shop_url.")
        if not self.api_key:
            raise ValueError("PrestaShop API Key is required. Set PRESTASHOP_API_KEY environment variable or pass api_key.")
        
        if not (self.shop_url.startswith("http://") or self.shop_url.startswith("https://")):
            raise ValueError("PrestaShop Shop URL must start with http:// or https://")

    def sanitize_log_message(self, message: str) -> str:
        """
        Masks the PrestaShop API key from any log string or URL.
        """
        if not self.api_key:
            return message
        
        # Mask exact key
        sanitized = message.replace(self.api_key, "********")
        # Mask basic auth pattern in URL if present
        sanitized = re.sub(r'https?://([^:@]+):?([^@]*)(@)', r'https://********\3', sanitized)
        # Mask ws_key query param if present
        sanitized = re.sub(r'ws_key=[^&]+', 'ws_key=********', sanitized)
        return sanitized
