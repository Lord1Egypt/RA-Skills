#!/usr/bin/env python3
"""
India GST toolkit for AI agents. Pure Python standard library, works offline.

Commands (input is a JSON string or a path to a .json file):
  validate  '{"gstin": "27AAPFU0939F1ZV"}'                     GSTIN check (format, checksum, state, PAN, entity)
  calc      '{"amount": 1000, "rate": 18, "inclusive": false,
               "supplier_state": "27", "pos_state": "29"}'      add/remove GST with CGST+SGST/UTGST or IGST split
  invoice   invoice.json  [--html out.html]                     GST tax invoice / bill of supply, Rule 46 checks
  check     '{"turnover_prev_fy": 62000000, "supply": "goods", "state": "27"}'
                                                                registration, composition, e-invoice, HSN digits,
                                                                e-way bill, return frequency
  dates     '{"month": "2026-11", "state": "27", "qrmp": false}' return due dates for a tax period
  words     '{"amount": 118000.5}'                               amount in words, Indian system (lakh/crore)
  example   invoice                                              print a sample invoice input

Rules as of November 2026 (GST 2.0 slabs from 22 Sep 2025). See references/rules.md.
"""
import html, json, re, sys
from datetime import date
from decimal import Decimal, ROUND_HALF_UP

RULES_AS_OF = "November 2026"
CURRENT_RATES = [0, 0.25, 1.5, 3, 5, 18, 40]   # 0.25 rough stones, 1.5 cut diamonds, 3 gold/silver
LEGACY_RATES = [12, 28]                         # removed for almost all goods/services on 22 Sep 2025

STATES = {
    "01": "Jammu and Kashmir", "02": "Himachal Pradesh", "03": "Punjab", "04": "Chandigarh",
    "05": "Uttarakhand", "06": "Haryana", "07": "Delhi", "08": "Rajasthan", "09": "Uttar Pradesh",
    "10": "Bihar", "11": "Sikkim", "12": "Arunachal Pradesh", "13": "Nagaland", "14": "Manipur",
    "15": "Mizoram", "16": "Tripura", "17": "Meghalaya", "18": "Assam", "19": "West Bengal",
    "20": "Jharkhand", "21": "Odisha", "22": "Chhattisgarh", "23": "Madhya Pradesh", "24": "Gujarat",
    "25": "Daman and Diu (old code)", "26": "Dadra and Nagar Haveli and Daman and Diu",
    "27": "Maharashtra", "28": "Andhra Pradesh (old code)", "29": "Karnataka", "30": "Goa",
    "31": "Lakshadweep", "32": "Kerala", "33": "Tamil Nadu", "34": "Puducherry",
    "35": "Andaman and Nicobar Islands", "36": "Telangana", "37": "Andhra Pradesh",
    "38": "Ladakh", "97": "Other Territory", "99": "Centre Jurisdiction",
}
# Union territories without a legislature charge UTGST instead of SGST
UTGST_STATES = {"04", "25", "26", "31", "35", "38", "97"}
# Registration thresholds (aggregate turnover, Rs) by state code
GOODS_THRESHOLD_20L = {"11", "12", "17", "05", "34", "36"}      # Sikkim, Arunachal, Meghalaya, Uttarakhand, Puducherry, Telangana
LOW_THRESHOLD_10L = {"13", "14", "15", "16"}                    # Nagaland, Manipur, Mizoram, Tripura (goods and services)
COMPOSITION_75L = {"11", "12", "13", "14", "15", "16", "17", "05"}  # special category states
# QRMP GSTR-3B due day: 22nd for these states, 24th for the rest
QRMP_22 = {"22", "23", "24", "25", "26", "27", "29", "30", "31", "32", "33", "34", "35", "36", "37"}

PAN_ENTITY = {"P": "Individual", "C": "Company", "H": "Hindu Undivided Family (HUF)", "F": "Firm / LLP",
              "A": "Association of Persons (AOP)", "T": "Trust", "B": "Body of Individuals (BOI)",
              "L": "Local Authority", "J": "Artificial Juridical Person", "G": "Government", "K": "Krish (trust)"}
CHARSET = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
GSTIN_RE = re.compile(r"^[0-9]{2}[A-Z]{5}[0-9]{4}[A-Z][1-9A-Z][A-Z][0-9A-Z]$")


def D(x):
    return Decimal(str(x))


def r2(x):
    return D(x).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)


def money(x):
    """Indian digit grouping: 1234567.5 -> 12,34,567.50"""
    x = r2(x)
    neg = x < 0
    s = f"{abs(x):.2f}"
    whole, frac = s.split(".")
    if len(whole) > 3:
        head, tail = whole[:-3], whole[-3:]
        head = re.sub(r"(\d)(?=(\d\d)+$)", r"\1,", head)
        whole = head + "," + tail
    return ("-" if neg else "") + whole + "." + frac


def state_code(v):
    """Accept '27', 27, 'Maharashtra', 'MH-like names' or a GSTIN; return 2-digit code or None."""
    if v is None:
        return None
    s = str(v).strip()
    if len(s) == 15 and s[:2].isdigit():
        return s[:2]
    if s.isdigit():
        s = s.zfill(2)
        return s if s in STATES else None
    low = s.lower()
    for code, name in STATES.items():
        if name.lower() == low or name.lower().startswith(low):
            if code not in ("25", "28"):
                return code
    return None


# ---------------------------------------------------------------- GSTIN
def gstin_checksum(first14):
    total = 0
    for i, ch in enumerate(first14):
        prod = CHARSET.index(ch) * (1 if i % 2 == 0 else 2)
        total += prod // 36 + prod % 36
    return CHARSET[(36 - total % 36) % 36]


def validate_gstin(g):
    g = str(g or "").strip().upper().replace(" ", "")
    out = {"gstin": g, "valid": False, "errors": [], "warnings": []}
    if len(g) != 15:
        out["errors"].append(f"GSTIN must be 15 characters (got {len(g)}).")
        return out
    if any(c not in CHARSET for c in g):
        out["errors"].append("Only capital letters A-Z and digits 0-9 are allowed.")
        return out
    if not GSTIN_RE.match(g):
        out["errors"].append("Pattern should be: 2-digit state code + 10-character PAN + entity number + letter + check character "
                             "(e.g. 27AAPFU0939F1ZV).")
    code = g[:2]
    if code not in STATES:
        out["errors"].append(f"'{code}' is not a valid GST state code.")
    expected = gstin_checksum(g[:14])
    if g[14] != expected:
        out["errors"].append(f"Check character is wrong: expected '{expected}', found '{g[14]}'. "
                             "Likely a typo - re-check the number.")
    if g[13] != "Z":
        out["warnings"].append("14th character is normally 'Z'; other letters are used for special registrations.")
    pan = g[2:12]
    out.update({
        "state_code": code, "state": STATES.get(code),
        "pan": pan, "entity_type": PAN_ENTITY.get(pan[3], "Other / special"),
        "registration_number_in_state": g[12],
        "valid": not out["errors"],
        "note": "Format and checksum only. Whether it is ACTIVE must be checked on services.gst.gov.in (Search Taxpayer).",
    })
    return out


# ---------------------------------------------------------------- calculation
def rate_warnings(rate):
    rate = float(rate)
    if rate in LEGACY_RATES:
        return [f"{rate:g}% was removed for almost all items on 22 Sep 2025 (GST 2.0). Most 12% items are now 5% and "
                f"most 28% items are now 18% (sin/luxury goods 40%). Use {rate:g}% only for old invoices or a notified exception."]
    if rate not in CURRENT_RATES:
        return [f"{rate:g}% is not a standard GST rate (current: 0, 5, 18, 40; special 0.25, 1.5, 3). Double-check it."]
    return []


def split_tax(taxable, rate, supplier, pos, export_lut=False):
    """Return dict of tax heads for one taxable value."""
    taxable = D(taxable)
    rate = D(rate)
    if export_lut:
        return {"type": "zero_rated_lut", "igst": r2(0), "cgst": r2(0), "sgst": r2(0), "label_sgst": "SGST"}
    inter = (supplier is None or pos is None or supplier != pos or pos == "97")
    if inter:
        return {"type": "inter_state", "igst": r2(taxable * rate / 100), "cgst": r2(0), "sgst": r2(0), "label_sgst": "SGST"}
    half = r2(taxable * rate / 200)
    return {"type": "intra_state", "igst": r2(0), "cgst": half, "sgst": half,
            "label_sgst": "UTGST" if supplier in UTGST_STATES else "SGST"}


def calc(d):
    amount, rate = D(d["amount"]), D(d.get("rate", 18))
    inclusive = bool(d.get("inclusive", False))
    sup, pos = state_code(d.get("supplier_state")), state_code(d.get("pos_state", d.get("supplier_state")))
    taxable = r2(amount * 100 / (100 + rate)) if inclusive else r2(amount)
    t = split_tax(taxable, rate, sup, pos)
    tax = t["igst"] + t["cgst"] + t["sgst"]
    if inclusive:   # keep the total exactly equal to what was entered
        taxable = r2(amount - tax)
    lab = t["label_sgst"]
    res = {"rate": float(rate), "taxable_value": float(taxable), "supply_type": t["type"],
           "cgst": float(t["cgst"]), lab.lower(): float(t["sgst"]), "igst": float(t["igst"]),
           "total_tax": float(tax), "total_amount": float(taxable + tax),
           "warnings": rate_warnings(rate)}
    if sup and pos:
        res["supplier_state"], res["place_of_supply"] = STATES[sup], STATES[pos]
    elif d.get("supplier_state") is None:
        res["warnings"].append("States not given: shown as IGST. Give supplier_state and pos_state for the correct split.")
    return res


# ---------------------------------------------------------------- amount in words
ONES = ["", "One", "Two", "Three", "Four", "Five", "Six", "Seven", "Eight", "Nine", "Ten", "Eleven", "Twelve",
        "Thirteen", "Fourteen", "Fifteen", "Sixteen", "Seventeen", "Eighteen", "Nineteen"]
TENS = ["", "", "Twenty", "Thirty", "Forty", "Fifty", "Sixty", "Seventy", "Eighty", "Ninety"]


def _two(n):
    return ONES[n] if n < 20 else (TENS[n // 10] + (" " + ONES[n % 10] if n % 10 else ""))


def _three(n):
    h, rest = divmod(n, 100)
    return ((ONES[h] + " Hundred" + (" " if rest else "")) if h else "") + (_two(rest) if rest else "")


def int_words(n):
    if n == 0:
        return "Zero"
    parts = []
    crore, n = divmod(n, 10000000)
    lakh, n = divmod(n, 100000)
    thousand, n = divmod(n, 1000)
    if crore:
        parts.append(int_words(crore) + " Crore")
    if lakh:
        parts.append(_two(lakh) + " Lakh")
    if thousand:
        parts.append(_two(thousand) + " Thousand")
    if n:
        parts.append(_three(n))
    return " ".join(parts)


def amount_words(x):
    x = r2(x)
    rupees = int(x)
    paise = int((x - rupees) * 100)
    s = "Rupees " + int_words(rupees)
    if paise:
        s += " and " + _two(paise) + " Paise"
    return s + " Only"


# ---------------------------------------------------------------- invoice
INV_NO_RE = re.compile(r"^[A-Za-z0-9/-]{1,16}$")


def build_invoice(d):
    errors, warnings = [], []
    sup = d.get("supplier", {})
    buy = d.get("buyer", {})
    scheme = d.get("scheme", "regular")              # regular | composition
    export_lut = bool(d.get("export_under_lut", False))
    turnover = float(d.get("supplier_turnover_prev_fy", 0) or 0)

    # supplier
    sv = validate_gstin(sup.get("gstin"))
    if not sv["valid"]:
        errors.append("Supplier GSTIN: " + "; ".join(sv["errors"]))
    s_code = sv.get("state_code") if sv.get("state_code") in STATES else state_code(sup.get("state"))
    for f in ("name", "address"):
        if not sup.get(f):
            errors.append(f"Supplier {f} is missing (Rule 46).")

    # buyer
    b2b = bool(buy.get("gstin"))
    b_code = None
    if b2b:
        bv = validate_gstin(buy["gstin"])
        if not bv["valid"]:
            errors.append("Buyer GSTIN: " + "; ".join(bv["errors"]))
        b_code = bv.get("state_code") if bv.get("state_code") in STATES else None
    pos = state_code(d.get("place_of_supply")) or state_code(buy.get("state")) or b_code
    if pos is None:
        pos = s_code
        warnings.append("Place of supply not given; assumed same state as supplier (intra-state).")

    # invoice number / date
    no = str(d.get("invoice_no", ""))
    if not INV_NO_RE.match(no):
        errors.append("Invoice number must be 1-16 characters using only letters, digits, '-' or '/', "
                      "unique and consecutive within the financial year.")
    inv_date = d.get("invoice_date") or date.today().isoformat()

    # lines
    lines, hsn_summary = [], {}
    tot = {"taxable": D(0), "cgst": D(0), "sgst": D(0), "igst": D(0)}
    label_sgst = "SGST"
    for i, it in enumerate(d.get("items", []), 1):
        qty, price = D(it.get("qty", 1)), D(it.get("rate", it.get("price", 0)))
        disc = D(it.get("discount", 0))
        gross = r2(qty * price)
        if it.get("price_includes_gst") and scheme != "composition":
            gross = r2(gross * 100 / (100 + D(it.get("gst_rate", 18))))
        taxable = r2(gross - disc)
        rate = D(0) if scheme == "composition" else D(it.get("gst_rate", 18))
        hsn = str(it.get("hsn", "")).strip()
        need = 6 if turnover > 5e7 else 4
        if not hsn:
            if b2b or turnover > 5e7:
                errors.append(f"Line {i}: HSN/SAC code is mandatory ({need}+ digits for this business).")
        elif len(hsn) < need and (b2b or turnover > 5e7):
            warnings.append(f"Line {i}: HSN/SAC '{hsn}' has {len(hsn)} digits; at least {need} are required.")
        if scheme != "composition":
            warnings += [f"Line {i}: {w}" for w in rate_warnings(rate)]
        t = split_tax(taxable, rate, s_code, pos, export_lut)
        label_sgst = t["label_sgst"]
        line = {"sno": i, "description": it.get("description", ""), "hsn": hsn, "qty": float(qty),
                "unit": it.get("unit", "NOS"), "rate": float(price), "discount": float(disc),
                "taxable": float(taxable), "gst_rate": float(rate),
                "cgst": float(t["cgst"]), "sgst": float(t["sgst"]), "igst": float(t["igst"])}
        line["total"] = float(taxable + t["cgst"] + t["sgst"] + t["igst"])
        lines.append(line)
        for k, v in (("taxable", taxable), ("cgst", t["cgst"]), ("sgst", t["sgst"]), ("igst", t["igst"])):
            tot[k] += v
        key = (hsn or "-", float(rate))
        h = hsn_summary.setdefault(key, {"hsn": key[0], "gst_rate": key[1], "taxable": D(0), "cgst": D(0), "sgst": D(0), "igst": D(0)})
        for k in ("taxable", "cgst", "sgst", "igst"):
            h[k] += {"taxable": taxable, "cgst": t["cgst"], "sgst": t["sgst"], "igst": t["igst"]}[k]
    if not lines:
        errors.append("At least one item is required.")

    grand = tot["taxable"] + tot["cgst"] + tot["sgst"] + tot["igst"]
    rounded = grand.quantize(Decimal("1"), rounding=ROUND_HALF_UP)
    round_off = rounded - grand

    # document-level rules
    inter = s_code != pos
    if not b2b and grand >= 50000 and not buy.get("address"):
        errors.append("Unregistered buyer, invoice Rs 50,000 or more: buyer name, address and delivery state are mandatory (Rule 46).")
    if not b2b and inter and grand > 100000:
        warnings.append("Inter-state B2C invoice above Rs 1 lakh: report invoice-wise in GSTR-1 (B2CL).")
    if turnover > 5e7 and b2b:
        warnings.append("Supplier turnover crossed Rs 5 crore: this B2B invoice must be an e-invoice with IRN + QR code from the IRP.")
    if scheme == "composition" and inter:
        errors.append("Composition taxpayers cannot make inter-state supplies of goods.")
    if d.get("goods", True) and grand > 50000 and not export_lut:
        warnings.append("Goods worth over Rs 50,000: an e-way bill is needed before moving them.")

    title = "Bill of Supply" if scheme == "composition" else "Tax Invoice"
    declaration = None
    if scheme == "composition":
        declaration = "Composition taxable person, not eligible to collect tax on supplies."
    elif export_lut:
        declaration = "Supply meant for export / supply to SEZ unit or developer under LUT without payment of integrated tax."

    return {
        "title": title, "invoice_no": no, "invoice_date": inv_date,
        "supplier": {**sup, "state_code": s_code, "state": STATES.get(s_code)},
        "buyer": {**buy, "type": "B2B" if b2b else "B2C"},
        "place_of_supply": {"code": pos, "state": STATES.get(pos)},
        "supply_type": "zero-rated (LUT)" if export_lut else ("inter-state (IGST)" if inter else f"intra-state (CGST + {label_sgst})"),
        "reverse_charge": "Yes" if d.get("reverse_charge") else "No",
        "items": lines,
        "hsn_summary": [{k: (float(v) if isinstance(v, Decimal) else v) for k, v in h.items()} for h in hsn_summary.values()],
        "totals": {"taxable": float(tot["taxable"]), "cgst": float(tot["cgst"]), label_sgst.lower(): float(tot["sgst"]),
                   "igst": float(tot["igst"]), "round_off": float(round_off), "grand_total": float(rounded),
                   "in_words": amount_words(rounded)},
        "label_sgst": label_sgst, "declaration": declaration,
        "bank": d.get("bank"), "upi_id": d.get("upi_id"), "notes": d.get("notes"),
        "errors": errors, "warnings": warnings, "ready_to_issue": not errors,
    }


LABELS = {"ifsc": "IFSC", "account_no": "Account No", "account_name": "Account Name", "bank_name": "Bank", "branch": "Branch"}


def invoice_html(inv):
    e = lambda x: html.escape(str(x if x is not None else ""))
    s, b, t = inv["supplier"], inv["buyer"], inv["totals"]
    L = inv["label_sgst"]
    rows = "".join(
        f"<tr><td>{l['sno']}</td><td>{e(l['description'])}</td><td>{e(l['hsn'])}</td>"
        f"<td class=r>{l['qty']:g} {e(l['unit'])}</td><td class=r>{money(l['rate'])}</td>"
        f"<td class=r>{money(l['discount']) if l['discount'] else '-'}</td><td class=r>{money(l['taxable'])}</td>"
        f"<td class=r>{l['gst_rate']:g}%</td><td class=r>{money(l['total'])}</td></tr>" for l in inv["items"])
    hs = "".join(
        f"<tr><td>{e(h['hsn'])}</td><td class=r>{money(h['taxable'])}</td><td class=r>{h['gst_rate']:g}%</td>"
        f"<td class=r>{money(h['cgst'])}</td><td class=r>{money(h['sgst'])}</td><td class=r>{money(h['igst'])}</td>"
        f"<td class=r>{money(h['cgst'] + h['sgst'] + h['igst'])}</td></tr>" for h in inv["hsn_summary"])
    pay = ""
    if inv.get("bank") or inv.get("upi_id"):
        bk = inv.get("bank") or {}
        pay = "<div class=box><b>Payment details</b><br>" + "<br>".join(
            e(f"{LABELS.get(k, k.replace('_', ' ').title())}: {v}") for k, v in bk.items()) + (
            f"<br>UPI: {e(inv['upi_id'])}" if inv.get("upi_id") else "") + "</div>"
    decl = f"<p class=decl>{e(inv['declaration'])}</p>" if inv.get("declaration") else ""
    tax_rows = ""
    if t["igst"]:
        tax_rows += f"<tr><td>IGST</td><td class=r>{money(t['igst'])}</td></tr>"
    if t["cgst"] or t.get(L.lower()):
        tax_rows += f"<tr><td>CGST</td><td class=r>{money(t['cgst'])}</td></tr><tr><td>{L}</td><td class=r>{money(t[L.lower()])}</td></tr>"
    return f"""<!DOCTYPE html><html><head><meta charset="utf-8"><title>{e(inv['title'])} {e(inv['invoice_no'])}</title>
<style>
body{{font-family:Arial,Helvetica,sans-serif;font-size:12px;color:#111;max-width:820px;margin:24px auto;padding:0 16px}}
h1{{font-size:20px;text-align:center;margin:0 0 2px;letter-spacing:1px}} .sub{{text-align:center;color:#555;margin-bottom:14px}}
.grid{{display:flex;gap:12px}} .box{{border:1px solid #999;padding:8px;flex:1;margin-bottom:10px}}
table{{width:100%;border-collapse:collapse;margin-bottom:10px}} th,td{{border:1px solid #999;padding:5px;vertical-align:top}}
th{{background:#f0f0f0;font-size:11px}} .r{{text-align:right}} .tot td{{border:none;padding:3px 5px}}
.grand{{font-size:15px;font-weight:bold;border-top:2px solid #111!important}} .decl{{font-weight:bold;border:1px dashed #555;padding:6px}}
.sign{{text-align:right;margin-top:40px}} @media print{{body{{margin:0}}}}
</style></head><body>
<h1>{e(inv['title']).upper()}</h1><div class=sub>Original for Recipient</div>
<div class=grid>
 <div class=box><b>{e(s.get('name'))}</b><br>{e(s.get('address'))}<br>GSTIN: <b>{e(s.get('gstin'))}</b><br>
 State: {e(s.get('state'))} ({e(s.get('state_code'))}){('<br>Phone: ' + e(s['phone'])) if s.get('phone') else ''}</div>
 <div class=box>Invoice No: <b>{e(inv['invoice_no'])}</b><br>Date: <b>{e(inv['invoice_date'])}</b><br>
 Place of Supply: {e(inv['place_of_supply']['state'])} ({e(inv['place_of_supply']['code'])})<br>
 Reverse Charge: {e(inv['reverse_charge'])}</div>
</div>
<div class=box><b>Bill To:</b> {e(b.get('name'))}<br>{e(b.get('address'))}<br>
{('GSTIN: <b>' + e(b['gstin']) + '</b>') if b.get('gstin') else 'Unregistered (B2C)'}
{('<br><b>Ship To:</b> ' + e(b['ship_to'])) if b.get('ship_to') else ''}</div>
<table><tr><th>#</th><th>Description</th><th>HSN/SAC</th><th>Qty</th><th>Rate</th><th>Discount</th><th>Taxable Value</th><th>GST</th><th>Amount</th></tr>{rows}</table>
<div class=grid>
 <div style="flex:1.4">
  <table><tr><th>HSN/SAC</th><th>Taxable</th><th>Rate</th><th>CGST</th><th>{L}</th><th>IGST</th><th>Total Tax</th></tr>{hs}</table>
  <div class=box><b>Amount in words:</b><br>{e(t['in_words'])}</div>{pay}
 </div>
 <div style="flex:1"><table class=tot>
  <tr><td>Taxable Value</td><td class=r>{money(t['taxable'])}</td></tr>{tax_rows}
  <tr><td>Round Off</td><td class=r>{money(t['round_off'])}</td></tr>
  <tr><td class=grand>Grand Total</td><td class="r grand">&#8377; {money(t['grand_total'])}</td></tr></table></div>
</div>
{decl}{('<p>' + e(inv['notes']) + '</p>') if inv.get('notes') else ''}
<div class=sign>For <b>{e(s.get('name'))}</b><br><br><br>Authorised Signatory</div>
</body></html>"""


EXAMPLE_INVOICE = {
    "invoice_no": "INV/26-27/0042",
    "invoice_date": "2026-11-19",
    "supplier": {"name": "Bhatia Digital Studio", "address": "12 MG Road, Pune 411001",
                 "gstin": "27AAPFU0939F1ZV", "phone": "+91 98xxxxxx10"},
    "supplier_turnover_prev_fy": 3500000,
    "buyer": {"name": "Acme Retail Pvt Ltd", "address": "4th Floor, Koramangala, Bengaluru 560034",
              "gstin": "29AAGCA1234B1Z8"},
    "place_of_supply": "29",
    "goods": False,
    "items": [
        {"description": "Website design and development", "hsn": "998314", "qty": 1, "unit": "NOS",
         "rate": 85000, "gst_rate": 18},
        {"description": "Social media creatives (pack of 20)", "hsn": "998361", "qty": 2, "unit": "NOS",
         "rate": 7500, "discount": 1000, "gst_rate": 18},
    ],
    "bank": {"account_name": "Bhatia Digital Studio", "account_no": "XXXX XXXX 1234", "ifsc": "HDFC0000123"},
    "upi_id": "bhatiastudio@okhdfc",
    "notes": "Payment due within 15 days.",
}


# ---------------------------------------------------------------- compliance check
def compliance(d):
    prev = float(d.get("turnover_prev_fy", 0) or 0)
    curr = float(d.get("turnover_current_fy", prev) or 0)
    supply = str(d.get("supply", "goods")).lower()          # goods | services | both
    st = state_code(d.get("state")) or "27"
    agg = max(prev, curr)
    out = {"state": STATES.get(st), "rules_as_of": RULES_AS_OF, "items": []}
    add = lambda topic, verdict, detail: out["items"].append({"topic": topic, "verdict": verdict, "detail": detail})

    # registration
    if supply == "goods":
        limit = 1000000 if st in LOW_THRESHOLD_10L else 2000000 if st in GOODS_THRESHOLD_20L else 4000000
    else:
        limit = 1000000 if st in LOW_THRESHOLD_10L else 2000000
    must = agg > limit or d.get("inter_state_goods") or d.get("sells_on_ecommerce")
    why = f"threshold in {STATES[st]} for {supply}: Rs {money(limit)[:-3]}"
    if d.get("inter_state_goods"):
        why += "; inter-state supply of goods needs registration regardless of turnover"
    if d.get("sells_on_ecommerce"):
        why += "; selling goods through e-commerce operators generally needs registration (small-seller relaxations may apply)"
    add("GST registration", "REQUIRED" if must else "Not required (voluntary allowed)", why)

    # composition
    if supply == "goods":
        climit = 7500000 if st in COMPOSITION_75L else 15000000
        crate = "1% (traders/manufacturers), 5% (restaurants)"
    else:
        climit, crate = 5000000, "6% (services / mixed suppliers)"
    elig = prev <= climit and not d.get("inter_state_goods") and not d.get("sells_on_ecommerce")
    add("Composition scheme", "Eligible" if elig else "Not eligible",
        f"limit Rs {money(climit)[:-3]}, rate {crate}. Composition dealers issue a Bill of Supply, cannot charge GST "
        "or claim input tax credit, and cannot supply goods inter-state.")

    # e-invoice
    ever = float(d.get("max_turnover_any_fy_since_2017", prev) or 0)
    if ever > 5e7:
        add("E-invoicing", "MANDATORY", "Aggregate turnover crossed Rs 5 crore in a year since 2017-18: all B2B, export and "
            "B2G invoices need an IRN + QR code." + (" Turnover is Rs 10 crore or more: report each invoice to the IRP within "
            "30 days of its date or it is rejected." if ever >= 1e8 else ""))
    else:
        add("E-invoicing", "Not required", "Applies only once aggregate turnover crosses Rs 5 crore in any year since 2017-18.")

    # HSN
    add("HSN/SAC on invoices", "6 digits" if prev > 5e7 else "4 digits",
        "6 digits on all invoices (turnover above Rs 5 crore)." if prev > 5e7 else
        "4 digits on B2B invoices; optional on B2C invoices (turnover up to Rs 5 crore).")

    # e-way bill
    if supply in ("goods", "both"):
        add("E-way bill", "When moving goods > Rs 50,000",
            "Needed for each consignment worth over Rs 50,000; validity is 1 day per 200 km for normal cargo.")

    # returns
    if elig and d.get("opted_composition"):
        add("Returns", "CMP-08 quarterly + GSTR-4 yearly", "CMP-08 by the 18th after each quarter; GSTR-4 by 30 April.")
    elif prev <= 5e7:
        add("Returns", "Monthly or QRMP (quarterly) - your choice",
            "QRMP: GSTR-1 quarterly (13th), GSTR-3B quarterly (22nd/24th by state), tax paid monthly by the 25th via PMT-06. "
            "Monthly: GSTR-1 by the 11th, GSTR-3B by the 20th.")
    else:
        add("Returns", "Monthly", "GSTR-1 by the 11th, GSTR-3B by the 20th of the next month; GSTR-9 annual return by 31 December.")
    add("Input tax credit", "Only what appears in GSTR-2B / IMS",
        "Accept, reject or keep pending supplier invoices in the Invoice Management System (IMS) before filing GSTR-3B; "
        "ITC in GSTR-3B is auto-filled from GSTR-2B/IMS.")
    out["note"] = ("Thresholds are general rules; special cases (casual/non-resident taxable persons, TDS/TCS, notified goods) differ. "
                   "Confirm on gst.gov.in or with a CA.")
    return out


# ---------------------------------------------------------------- due dates
def due_dates(d):
    y, m = map(int, str(d.get("month", date.today().strftime("%Y-%m"))).split("-"))
    ny, nm = (y + 1, 1) if m == 12 else (y, m + 1)
    st = state_code(d.get("state")) or "27"
    nxt = lambda day: date(ny, nm, day).isoformat()
    period = f"{y}-{m:02d}"
    if d.get("composition"):
        if m in (6, 9, 12, 3):
            return {"tax_period": period, "CMP-08 (quarterly payment)": nxt(18),
                    "note": "GSTR-4 annual return is due 30 April after the financial year."}
        return {"tax_period": period, "note": "No composition filing this month; CMP-08 is due on the 18th after the quarter ends."}
    if d.get("qrmp"):
        if m in (6, 9, 12, 3):
            day = 22 if st in QRMP_22 else 24
            return {"tax_period": period, "GSTR-1 (quarterly)": nxt(13), "GSTR-3B (quarterly)": nxt(day),
                    "late_fee": "Rs 50/day (Rs 20/day for nil returns) + 18% interest on late tax"}
        return {"tax_period": period, "IFF (optional B2B invoices)": nxt(13), "PMT-06 (monthly tax payment)": nxt(25)}
    res = {"tax_period": period, "GSTR-1": nxt(11), "GSTR-3B": nxt(20),
           "late_fee": "Rs 50/day (Rs 20/day for nil returns) + 18% interest on late tax"}
    if m == 3:
        res["GSTR-9 (annual)"] = date(y, 12, 31).isoformat()
    res["note"] = ("Standard due dates; if a date falls on a holiday or the government extends it, the extended date applies. "
                   "Returns older than 3 years can no longer be filed.")
    return res


# ---------------------------------------------------------------- CLI
def load(arg):
    if arg.endswith(".json"):
        return json.load(open(arg, encoding="utf-8"))
    return json.loads(arg)


def main():
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    cmd = sys.argv[1]
    if cmd == "example":
        print(json.dumps(EXAMPLE_INVOICE, indent=2))
        return
    if len(sys.argv) < 3:
        sys.exit(__doc__)
    data = load(sys.argv[2])
    if cmd == "validate":
        res = validate_gstin(data.get("gstin")) if isinstance(data, dict) and "gstin" in data else \
              [validate_gstin(g) for g in data.get("gstins", [])]
    elif cmd == "calc":
        res = calc(data)
    elif cmd == "words":
        res = {"amount": data["amount"], "in_words": amount_words(data["amount"])}
    elif cmd == "check":
        res = compliance(data)
    elif cmd == "dates":
        res = due_dates(data)
    elif cmd == "invoice":
        res = build_invoice(data)
        if "--html" in sys.argv:
            path = sys.argv[sys.argv.index("--html") + 1]
            with open(path, "w", encoding="utf-8") as f:
                f.write(invoice_html(res))
            res["html_file"] = path
    else:
        sys.exit(f"Unknown command '{cmd}'.\n" + __doc__)
    print(json.dumps(res, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
