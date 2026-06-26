"""
Exchange connection management.
Handles authentication and connection to Exchange server.
"""

import sys
import os
import time
from typing import Optional, Dict

# Add scripts directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from exchangelib import Account, Configuration, Credentials, DELEGATE, IMPERSONATION
    from exchangelib.errors import UnauthorizedError

    HAS_EXCHANGELIB = True
except ImportError:
    HAS_EXCHANGELIB = False
    Account = None  # type: ignore
    Configuration = None  # type: ignore
    Credentials = None  # type: ignore
    DELEGATE = None  # type: ignore
    IMPERSONATION = None  # type: ignore

    class UnauthorizedError(Exception):
        pass

from config import get_connection_config, clear_config
from utils import die, mask_email
from logger import get_logger

# Global account instances (cached)
_account: Optional[Account] = None
_accounts_for: Dict[str, Account] = {}  # smtp_address -> Account
_logger = get_logger()


def check_dependencies() -> None:
    """Check if required dependencies are installed."""
    if not HAS_EXCHANGELIB:
        _logger.error("Missing dependency: exchangelib")
        die(
            "exchangelib not installed. Run: pip3 install exchangelib requests_ntlm --break-system-packages"
        )


def get_account() -> Account:
    """
    Get authenticated Exchange account.

    Uses configuration from:
    1. CLI arguments
    2. Environment variables
    3. Config file
    4. Interactive prompts

    Returns cached account if already connected.
    """
    global _account

    if _account is not None:
        _logger.debug("Using cached Exchange account")
        return _account

    check_dependencies()

    # Get connection configuration
    _logger.debug("Loading connection configuration")
    conn_config = get_connection_config()
    start_time = time.time()

    try:
        _logger.info(
            "Connecting to Exchange",
            {
                "server": conn_config.get("server", "autodiscover"),
                "email": mask_email(conn_config["email"]),
            },
        )

        # Create credentials
        credentials = Credentials(
            username=conn_config["username"], password=conn_config["password"]
        )

        # Create configuration
        if conn_config.get("server"):
            # Use provided server
            config = Configuration(
                service_endpoint=conn_config["server"],
                credentials=credentials,
            )
            autodiscover = False
        else:
            # Use autodiscover
            config = None
            autodiscover = True

        # Access type
        access_type = DELEGATE
        if conn_config.get("access_type") == "impersonation":
            access_type = IMPERSONATION

        # Create account
        _account = Account(
            primary_smtp_address=conn_config["email"],
            config=config,
            autodiscover=autodiscover,
            access_type=access_type,
        )

        duration = (time.time() - start_time) * 1000
        _logger.log_connection(
            server=conn_config.get("server", "autodiscover"),
            email=mask_email(conn_config["email"]),
            success=True,
        )
        _logger.debug(f"Connected in {duration:.0f}ms")

        return _account

    except UnauthorizedError:
        _logger.log_connection(
            server=conn_config.get("server", "autodiscover"),
            email=mask_email(conn_config["email"]),
            success=False,
        )
        die(
            f"Authentication failed. Check username and password for {mask_email(conn_config['email'])}"
        )
    except Exception as e:
        _logger.log_connection(
            server=conn_config.get("server", "autodiscover"),
            email=mask_email(conn_config["email"]),
            success=False,
        )
        # Clear cached config on connection failure
        clear_config()
        die(f"Failed to connect to Exchange: {e}")


def test_connection() -> dict:
    """
    Test connection to Exchange server.

    Returns dict with connection status and account info.
    """
    check_dependencies()

    _logger.info("Testing Exchange connection")
    account = get_account()

    try:
        # Get folder counts
        _logger.debug("Fetching mailbox statistics")
        inbox_total = account.inbox.total_count
        inbox_unread = account.inbox.unread_count
        calendar_count = account.calendar.total_count
        tasks_count = account.tasks.total_count
        contacts_count = account.contacts.total_count

        result = {
            "ok": True,
            "email": account.primary_smtp_address,
            "server": (
                account.protocol.service_endpoint
                if hasattr(account, "protocol")
                else "autodiscover"
            ),
            "inbox_total": inbox_total,
            "inbox_unread": inbox_unread,
            "calendar_count": calendar_count,
            "tasks_count": tasks_count,
            "contacts_count": contacts_count,
        }

        _logger.info(
            "Connection test successful",
            {
                "email": mask_email(account.primary_smtp_address),
                "inbox": inbox_total,
                "unread": inbox_unread,
            },
        )

        return result
    except Exception as e:
        _logger.error(f"Connection test failed: {e}")
        die(f"Connection test failed: {e}")


def get_account_for(smtp_address: str) -> Account:
    """
    Get authenticated Exchange account for a specific mailbox.

    Uses the same credentials as get_account() but connects to a different
    user's mailbox via delegate access. Requires the service account to have
    delegate permissions on the target mailbox.

    Args:
        smtp_address: Target mailbox email address (e.g., user@domain.com)

    Returns:
        Account connected to the target mailbox

    Raises:
        Exception if connection fails or no delegate access
    """
    global _accounts_for
    
    # Return cached account if available
    if smtp_address in _accounts_for:
        _logger.debug(f"Using cached account for {smtp_address}")
        return _accounts_for[smtp_address]
    
    from exchangelib import DELEGATE as ACCESS_TYPE

    conn_config = get_connection_config()

    credentials = Credentials(
        username=conn_config["username"], password=conn_config["password"]
    )

    if conn_config.get("server"):
        config = Configuration(
            service_endpoint=conn_config["server"],
            credentials=credentials,
        )
        autodiscover = False
    else:
        config = None
        autodiscover = True

    try:
        account = Account(
            primary_smtp_address=smtp_address,
            config=config,
            autodiscover=autodiscover,
            access_type=ACCESS_TYPE,
        )
        # Cache the account
        _accounts_for[smtp_address] = account
        _logger.debug(f"Created and cached account for {smtp_address}")
        return account
    except Exception as e:
        raise Exception(f"Failed to access mailbox {smtp_address}: {e}")


def clear_account() -> None:
    """Clear cached account (useful for testing or reconnection)."""
    global _account
    _account = None
    clear_config()
