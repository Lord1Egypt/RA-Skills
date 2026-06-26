"""
Nex E-Invoice - UBL 2.1 / Peppol BIS 3.0 Invoice Generator
MIT-0 License - Copyright 2026 Nex AI (Kevin Blancaflor)
"""

import xml.etree.ElementTree as ET
import xml.dom.minidom
from decimal import Decimal, ROUND_HALF_UP
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
from collections import defaultdict

from .config import (
    CUSTOMIZATION_ID,
    PROFILE_ID,
    PEPPOL_ENDPOINT_SCHEME,
    BTW_TO_UBL,
    DEFAULT_CURRENCY,
    DEFAULT_COUNTRY,
    PAYMENT_TERMS_DAYS,
)


# ─────────────────────────────────────────────────────────────────────────────
# UBL Namespace Configuration
# ─────────────────────────────────────────────────────────────────────────────

UBL_NS = "urn:oasis:names:specification:ubl:schema:xsd:Invoice-2"
CAC_NS = "urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2"
CBC_NS = "urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2"

NS = {
    None: UBL_NS,
    "cac": CAC_NS,
    "cbc": CBC_NS,
}

# Register namespaces to avoid ns0, ns1 prefixes
ET.register_namespace("", UBL_NS)
ET.register_namespace("cac", CAC_NS)
ET.register_namespace("cbc", CBC_NS)


# ─────────────────────────────────────────────────────────────────────────────
# Helper Functions
# ─────────────────────────────────────────────────────────────────────────────


def _q(tag: str, ns: Optional[str] = None) -> str:
    """Create a qualified tag name with namespace."""
    if ns:
        return f"{{{NS[ns]}}}{tag}"
    return tag


def _set_element(parent: ET.Element, tag: str, text: str, ns: Optional[str] = None) -> ET.Element:
    """Create and append an element with text."""
    elem = ET.SubElement(parent, _q(tag, ns))
    if text is not None:
        elem.text = str(text)
    return elem


def _format_amount(value) -> str:
    """Format a value as a decimal with 2 places."""
    if isinstance(value, str):
        value = Decimal(value)
    elif not isinstance(value, Decimal):
        value = Decimal(str(value))

    quantized = value.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
    return str(quantized)


def validate_vat_number(vat: str) -> bool:
    """
    Validate a Belgian VAT number using modulo 97 check digit.
    Format: BE + 10 digits (check digit at position 2-3)
    """
    vat = vat.upper().strip()

    if not vat.startswith("BE"):
        return False

    digits = vat[2:]
    if len(digits) != 10 or not digits.isdigit():
        return False

    # Extract check digit (first 2 digits after BE)
    check_digits = int(digits[:2])
    number = int(digits[2:])

    # Calculate modulo 97
    # For Belgian VAT: 98 - ((97 - (96 - number % 97)) % 97) = check_digits
    calculated_check = 98 - ((97 - (96 + number) % 97) % 97)

    return calculated_check == check_digits


def generate_payment_reference(invoice_number: str) -> str:
    """
    Generate a Belgian structured payment reference (gestructureerde mededeling).
    Format: +++XXX/XXXX/XXXXX+++ with modulo 97 check digits.

    Algorithm:
    1. Take invoice number, pad/truncate to 9 digits
    2. Calculate modulo 97: 97 - (9-digit number % 97)
    3. Format as +++XXX/XXXX/XXXXX+++
    """
    # Extract digits from invoice number
    digits_only = "".join(c for c in invoice_number if c.isdigit())

    # Pad or truncate to 9 digits
    digits_only = digits_only[-9:].zfill(9)
    number = int(digits_only)

    # Calculate modulo 97 check digit
    check_digit = 97 - (number % 97)

    # Format as 12-digit number: 2-digit check + 9-digit base + 1 padding
    reference = f"{check_digit:02d}{digits_only}0"

    # Format as +++XXX/XXXX/XXXXX+++
    formatted = f"+++{reference[:3]}/{reference[3:7]}/{reference[7:12]}+++"

    return formatted


def _calculate_line_total(quantity: Decimal, unit_price: Decimal) -> Decimal:
    """Calculate line total (quantity * unit_price)."""
    return (quantity * unit_price).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)


def _group_lines_by_tax_rate(lines: List[Dict]) -> Dict[int, List[Dict]]:
    """Group invoice lines by VAT rate for tax calculation."""
    grouped = defaultdict(list)
    for line in lines:
        btw_rate = int(line.get("btw_rate", 21))
        grouped[btw_rate].append(line)
    return grouped


# ─────────────────────────────────────────────────────────────────────────────
# Core UBL Building Functions
# ─────────────────────────────────────────────────────────────────────────────


def _build_party(parent: ET.Element, party_type: str, party_data: Dict) -> ET.Element:
    """
    Build AccountingSupplierParty or AccountingCustomerParty element.

    Args:
        parent: Parent XML element
        party_type: "supplier" or "customer"
        party_data: Dict with name, vat, kbo, street, city, postcode, country, email, phone, peppol_id

    Returns:
        The party element
    """
    tag = "AccountingSupplierParty" if party_type == "supplier" else "AccountingCustomerParty"
    party_elem = ET.SubElement(parent, _q(tag, "cac"))

    # Party element with endpoint ID
    party = ET.SubElement(party_elem, _q("Party", "cac"))

    # Endpoint ID (Peppol ID) - required
    if peppol_id := party_data.get("peppol_id"):
        endpoint = _set_element(party, "EndpointID", peppol_id, "cbc")
        endpoint.set("schemeID", PEPPOL_ENDPOINT_SCHEME)

    # Party Identification (KBO number)
    if kbo := party_data.get("kbo"):
        party_id = ET.SubElement(party, _q("PartyIdentification", "cac"))
        _set_element(party_id, "ID", kbo, "cbc")

    # Party Name
    party_name = ET.SubElement(party, _q("PartyName", "cac"))
    _set_element(party_name, "Name", party_data.get("name", ""), "cbc")

    # Postal Address
    address = ET.SubElement(party, _q("PostalAddress", "cac"))
    if street := party_data.get("street"):
        _set_element(address, "StreetName", street, "cbc")
    if city := party_data.get("city"):
        _set_element(address, "CityName", city, "cbc")
    if postcode := party_data.get("postcode"):
        _set_element(address, "PostalZone", postcode, "cbc")

    country = ET.SubElement(address, _q("Country", "cac"))
    _set_element(country, "IdentificationCode", party_data.get("country", DEFAULT_COUNTRY), "cbc")

    # Tax Scheme (VAT)
    if vat := party_data.get("vat"):
        tax_scheme = ET.SubElement(party, _q("PartyTaxScheme", "cac"))
        _set_element(tax_scheme, "CompanyID", vat, "cbc")

        ts = ET.SubElement(tax_scheme, _q("TaxScheme", "cac"))
        _set_element(ts, "ID", "VAT", "cbc")

    # Party Legal Entity (Registration Name)
    if name := party_data.get("name"):
        legal = ET.SubElement(party, _q("PartyLegalEntity", "cac"))
        _set_element(legal, "RegistrationName", name, "cbc")

    # Contact (optional)
    email = party_data.get("email")
    phone = party_data.get("phone")
    if email or phone:
        contact = ET.SubElement(party, _q("Contact", "cac"))
        if email:
            _set_element(contact, "ElectronicMail", email, "cbc")
        if phone:
            _set_element(contact, "Telephone", phone, "cbc")

    return party_elem


def _build_payment_means(parent: ET.Element, payment_data: Dict) -> ET.Element:
    """Build PaymentMeans element."""
    payment = ET.SubElement(parent, _q("PaymentMeans", "cac"))

    means_code = payment_data.get("means_code", "30")
    _set_element(payment, "PaymentMeansCode", means_code, "cbc")

    if reference := payment_data.get("reference"):
        _set_element(payment, "PaymentID", reference, "cbc")

    # Payee Financial Account (IBAN)
    if iban := payment_data.get("iban"):
        account = ET.SubElement(payment, _q("PayeeFinancialAccount", "cac"))
        _set_element(account, "ID", iban, "cbc")

        # BIC (optional)
        if bic := payment_data.get("bic"):
            branch = ET.SubElement(account, _q("FinancialInstitutionBranch", "cac"))
            _set_element(branch, "ID", bic, "cbc")

    return payment


def _build_payment_terms(parent: ET.Element, payment_data: Dict) -> ET.Element:
    """Build PaymentTerms element."""
    terms = ET.SubElement(parent, _q("PaymentTerms", "cac"))

    if note := payment_data.get("terms"):
        _set_element(terms, "Note", note, "cbc")

    return terms


def _build_tax_totals(lines: List[Dict], currency: str) -> ET.Element:
    """
    Build TaxTotal element with TaxSubtotal for each VAT rate group.

    Returns the parent element that should be appended to root.
    """
    grouped = _group_lines_by_tax_rate(lines)

    # Calculate total tax amount across all groups
    total_tax = Decimal("0")
    for btw_rate, group_lines in grouped.items():
        for line in group_lines:
            qty = Decimal(str(line.get("quantity", 0)))
            price = Decimal(str(line.get("unit_price", 0)))
            line_total = _calculate_line_total(qty, price)
            tax_rate = Decimal(str(btw_rate)) / Decimal("100")
            total_tax += (line_total * tax_rate).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

    # Create root TaxTotal
    tax_total = ET.Element(_q("TaxTotal", "cac"))
    tax_amount_elem = _set_element(tax_total, "TaxAmount", _format_amount(total_tax), "cbc")
    tax_amount_elem.set("currencyID", currency)

    # Create TaxSubtotal for each rate
    for btw_rate, group_lines in sorted(grouped.items()):
        subtotal = ET.SubElement(tax_total, _q("TaxSubtotal", "cac"))

        # Calculate taxable amount and tax for this group
        taxable_amount = Decimal("0")
        tax_amount = Decimal("0")

        for line in group_lines:
            qty = Decimal(str(line.get("quantity", 0)))
            price = Decimal(str(line.get("unit_price", 0)))
            line_total = _calculate_line_total(qty, price)
            taxable_amount += line_total
            tax_rate = Decimal(str(btw_rate)) / Decimal("100")
            tax_amount += (line_total * tax_rate).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

        # TaxableAmount
        taxable_elem = _set_element(subtotal, "TaxableAmount", _format_amount(taxable_amount), "cbc")
        taxable_elem.set("currencyID", currency)

        # TaxAmount
        tax_elem = _set_element(subtotal, "TaxAmount", _format_amount(tax_amount), "cbc")
        tax_elem.set("currencyID", currency)

        # TaxCategory with Percent and TaxScheme
        category = ET.SubElement(subtotal, _q("TaxCategory", "cac"))

        # Map BTW rate to UBL tax category
        ubl_category, percent_str = BTW_TO_UBL.get(btw_rate, ("O", "0.00"))
        _set_element(category, "ID", ubl_category, "cbc")
        _set_element(category, "Percent", percent_str, "cbc")

        scheme = ET.SubElement(category, _q("TaxScheme", "cac"))
        _set_element(scheme, "ID", "VAT", "cbc")

    return tax_total


def _build_monetary_totals(lines: List[Dict], tax_total_elem: ET.Element, currency: str) -> ET.Element:
    """
    Build LegalMonetaryTotal element.

    Requires tax_total_elem to extract total tax amount.
    """
    # Calculate line extension amount (sum of all line totals excl. VAT)
    line_extension = Decimal("0")
    for line in lines:
        qty = Decimal(str(line.get("quantity", 0)))
        price = Decimal(str(line.get("unit_price", 0)))
        line_total = _calculate_line_total(qty, price)
        line_extension += line_total

    # Extract total tax from tax_total_elem
    tax_amount_elem = tax_total_elem.find(_q("TaxAmount", "cbc"))
    total_tax = Decimal(tax_amount_elem.text) if tax_amount_elem is not None else Decimal("0")

    # Calculate totals
    tax_exclusive = line_extension
    tax_inclusive = tax_exclusive + total_tax
    payable_amount = tax_inclusive

    # Create LegalMonetaryTotal
    monetary = ET.Element(_q("LegalMonetaryTotal", "cac"))

    line_ext_elem = _set_element(monetary, "LineExtensionAmount", _format_amount(line_extension), "cbc")
    line_ext_elem.set("currencyID", currency)

    tax_excl_elem = _set_element(monetary, "TaxExclusiveAmount", _format_amount(tax_exclusive), "cbc")
    tax_excl_elem.set("currencyID", currency)

    tax_incl_elem = _set_element(monetary, "TaxInclusiveAmount", _format_amount(tax_inclusive), "cbc")
    tax_incl_elem.set("currencyID", currency)

    payable_elem = _set_element(monetary, "PayableAmount", _format_amount(payable_amount), "cbc")
    payable_elem.set("currencyID", currency)

    return monetary


def _pretty_print_xml(xml_str: str, indent: str = "  ") -> str:
    """Fallback pretty-print XML string without reparsing."""
    result = []
    current_indent = 0

    # Simple pretty-printer
    in_tag = False
    tag_content = ""

    for char in xml_str:
        if char == "<":
            if tag_content.strip():
                result.append(" " * (current_indent * 2) + tag_content.strip())
            in_tag = True
            tag_content = "<"
        elif char == ">":
            tag_content += ">"
            # Check if it's a closing or self-closing tag
            if tag_content.startswith("</"):
                current_indent = max(0, current_indent - 1)
            result.append(" " * (current_indent * 2) + tag_content.strip())
            if not tag_content.startswith("</") and not tag_content.endswith("/>"):
                current_indent += 1
            in_tag = False
            tag_content = ""
        else:
            tag_content += char

    if tag_content.strip():
        result.append(tag_content.strip())

    return '<?xml version="1.0" encoding="UTF-8"?>\n' + "\n".join(result)


def _build_invoice_lines(lines: List[Dict], currency: str) -> List[ET.Element]:
    """Build InvoiceLine elements (one per line item)."""
    invoice_lines = []

    for idx, line in enumerate(lines, 1):
        line_elem = ET.Element(_q("InvoiceLine", "cac"))

        # Line ID
        _set_element(line_elem, "ID", str(idx), "cbc")

        # Quantity and unit code
        qty = line.get("quantity", 0)
        unit_code = line.get("unit_code", "C62")  # C62 = unit, HUR = hour, DAY = day
        qty_elem = _set_element(line_elem, "InvoicedQuantity", _format_amount(qty), "cbc")
        qty_elem.set("unitCode", unit_code)

        # Line Extension Amount (total excl. VAT)
        qty_decimal = Decimal(str(qty))
        price_decimal = Decimal(str(line.get("unit_price", 0)))
        line_total = _calculate_line_total(qty_decimal, price_decimal)

        line_ext = _set_element(line_elem, "LineExtensionAmount", _format_amount(line_total), "cbc")
        line_ext.set("currencyID", currency)

        # Item
        item = ET.SubElement(line_elem, _q("Item", "cac"))
        _set_element(item, "Name", line.get("description", ""), "cbc")

        # Item Tax Category
        tax_cat = ET.SubElement(item, _q("ClassifiedTaxCategory", "cac"))
        btw_rate = int(line.get("btw_rate", 21))
        ubl_category, percent_str = BTW_TO_UBL.get(btw_rate, ("O", "0.00"))

        _set_element(tax_cat, "ID", ubl_category, "cbc")
        _set_element(tax_cat, "Percent", percent_str, "cbc")

        tax_scheme = ET.SubElement(tax_cat, _q("TaxScheme", "cac"))
        _set_element(tax_scheme, "ID", "VAT", "cbc")

        # Price
        price = ET.SubElement(line_elem, _q("Price", "cac"))
        price_amount = _set_element(price, "PriceAmount", _format_amount(price_decimal), "cbc")
        price_amount.set("currencyID", currency)

        invoice_lines.append(line_elem)

    return invoice_lines


# ─────────────────────────────────────────────────────────────────────────────
# Main Invoice Generator
# ─────────────────────────────────────────────────────────────────────────────


def generate_invoice_xml(invoice_data: Dict) -> str:
    """
    Generate a complete UBL 2.1 Invoice XML string.

    Args:
        invoice_data: Dictionary with structure:
            {
                "invoice_number": "INV-2026-0001",
                "issue_date": "2026-04-05",
                "due_date": "2026-05-05",
                "type_code": "380",
                "currency": "EUR",
                "note": "optional",
                "buyer_reference": "optional",
                "seller": {
                    "name": str,
                    "vat": str,
                    "kbo": str,
                    "street": str,
                    "city": str,
                    "postcode": str,
                    "country": str,
                    "email": str (optional),
                    "phone": str (optional),
                    "iban": str,
                    "bic": str,
                    "peppol_id": str,
                },
                "buyer": {
                    "name": str,
                    "vat": str,
                    "kbo": str,
                    "street": str,
                    "city": str,
                    "postcode": str,
                    "country": str,
                    "email": str (optional),
                    "peppol_id": str,
                },
                "payment": {
                    "means_code": "30" (credit transfer) or "58" (SEPA),
                    "reference": "+++xxx/xxx/xxxxx+++",
                    "terms": "Betaling binnen 30 dagen",
                    "iban": str (optional),
                    "bic": str (optional),
                },
                "lines": [
                    {
                        "description": str,
                        "quantity": float or Decimal,
                        "unit_code": "C62" (units) or "HUR" (hours) or "DAY" (days),
                        "unit_price": float or Decimal,
                        "btw_rate": int (0, 6, 12, or 21),
                    },
                    ...
                ],
            }

    Returns:
        Pretty-printed UBL 2.1 XML string
    """

    currency = invoice_data.get("currency", DEFAULT_CURRENCY)
    lines = invoice_data.get("lines", [])

    # Root element: Invoice
    # Create root element with the default UBL namespace
    root = ET.Element("{%s}Invoice" % UBL_NS)

    # ─── Document Header ─────────────────────────────────────────────────────

    _set_element(root, "CustomizationID", CUSTOMIZATION_ID, "cbc")
    _set_element(root, "ProfileID", PROFILE_ID, "cbc")
    _set_element(root, "ID", invoice_data.get("invoice_number", ""), "cbc")
    _set_element(root, "IssueDate", invoice_data.get("issue_date", ""), "cbc")
    _set_element(root, "DueDate", invoice_data.get("due_date", ""), "cbc")

    type_code = _set_element(root, "InvoiceTypeCode", invoice_data.get("type_code", "380"), "cbc")
    type_code.set("listID", "UNCL1001")
    type_code.set("listAgencyID", "6")

    if note := invoice_data.get("note"):
        _set_element(root, "Note", note, "cbc")

    doc_currency = _set_element(root, "DocumentCurrencyCode", currency, "cbc")
    doc_currency.set("listID", "ISO4217")
    doc_currency.set("listAgencyID", "6")

    if buyer_ref := invoice_data.get("buyer_reference"):
        _set_element(root, "BuyerReference", buyer_ref, "cbc")

    # ─── Parties ─────────────────────────────────────────────────────────────

    seller_data = invoice_data.get("seller", {})
    buyer_data = invoice_data.get("buyer", {})

    _build_party(root, "supplier", seller_data)
    _build_party(root, "customer", buyer_data)

    # ─── Payment ─────────────────────────────────────────────────────────────

    payment_data = invoice_data.get("payment", {})
    if not payment_data.get("reference"):
        payment_data["reference"] = generate_payment_reference(invoice_data.get("invoice_number", ""))

    _build_payment_means(root, payment_data)
    _build_payment_terms(root, payment_data)

    # ─── Tax Totals ──────────────────────────────────────────────────────────

    tax_total_elem = _build_tax_totals(lines, currency)
    root.append(tax_total_elem)

    # ─── Monetary Totals ─────────────────────────────────────────────────────

    monetary_elem = _build_monetary_totals(lines, tax_total_elem, currency)
    root.append(monetary_elem)

    # ─── Invoice Lines ──────────────────────────────────────────────────────

    for line_elem in _build_invoice_lines(lines, currency):
        root.append(line_elem)

    # ─── Pretty-print and return ─────────────────────────────────────────────

    xml_str = ET.tostring(root, encoding="unicode", method="xml")

    # Pretty-print without reparsing to avoid namespace duplication
    try:
        dom = xml.dom.minidom.parseString(xml_str)
        pretty_xml = dom.toprettyxml(indent="  ")
        # Remove XML declaration and extra blank lines
        lines_out = [line for line in pretty_xml.split("\n") if line.strip()]
        xml_output = '<?xml version="1.0" encoding="UTF-8"?>\n'
        xml_output += "\n".join(lines_out[1:])
    except Exception:
        # Fallback: manually format with indentation
        xml_output = _pretty_print_xml(xml_str)

    return xml_output
