"""
config.py - Configuration Management Module

Provides multi-layer configuration for KDTS server connection:
1. Environment variables (highest priority)
2. Explicit parameters passed at initialization
3. Configuration file (config.yaml or config.json)
4. Default values (lowest priority)

Environment Variables:
    KDTS_BASE_URL: Full KDTS server URL (e.g., http://127.0.0.1:8989)
    KDTS_HOST: KDTS server host (e.g., 127.0.0.1)
    KDTS_PORT: KDTS server port (e.g., 8989)
    KDTS_API_PREFIX: API prefix (default: /kdts/api/v1)
    KDTS_TIMEOUT: Request timeout in seconds (default: 300)
    KDTS_CONNECT_TIMEOUT: Connection timeout in seconds (default: 5)

Usage:
    from scripts.config import KDTSConfig

    # Get configuration with all layers
    config = KDTSConfig()
    base_url = config.get_base_url()

    # Or use helper function
    base_url = resolve_base_url(explicit_url=None)
"""

import os
import json
import logging
from typing import Optional, Dict, Any
from pathlib import Path

logger = logging.getLogger(__name__)

# Default values
DEFAULT_HOST = "127.0.0.1"
DEFAULT_PORT = 8989
DEFAULT_API_PREFIX = "/kdts/api/v1"
DEFAULT_TIMEOUT = 300
DEFAULT_CONNECT_TIMEOUT = 5

# Environment variable names
ENV_BASE_URL = "KDTS_BASE_URL"
ENV_HOST = "KDTS_HOST"
ENV_PORT = "KDTS_PORT"
ENV_API_PREFIX = "KDTS_API_PREFIX"
ENV_TIMEOUT = "KDTS_TIMEOUT"
ENV_CONNECT_TIMEOUT = "KDTS_CONNECT_TIMEOUT"


class KDTSConfig:
    """
    KDTS Configuration Manager.

    Implements priority chain for configuration values:
    Environment Variables > Explicit Parameters > Config File > Defaults
    """

    def __init__(self, config_file: Optional[str] = None):
        """
        Initialize configuration manager.

        Args:
            config_file: Optional path to config file (YAML or JSON).
                        If not provided, looks for default locations.
        """
        self._config_file = config_file
        self._file_config = self._load_config_file()

    def _load_config_file(self) -> Dict[str, Any]:
        """Load configuration from file if it exists."""
        try:
            # Try specified file first
            config_path = None
            if self._config_file:
                config_path = Path(self._config_file)
            else:
                # Look for default locations
                possible_paths = [
                    Path.cwd() / "kdts_config.json",
                    Path.cwd() / "config" / "kdts_config.json",
                    Path(__file__).parent / "kdts_config.json",
                    Path(__file__).parent.parent / "kdts_config.json",
                ]
                for p in possible_paths:
                    if p.exists():
                        config_path = p
                        break

            if config_path and config_path.exists():
                logger.info(f"Loading config from {config_path}")
                with open(config_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    # Support both YAML and JSON (simple detection)
                    if config_path.suffix == '.yaml' or config_path.suffix == '.yml':
                        try:
                            import yaml
                            return yaml.safe_load(content) or {}
                        except ImportError:
                            logger.warning("PyYAML not installed, falling back to JSON parsing")
                            # Try parsing as JSON anyway
                            pass
                    return json.loads(content)

            logger.debug("No config file found, using environment/defaults")
            return {}

        except Exception as e:
            logger.warning(f"Failed to load config file: {e}")
            return {}

    def get_base_url(self, explicit_url: Optional[str] = None) -> str:
        """
        Resolve KDTS base URL with priority chain.

        Priority:
        1. Explicit URL passed as parameter
        2. KDTS_BASE_URL environment variable
        3. KDTS_HOST + KDTS_PORT environment variables
        4. Config file base_url
        5. Config file host + port
        6. Default (127.0.0.1:8989)

        Args:
            explicit_url: Explicitly provided base URL (highest priority)

        Returns:
            Resolved base URL string
        """
        # 1. Explicit parameter
        if explicit_url:
            logger.info(f"Using explicit base_url: {explicit_url}")
            return self._normalize_url(explicit_url)

        # 2. Full base URL from environment
        env_base_url = os.environ.get(ENV_BASE_URL)
        if env_base_url:
            logger.info(f"Using base_url from environment: {env_base_url}")
            return self._normalize_url(env_base_url)

        # 3. Host + Port from environment
        env_host = os.environ.get(ENV_HOST)
        env_port = os.environ.get(ENV_PORT)
        if env_host and env_port:
            url = f"http://{env_host}:{env_port}"
            logger.info(f"Using host+port from environment: {url}")
            return self._normalize_url(url)

        # 4. Config file full URL
        file_base_url = self._file_config.get("base_url")
        if file_base_url:
            logger.info(f"Using base_url from config file: {file_base_url}")
            return self._normalize_url(file_base_url)

        # 5. Config file host + port
        file_host = self._file_config.get("host")
        file_port = self._file_config.get("port")
        if file_host and file_port:
            url = f"http://{file_host}:{file_port}"
            logger.info(f"Using host+port from config file: {url}")
            return self._normalize_url(url)

        # 6. Default
        default_url = f"http://{DEFAULT_HOST}:{DEFAULT_PORT}"
        logger.info(f"Using default base_url: {default_url}")
        return default_url

    def get_api_prefix(self) -> str:
        """Resolve API prefix."""
        env_prefix = os.environ.get(ENV_API_PREFIX)
        if env_prefix:
            return env_prefix

        file_prefix = self._file_config.get("api_prefix")
        if file_prefix:
            return file_prefix

        return DEFAULT_API_PREFIX

    def get_timeout(self) -> int:
        """Resolve request timeout in seconds."""
        env_timeout = os.environ.get(ENV_TIMEOUT)
        if env_timeout:
            return int(env_timeout)

        file_timeout = self._file_config.get("timeout")
        if file_timeout:
            return int(file_timeout)

        return DEFAULT_TIMEOUT

    def get_connect_timeout(self) -> int:
        """Resolve connection timeout in seconds."""
        env_connect_timeout = os.environ.get(ENV_CONNECT_TIMEOUT)
        if env_connect_timeout:
            return int(env_connect_timeout)

        file_connect_timeout = self._file_config.get("connect_timeout")
        if file_connect_timeout:
            return int(file_connect_timeout)

        return DEFAULT_CONNECT_TIMEOUT

    def get_full_config(self) -> Dict[str, Any]:
        """Get all resolved configuration values."""
        return {
            "base_url": self.get_base_url(),
            "api_prefix": self.get_api_prefix(),
            "timeout": self.get_timeout(),
            "connect_timeout": self.get_connect_timeout(),
        }

    def detect_config_source(self) -> str:
        """Detect which configuration source is being used."""
        # Check environment variables first
        if os.environ.get(ENV_BASE_URL):
            return "environment_variable:KDTS_BASE_URL"
        if os.environ.get(ENV_HOST) and os.environ.get(ENV_PORT):
            return "environment_variable:KDTS_HOST+KDTS_PORT"

        # Check config file
        if self._config_file:
            return f"config_file:{self._config_file}"
        if self._file_config:
            return "config_file:auto_detected"

        return "default"

    @staticmethod
    def _normalize_url(url: str) -> str:
        """Normalize URL by adding http:// prefix if missing."""
        url = url.rstrip('/')
        if not url.startswith(('http://', 'https://')):
            url = f"http://{url}"
        return url

    @staticmethod
    def create_config_file_template(path: str) -> bool:
        """
        Create a template configuration file.

        Args:
            path: Path where to create the template file

        Returns:
            True if created successfully
        """
        template = {
            "base_url": "http://127.0.0.1:8989",
            "api_prefix": "/kdts/api/v1",
            "timeout": 30,
            "connect_timeout": 5,
        }

        try:
            with open(path, 'w', encoding='utf-8') as f:
                json.dump(template, f, indent=2)
            logger.info(f"Created config template at {path}")
            return True
        except Exception as e:
            logger.error(f"Failed to create config template: {e}")
            return False


# Convenience functions

def resolve_base_url(explicit_url: Optional[str] = None) -> str:
    """
    Resolve KDTS base URL using priority chain.

    Args:
        explicit_url: Explicitly provided URL (highest priority)

    Returns:
        Resolved base URL
    """
    config = KDTSConfig()
    return config.get_base_url(explicit_url)


def get_environment_info() -> Dict[str, Any]:
    """
    Get information about current environment configuration.

    Returns:
        Dict with environment variable status and current values
    """
    env_vars = {
        "KDTS_BASE_URL": os.environ.get(ENV_BASE_URL),
        "KDTS_HOST": os.environ.get(ENV_HOST),
        "KDTS_PORT": os.environ.get(ENV_PORT),
        "KDTS_API_PREFIX": os.environ.get(ENV_API_PREFIX),
        "KDTS_TIMEOUT": os.environ.get(ENV_TIMEOUT),
        "KDTS_CONNECT_TIMEOUT": os.environ.get(ENV_CONNECT_TIMEOUT),
    }

    config = KDTSConfig()

    return {
        "environment_variables": env_vars,
        "current_config": config.get_full_config(),
        "config_source": config.detect_config_source(),
    }
