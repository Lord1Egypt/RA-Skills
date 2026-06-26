#!/usr/bin/env python3
"""
Threat Intelligence Service Clients
Each class wraps an external API for querying threat intel data.
"""

from .base import BaseService
from .virustotal import VirusTotal
from .greynoise import GreyNoise
from .shodan import Shodan
from .otx import AlienVaultOTX
from .abuseipdb import AbuseIPDB
from .urlscan import URLScan
from .malwarebazaar import MalwareBazaar
from .urlhaus import URLhaus
from .pulsedive import Pulsedive
from .dns import DNSResolver
from .spur import SpurUs
from .validin import Validin

__all__ = [
    "BaseService",
    "VirusTotal",
    "GreyNoise",
    "Shodan",
    "AlienVaultOTX",
    "AbuseIPDB",
    "URLScan",
    "MalwareBazaar",
    "URLhaus",
    "Pulsedive",
    "DNSResolver",
    "SpurUs",
    "Validin",
]