"""
Nex E-Invoice - Configuration
MIT-0 License - Copyright 2026 Nex AI (Kevin Blancaflor)
"""
import os
from pathlib import Path

# Data directory for invoices, XML exports, and database
# All generated invoices and XMLs are stored locally in this directory
DATA_DIR = Path(os.environ.get("NEX_EINVOICE_DATA", Path.home() / ".nex-einvoice"))
DB_PATH = DATA_DIR / "invoices.db"
LOG_PATH = DATA_DIR / "nex-einvoice.log"
EXPORT_DIR = DATA_DIR / "exports"

# ── Belgian VAT Rates ────────────────────────────────

BTW_RATES = {
    "standaard": 21,      # Standard rate (21%)
    "verlaagd_12": 12,    # Reduced rate (12%)
    "verlaagd_6": 6,      # Super-reduced rate (6%)
    "vrijgesteld": 0,     # VAT-exempt (0%)
}

# ── UBL Tax Categories (EN 16931 Classification) ─────

TAX_CATEGORIES = {
    "S": "Standard rate",
    "AE": "VAT Reverse Charge",
    "E": "Exempt from VAT",
    "Z": "Zero rated",
    "O": "Not subject to VAT",
}

# ── Mapping Belgian BTW rates to UBL ─────────────────

BTW_TO_UBL = {
    21: ("S", "21.00"),
    12: ("S", "12.00"),
    6: ("S", "6.00"),
    0: ("E", "0.00"),
}

# ── Peppol / BIS Billing 3.0 Identifiers ────────────

CUSTOMIZATION_ID = "urn:cen.eu:en16931:2017#compliant#urn:fdc:peppol.eu:2017:poacc:billing:3.0"
PROFILE_ID = "urn:fdc:peppol.eu:2017:poacc:billing:01:1.0"
PEPPOL_ENDPOINT_SCHEME = "0208"  # Belgian KBO/BCE scheme

# ── Currency & Localization ──────────────────────────

DEFAULT_CURRENCY = "EUR"
DEFAULT_COUNTRY = "BE"

# ── Invoice Configuration ────────────────────────────

INVOICE_PREFIX = os.environ.get("NEX_EINVOICE_PREFIX", "INV")
PAYMENT_TERMS_DAYS = 30

# ── Seller Defaults (from environment) ───────────────

SELLER_NAME = os.environ.get("NEX_EINVOICE_SELLER_NAME", "")
SELLER_VAT = os.environ.get("NEX_EINVOICE_SELLER_VAT", "")
SELLER_STREET = os.environ.get("NEX_EINVOICE_SELLER_STREET", "")
SELLER_CITY = os.environ.get("NEX_EINVOICE_SELLER_CITY", "")
SELLER_POSTCODE = os.environ.get("NEX_EINVOICE_SELLER_POSTCODE", "")
SELLER_COUNTRY = os.environ.get("NEX_EINVOICE_SELLER_COUNTRY", DEFAULT_COUNTRY)
SELLER_EMAIL = os.environ.get("NEX_EINVOICE_SELLER_EMAIL", "")
SELLER_PHONE = os.environ.get("NEX_EINVOICE_SELLER_PHONE", "")
SELLER_KBO = os.environ.get("NEX_EINVOICE_SELLER_KBO", "")
SELLER_IBAN = os.environ.get("NEX_EINVOICE_SELLER_IBAN", "")
SELLER_BIC = os.environ.get("NEX_EINVOICE_SELLER_BIC", "")
SELLER_PEPPOL_ID = os.environ.get("NEX_EINVOICE_SELLER_PEPPOL_ID", "")

# ── Constraints & Limits ─────────────────────────────

MAX_LINE_ITEMS = 999
MAX_DESCRIPTION_LENGTH = 1000
MAX_INVOICE_NUMBER_LENGTH = 20

# ── UBL XML Namespaces ───────────────────────────────

UBL_NAMESPACES = {
    "cac": "urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2",
    "cbc": "urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2",
    "ext": "urn:oasis:names:specification:ubl:schema:xsd:CommonExtensionComponents-2",
    "qdt": "urn:oasis:names:specification:ubl:schema:xsd:QualifiedDatatypes-2",
    "udt": "urn:oasis:names:specification:ubl:schema:xsd:UnqualifiedDatatypes-2",
}
