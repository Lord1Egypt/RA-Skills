#!/usr/bin/env python3
# Nex GDPR Library
# MIT-0 License - Copyright 2026 Nex AI (Kevin Blancaflor)

from .config import *
from .storage import GDPRStorage
from .scanner import DataScanner
from .processor import RequestProcessor

__version__ = "1.0.0"
__author__ = "Nex AI"
__license__ = "MIT-0"

__all__ = [
    "GDPRStorage",
    "DataScanner",
    "RequestProcessor",
]
