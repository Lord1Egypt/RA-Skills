"""
Nex Expenses - Configuration
MIT-0 License - Copyright 2026 Nex AI (Kevin Blancaflor)
"""
import os
from pathlib import Path

# Data directory
# All receipts and expense data are stored locally in this directory. No data is sent externally
# unless the user explicitly configures an accountant export or tax filing service.
DATA_DIR = Path(os.environ.get("NEX_EXPENSES_DATA", Path.home() / ".nex-expenses"))
DB_PATH = DATA_DIR / "expenses.db"
LOG_PATH = DATA_DIR / "nex-expenses.log"
RECEIPTS_DIR = DATA_DIR / "receipts"
EXPORT_DIR = DATA_DIR / "exports"

# Belgian Tax Deduction Categories
# Reference: Belgian tax law for independent professionals (zelfstandigen)
# Deduction percentages reflect current tax code as of 2026
BELGIAN_TAX_CATEGORIES = {
    "beroepskosten_100": {
        "name": "Beroepskosten (100%)",
        "deduction": 100,
        "description": "General professional expenses fully deductible",
    },
    "representatie_50": {
        "name": "Representatiekosten (50%)",
        "deduction": 50,
        "description": "Restaurant, entertainment, client gifts - 50% deductible",
    },
    "autokosten_variable": {
        "name": "Autokosten (variabel)",
        "deduction": 75,
        "description": "Vehicle expenses - varies 50-120% based on CO2 emission, default 75%",
    },
    "autokosten_brandstof": {
        "name": "Brandstofkosten (75%)",
        "deduction": 75,
        "description": "Fuel costs - 75% deductible",
    },
    "kantoorkosten_100": {
        "name": "Kantoorkosten (100%)",
        "deduction": 100,
        "description": "Office supplies, software, subscriptions",
    },
    "telecom_100": {
        "name": "Telecom (100%)",
        "deduction": 100,
        "description": "Phone, internet if 100% professional",
    },
    "telecom_gemengd": {
        "name": "Telecom gemengd (50-75%)",
        "deduction": 75,
        "description": "Phone/internet mixed use - typically 75%",
    },
    "kledij_0": {
        "name": "Kledij (0%)",
        "deduction": 0,
        "description": "Regular clothing not deductible",
    },
    "werkkledij_100": {
        "name": "Werkkledij (100%)",
        "deduction": 100,
        "description": "Work uniforms, safety gear - 100% deductible",
    },
    "verzekering_100": {
        "name": "Verzekeringen (100%)",
        "deduction": 100,
        "description": "Professional insurance - fully deductible",
    },
    "opleiding_100": {
        "name": "Opleiding (100%)",
        "deduction": 100,
        "description": "Professional training, courses, books",
    },
    "huur_kantoor_100": {
        "name": "Huur kantoor (100%)",
        "deduction": 100,
        "description": "Office rent - fully deductible",
    },
    "huur_thuiskantoor": {
        "name": "Thuiskantoor (variabel)",
        "deduction": 20,
        "description": "Home office - typically 20% of rent/mortgage",
    },
    "afschrijving": {
        "name": "Afschrijving",
        "deduction": 100,
        "description": "Depreciation of professional assets",
    },
    "niet_aftrekbaar": {
        "name": "Niet aftrekbaar (0%)",
        "deduction": 0,
        "description": "Personal expenses, not deductible",
    },
}

# Belgian VAT (BTW) rates for expense side
BTW_RATES = {
    21: "Standaard",
    12: "Verlaagd 12%",
    6: "Verlaagd 6%",
    0: "Vrijgesteld",
}

# Vendor auto-categorization keyword mapping
# Maps vendor names/transaction keywords to default tax categories for quick categorization
VENDOR_CATEGORY_MAP = {
    "restaurant": "representatie_50",
    "resto": "representatie_50",
    "brasserie": "representatie_50",
    "cafe": "representatie_50",
    "eetcafe": "representatie_50",
    "total": "autokosten_brandstof",
    "shell": "autokosten_brandstof",
    "q8": "autokosten_brandstof",
    "lukoil": "autokosten_brandstof",
    "esso": "autokosten_brandstof",
    "texaco": "autokosten_brandstof",
    "proximus": "telecom_100",
    "telenet": "telecom_gemengd",
    "orange": "telecom_gemengd",
    "base": "telecom_gemengd",
    "bol.com": "kantoorkosten_100",
    "amazon": "kantoorkosten_100",
    "coolblue": "kantoorkosten_100",
    "google": "kantoorkosten_100",
    "microsoft": "kantoorkosten_100",
    "adobe": "kantoorkosten_100",
    "github": "kantoorkosten_100",
    "vercel": "kantoorkosten_100",
    "cloudflare": "kantoorkosten_100",
    "udemy": "opleiding_100",
    "coursera": "opleiding_100",
    "ethias": "verzekering_100",
    "ag insurance": "verzekering_100",
    "axa": "verzekering_100",
    "colruyt": "niet_aftrekbaar",
    "delhaize": "niet_aftrekbaar",
    "albert heijn": "niet_aftrekbaar",
    "lidl": "niet_aftrekbaar",
    "aldi": "niet_aftrekbaar",
}

# Quarterly periods for tax filing
QUARTERS = {
    "Q1": {"months": [1, 2, 3], "name": "Januari - Maart"},
    "Q2": {"months": [4, 5, 6], "name": "April - Juni"},
    "Q3": {"months": [7, 8, 9], "name": "Juli - September"},
    "Q4": {"months": [10, 11, 12], "name": "Oktober - December"},
}

# BTW small business exemption threshold (kleine onderneming)
# If annual turnover <= this amount, can claim BTW exemption
BTW_EXEMPTION_THRESHOLD = 25000

# OCR Configuration
TESSERACT_CMD = os.environ.get("TESSERACT_CMD", "tesseract")
OCR_LANG = "nld+eng+fra"
OCR_CONFIG = "--psm 6"

# Export formats
EXPORT_FORMATS = ["csv", "json", "pdf"]

# Receipt image settings
MAX_RECEIPT_SIZE_MB = 10
SUPPORTED_IMAGE_FORMATS = ["jpg", "jpeg", "png", "pdf", "webp"]

# Security settings
MAX_EXPENSE_AMOUNT = 999999.99
MAX_DESCRIPTION_LENGTH = 500
MAX_NOTES_LENGTH = 2000

# Payment methods
PAYMENT_METHODS = ["cash", "bank_transfer", "credit_card", "debit_card", "cheque"]

# Recurring expense frequencies
RECURRENCE_FREQUENCIES = ["monthly", "quarterly", "yearly"]
