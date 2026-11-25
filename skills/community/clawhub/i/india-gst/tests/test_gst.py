"""Run: python3 tests/test_gst.py  (from the skill folder)"""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))
from gst import validate_gstin, calc, amount_words, build_invoice, compliance, due_dates, money, EXAMPLE_INVOICE
import copy

results = []
def check(name, got, want):
    results.append((name, got == want, got, want))

# GSTIN
check("valid sample GSTIN", validate_gstin("27AAPFU0939F1ZV")["valid"], True)
check("lowercase + spaces accepted", validate_gstin(" 27aapfu0939f1zv ")["valid"], True)
check("typo caught by checksum", validate_gstin("27AAPFU0939F1ZW")["valid"], False)
check("bad state code", validate_gstin("99AAPFU0939F1Z" + "V")["state_code"], "99")
check("wrong length", validate_gstin("27AAPFU0939F1Z")["valid"], False)
check("entity type firm", validate_gstin("27AAPFU0939F1ZV")["entity_type"], "Firm / LLP")
check("state name", validate_gstin("24AAACC1206D1ZM")["state"], "Gujarat")

# calc
c = calc({"amount": 1000, "rate": 18, "supplier_state": "27", "pos_state": "27"})
check("intra-state split", (c["cgst"], c["sgst"], c["igst"]), (90.0, 90.0, 0.0))
c = calc({"amount": 1000, "rate": 18, "supplier_state": "Maharashtra", "pos_state": "Karnataka"})
check("inter-state IGST", (c["igst"], c["total_amount"]), (180.0, 1180.0))
c = calc({"amount": 1180, "rate": 18, "inclusive": True, "supplier_state": "27", "pos_state": "27"})
check("remove GST from 1180", c["taxable_value"], 1000.0)
c = calc({"amount": 999, "rate": 5, "inclusive": True, "supplier_state": "07", "pos_state": "07"})
check("inclusive total preserved", c["total_amount"], 999.0)
c = calc({"amount": 1000, "rate": 18, "supplier_state": "Chandigarh", "pos_state": "04"})
check("Chandigarh uses UTGST", c.get("utgst"), 90.0)
check("12% rate warns", len(calc({"amount": 100, "rate": 12, "supplier_state": "27"})["warnings"]) > 0, True)

# words / money
check("words lakh", amount_words(118000), "Rupees One Lakh Eighteen Thousand Only")
check("words crore+paise", amount_words(12500000.5), "Rupees One Crore Twenty Five Lakh and Fifty Paise Only")
check("words 101", amount_words(101), "Rupees One Hundred One Only")
check("indian grouping", money(1234567.5), "12,34,567.50")

# invoice
inv = build_invoice(copy.deepcopy(EXAMPLE_INVOICE))
check("example invoice has no errors", inv["errors"], [])
check("example totals", (inv["totals"]["taxable"], inv["totals"]["igst"], inv["totals"]["grand_total"]), (99000.0, 17820.0, 116820.0))
bad = copy.deepcopy(EXAMPLE_INVOICE); bad["invoice_no"] = "INV#2026-27-000001"
check("invalid invoice number caught", any("Invoice number" in e for e in build_invoice(bad)["errors"]), True)
b2c = copy.deepcopy(EXAMPLE_INVOICE); b2c["buyer"] = {"name": "Walk-in"}; b2c["place_of_supply"] = "27"
r = build_invoice(b2c)
check("B2C >= 50k needs address", any("50,000" in e for e in r["errors"]), True)
check("same state -> CGST+SGST", r["supply_type"].startswith("intra"), True)
comp = copy.deepcopy(EXAMPLE_INVOICE); comp["scheme"] = "composition"; comp["place_of_supply"] = "27"
comp["buyer"]["gstin"] = "27AAPFU0939F1ZV"
r = build_invoice(comp)
check("composition = bill of supply, no tax", (r["title"], r["totals"]["cgst"]), ("Bill of Supply", 0.0))
lut = copy.deepcopy(EXAMPLE_INVOICE); lut["export_under_lut"] = True
check("LUT export zero tax", build_invoice(lut)["totals"]["igst"], 0.0)
big = copy.deepcopy(EXAMPLE_INVOICE); big["supplier_turnover_prev_fy"] = 80000000; big["items"][0]["hsn"] = "9983"
r = build_invoice(big)
check("6-digit HSN warning above 5cr", any("at least 6" in w for w in r["warnings"]), True)
check("e-invoice warning above 5cr", any("e-invoice" in w for w in r["warnings"]), True)

# compliance + dates
v = {i["topic"]: i["verdict"] for i in compliance({"turnover_prev_fy": 3000000, "supply": "goods", "state": "27"})["items"]}
check("30L goods in MH: no registration", v["GST registration"].startswith("Not"), True)
v = {i["topic"]: i["verdict"] for i in compliance({"turnover_prev_fy": 3000000, "supply": "goods", "state": "Telangana"})["items"]}
check("30L goods in Telangana: registration", v["GST registration"], "REQUIRED")
v = {i["topic"]: i["verdict"] for i in compliance({"turnover_prev_fy": 60000000, "supply": "services", "state": "07"})["items"]}
check("6cr: e-invoice mandatory", v["E-invoicing"], "MANDATORY")
check("monthly dates", (due_dates({"month": "2026-11"})["GSTR-1"], due_dates({"month": "2026-11"})["GSTR-3B"]), ("2026-12-11", "2026-12-20"))
check("QRMP Maharashtra 22nd", due_dates({"month": "2026-12", "state": "27", "qrmp": True})["GSTR-3B (quarterly)"], "2027-01-22")
check("QRMP Delhi 24th", due_dates({"month": "2027-03", "state": "07", "qrmp": True})["GSTR-3B (quarterly)"], "2027-04-24")

fails = 0
for name, ok, got, want in results:
    fails += not ok
    print(("PASS " if ok else "FAIL ") + name + ("" if ok else f": got {got!r}, expected {want!r}"))
print(f"\n{len(results) - fails}/{len(results)} passed")
sys.exit(fails)
