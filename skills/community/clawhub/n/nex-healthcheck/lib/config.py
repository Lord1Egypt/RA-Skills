"""
Nex HealthCheck - Configuration
MIT-0 License - Copyright 2026 Nex AI (Kevin Blancaflor)
"""
import os
from pathlib import Path
from enum import Enum

# Data directory and paths
DATA_DIR = Path(os.environ.get("HEALTHCHECK_DATA", Path.home() / ".nex-healthcheck"))
DB_PATH = DATA_DIR / "healthcheck.db"
LOG_PATH = DATA_DIR / "healthcheck.log"
CONFIG_DIR = DATA_DIR / "config"

# Check types
class CheckType(Enum):
    HTTP = "http"
    TCP = "tcp"
    DNS = "dns"
    SSL_CERT = "ssl_cert"
    DOCKER = "docker"
    SYSTEMD = "systemd"
    SSH_CMD = "ssh_cmd"
    PING = "ping"
    DISK = "disk"

# Status levels
class StatusLevel(Enum):
    OK = "ok"
    WARNING = "warning"
    CRITICAL = "critical"
    UNKNOWN = "unknown"

# Default timeouts per check type (seconds)
DEFAULT_TIMEOUTS = {
    CheckType.HTTP: 10,
    CheckType.TCP: 5,
    CheckType.DNS: 5,
    CheckType.SSL_CERT: 10,
    CheckType.DOCKER: 10,
    CheckType.SYSTEMD: 5,
    CheckType.SSH_CMD: 15,
    CheckType.PING: 5,
    CheckType.DISK: 10,
}

# Alert thresholds
SSL_CERT_WARNING_DAYS = 30
SSL_CERT_CRITICAL_DAYS = 7
DISK_WARNING_PERCENT = 80
DISK_CRITICAL_PERCENT = 90

# Default check interval (seconds)
DEFAULT_CHECK_INTERVAL = 300  # 5 minutes

# History retention (days)
HISTORY_RETENTION_DAYS = 30

# Telegram notification settings (from environment)
TELEGRAM_BOT_TOKEN = os.environ.get("HEALTHCHECK_TELEGRAM_TOKEN", "")
TELEGRAM_CHAT_ID = os.environ.get("HEALTHCHECK_TELEGRAM_CHAT", "")

# Enable alerts by default
ALERTS_ENABLED = True
