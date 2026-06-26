"""
Nex Reports - Library modules
MIT-0 License - Copyright 2026 Nex AI (Kevin Blancaflor)
"""

from .config import REPORT_MODULES, SCHEDULE_PRESETS, OUTPUT_FORMATS
from .storage import get_db, ReportDatabase
from .modules import run_module
from .formatter import format_report
from .notifier import send_telegram, save_to_file, save_report

__version__ = "1.0.0"
__author__ = "Nex AI (Kevin Blancaflor)"

__all__ = [
    "get_db",
    "ReportDatabase",
    "run_module",
    "format_report",
    "send_telegram",
    "save_to_file",
    "save_report",
    "REPORT_MODULES",
    "SCHEDULE_PRESETS",
    "OUTPUT_FORMATS",
]
