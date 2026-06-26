"""
Nex E-Invoice - Natural Language Invoice Parser
MIT-0 License - Copyright 2026 Nex AI (Kevin Blancaflor)

Parses Dutch and English natural language invoice descriptions into structured data.
"""

import re
from decimal import Decimal, InvalidOperation
from typing import Optional, Tuple


def parse_amount(text: str) -> Optional[Decimal]:
    """
    Extract a monetary amount from text.
    Handles: "2.50", "2,50", "2.500,00" (European format), "€2.50", "2.50 euro"

    Args:
        text: Input text containing an amount

    Returns:
        Decimal amount, or None if no valid amount found
    """
    if not text:
        return None

    # Remove currency symbols
    text = re.sub(r'[€$]', '', text).strip()

    # Match amounts with various separators
    # Pattern: optional digits, optional separator (. or ,), digits
    # European format: 1.000,00 or 1000,00
    # US format: 1,000.00 or 1000.00

    # Try European format first (comma as decimal separator)
    euro_match = re.search(r'\b(\d{1,3}(?:\.\d{3})*|\d+),(\d{2})\b', text)
    if euro_match:
        amount_str = euro_match.group(1).replace('.', '') + '.' + euro_match.group(2)
        try:
            return Decimal(amount_str)
        except (InvalidOperation, ValueError):
            pass

    # Try simple decimal format with either . or , as separator
    decimal_match = re.search(r'\b(\d+[.,]\d{2})\b', text)
    if decimal_match:
        amount_str = decimal_match.group(1).replace(',', '.')
        try:
            return Decimal(amount_str)
        except (InvalidOperation, ValueError):
            pass

    # Try integer amounts
    int_match = re.search(r'\b(\d+)\s*(?:euro|EUR|€)?\b', text)
    if int_match:
        try:
            return Decimal(int_match.group(1))
        except (InvalidOperation, ValueError):
            pass

    return None


def parse_quantity(text: str) -> Tuple[Decimal, str]:
    """
    Extract quantity and unit code from text.

    Examples:
        "3x" -> (Decimal(3), "C62")
        "5 hours" -> (Decimal(5), "HUR")
        "12 maanden" -> (Decimal(12), "MON")
        "1 dag" -> (Decimal(1), "DAY")

    Args:
        text: Input text containing quantity and optional unit

    Returns:
        Tuple of (quantity, unit_code). Default unit is "C62" (piece)
    """
    if not text:
        return Decimal(1), "C62"

    # Match quantity patterns: "3x", "3x ", "3 ", "3"
    qty_match = re.search(r'(\d+)\s*[x×]?\s*', text)
    quantity = Decimal(1)
    if qty_match:
        try:
            quantity = Decimal(qty_match.group(1))
        except (InvalidOperation, ValueError):
            quantity = Decimal(1)

    # Detect unit type
    unit_code = "C62"  # Default: piece

    text_lower = text.lower()

    # Hours
    if re.search(r'\b(uur|hour|hours|uren|hrs?)\b', text_lower):
        unit_code = "HUR"
    # Days
    elif re.search(r'\b(dag|day|days|dagen)\b', text_lower):
        unit_code = "DAY"
    # Months
    elif re.search(r'\b(maand|maanden|month|months|mnd)\b', text_lower):
        unit_code = "MON"
    # Weeks
    elif re.search(r'\b(week|weeks|weken)\b', text_lower):
        unit_code = "WEE"
    # Kilograms
    elif re.search(r'\b(kg|kilogram|kilograms)\b', text_lower):
        unit_code = "KGM"
    # Meters
    elif re.search(r'\b(m|meter|meters|metre|metres)\b', text_lower):
        unit_code = "MTR"
    # Liters
    elif re.search(r'\b(l|liter|liters|litre|litres)\b', text_lower):
        unit_code = "LTR"

    return quantity, unit_code


def detect_btw_rate(text: str) -> Optional[int]:
    """
    Extract BTW/VAT rate from text fragment.

    Returns: 21, 12, 6, or 0 (for BTW-vrij/exempt), or None if not specified
    """
    if not text:
        return None

    text_lower = text.lower()

    # Check for zero-rated/exempt
    if re.search(r'btw-vrij|btw\s*vrij|vat\s*exempt|exempt|0%\s*(?:btw|vat)', text_lower):
        return 0

    # Check for specific rates (order matters - check longer patterns first)
    if re.search(r'(21\s*%|%\s*21|btw\s*21|21\s*btw|vat\s*21|21\s*vat)', text_lower):
        return 21
    if re.search(r'(12\s*%|%\s*12|btw\s*12|12\s*btw|vat\s*12|12\s*vat)', text_lower):
        return 12
    if re.search(r'(6\s*%|%\s*6|btw\s*6|6\s*btw|vat\s*6|6\s*vat)', text_lower):
        return 6

    return None


def normalize_company_name(name: str) -> str:
    """
    Clean up company name: strip quotes, normalize whitespace, capitalize properly.

    Args:
        name: Raw company name

    Returns:
        Normalized company name
    """
    if not name:
        return ""

    # Remove quotes
    name = re.sub(r'^["\']|["\']$', '', name.strip())

    # Normalize whitespace
    name = ' '.join(name.split())

    # Capitalize each word (but preserve all-caps abbreviations like BV, NV)
    words = name.split()
    result = []
    for word in words:
        if len(word) <= 2 and word.isupper():
            # Keep 2-letter abbreviations in lowercase for title case
            result.append(word.lower() if len(word) == 2 else word)
        else:
            # Title case
            result.append(word.capitalize())

    return ' '.join(result)


def parse_invoice_text(text: str) -> dict:
    """
    Parse natural language invoice description into structured data.

    Input examples:
        - "factureer Bakkerij Peeters 3x broodjes aan 2.50, BTW 6%"
        - "invoice ECHO Management for 5 hours consulting at 95/hour, 21% VAT"
        - "factuur voor Ribbens Airco: website redesign 2499 euro, BTW 21% en hosting 12 maanden x 29.99, BTW 21%"
        - "credit nota voor Watt's Smart BV: retour 2x sensor 45 euro, 21%"

    Returns:
        dict with:
            - "buyer_name": extracted company/person name
            - "is_credit_note": bool
            - "lines": list of line items
            - "notes": any additional text
            - "errors": list of parsing warnings
    """
    errors = []

    if not text or not text.strip():
        return {
            "buyer_name": "",
            "is_credit_note": False,
            "lines": [],
            "notes": "",
            "errors": ["Empty input text"]
        }

    original_text = text
    text = text.strip()

    # Detect credit note
    is_credit_note = bool(re.search(
        r'\b(credit\s*nota|creditnota|credit\s*note|retour)\b',
        text,
        re.IGNORECASE
    ))

    # Extract buyer name
    buyer_name = ""

    # Pattern 1: "credit nota voor <name>"
    credit_pattern = re.search(
        r'credit\s+nota?\s+voor\s+(.+?)(?:\s*:|\s+retour)',
        text,
        re.IGNORECASE
    )
    if credit_pattern:
        name_candidate = credit_pattern.group(1).strip()
        if name_candidate and len(name_candidate) > 1:
            buyer_name = normalize_company_name(name_candidate)

    # Pattern 2: "factureer <name>" - stop before quantity indicators
    if not buyer_name:
        factureer_pattern = re.search(
            r'factureer\s+([^:]+?)(?:\s+(?:\d+\s*[x×]|\d+\s+(?:hour|uur)))',
            text,
            re.IGNORECASE
        )
        if factureer_pattern:
            buyer_name = normalize_company_name(factureer_pattern.group(1).strip())

    # Pattern 3: "factuur voor <name>" - stop before colon
    if not buyer_name:
        factuur_pattern = re.search(
            r'factuur\s+voor\s+([^:]+?)(?:\s*:)',
            text,
            re.IGNORECASE
        )
        if factuur_pattern:
            buyer_name = normalize_company_name(factuur_pattern.group(1).strip())

    # Pattern 4: "invoice <name>" - stop before quantity indicators
    if not buyer_name:
        invoice_pattern = re.search(
            r'invoice\s+([^:]+?)(?:\s+(?:for|at))',
            text,
            re.IGNORECASE
        )
        if invoice_pattern:
            buyer_name = normalize_company_name(invoice_pattern.group(1).strip())

    # Extract line items content - remove just the header part
    lines = []
    notes = []
    invoice_text = text

    # Remove invoice descriptor (factureer, invoice, etc.) but keep everything after
    invoice_text = re.sub(
        r'^(?:factureer|factuur\s+voor|invoice|bill)\s+',
        '',
        invoice_text,
        flags=re.IGNORECASE
    )

    # Remove credit nota header
    invoice_text = re.sub(
        r'^credit\s+nota?\s+voor\s+',
        '',
        invoice_text,
        flags=re.IGNORECASE
    )

    # Remove company name up to colon (if present)
    if ':' in invoice_text:
        # Remove everything up to and including the colon
        invoice_text = re.sub(r'^[^:]*:\s*', '', invoice_text)
    else:
        # Try to find where line items start, backing up to include description
        match = re.search(r'(\w+\s+)*?(\d+\s*[x×]|\d+\s+(?:hour|uur|maanden)|\d+(?:\s*(?:euro|EUR|€)))', invoice_text, re.IGNORECASE)
        if match:
            # Find the start of the first descriptive word before the numbers
            # Back up to find word boundary before first number
            start = match.start(2)
            if match.group(1):
                start = match.start(1)
            invoice_text = invoice_text[start:]

    # Split by "en" (Dutch and) - but be careful not to split inside words
    invoice_text = invoice_text.strip()
    segments = re.split(r'\s+en\s+', invoice_text, flags=re.IGNORECASE)

    for segment in segments:
        segment = segment.strip()
        if not segment:
            continue

        # Try to parse as line item
        line = _parse_line_item(segment)

        if line:
            lines.append(line)
        else:
            # If didn't parse as single line, try splitting by comma
            if ',' in segment:
                subsegments = re.split(r',', segment)
                found_line = False
                for subseg in subsegments:
                    subseg = subseg.strip()
                    if not subseg:
                        continue
                    subline = _parse_line_item(subseg)
                    if subline:
                        lines.append(subline)
                        found_line = True
                    else:
                        if subseg:
                            notes.append(subseg)
                if not found_line and segment:
                    notes.append(segment)
            else:
                # Couldn't parse, treat as note
                if segment:
                    notes.append(segment)

    return {
        "buyer_name": buyer_name,
        "is_credit_note": is_credit_note,
        "lines": lines,
        "notes": " ".join(notes),
        "errors": errors
    }


def _parse_line_item(text: str) -> Optional[dict]:
    """
    Parse a single line item from text.

    Examples:
        "3x broodjes aan 2.50" -> qty=3, desc="broodjes", price=2.50
        "5 hours consulting at 95/hour" -> qty=5, desc="consulting", price=95, unit="HUR"
        "12 maanden x 29.99" -> qty=12, desc="maanden", price=29.99
        "website redesign 2499 euro" -> qty=1, desc="website redesign", price=2499
        "2x sensor 45 euro" -> qty=2, desc="sensor", price=45

    Returns:
        dict with description, quantity, unit_price, btw_rate, unit_code, or None
    """
    text = text.strip()
    if not text:
        return None

    # Extract BTW rate from the line
    btw_rate = detect_btw_rate(text)
    if btw_rate is None:
        btw_rate = 21  # Default to Belgian standard rate

    # Remove BTW info from text for further parsing
    text_no_btw = re.sub(
        r',?\s*(?:btw|vat)\s*[0-9%]*\s*(?:btw|vat)?\s*,?',
        '',
        text,
        flags=re.IGNORECASE
    ).strip()

    # Try pattern: "QTY x description aan/at PRICE"
    # Examples: "3x broodjes aan 2.50", "2x sensor 45 euro"
    pattern1 = re.search(
        r'(\d+)\s*[x×]\s*(\w+(?:\s+\w+)?)\s+(?:aan|at|for)\s+([0-9.,€\s]+)',
        text_no_btw,
        re.IGNORECASE
    )

    if pattern1:
        qty_str = pattern1.group(1)
        desc = pattern1.group(2).strip()
        price_str = pattern1.group(3).strip()

        try:
            quantity = Decimal(qty_str)
            price = parse_amount(price_str)

            if price is not None:
                _, unit_code = parse_quantity(desc)
                return {
                    "description": desc,
                    "quantity": quantity,
                    "unit_price": price,
                    "btw_rate": btw_rate,
                    "unit_code": unit_code
                }
        except (InvalidOperation, ValueError):
            pass

    # Try pattern: "QTY hours description at PRICE/hour"
    # Example: "5 hours consulting at 95/hour"
    pattern_hours = re.search(
        r'(\d+)\s+(?:hour|hours|uur|uren)\s+([a-zA-Z\s]+?)\s+(?:at|@)\s+([0-9.,]+)',
        text_no_btw,
        re.IGNORECASE
    )

    if pattern_hours:
        qty_str = pattern_hours.group(1)
        desc = pattern_hours.group(2).strip()
        price_str = pattern_hours.group(3).strip()

        try:
            quantity = Decimal(qty_str)
            price = parse_amount(price_str)

            if price is not None:
                return {
                    "description": desc,
                    "quantity": quantity,
                    "unit_price": price,
                    "btw_rate": btw_rate,
                    "unit_code": "HUR"
                }
        except (InvalidOperation, ValueError):
            pass

    # Try pattern: "QTY description x PRICE"
    # Example: "12 maanden x 29.99"
    pattern2 = re.search(
        r'(\d+)\s+([a-zA-Z]+)\s+[x×]\s+([0-9.,€\s]+)',
        text_no_btw,
        re.IGNORECASE
    )

    if pattern2:
        qty_str = pattern2.group(1)
        unit_str = pattern2.group(2)
        price_str = pattern2.group(3).strip()

        try:
            quantity = Decimal(qty_str)
            price = parse_amount(price_str)

            if price is not None:
                _, unit_code = parse_quantity(unit_str)
                return {
                    "description": unit_str,
                    "quantity": quantity,
                    "unit_price": price,
                    "btw_rate": btw_rate,
                    "unit_code": unit_code
                }
        except (InvalidOperation, ValueError):
            pass

    # Try pattern: "QTY x description PRICE euro"
    # Example: "2x sensor 45 euro"
    pattern3a = re.search(
        r'(\d+)\s*[x×]\s+(\w+(?:\s+\w+)?)\s+([0-9.,]+)\s*(?:euro|EUR|€)?',
        text_no_btw,
        re.IGNORECASE
    )

    if pattern3a:
        qty_str = pattern3a.group(1)
        desc = pattern3a.group(2).strip()
        price_str = pattern3a.group(3).strip()

        try:
            quantity = Decimal(qty_str)
            price = parse_amount(price_str)

            if price is not None:
                return {
                    "description": desc,
                    "quantity": quantity,
                    "unit_price": price,
                    "btw_rate": btw_rate,
                    "unit_code": "C62"
                }
        except (InvalidOperation, ValueError):
            pass

    # Try pattern: "description QTY x PRICE"
    # Example: "sensor 2x 45 euro"
    pattern3 = re.search(
        r'(\w+(?:\s+\w+)?)\s+(\d+)\s*[x×]\s+([0-9.,€\s]+)',
        text_no_btw,
        re.IGNORECASE
    )

    if pattern3:
        desc = pattern3.group(1).strip()
        qty_str = pattern3.group(2)
        price_str = pattern3.group(3).strip()

        try:
            quantity = Decimal(qty_str)
            price = parse_amount(price_str)

            if price is not None:
                return {
                    "description": desc,
                    "quantity": quantity,
                    "unit_price": price,
                    "btw_rate": btw_rate,
                    "unit_code": "C62"
                }
        except (InvalidOperation, ValueError):
            pass

    # Try pattern: "description NUMBER euro/EUR"
    # Example: "website redesign 2499 euro"
    pattern4 = re.search(
        r'([a-zA-Z\s]+?)\s+([0-9.,]+)\s*(?:euro|EUR|€)',
        text_no_btw,
        re.IGNORECASE
    )

    if pattern4:
        desc = pattern4.group(1).strip()
        price_str = pattern4.group(2).strip()

        try:
            price = parse_amount(price_str)
            if price is not None:
                return {
                    "description": desc,
                    "quantity": Decimal(1),
                    "unit_price": price,
                    "btw_rate": btw_rate,
                    "unit_code": "C62"
                }
        except (InvalidOperation, ValueError):
            pass

    # Fallback: try to find ANY price in the text
    price = parse_amount(text_no_btw)
    if price is not None:
        # Remove the price from description
        desc = re.sub(r'[0-9.,€]+\s*(?:euro|EUR|€)?', '', text_no_btw).strip()
        if desc and len(desc) > 1:  # Make sure description is not just 1-2 chars
            return {
                "description": desc,
                "quantity": Decimal(1),
                "unit_price": price,
                "btw_rate": btw_rate,
                "unit_code": "C62"
            }

    return None


# ==============================================================================
# COMPREHENSIVE UNIT TESTS
# ==============================================================================

if __name__ == "__main__":
    import sys

    test_cases = [
        {
            "input": "factureer Bakkerij Peeters 3x broodjes aan 2.50, BTW 6%",
            "expected": {
                "buyer_name": "Bakkerij Peeters",
                "is_credit_note": False,
                "lines_count": 1,
                "first_line": {
                    "description": "broodjes",
                    "quantity": Decimal(3),
                    "unit_price": Decimal("2.50"),
                    "btw_rate": 6,
                }
            },
            "name": "Dutch: factureer with quantity and BTW"
        },
        {
            "input": "invoice ECHO Management for 5 hours consulting at 95/hour, 21% VAT",
            "expected": {
                "buyer_name": "Echo Management",
                "is_credit_note": False,
                "lines_count": 1,
                "first_line": {
                    "description": "consulting",
                    "quantity": Decimal(5),
                    "unit_price": Decimal(95),
                    "btw_rate": 21,
                    "unit_code": "HUR"
                }
            },
            "name": "English: invoice with hours"
        },
        {
            "input": "factuur voor Ribbens Airco: website redesign 2499 euro, BTW 21% en hosting 12 maanden x 29.99, BTW 21%",
            "expected": {
                "buyer_name": "Ribbens Airco",
                "is_credit_note": False,
                "lines_count": 2,
                "first_line": {
                    "description": "website redesign",
                    "quantity": Decimal(1),
                    "unit_price": Decimal(2499),
                    "btw_rate": 21,
                }
            },
            "name": "Dutch: factuur voor with multiple items"
        },
        {
            "input": "credit nota voor Watt's Smart BV: retour 2x sensor 45 euro, 21%",
            "expected": {
                "buyer_name": "Watt's Smart bv",
                "is_credit_note": True,
                "lines_count": 1,
                "first_line": {
                    "description": "sensor",
                    "quantity": Decimal(2),
                    "unit_price": Decimal(45),
                    "btw_rate": 21,
                }
            },
            "name": "Dutch: credit nota with retour"
        },
        {
            "input": "factureer Jan Jansen 10x koffie aan 1,50",
            "expected": {
                "buyer_name": "Jan Jansen",
                "is_credit_note": False,
                "lines_count": 1,
                "first_line": {
                    "description": "koffie",
                    "quantity": Decimal(10),
                    "unit_price": Decimal("1.50"),
                    "btw_rate": 21,  # Default
                }
            },
            "name": "Dutch: comma as decimal separator"
        },
    ]

    passed = 0
    failed = 0

    for test in test_cases:
        result = parse_invoice_text(test["input"])

        success = True
        errors = []

        # Check buyer name
        if result["buyer_name"] != test["expected"]["buyer_name"]:
            success = False
            errors.append(f"  buyer_name: expected '{test['expected']['buyer_name']}', got '{result['buyer_name']}'")

        # Check credit note flag
        if result["is_credit_note"] != test["expected"]["is_credit_note"]:
            success = False
            errors.append(f"  is_credit_note: expected {test['expected']['is_credit_note']}, got {result['is_credit_note']}")

        # Check line count
        if len(result["lines"]) != test["expected"]["lines_count"]:
            success = False
            errors.append(f"  lines_count: expected {test['expected']['lines_count']}, got {len(result['lines'])}")

        # Check first line details
        if result["lines"] and "first_line" in test["expected"]:
            first = result["lines"][0]
            expected_first = test["expected"]["first_line"]

            for key, expected_val in expected_first.items():
                actual_val = first.get(key)
                if actual_val != expected_val:
                    success = False
                    errors.append(f"  first_line.{key}: expected {expected_val}, got {actual_val}")

        # Print result
        status = "PASS" if success else "FAIL"
        print(f"[{status}] {test['name']}")
        if errors:
            for error in errors:
                print(error)

        if success:
            passed += 1
        else:
            failed += 1

    # Additional unit tests for individual functions
    print("\n--- Function-level tests ---\n")

    function_tests = [
        {
            "func": "parse_amount",
            "input": "€2.50",
            "expected": Decimal("2.50"),
            "name": "parse_amount: EUR symbol with dot"
        },
        {
            "func": "parse_amount",
            "input": "2,50 euro",
            "expected": Decimal("2.50"),
            "name": "parse_amount: comma separator with euro"
        },
        {
            "func": "parse_amount",
            "input": "1.234,56",
            "expected": Decimal("1234.56"),
            "name": "parse_amount: European thousands format"
        },
        {
            "func": "parse_quantity",
            "input": "5 hours",
            "expected": (Decimal(5), "HUR"),
            "name": "parse_quantity: hours"
        },
        {
            "func": "parse_quantity",
            "input": "12 maanden",
            "expected": (Decimal(12), "MON"),
            "name": "parse_quantity: maanden"
        },
        {
            "func": "detect_btw_rate",
            "input": "btw 6%",
            "expected": 6,
            "name": "detect_btw_rate: 6%"
        },
        {
            "func": "detect_btw_rate",
            "input": "21% VAT",
            "expected": 21,
            "name": "detect_btw_rate: 21% VAT"
        },
        {
            "func": "detect_btw_rate",
            "input": "BTW-vrij",
            "expected": 0,
            "name": "detect_btw_rate: exempt"
        },
        {
            "func": "normalize_company_name",
            "input": "'watt's smart bv'",
            "expected": "Watt's Smart Bv",
            "name": "normalize_company_name: with quotes"
        },
    ]

    for test in function_tests:
        func_name = test["func"]

        if func_name == "parse_amount":
            result = parse_amount(test["input"])
        elif func_name == "parse_quantity":
            result = parse_quantity(test["input"])
        elif func_name == "detect_btw_rate":
            result = detect_btw_rate(test["input"])
        elif func_name == "normalize_company_name":
            result = normalize_company_name(test["input"])

        success = result == test["expected"]
        status = "PASS" if success else "FAIL"
        print(f"[{status}] {test['name']}")
        if not success:
            print(f"  expected {test['expected']}, got {result}")

        if success:
            passed += 1
        else:
            failed += 1

    # Summary
    print(f"\n{'='*60}")
    print(f"Total: {passed} passed, {failed} failed")
    print(f"{'='*60}")

    sys.exit(0 if failed == 0 else 1)
