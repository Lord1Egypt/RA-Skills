"""
Nex Expenses - Expense Categorizer
MIT-0 License - Copyright 2026 Nex AI (Kevin Blancaflor)

Auto-categorizes expenses into Belgian tax deduction categories based on
vendor name, description, amount patterns, and learned behavior.
"""

import logging
from decimal import Decimal
from typing import Optional, Dict, List

from . import config

logger = logging.getLogger(__name__)

# Keyword-to-category mapping for description analysis
DESCRIPTION_KEYWORDS = {
    "lunch": "representatie_50",
    "diner": "representatie_50",
    "dinner": "representatie_50",
    "etentje": "representatie_50",
    "lunch": "representatie_50",
    "eten": "representatie_50",
    "maaltijd": "representatie_50",
    "hotel": "representatie_50",
    "logement": "representatie_50",
    "accommodation": "representatie_50",
    "overnacht": "representatie_50",
    "parking": "autokosten_variable",
    "parkeren": "autokosten_variable",
    "parkeering": "autokosten_variable",
    "tolweg": "autokosten_variable",
    "toll": "autokosten_variable",
    "autosnelweg": "autokosten_variable",
    "carwash": "autokosten_variable",
    "car wash": "autokosten_variable",
    "benzine": "autokosten_brandstof",
    "gasoline": "autokosten_brandstof",
    "diesel": "autokosten_brandstof",
    "brandstof": "autokosten_brandstof",
    "fuel": "autokosten_brandstof",
    "mazout": "autokosten_brandstof",
    "hosting": "kantoorkosten_100",
    "domain": "kantoorkosten_100",
    "domein": "kantoorkosten_100",
    "server": "kantoorkosten_100",
    "software": "kantoorkosten_100",
    "licentie": "kantoorkosten_100",
    "license": "kantoorkosten_100",
    "abonnement": "kantoorkosten_100",
    "subscription": "kantoorkosten_100",
    "laptop": "afschrijving",
    "computer": "afschrijving",
    "pc": "afschrijving",
    "monitor": "afschrijving",
    "printer": "afschrijving",
    "apparaat": "afschrijving",
    "device": "afschrijving",
    "equipment": "afschrijving",
    "telefoon": "telecom_gemengd",
    "phone": "telecom_gemengd",
    "gsm": "telecom_gemengd",
    "mobile": "telecom_gemengd",
    "smartphone": "telecom_gemengd",
    "internet": "telecom_gemengd",
    "wifi": "telecom_gemengd",
    "wi-fi": "telecom_gemengd",
    "telecom": "telecom_gemengd",
    "cursus": "opleiding_100",
    "course": "opleiding_100",
    "opleiding": "opleiding_100",
    "training": "opleiding_100",
    "boek": "opleiding_100",
    "book": "opleiding_100",
    "conference": "opleiding_100",
    "conferentie": "opleiding_100",
    "seminar": "opleiding_100",
    "workshop": "opleiding_100",
    "verzekering": "verzekering_100",
    "insurance": "verzekering_100",
    "polis": "verzekering_100",
    "policy": "verzekering_100",
    "huur": "huur_kantoor_100",
    "rent": "huur_kantoor_100",
    "kantoor": "huur_kantoor_100",
    "office": "huur_kantoor_100",
    "thuiskantoor": "huur_thuiskantoor",
    "home office": "huur_thuiskantoor",
    "werkkledij": "werkkledij_100",
    "work clothes": "werkkledij_100",
    "uniform": "werkkledij_100",
    "veiligheid": "werkkledij_100",
    "safety": "werkkledij_100",
    "factuur": "beroepskosten_100",
    "invoice": "beroepskosten_100",
    "professional": "beroepskosten_100",
}


def categorize_expense(
    vendor: Optional[str] = None,
    description: str = "",
    amount: Optional[Decimal] = None,
) -> dict:
    """
    Categorize a single expense based on vendor, description, and amount.

    Args:
        vendor: Vendor/merchant name
        description: Transaction description
        amount: Transaction amount (for pattern analysis)

    Returns:
        Dictionary with keys:
        - category: Category key (e.g., "representatie_50")
        - deduction_pct: Percentage deductible
        - confidence: Float 0-1
        - reason: Explanation of categorization
    """
    if not vendor and not description:
        return {
            "category": "beroepskosten_100",
            "deduction_pct": 100,
            "confidence": 0.0,
            "reason": "No vendor or description provided",
        }

    confidence = 0.0
    matched_category = None
    reason = ""

    # 1. Check vendor against VENDOR_CATEGORY_MAP (highest confidence)
    if vendor:
        vendor_lower = vendor.lower()
        for keyword, category in config.VENDOR_CATEGORY_MAP.items():
            if keyword.lower() in vendor_lower or vendor_lower.find(
                keyword.lower()
            ) != -1:
                matched_category = category
                confidence = 0.95
                reason = f"Matched vendor keyword: {keyword}"
                break

    # 2. Check description keywords (high confidence)
    if not matched_category and description:
        description_lower = description.lower()
        for keyword, category in DESCRIPTION_KEYWORDS.items():
            if keyword.lower() in description_lower:
                matched_category = category
                confidence = 0.85
                reason = f"Matched description keyword: {keyword}"
                break

    # 3. Check amount patterns (medium confidence)
    if not matched_category and amount is not None:
        # Small amounts under 5 EUR might be personal/misc
        if amount < Decimal("5"):
            matched_category = "beroepskosten_100"
            confidence = 0.3
            reason = "Small amount (<5 EUR), assumed general professional expense"

        # Large software/tech amounts (>100 EUR)
        elif amount > Decimal("100") and any(
            word in (description or vendor or "").lower()
            for word in ["software", "license", "subscription", "hosting"]
        ):
            matched_category = "kantoorkosten_100"
            confidence = 0.75
            reason = "Large amount with tech keywords -> office costs"

    # 4. Default to general professional expenses
    if not matched_category:
        matched_category = "beroepskosten_100"
        confidence = 0.2
        reason = "Default: general professional expense"

    deduction_pct = config.BELGIAN_TAX_CATEGORIES[matched_category]["deduction"]

    return {
        "category": matched_category,
        "deduction_pct": deduction_pct,
        "confidence": confidence,
        "reason": reason,
    }


def suggest_category(vendor: str = "", description: str = "") -> List[dict]:
    """
    Suggest top 3 likely categories for an expense.

    Useful when the auto-categorization should show alternatives to the user.

    Args:
        vendor: Vendor/merchant name
        description: Transaction description

    Returns:
        List of up to 3 dicts with:
        - category: Category key
        - name: Human-readable category name
        - confidence: Float 0-1
        - reason: Why it matched
    """
    candidates = {}

    # Score all categories based on vendor and description
    text = (vendor + " " + description).lower()

    # Check vendor map
    if vendor:
        vendor_lower = vendor.lower()
        for keyword, category in config.VENDOR_CATEGORY_MAP.items():
            if keyword.lower() in vendor_lower:
                candidates[category] = max(
                    candidates.get(category, 0), 0.9
                )

    # Check description keywords
    for keyword, category in DESCRIPTION_KEYWORDS.items():
        if keyword.lower() in text:
            candidates[category] = max(candidates.get(category, 0), 0.8)

    # Convert to list and sort by confidence
    suggestions = []
    for category, confidence in sorted(
        candidates.items(), key=lambda x: x[1], reverse=True
    )[:3]:
        cat_info = config.BELGIAN_TAX_CATEGORIES[category]
        suggestions.append(
            {
                "category": category,
                "name": cat_info["name"],
                "deduction_pct": cat_info["deduction"],
                "confidence": confidence,
                "description": cat_info["description"],
            }
        )

    # Ensure at least 3 suggestions by adding defaults
    if len(suggestions) < 3:
        default_categories = [
            "beroepskosten_100",
            "kantoorkosten_100",
            "representatie_50",
        ]
        for cat in default_categories:
            if cat not in [s["category"] for s in suggestions]:
                cat_info = config.BELGIAN_TAX_CATEGORIES[cat]
                suggestions.append(
                    {
                        "category": cat,
                        "name": cat_info["name"],
                        "deduction_pct": cat_info["deduction"],
                        "confidence": 0.3,
                        "description": cat_info["description"],
                    }
                )
            if len(suggestions) >= 3:
                break

    return suggestions[:3]


def calculate_deduction(amount: Decimal, category: str) -> dict:
    """
    Calculate the deductible amount for an expense.

    Args:
        amount: Total amount
        category: Tax category key

    Returns:
        Dictionary with:
        - deductible_amount: Decimal
        - non_deductible: Decimal
        - deduction_pct: int
    """
    if category not in config.BELGIAN_TAX_CATEGORIES:
        category = "beroepskosten_100"

    deduction_pct = config.BELGIAN_TAX_CATEGORIES[category]["deduction"]
    deductible = amount * Decimal(deduction_pct) / Decimal(100)
    non_deductible = amount - deductible

    return {
        "deductible_amount": deductible.quantize(Decimal("0.01")),
        "non_deductible": non_deductible.quantize(Decimal("0.01")),
        "deduction_pct": deduction_pct,
    }


def calculate_btw_recovery(
    amount_incl: Decimal, btw_rate: int, category: str
) -> dict:
    """
    Calculate BTW (VAT) recovery based on category.

    BTW on representatiekosten (entertainment) is only 50% recoverable.
    BTW recovery matches the deduction percentage for other categories.

    Args:
        amount_incl: Amount including BTW
        btw_rate: BTW rate (21, 6, etc.)
        category: Tax category key

    Returns:
        Dictionary with:
        - btw_amount: Total BTW in the amount
        - btw_recoverable: Recoverable BTW
        - btw_non_recoverable: Non-recoverable BTW
    """
    if btw_rate <= 0 or btw_rate >= 100:
        # No or invalid BTW
        return {
            "btw_amount": Decimal("0"),
            "btw_recoverable": Decimal("0"),
            "btw_non_recoverable": Decimal("0"),
        }

    # Calculate BTW amount from inclusive amount
    # amount_incl = amount_excl * (1 + btw_rate/100)
    # amount_excl = amount_incl / (1 + btw_rate/100)
    # btw = amount_incl - amount_excl
    btw_multiplier = Decimal(100 + btw_rate) / Decimal(100)
    amount_excl = amount_incl / btw_multiplier
    btw_amount = amount_incl - amount_excl

    # Determine recovery percentage based on category
    if category == "representatie_50":
        # Entertainment: 50% of BTW is recoverable
        recovery_pct = 50
    else:
        # Other categories: recover based on deduction percentage
        deduction_pct = config.BELGIAN_TAX_CATEGORIES.get(category, {}).get(
            "deduction", 100
        )
        recovery_pct = deduction_pct

    btw_recoverable = btw_amount * Decimal(recovery_pct) / Decimal(100)
    btw_non_recoverable = btw_amount - btw_recoverable

    return {
        "btw_amount": btw_amount.quantize(Decimal("0.01")),
        "btw_recoverable": btw_recoverable.quantize(Decimal("0.01")),
        "btw_non_recoverable": btw_non_recoverable.quantize(Decimal("0.01")),
    }


def categorize_from_ocr(ocr_result: dict) -> dict:
    """
    Categorize an expense from OCR results.

    Takes the complete output of ocr.ocr_receipt() and returns
    full categorization with tax calculations.

    Args:
        ocr_result: Output from ocr.ocr_receipt()

    Returns:
        Dictionary with:
        - category: Tax category
        - deduction_pct: Percentage deductible
        - confidence: Overall confidence 0-1
        - vendor: Vendor name
        - description: From OCR items
        - amount_total: Total amount
        - amount_excl: Amount excluding BTW
        - btw_rate: BTW percentage
        - btw_amount: BTW amount
        - btw_recovery: BTW recovery breakdown
        - deduction_amount: Deductible amount
        - reason: Explanation of categorization
    """
    vendor = ocr_result.get("vendor", "")
    description = ""

    # Combine item descriptions
    if ocr_result.get("items"):
        description = " ".join(
            [item.get("description", "") for item in ocr_result.get("items", [])]
        )

    # Get main amount
    amount_incl = ocr_result.get("total_incl")
    amount_excl = ocr_result.get("total_excl")
    btw_amount = ocr_result.get("btw_amount")
    btw_rate = ocr_result.get("btw_rate", 21)  # Default to 21% if not detected

    # Use total_incl if available, otherwise total_excl
    main_amount = amount_incl or amount_excl
    if not main_amount:
        main_amount = Decimal("0")

    # Categorize the expense
    cat_result = categorize_expense(vendor, description, main_amount)

    category = cat_result["category"]
    deduction_pct = cat_result["deduction_pct"]
    confidence = (ocr_result.get("confidence", 0) + cat_result.get("confidence", 0)) / 2

    # Calculate deductions
    if main_amount and main_amount > 0:
        deduction_info = calculate_deduction(main_amount, category)
        deductible_amount = deduction_info["deductible_amount"]
    else:
        deductible_amount = Decimal("0")

    # Calculate BTW recovery
    if amount_incl and amount_incl > 0 and btw_rate and btw_rate > 0:
        btw_recovery = calculate_btw_recovery(amount_incl, btw_rate, category)
    else:
        btw_recovery = {
            "btw_amount": Decimal("0"),
            "btw_recoverable": Decimal("0"),
            "btw_non_recoverable": Decimal("0"),
        }

    return {
        "category": category,
        "deduction_pct": deduction_pct,
        "confidence": min(confidence, 1.0),  # Ensure 0-1 range
        "vendor": vendor,
        "description": description[:100] if description else "",
        "amount_total": main_amount,
        "amount_excl": amount_excl,
        "btw_rate": btw_rate,
        "btw_amount": btw_amount or btw_recovery["btw_amount"],
        "btw_recovery": btw_recovery,
        "deduction_amount": deductible_amount,
        "reason": cat_result["reason"],
    }
