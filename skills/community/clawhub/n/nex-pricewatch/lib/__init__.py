"""
Nex PriceWatch Library
Price tracking and monitoring modules
"""

__version__ = "1.0.0"
__author__ = "Nex AI (Kevin Blancaflor)"
__license__ = "MIT-0"

from .config import (
    DATA_DIR, DB_PATH, CHECK_INTERVAL_HOURS,
    ALERT_INCREASE_PCT, ALERT_DECREASE_PCT
)
from .storage import init_db
from .scraper import scrape_price, check_all_targets
from .alerter import detect_changes, format_price_alert, send_alerts

__all__ = [
    'DATA_DIR',
    'DB_PATH',
    'CHECK_INTERVAL_HOURS',
    'ALERT_INCREASE_PCT',
    'ALERT_DECREASE_PCT',
    'init_db',
    'scrape_price',
    'check_all_targets',
    'detect_changes',
    'format_price_alert',
    'send_alerts',
]
