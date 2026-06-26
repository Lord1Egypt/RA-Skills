"""
Configuration management for Exchange Mailbox skill.
Supports multiple configuration sources with priority:
1. CLI arguments (highest)
2. Environment variables
3. config.yaml file
4. Interactive prompts (fallback)
"""

import os
import sys
import json
import getpass
from pathlib import Path
from typing import Optional, Dict, Any

# Add scripts directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Try to import yaml, fall back to json if not available
try:
    import yaml

    HAS_YAML = True
except ImportError:
    HAS_YAML = False

from utils import die

# Default config file locations (in order of priority)
CONFIG_FILE_LOCATIONS = [
    "./config.yaml",
    "./config.yml",
    "./config.json",
    "~/.config/exchange-mailbox/config.yaml",
    "~/.config/exchange-mailbox/config.json",
    "/etc/exchange-mailbox/config.yaml",
    "/etc/exchange-mailbox/config.json",
]

# Environment variable names
ENV_VARS = {
    "server": "EXCHANGE_SERVER",
    "username": "EXCHANGE_USERNAME",
    "password": "EXCHANGE_PASSWORD",
    "email": "EXCHANGE_EMAIL",
    "autodiscover": "EXCHANGE_AUTODISCOVER",
    "access_type": "EXCHANGE_ACCESS_TYPE",
    "owner_email": "OWNER_EMAIL",
}

# Defaults
DEFAULTS = {
    "autodiscover": True,
    "access_type": "delegate",
    "mail_limit": 10,
    "calendar_days": 7,
    "calendar_limit": 50,
    "tasks_limit": 20,
    "contacts_limit": 50,
}


class Config:
    """Configuration manager with multi-source support."""

    def __init__(self):
        self._config: Dict[str, Any] = {}
        self._loaded = False

    def load(self, cli_args: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Load configuration from multiple sources.

        Priority (highest to lowest):
        1. CLI arguments
        2. Environment variables
        3. Config file
        4. Interactive prompts

        Returns validated config dict.
        """
        if self._loaded:
            return self._config

        # Start with defaults
        self._config = DEFAULTS.copy()

        # Try config file first
        file_config = self._load_from_file()
        if file_config:
            self._config.update(file_config)

        # Override with environment variables
        env_config = self._load_from_env()
        if env_config:
            self._config.update(env_config)

        # Override with CLI arguments
        if cli_args:
            cli_config = self._extract_cli_config(cli_args)
            if cli_config:
                self._config.update(cli_config)

        # Validate and prompt for missing
        self._validate_and_prompt()

        self._loaded = True
        return self._config

    def _load_from_file(self) -> Optional[Dict[str, Any]]:
        """Load configuration from file."""
        for location in CONFIG_FILE_LOCATIONS:
            path = Path(location).expanduser()
            if path.exists():
                try:
                    content = path.read_text()

                    if HAS_YAML:
                        data = yaml.safe_load(content)
                    else:
                        # Fallback to JSON
                        data = json.loads(content)

                    # Flatten the exchange section if present
                    if "exchange" in data:
                        exchange = data.pop("exchange")
                        data.update(exchange)

                    # Flatten defaults section
                    if "defaults" in data:
                        defaults = data.pop("defaults")
                        # Flatten nested defaults
                        for section, values in defaults.items():
                            if isinstance(values, dict):
                                for key, val in values.items():
                                    self._config[f"{section}_{key}"] = val

                    return data

                except Exception as e:
                    print(
                        f"Warning: Failed to load config from {path}: {e}",
                        file=sys.stderr,
                    )

        return None

    def _load_from_env(self) -> Dict[str, Any]:
        """Load configuration from environment variables."""
        config = {}

        for key, env_var in ENV_VARS.items():
            value = os.environ.get(env_var)
            if value:
                # Convert boolean strings
                if value.lower() in ("true", "yes", "1"):
                    value = True
                elif value.lower() in ("false", "no", "0"):
                    value = False
                config[key] = value

        return config

    def _extract_cli_config(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Extract configuration from CLI arguments."""
        config = {}

        # Direct mappings
        direct_keys = ["server", "username", "password", "email"]
        for key in direct_keys:
            if args.get(key):
                config[key] = args[key]

        return config

    def _validate_and_prompt(self) -> None:
        """Validate configuration and prompt for missing required values."""
        # Required fields
        required = {
            "username": "Username (e.g., DOMAIN\\user or user@domain.com): ",
            "email": "Email address: ",
        }

        # Check username
        if not self._config.get("username"):
            if sys.stdin.isatty():
                self._config["username"] = input("Enter " + required["username"])
            else:
                die(
                    "Missing required configuration: username. Set EXCHANGE_USERNAME or use --username"
                )

        # Check email
        if not self._config.get("email"):
            # Try to derive from username
            username = self._config.get("username", "")
            if "@" in username:
                self._config["email"] = username
            elif sys.stdin.isatty():
                self._config["email"] = input("Enter " + required["email"])
            else:
                die(
                    "Missing required configuration: email. Set EXCHANGE_EMAIL or use --email"
                )

        # Check password (never store in config file, always from ENV or prompt)
        if not self._config.get("password"):
            if sys.stdin.isatty():
                self._config["password"] = getpass.getpass("Enter password: ")
            else:
                die(
                    "Missing required configuration: password. Set EXCHANGE_PASSWORD environment variable"
                )

        # Validate email format
        email = self._config.get("email", "")
        if "@" not in email:
            die(f"Invalid email format: {email}")

        # Server is optional if autodiscover is enabled
        # If autodiscover is disabled, server is required
        if not self._config.get("autodiscover", True) and not self._config.get(
            "server"
        ):
            die(
                "Server URL is required when autodiscover is disabled. Set EXCHANGE_SERVER or use --server"
            )

    def get(self, key: str, default: Any = None) -> Any:
        """Get a configuration value."""
        return self._config.get(key, default)

    def get_connection_config(self) -> Dict[str, Any]:
        """Get configuration needed for Exchange connection."""
        return {
            "server": self._config.get("server"),
            "username": self._config.get("username"),
            "password": self._config.get("password"),
            "email": self._config.get("email"),
            "autodiscover": self._config.get("autodiscover", True),
            "access_type": self._config.get("access_type", "delegate"),
            "owner_email": self._config.get("owner_email") or self._config.get("email"),
        }

    def save_to_file(self, path: Optional[str] = None) -> None:
        """Save current configuration to file (without password)."""
        if not path:
            # Save to user config directory
            config_dir = Path.home() / ".config" / "exchange-mailbox"
            config_dir.mkdir(parents=True, exist_ok=True)
            path = str(config_dir / "config.yaml")

        # Don't save password to file
        config_to_save = {
            "exchange": {
                "server": self._config.get("server", ""),
                "username": self._config.get("username", ""),
                "email": self._config.get("email", ""),
                "autodiscover": self._config.get("autodiscover", True),
                "access_type": self._config.get("access_type", "delegate"),
            },
            "defaults": {
                "mail": {"limit": self._config.get("mail_limit", 10)},
                "calendar": {"days": self._config.get("calendar_days", 7)},
                "tasks": {"limit": self._config.get("tasks_limit", 20)},
                "contacts": {"limit": self._config.get("contacts_limit", 50)},
            },
        }

        try:
            path_obj = Path(path)
            content = (
                yaml.dump(config_to_save, default_flow_style=False)
                if HAS_YAML
                else json.dumps(config_to_save, indent=2)
            )
            path_obj.write_text(content)
            path_obj.chmod(0o600)
            print(f"Configuration saved to {path}")
        except Exception as e:
            print(f"Warning: Could not save config: {e}", file=sys.stderr)


# Global config instance
_config: Optional[Config] = None


def get_config(cli_args: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """
    Get or load configuration.

    This is the main entry point for getting configuration.
    """
    global _config

    if _config is None:
        _config = Config()

    return _config.load(cli_args)


def get_connection_config() -> Dict[str, Any]:
    """Get configuration needed for Exchange connection."""
    global _config

    if _config is None:
        _config = Config()
        _config.load()

    return _config.get_connection_config()


def clear_config() -> None:
    """Clear cached configuration (useful for testing)."""
    global _config
    _config = None
