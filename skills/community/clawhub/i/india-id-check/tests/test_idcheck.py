"""Run: python3 tests/test_idcheck.py  (from the skill folder)"""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))
from idcheck import (verhoeff_digit, verhoeff_valid, luhn_valid, validate, detect, redact, crosscheck, mask)

R = []
def check(name, got, want):
    R.append((name, got == want, got, want))
def ok(d):
    return validate(d)["valid"]

AADHAAR = "23412341234" + verhoeff_digit("23412341234")   # synthetic, checksum-valid

# checksum algorithms vs published examples
check("Verhoeff: 236 -> 3", verhoeff_digit("236"), "3")
check("Verhoeff: 12345 -> 1", verhoeff_digit("12345"), "1")
check("Luhn: Visa test card", luhn_valid("4111111111111111"), True)
# Aadhaar
check("Aadhaar valid with spaces", ok({"type": "aadhaar", "value": AADHAAR[:4] + " " + AADHAAR[4:8] + " " + AADHAAR[8:]}), True)
check("Aadhaar one digit changed", ok({"type": "aadhaar", "value": AADHAAR[:-1] + str((int(AADHAAR[-1]) + 1) % 10)}), False)
check("Aadhaar starting with 1 rejected", ok({"type": "aadhaar", "value": "1" + AADHAAR[1:]}), False)
check("Aadhaar never echoed", validate({"type": "aadhaar", "value": AADHAAR})["value"], "[hidden]")
check("Aadhaar masked", mask({"value": AADHAAR})["masked"], "XXXX XXXX " + AADHAAR[-4:])
# PAN
check("PAN valid individual", validate({"value": "ABCPE1234F"})["details"]["holder_type"], "Individual")
check("PAN bad 4th char", ok({"type": "pan", "value": "ABCXE1234F"}), False)
check("PAN surname warning", len(validate({"type": "pan", "value": "ABCPE1234F", "name": "Rahul Sharma"})["warnings"]), 1)
check("PAN surname match", len(validate({"type": "pan", "value": "ABCPS1234F", "name": "Rahul Sharma"})["warnings"]), 0)
# GSTIN / TAN / IFSC
check("GSTIN valid", ok({"value": "27AAPFU0939F1ZV"}), True)
check("GSTIN typo", ok({"type": "gstin", "value": "27AAPFU0939F1ZW"}), False)
check("TAN valid", ok({"value": "PNEA12345B"}), True)
check("IFSC bank name", validate({"value": "SBIN0001234"})["details"]["bank"], "State Bank of India")
check("IFSC 5th char must be 0", ok({"type": "ifsc", "value": "SBIN1001234"}), False)
# UPI / mobile / PIN
check("UPI PhonePe", validate({"value": "someone@ybl"})["details"]["app_or_bank"], "PhonePe (Yes Bank)")
check("UPI Paytm new handle", validate({"value": "someone@ptsbi"})["details"]["app_or_bank"], "Paytm (SBI)")
check("UPI bad format", ok({"type": "upi", "value": "no-at-sign"}), False)
check("Mobile +91", validate({"value": "+91 98765 43210"})["details"]["e164"], "+919876543210")
check("Mobile starting 5 invalid", ok({"type": "mobile", "value": "5876543210"}), False)
check("PIN Pune -> Maharashtra", validate({"value": "411001"})["details"]["likely_state"], "Maharashtra")
check("PIN Goa override", validate({"value": "403001"})["details"]["likely_state"], "Goa")
check("PIN Jharkhand range", validate({"value": "834001"})["details"]["likely_state"], "Jharkhand")
check("PIN starting 0 invalid", ok({"type": "pin", "value": "011001"}), False)
# vehicles
check("Vehicle MH formatted", validate({"value": "mh12ab1234"})["details"]["formatted"], "MH 12 AB 1234")
check("Vehicle Delhi DL3CAF", validate({"value": "DL3CAF0001"})["details"]["rto_code"], "DL03")
check("Vehicle BH series", validate({"value": "22BH1234AB"})["details"]["registration_year"], 2022)
check("Vehicle Telangana TG", validate({"value": "TG09AB1234"})["details"]["state"], "Telangana")
check("Vehicle old TS warns", len(validate({"value": "TS09EA1234"})["warnings"]), 1)
check("Vehicle bad state", ok({"type": "vehicle", "value": "XX12AB1234"}), False)
# DL / passport / voter
check("DL valid", validate({"value": "MH1420110012345"})["details"]["year_issued"], 2011)
check("DL impossible year", ok({"type": "driving_licence", "value": "MH1430110012345"}), False)
check("Passport valid", ok({"value": "J8369854"}), True)
check("Passport Q not allowed", ok({"type": "passport", "value": "Q8369854"}), False)
check("Voter ID valid", ok({"value": "ABC1234567"}), True)
# CIN / LLPIN / Udyam
c = validate({"value": "U72900MH2015PTC123456"})["details"]
check("CIN decoded", (c["listed"], c["state"], c["year_incorporated"], c["company_type"]),
      (False, "Maharashtra", 2015, "Private Limited Company"))
check("CIN bad type", ok({"type": "cin", "value": "U72900MH2015XYZ123456"}), False)
check("LLPIN valid", ok({"value": "AAB-1234"}), True)
check("Udyam valid", validate({"value": "UDYAM-MH-26-0012345"})["details"]["state"], "Maharashtra")
check("Udyam bad format", ok({"type": "udyam", "value": "UDYAM-MH-260012345"}), False)
# card
check("Card network", validate({"type": "card", "value": "4111 1111 1111 1111"})["details"]["network"], "Visa")
# redaction
t = (f"Aadhaar {AADHAAR[:4]} {AADHAAR[4:8]} {AADHAAR[8:]}, PAN ABCPE1234F, phone 9876543210, "
     "order 123456789012, amount 5000, pin 411001, card 4111111111111111")
r = redact({"text": t})
check("redact finds Aadhaar", r["found"].get("aadhaar"), 1)
check("redact finds PAN+mobile+card", (r["found"].get("pan"), r["found"].get("mobile"), r["found"].get("card")), (1, 1, 1))
check("redact leaves order number (bad checksum)", "123456789012" in r["redacted_text"], True)
check("redact leaves PIN and amount", ("411001" in r["redacted_text"], "5000" in r["redacted_text"]), (True, True))
check("redact removes full Aadhaar", AADHAAR[:4] + " " + AADHAAR[4:8] in r["redacted_text"], False)
check("redact label style", "[PAN]" in redact({"text": "PAN ABCPE1234F", "style": "label"})["redacted_text"], True)
# crosscheck
x = crosscheck({"pan": "AAPFU0939F", "gstin": "27AAPFU0939F1ZV", "entity": "firm"})
check("crosscheck PAN-GSTIN ok", x["all_ok"], True)
x = crosscheck({"pan": "ABCPE1234F", "gstin": "27AAPFU0939F1ZV"})
check("crosscheck PAN mismatch", x["all_ok"], False)
# detect
check("detect unknown", detect("hello world")["best_guess"], None)

fails = 0
for name, good, got, want in R:
    fails += not good
    print(("PASS " if good else "FAIL ") + name + ("" if good else f": got {got!r}, expected {want!r}"))
print(f"\n{len(R) - fails}/{len(R)} passed")
sys.exit(fails)
