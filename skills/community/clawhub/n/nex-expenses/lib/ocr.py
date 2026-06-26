"""
Nex Expenses - Receipt OCR Module
MIT-0 License - Copyright 2026 Nex AI (Kevin Blancaflor)

Extracts text from receipt images using Tesseract OCR, then parses
vendor, amount, date, and BTW from the extracted text.
"""

import subprocess
import re
import tempfile
import logging
from pathlib import Path
from decimal import Decimal
from typing import Optional, Dict, List, Tuple
from datetime import datetime

from . import config

logger = logging.getLogger(__name__)

try:
    from PIL import Image, ImageEnhance
    HAS_PIL = True
except ImportError:
    HAS_PIL = False


def ocr_receipt(image_path: str) -> dict:
    """
    Main function to extract receipt data from an image.

    Args:
        image_path: Path to receipt image (jpg, png, webp, etc.)

    Returns:
        Dictionary with keys:
        - raw_text: Full OCR output
        - vendor: Detected vendor name or None
        - date: Detected date (ISO format) or None
        - amounts: List of dicts with "amount" (Decimal) and "label"
        - total_incl: Total including BTW or None
        - total_excl: Total excluding BTW or None
        - btw_amount: BTW amount or None
        - btw_rate: BTW percentage (21, 6, etc.) or None
        - items: List of dicts with "description" and "amount"
        - confidence: Float 0-1 indicating confidence in parsing
        - errors: List of error messages encountered
    """
    errors = []
    result = {
        "raw_text": "",
        "vendor": None,
        "date": None,
        "amounts": [],
        "total_incl": None,
        "total_excl": None,
        "btw_amount": None,
        "btw_rate": None,
        "items": [],
        "confidence": 0.0,
        "errors": errors,
    }

    try:
        # Check if tesseract is available
        if not check_tesseract():
            errors.append(
                "Tesseract not installed. Install: sudo apt-get install tesseract-ocr (Linux) "
                "or brew install tesseract (macOS)"
            )
            return result

        # Preprocess image for better OCR
        processed_image = _preprocess_image(image_path)

        # Run tesseract OCR
        raw_text = _run_tesseract(processed_image)
        result["raw_text"] = raw_text

        if not raw_text.strip():
            errors.append("No text extracted from image by OCR")
            return result

        # Parse the OCR text
        parsed = _parse_receipt_text(raw_text)
        result.update(parsed)

        # Calculate confidence based on what we found
        confidence_score = 0.0
        checks = [
            (result["vendor"] is not None, 0.25),
            (result["date"] is not None, 0.25),
            (result["total_incl"] is not None or result["total_excl"] is not None, 0.25),
            (len(result["items"]) > 0, 0.25),
        ]

        for check, score in checks:
            if check:
                confidence_score += score

        result["confidence"] = confidence_score

    except Exception as e:
        errors.append(f"OCR processing error: {str(e)}")
        logger.exception("Error in ocr_receipt")

    return result


def _run_tesseract(image_path: str) -> str:
    """
    Run tesseract OCR on an image and return extracted text.

    Args:
        image_path: Path to image file

    Returns:
        Extracted text from OCR

    Raises:
        RuntimeError: If tesseract fails or is not installed
    """
    try:
        cmd = [
            config.TESSERACT_CMD,
            str(image_path),
            "stdout",
            "-l",
            config.OCR_LANG,
        ]

        if config.OCR_CONFIG:
            cmd.extend(config.OCR_CONFIG.split())

        result = subprocess.run(
            cmd, capture_output=True, text=True, timeout=30
        )

        if result.returncode != 0:
            error_msg = result.stderr or f"Tesseract failed with code {result.returncode}"
            raise RuntimeError(error_msg)

        return result.stdout

    except FileNotFoundError:
        raise RuntimeError(
            "Tesseract not found. Install: sudo apt-get install tesseract-ocr (Linux) "
            "or brew install tesseract (macOS)"
        )
    except subprocess.TimeoutExpired:
        raise RuntimeError("Tesseract OCR timed out (>30 seconds)")


def _preprocess_image(image_path: str) -> str:
    """
    Preprocess image for better OCR results.

    If PIL is available, converts to grayscale and increases contrast.
    Otherwise returns original image path.

    Args:
        image_path: Path to input image

    Returns:
        Path to processed image (temp file) or original path if PIL unavailable
    """
    if not HAS_PIL:
        return image_path

    try:
        img = Image.open(image_path)

        # Convert to grayscale
        img = img.convert("L")

        # Increase contrast
        enhancer = ImageEnhance.Contrast(img)
        img = enhancer.enhance(1.5)

        # Save to temp file
        temp_fd, temp_path = tempfile.mkstemp(suffix=".png")
        img.save(temp_path, "PNG")

        return temp_path

    except Exception as e:
        logger.warning(f"Image preprocessing failed, using original: {e}")
        return image_path


def _parse_receipt_text(text: str) -> dict:
    """
    Core parser for receipt text.

    Detects vendor, date, amounts, BTW, and individual line items
    from OCR text. Optimized for Belgian/Dutch receipts.

    Args:
        text: Raw OCR text from receipt

    Returns:
        Dictionary with parsed receipt data
    """
    result = {
        "vendor": None,
        "date": None,
        "amounts": [],
        "total_incl": None,
        "total_excl": None,
        "btw_amount": None,
        "btw_rate": None,
        "items": [],
    }

    lines = text.split("\n")

    # Detect vendor (usually in first few lines)
    result["vendor"] = _detect_vendor(text)

    # Detect date
    result["date"] = _detect_date(text)

    # Detect all amounts and their context
    amounts_data = _detect_amounts(text)
    result["amounts"] = amounts_data["all_amounts"]
    result["total_incl"] = amounts_data["total_incl"]
    result["total_excl"] = amounts_data["total_excl"]
    result["btw_amount"] = amounts_data["btw_amount"]
    result["btw_rate"] = amounts_data["btw_rate"]

    # Extract line items (description + amount pairs)
    result["items"] = _extract_items(lines)

    return result


def _detect_vendor(text: str) -> Optional[str]:
    """
    Detect vendor name from receipt text.

    Checks against known vendors from VENDOR_CATEGORY_MAP,
    then tries to extract from first non-empty line.

    Args:
        text: Full receipt text

    Returns:
        Vendor name or None
    """
    text_lower = text.lower()

    # Check against known vendors (exact/partial match)
    for vendor_keyword in config.VENDOR_CATEGORY_MAP.keys():
        if vendor_keyword.lower() in text_lower:
            # Return the more readable version if available
            return vendor_keyword.title()

    # Try to extract from first meaningful line
    lines = [line.strip() for line in text.split("\n") if line.strip()]
    if lines:
        first_line = lines[0]
        # Remove common noise
        if len(first_line) > 3 and len(first_line) < 100:
            # Skip if it looks like a number or date
            if not re.match(r"^\d{1,2}[-/\.]\d{1,2}[-/\.]\d{2,4}", first_line):
                return first_line

    return None


def _detect_date(text: str) -> Optional[str]:
    """
    Detect date from receipt text in ISO format (YYYY-MM-DD).

    Handles European date formats: DD/MM/YYYY, DD-MM-YYYY, DD.MM.YYYY

    Args:
        text: Receipt text

    Returns:
        ISO format date string or None
    """
    # Pattern: DD/MM/YYYY, DD-MM-YYYY, DD.MM.YYYY
    patterns = [
        r"(\d{1,2})[-/\.](\d{1,2})[-/\.](\d{4})",
    ]

    for pattern in patterns:
        matches = re.findall(pattern, text)
        for match in matches:
            day, month, year = match
            try:
                day_int = int(day)
                month_int = int(month)
                year_int = int(year)

                # Validate ranges (European format: DD/MM/YYYY)
                if 1 <= day_int <= 31 and 1 <= month_int <= 12:
                    # Create date and return ISO format
                    date_obj = datetime(year_int, month_int, day_int)
                    return date_obj.strftime("%Y-%m-%d")
            except ValueError:
                continue

    return None


def _detect_amounts(text: str) -> dict:
    """
    Find all monetary amounts and their context.

    Detects TOTAAL, SUBTOTAAL, BTW, TOTAL, TE BETALEN, etc.

    Args:
        text: Receipt text

    Returns:
        Dictionary with:
        - all_amounts: List of {"amount": Decimal, "label": str}
        - total_incl: Decimal or None
        - total_excl: Decimal or None
        - btw_amount: Decimal or None
        - btw_rate: int or None
    """
    result = {
        "all_amounts": [],
        "total_incl": None,
        "total_excl": None,
        "btw_amount": None,
        "btw_rate": None,
    }

    # Pattern for European number format: 1.234,56 or 1234,56
    amount_pattern = r"(TOTAAL|TOTAL|TE BETALEN|BEDRAG|SUBTOTAAL|SUBTOTAL|BTW|TVA|NETTO|BRUTO|OMZET)[:\s]+[\w\s]*?([\d\s.,]+)\s*EUR?"
    amount_pattern_simple = r"([\d\s.,]+)\s*EUR?"

    lines = text.split("\n")
    btw_rate_pattern = r"(BTW|TVA)\s+(\d{1,2})%"

    # Find BTW rate
    btw_matches = re.findall(btw_rate_pattern, text, re.IGNORECASE)
    if btw_matches:
        try:
            result["btw_rate"] = int(btw_matches[0][1])
        except (ValueError, IndexError):
            pass

    # Find labeled amounts
    for line in lines:
        line_upper = line.upper()

        # Match patterns like "TOTAAL: 123,45" or "TOTAL 456,78"
        matches = re.findall(amount_pattern, line, re.IGNORECASE)
        for match in matches:
            label = match[0].upper()
            amount_str = match[1]

            try:
                amount = _parse_decimal(amount_str)
                if amount:
                    result["all_amounts"].append({"amount": amount, "label": label})

                    # Categorize the amount
                    if "TOTAAL" in label or "TOTAL" in label:
                        if "TE BETALEN" in label or "BRUTO" in label:
                            result["total_incl"] = amount
                        elif "NETTO" in label or "SUBTOTAAL" in label:
                            result["total_excl"] = amount
                        else:
                            # Default to total_incl if no qualifier
                            result["total_incl"] = amount

                    elif "BTW" in label or "TVA" in label:
                        result["btw_amount"] = amount

            except ValueError:
                continue

    return result


def _extract_items(lines: List[str]) -> List[dict]:
    """
    Extract line items from receipt.

    Looks for lines with description + amount pattern.

    Args:
        lines: Receipt text split by newlines

    Returns:
        List of dicts with "description" and "amount"
    """
    items = []

    for line in lines:
        line = line.strip()
        if not line or len(line) < 3:
            continue

        # Skip known header/footer lines
        if any(skip in line.upper() for skip in [
            "TOTAAL", "TOTAL", "TE BETALEN", "BEDRAG",
            "BTW", "TVA", "BANCONTACT", "MASTERCARD", "VISA",
            "SUBTOTAAL", "NETTO", "BRUTO", "DATUM", "DATE",
            "WELKOM", "BEDANKT", "MERCI", "THANK YOU"
        ]):
            continue

        # Look for amount at end of line
        match = re.search(r"(.+?)\s+([\d\s.,]+)\s*$", line)
        if match:
            description = match.group(1).strip()
            amount_str = match.group(2)

            try:
                amount = _parse_decimal(amount_str)
                if amount and amount > 0:
                    items.append({
                        "description": description,
                        "amount": amount,
                    })
            except ValueError:
                continue

    return items


def _parse_decimal(value_str: str) -> Optional[Decimal]:
    """
    Parse a European-format decimal number.

    Handles: 1.234,56 (period as thousands separator, comma as decimal)
    Also handles: 1234,56 and 1234.56 (ambiguous, assumes comma if present)

    Args:
        value_str: String representation of amount

    Returns:
        Decimal or None if parsing fails
    """
    if not value_str:
        return None

    # Clean up whitespace
    value_str = value_str.strip()

    # Remove currency symbols and letters
    value_str = re.sub(r"[^\d.,]", "", value_str)

    if not value_str:
        return None

    # Determine if comma or period is decimal separator
    # European format: 1.234,56 (period = thousands, comma = decimal)
    if "," in value_str:
        # Comma is present, so it's the decimal separator
        # Remove periods (thousands separator)
        value_str = value_str.replace(".", "")
        value_str = value_str.replace(",", ".")
    else:
        # No comma, check for period
        # If more than one period, it's thousands separator
        if value_str.count(".") > 1:
            value_str = value_str.replace(".", "")
        # else: single period could be decimal or thousands (ambiguous)
        # For amounts under 1000, assume decimal
        if "." in value_str:
            parts = value_str.split(".")
            if len(parts[0]) <= 3:
                # Likely decimal separator
                pass
            else:
                # Likely thousands separator
                value_str = value_str.replace(".", "")

    try:
        return Decimal(value_str)
    except Exception:
        return None


def check_tesseract() -> bool:
    """
    Check if tesseract is installed and available.

    Returns:
        True if tesseract is available, False otherwise
    """
    try:
        result = subprocess.run(
            [config.TESSERACT_CMD, "--version"],
            capture_output=True,
            timeout=5,
        )
        return result.returncode == 0
    except (FileNotFoundError, subprocess.TimeoutExpired):
        return False
