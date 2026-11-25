#!/usr/bin/env python3
"""
india-id-check: validate, identify, mask and redact Indian identifiers. Offline, standard library only.

Commands (input is a JSON string or a path to a .json file):
  validate   '{"value": "ABCPE1234F"}'                    auto-detects the type
             '{"type": "aadhaar", "value": "2341 2341 2346"}'
             '{"values": ["27AAPFU0939F1ZV", "HDFC0000123"]}'   batch
  detect     '{"value": "MH12AB1234"}'                     which ID types could this be?
  mask       '{"value": "234123412346"}'                   safe display form (XXXX XXXX 2346)
  redact     '{"text": "My Aadhaar is 2341 2341 2346 and PAN ABCPE1234F"}'
                                                          finds and masks IDs inside free text
  crosscheck '{"pan": "AAPFU0939F", "gstin": "27AAPFU0939F1ZV", "name": "..."}'
  lookup     '{"ifsc": "HDFC0000123"}' | '{"pin": "411001"}'   OPTIONAL online lookup (needs internet)

Supported types: aadhaar, pan, gstin, tan, ifsc, upi, mobile, pin, vehicle, driving_licence, passport,
voter_id, cin, llpin, udyam, card, email.
Format/checksum checks prove an ID is well-formed, NOT that it exists or belongs to someone.
"""
import json, re, sys
from datetime import date

THIS_YEAR = date.today().year
CHARSET = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"

# ------------------------------------------------------------------ reference data
GST_STATES = {
    "01": "Jammu and Kashmir", "02": "Himachal Pradesh", "03": "Punjab", "04": "Chandigarh", "05": "Uttarakhand",
    "06": "Haryana", "07": "Delhi", "08": "Rajasthan", "09": "Uttar Pradesh", "10": "Bihar", "11": "Sikkim",
    "12": "Arunachal Pradesh", "13": "Nagaland", "14": "Manipur", "15": "Mizoram", "16": "Tripura", "17": "Meghalaya",
    "18": "Assam", "19": "West Bengal", "20": "Jharkhand", "21": "Odisha", "22": "Chhattisgarh", "23": "Madhya Pradesh",
    "24": "Gujarat", "25": "Daman and Diu (old)", "26": "Dadra and Nagar Haveli and Daman and Diu", "27": "Maharashtra",
    "28": "Andhra Pradesh (old)", "29": "Karnataka", "30": "Goa", "31": "Lakshadweep", "32": "Kerala", "33": "Tamil Nadu",
    "34": "Puducherry", "35": "Andaman and Nicobar Islands", "36": "Telangana", "37": "Andhra Pradesh", "38": "Ladakh",
    "97": "Other Territory", "99": "Centre Jurisdiction",
}
# 2-letter state codes used in vehicle numbers, driving licences, CIN and Udyam
STATE_ABBR = {
    "AN": "Andaman and Nicobar Islands", "AP": "Andhra Pradesh", "AR": "Arunachal Pradesh", "AS": "Assam", "BR": "Bihar",
    "CG": "Chhattisgarh", "CT": "Chhattisgarh", "CH": "Chandigarh", "DD": "Dadra and Nagar Haveli and Daman and Diu",
    "DN": "Dadra and Nagar Haveli (old)", "DL": "Delhi", "GA": "Goa", "GJ": "Gujarat", "HP": "Himachal Pradesh",
    "HR": "Haryana", "JH": "Jharkhand", "JK": "Jammu and Kashmir", "KA": "Karnataka", "KL": "Kerala", "LA": "Ladakh",
    "LD": "Lakshadweep", "MH": "Maharashtra", "ML": "Meghalaya", "MN": "Manipur", "MP": "Madhya Pradesh",
    "MZ": "Mizoram", "NL": "Nagaland", "OD": "Odisha", "OR": "Odisha (old code)", "PB": "Punjab", "PY": "Puducherry",
    "RJ": "Rajasthan", "SK": "Sikkim", "TN": "Tamil Nadu", "TG": "Telangana", "TS": "Telangana (pre-March 2024 code)",
    "TR": "Tripura", "UK": "Uttarakhand", "UA": "Uttarakhand (old code)", "UP": "Uttar Pradesh", "WB": "West Bengal",
}
PAN_ENTITY = {"P": "Individual", "C": "Company", "H": "Hindu Undivided Family (HUF)", "F": "Firm / LLP",
              "A": "Association of Persons (AOP)", "T": "Trust", "B": "Body of Individuals (BOI)",
              "L": "Local Authority", "J": "Artificial Juridical Person", "G": "Government"}
BANKS = {
    "SBIN": "State Bank of India", "HDFC": "HDFC Bank", "ICIC": "ICICI Bank", "UTIB": "Axis Bank",
    "PUNB": "Punjab National Bank", "BARB": "Bank of Baroda", "CNRB": "Canara Bank", "UBIN": "Union Bank of India",
    "KKBK": "Kotak Mahindra Bank", "IDIB": "Indian Bank", "BKID": "Bank of India", "IOBA": "Indian Overseas Bank",
    "CBIN": "Central Bank of India", "MAHB": "Bank of Maharashtra", "UCBA": "UCO Bank", "PSIB": "Punjab & Sind Bank",
    "YESB": "Yes Bank", "INDB": "IndusInd Bank", "IDFB": "IDFC FIRST Bank", "FDRL": "Federal Bank",
    "IBKL": "IDBI Bank", "KARB": "Karnataka Bank", "SIBL": "South Indian Bank", "CSBK": "CSB Bank", "RATN": "RBL Bank",
    "KVBL": "Karur Vysya Bank", "TMBL": "Tamilnad Mercantile Bank", "CIUB": "City Union Bank", "DCBL": "DCB Bank",
    "DLXB": "Dhanlaxmi Bank", "JAKA": "Jammu & Kashmir Bank", "BDBL": "Bandhan Bank", "AUBL": "AU Small Finance Bank",
    "ESFB": "Equitas Small Finance Bank", "UJVN": "Ujjivan Small Finance Bank", "JSFB": "Jana Small Finance Bank",
    "SURY": "Suryoday Small Finance Bank", "FSFB": "Fincare Small Finance Bank", "AIRP": "Airtel Payments Bank",
    "IPOS": "India Post Payments Bank", "PYTM": "Paytm Payments Bank", "FINO": "Fino Payments Bank",
    "NSPB": "NSDL Payments Bank", "HSBC": "HSBC", "SCBL": "Standard Chartered Bank", "CITI": "Citibank",
    "DBSS": "DBS Bank India", "DEUT": "Deutsche Bank", "SRCB": "Saraswat Co-operative Bank",
    "COSB": "Cosmos Co-operative Bank", "SVCB": "SVC Co-operative Bank", "NKGS": "NKGSB Co-operative Bank",
    "HSBN": "HSBC", "RBIS": "Reserve Bank of India",
}
UPI_HANDLES = {
    "ybl": "PhonePe (Yes Bank)", "ibl": "PhonePe (ICICI Bank)", "axl": "PhonePe (Axis Bank)",
    "okhdfcbank": "Google Pay (HDFC Bank)", "okicici": "Google Pay (ICICI Bank)", "oksbi": "Google Pay (SBI)",
    "okaxis": "Google Pay (Axis Bank)", "paytm": "Paytm (legacy handle)", "ptyes": "Paytm (Yes Bank)",
    "ptaxis": "Paytm (Axis Bank)", "pthdfc": "Paytm (HDFC Bank)", "ptsbi": "Paytm (SBI)", "upi": "BHIM",
    "apl": "Amazon Pay", "yapl": "Amazon Pay", "rapl": "Amazon Pay", "axisbank": "Axis Bank / CRED",
    "icici": "ICICI Bank", "hdfcbank": "HDFC Bank", "sbi": "SBI", "kotak": "Kotak Mahindra Bank",
    "kmbl": "Kotak Mahindra Bank", "yesbank": "Yes Bank", "indus": "IndusInd Bank", "boi": "Bank of India",
    "barodampay": "Bank of Baroda", "cnrb": "Canara Bank", "pnb": "Punjab National Bank", "idbi": "IDBI Bank",
    "unionbank": "Union Bank of India", "uboi": "Union Bank of India", "federal": "Federal Bank", "sib": "South Indian Bank",
    "freecharge": "Freecharge", "ikwik": "MobiKwik", "yesg": "Groww", "pz": "PayZapp (HDFC Bank)",
    "jupiteraxis": "Jupiter", "fam": "FamPay", "slc": "slice", "sliceaxis": "slice", "hsbc": "HSBC", "aubank": "AU Bank",
    "airtel": "Airtel Payments Bank", "postbank": "India Post Payments Bank", "waicici": "WhatsApp Pay (ICICI)",
    "wahdfcbank": "WhatsApp Pay (HDFC)", "waaxis": "WhatsApp Pay (Axis)", "wasbi": "WhatsApp Pay (SBI)",
}
CIN_TYPES = {"PLC": "Public Limited Company", "PTC": "Private Limited Company", "OPC": "One Person Company",
             "NPL": "Section 8 (not-for-profit) company", "FTC": "Subsidiary of a foreign company",
             "FLC": "Foreign company (listed)", "GOI": "Government of India company", "SGC": "State Government company",
             "GAP": "Public company limited by guarantee", "GAT": "Private company limited by guarantee",
             "ULL": "Public company with unlimited liability", "ULT": "Private company with unlimited liability"}
PIN_ZONE = {"1": "North (Delhi, Haryana, Punjab, HP, J&K, Ladakh, Chandigarh)", "2": "North (UP, Uttarakhand)",
            "3": "West (Rajasthan, Gujarat, DNH & DD)", "4": "West (Maharashtra, Goa, MP, Chhattisgarh)",
            "5": "South (Telangana, Andhra Pradesh, Karnataka)", "6": "South (Tamil Nadu, Kerala, Puducherry, Lakshadweep)",
            "7": "East (West Bengal, Odisha, North East, Sikkim, A&N)", "8": "East (Bihar, Jharkhand)",
            "9": "Army Postal Service"}


def pin_state(pin):
    p2, p3 = int(pin[:2]), int(pin[:3])
    special = {160: "Chandigarh", 194: "Ladakh", 403: "Goa", 737: "Sikkim", 744: "Andaman and Nicobar Islands",
               795: "Manipur", 796: "Mizoram", 799: "Tripura"}
    if p3 in special:
        return special[p3]
    if 246 <= p3 <= 249 or p3 in (262, 263):
        return "Uttarakhand"
    if 790 <= p3 <= 792: return "Arunachal Pradesh"
    if p3 in (793, 794): return "Meghalaya"
    if p3 in (797, 798): return "Nagaland"
    if 814 <= p3 <= 835: return "Jharkhand"
    table = [(11, 11, "Delhi"), (12, 13, "Haryana"), (14, 16, "Punjab"), (17, 17, "Himachal Pradesh"),
             (18, 19, "Jammu and Kashmir"), (20, 28, "Uttar Pradesh"), (30, 34, "Rajasthan"), (36, 39, "Gujarat"),
             (40, 44, "Maharashtra"), (45, 48, "Madhya Pradesh"), (49, 49, "Chhattisgarh"), (50, 50, "Telangana"),
             (51, 53, "Andhra Pradesh"), (56, 59, "Karnataka"), (60, 64, "Tamil Nadu"), (67, 69, "Kerala"),
             (70, 74, "West Bengal"), (75, 77, "Odisha"), (78, 78, "Assam"), (80, 85, "Bihar"),
             (90, 99, "Army Postal Service")]
    for lo, hi, name in table:
        if lo <= p2 <= hi:
            return name
    return None


# ------------------------------------------------------------------ checksums
_V_D = [[0,1,2,3,4,5,6,7,8,9],[1,2,3,4,0,6,7,8,9,5],[2,3,4,0,1,7,8,9,5,6],[3,4,0,1,2,8,9,5,6,7],
        [4,0,1,2,3,9,5,6,7,8],[5,9,8,7,6,0,4,3,2,1],[6,5,9,8,7,1,0,4,3,2],[7,6,5,9,8,2,1,0,4,3],
        [8,7,6,5,9,3,2,1,0,4],[9,8,7,6,5,4,3,2,1,0]]
_V_P = [[0,1,2,3,4,5,6,7,8,9],[1,5,7,6,2,8,3,0,9,4],[5,8,0,3,7,9,6,1,4,2],[8,9,1,6,0,4,3,5,2,7],
        [9,4,5,3,1,2,6,8,7,0],[4,2,8,6,5,7,3,9,0,1],[2,7,9,3,8,0,6,4,1,5],[7,0,4,6,9,1,3,2,5,8]]
_V_INV = [0,4,3,2,1,5,6,7,8,9]


def verhoeff_valid(num):
    c = 0
    for i, ch in enumerate(reversed(num)):
        c = _V_D[c][_V_P[i % 8][int(ch)]]
    return c == 0


def verhoeff_digit(num):
    c = 0
    for i, ch in enumerate(reversed(num)):
        c = _V_D[c][_V_P[(i + 1) % 8][int(ch)]]
    return str(_V_INV[c])


def luhn_valid(num):
    total, alt = 0, False
    for ch in reversed(num):
        d = int(ch)
        if alt:
            d = d * 2 - 9 if d > 4 else d * 2
        total += d
        alt = not alt
    return total % 10 == 0


def gstin_checksum(first14):
    total = 0
    for i, ch in enumerate(first14):
        prod = CHARSET.index(ch) * (1 if i % 2 == 0 else 2)
        total += prod // 36 + prod % 36
    return CHARSET[(36 - total % 36) % 36]


# ------------------------------------------------------------------ validators
def _res(t, value, valid, info=None, errors=None, warnings=None, masked=None):
    r = {"type": t, "value": value, "valid": valid, "details": info or {}, "errors": errors or [], "warnings": warnings or []}
    if masked:
        r["masked"] = masked
    return r


def norm(v, keep="-/@."):
    return re.sub(r"[^A-Za-z0-9" + re.escape(keep) + "]", "", str(v or "")).upper()


def v_aadhaar(v):
    s = re.sub(r"[\s-]", "", str(v))
    errs = []
    if not re.fullmatch(r"\d{12}", s):
        return _res("aadhaar", "[hidden]", False, errors=["Aadhaar must be exactly 12 digits."])
    if s[0] in "01":
        errs.append("Aadhaar numbers never start with 0 or 1.")
    if not verhoeff_valid(s):
        errs.append("Check digit (Verhoeff) does not match - a digit is wrong or swapped.")
    return _res("aadhaar", "[hidden]", not errs, {"note": "Never store or log full Aadhaar numbers; display only the masked form."},
                errs, masked=mask_aadhaar(s))


def mask_aadhaar(s):
    return "XXXX XXXX " + s[-4:]


def v_pan(v, name=None):
    s = norm(v, "")
    if not re.fullmatch(r"[A-Z]{5}\d{4}[A-Z]", s):
        return _res("pan", s, False, errors=["PAN must be 5 letters, 4 digits, 1 letter (e.g. ABCPE1234F)."])
    errs, warns = [], []
    ent = PAN_ENTITY.get(s[3])
    if not ent:
        errs.append(f"4th character '{s[3]}' is not a valid PAN holder type (P, C, H, F, A, T, B, L, J, G).")
    info = {"holder_type": ent, "name_initial": s[4],
            "note": "PAN's last letter is a check character, but its algorithm is not public, so typos inside a "
                    "well-formed PAN cannot be detected offline. Verify on the Income Tax e-filing portal."}
    if name:
        words = [w for w in re.split(r"\s+", name.strip().upper()) if w]
        target = words[-1][0] if (s[3] == "P" and words) else (words[0][0] if words else "")
        if target and target != s[4]:
            warns.append(f"5th character '{s[4]}' should usually be the first letter of the "
                         f"{'surname' if s[3] == 'P' else 'entity name'} ('{target}'). Check the name or PAN.")
    return _res("pan", s, not errs, info, errs, warns, masked=s[:2] + "XXX" + s[5:9] + s[9])


def v_gstin(v):
    s = norm(v, "")
    if len(s) != 15:
        return _res("gstin", s, False, errors=[f"GSTIN must be 15 characters (got {len(s)})."])
    errs, warns = [], []
    if not re.fullmatch(r"\d{2}[A-Z]{5}\d{4}[A-Z][1-9A-Z][A-Z][0-9A-Z]", s):
        errs.append("Pattern: 2-digit state code + PAN + entity number + letter + check character.")
    if s[:2] not in GST_STATES:
        errs.append(f"'{s[:2]}' is not a GST state code.")
    if all(c in CHARSET for c in s) and gstin_checksum(s[:14]) != s[14]:
        errs.append(f"Check character wrong: expected '{gstin_checksum(s[:14])}', found '{s[14]}' (likely a typo).")
    if s[13] != "Z":
        warns.append("14th character is normally 'Z'.")
    return _res("gstin", s, not errs, {"state": GST_STATES.get(s[:2]), "pan": s[2:12],
                "holder_type": PAN_ENTITY.get(s[5]), "registration_number_in_state": s[12],
                "note": "Active/cancelled status: services.gst.gov.in > Search Taxpayer."}, errs, warns,
                masked=s[:2] + "XXXXXXXX" + s[10:])


def v_tan(v):
    s = norm(v, "")
    ok = bool(re.fullmatch(r"[A-Z]{4}\d{5}[A-Z]", s))
    return _res("tan", s, ok, {"jurisdiction_code": s[:3], "deductor_initial": s[3]} if ok else {},
                [] if ok else ["TAN must be 4 letters, 5 digits, 1 letter (e.g. PNEA12345B)."])


def v_ifsc(v):
    s = norm(v, "")
    if not re.fullmatch(r"[A-Z]{4}0[A-Z0-9]{6}", s):
        return _res("ifsc", s, False, errors=["IFSC must be 4 letters (bank) + '0' + 6 letters/digits (branch), 11 characters."])
    bank = BANKS.get(s[:4])
    return _res("ifsc", s, True, {"bank_code": s[:4], "bank": bank or "Unknown in offline list", "branch_code": s[5:],
                "note": "Use 'lookup' for branch name and address (needs internet)."},
                warnings=[] if bank else ["Bank code not in the offline list; it may still be valid."])


def v_upi(v):
    s = str(v or "").strip()
    m = re.fullmatch(r"([A-Za-z0-9.\-_]{2,256})@([A-Za-z][A-Za-z0-9.\-]{1,63})", s)
    if not m:
        return _res("upi", s, False, errors=["UPI ID must look like name@handle (letters, digits, '.', '-', '_' before @)."])
    h = m.group(2).lower()
    app = UPI_HANDLES.get(h)
    warns = [] if app else [f"Handle '@{h}' is not in the offline list of common handles; it may still be valid."]
    if re.fullmatch(r"\d{10}", m.group(1)):
        warns.append("This UPI ID is a mobile number - treat it as personal data.")
    return _res("upi", s, True, {"handle": "@" + h, "app_or_bank": app or "Unknown",
                "note": "Format check only. Confirm the payee name in a UPI app before paying."}, warnings=warns,
                masked=m.group(1)[:2] + "****@" + h)


def v_mobile(v):
    s = re.sub(r"[\s\-()]", "", str(v or ""))
    s = re.sub(r"^(\+91|0091|91|0)(?=\d{10}$)", "", s)
    ok = bool(re.fullmatch(r"[6-9]\d{9}", s))
    return _res("mobile", s, ok, {"e164": "+91" + s} if ok else {},
                [] if ok else ["Indian mobile numbers have 10 digits starting with 6, 7, 8 or 9 (optional +91)."],
                masked=("XXXXXX" + s[-4:]) if ok else None)


def v_pin(v):
    s = re.sub(r"\s", "", str(v or ""))
    if not re.fullmatch(r"[1-9]\d{5}", s):
        return _res("pin", s, False, errors=["PIN code must be 6 digits and cannot start with 0."])
    return _res("pin", s, True, {"zone": PIN_ZONE[s[0]], "likely_state": pin_state(s),
                "note": "State is inferred from the prefix (approximate near borders). Use 'lookup' for the exact post office."})


def v_vehicle(v):
    s = norm(v, "")
    m = re.fullmatch(r"(\d{2})BH(\d{4})([A-Z]{1,2})", s)
    if m:
        yr = 2000 + int(m.group(1))
        ok = 2021 <= yr <= THIS_YEAR
        return _res("vehicle", s, ok, {"series": "Bharat (BH) series - valid in all states", "registration_year": yr,
                    "formatted": f"{m.group(1)} BH {m.group(2)} {m.group(3)}"},
                    [] if ok else [f"BH series started in 2021; year {yr} is not possible."])
    m = re.fullmatch(r"([A-Z]{2})(\d{1,2})([A-Z]{0,3})(\d{1,4})", s)
    if not m:
        return _res("vehicle", s, False, errors=["Expected format like MH12AB1234, DL3CAF0001 or 22BH1234AB."])
    st, rto, series, num = m.groups()
    errs, warns = [], []
    if st not in STATE_ABBR:
        errs.append(f"'{st}' is not an Indian state/UT registration code.")
    if int(num) == 0:
        errs.append("Registration number cannot be 0000.")
    if st == "TS":
        warns.append("TS is Telangana's old code; new registrations since March 2024 use TG. Old TS plates remain valid.")
    return _res("vehicle", s, not errs, {"state": STATE_ABBR.get(st), "rto_code": f"{st}{int(rto):02d}",
                "series": series or None, "number": num.zfill(4),
                "formatted": f"{st} {int(rto):02d} {series + ' ' if series else ''}{num.zfill(4)}",
                "note": "Owner/insurance details need the official VAHAN/mParivahan service."}, errs, warns)


def v_dl(v):
    s = norm(v, "")
    m = re.fullmatch(r"([A-Z]{2})(\d{2})(\d{4})(\d{7})", s)
    if not m:
        return _res("driving_licence", s, False,
                    errors=["Standard format: 2-letter state + 2-digit RTO + 4-digit year + 7 digits (e.g. MH1420110012345). "
                            "Some older licences use other formats."])
    st, rto, yr, serial = m.groups()
    errs = []
    if st not in STATE_ABBR:
        errs.append(f"'{st}' is not a state code.")
    if not 1950 <= int(yr) <= THIS_YEAR:
        errs.append(f"Year of issue {yr} is not plausible.")
    return _res("driving_licence", s, not errs, {"state": STATE_ABBR.get(st), "rto_code": st + rto, "year_issued": int(yr)},
                errs, masked=s[:4] + "XXXXXXX" + s[-4:])


def v_passport(v):
    s = norm(v, "")
    ok = bool(re.fullmatch(r"[A-PR-WY][1-9]\d{6}", s))
    return _res("passport", s, ok, {} if ok else {},
                [] if ok else ["Indian passport numbers are 1 letter (not Q, X or Z) followed by 7 digits, e.g. J8369854."],
                masked=(s[0] + "XXXX" + s[-3:]) if ok else None)


def v_voter(v):
    s = norm(v, "")
    ok = bool(re.fullmatch(r"[A-Z]{3}\d{7}", s))
    return _res("voter_id", s, ok, {"note": "Verify on electoralsearch.eci.gov.in."} if ok else {},
                [] if ok else ["Voter ID (EPIC) is usually 3 letters + 7 digits, e.g. ABC1234567. Some old cards differ."],
                masked=(s[:3] + "XXX" + s[-4:]) if ok else None)


def v_cin(v):
    s = norm(v, "")
    m = re.fullmatch(r"([LU])(\d{5})([A-Z]{2})(\d{4})([A-Z]{3})(\d{6})", s)
    if not m:
        return _res("cin", s, False, errors=["CIN is 21 characters: L/U + 5-digit industry code + state + year + type + 6 digits "
                                             "(e.g. U72900MH2015PTC123456)."])
    lst, ind, st, yr, typ, reg = m.groups()
    errs = []
    if st not in STATE_ABBR:
        errs.append(f"'{st}' is not a state code.")
    if not 1850 <= int(yr) <= THIS_YEAR:
        errs.append(f"Incorporation year {yr} is not plausible.")
    if typ not in CIN_TYPES:
        errs.append(f"'{typ}' is not a known company type code.")
    return _res("cin", s, not errs, {"listed": lst == "L", "industry_code": ind, "state": STATE_ABBR.get(st),
                "year_incorporated": int(yr), "company_type": CIN_TYPES.get(typ), "roc_registration_no": reg,
                "note": "Check company status on the MCA portal (mca.gov.in)."}, errs)


def v_llpin(v):
    s = norm(v, "-")
    ok = bool(re.fullmatch(r"[A-Z]{3}-\d{4}", s))
    return _res("llpin", s, ok, {"note": "LLPs get an LLPIN instead of a CIN."} if ok else {},
                [] if ok else ["LLPIN format is 3 letters, hyphen, 4 digits (e.g. AAB-1234)."])


def v_udyam(v):
    s = norm(v, "-")
    m = re.fullmatch(r"UDYAM-([A-Z]{2})-(\d{2})-(\d{7})", s)
    if not m:
        return _res("udyam", s, False, errors=["Udyam number format: UDYAM-XX-00-0000000 (state letters, district digits, 7 digits)."])
    st = m.group(1)
    errs = [] if st in STATE_ABBR else [f"'{st}' is not a state code."]
    return _res("udyam", s, not errs, {"state": STATE_ABBR.get(st), "district_code": m.group(2), "serial": m.group(3),
                "note": "Verify on udyamregistration.gov.in > Print/Verify > Verify Udyam Registration."}, errs)


def card_network(n):
    if re.match(r"4", n): return "Visa"
    if re.match(r"5[1-5]|2(2[2-9]|[3-6]\d|7[01]|720)", n): return "Mastercard"
    if re.match(r"3[47]", n): return "American Express"
    if re.match(r"60|65|81|82|508", n): return "RuPay"
    if re.match(r"3(0[0-5]|[68])", n): return "Diners Club"
    if re.match(r"35", n): return "JCB"
    return "Unknown"


def v_card(v):
    s = re.sub(r"[\s-]", "", str(v or ""))
    if not re.fullmatch(r"\d{13,19}", s):
        return _res("card", "[hidden]", False, errors=["Card numbers have 13-19 digits."])
    ok = luhn_valid(s)
    return _res("card", "[hidden]", ok, {"network": card_network(s),
                "note": "Never store full card numbers (RBI tokenisation rules / PCI DSS)."},
                [] if ok else ["Luhn check failed - a digit is wrong."], masked="XXXX XXXX XXXX " + s[-4:])


def v_email(v):
    s = str(v or "").strip()
    ok = bool(re.fullmatch(r"[A-Za-z0-9._%+\-]+@[A-Za-z0-9.\-]+\.[A-Za-z]{2,}", s))
    return _res("email", s, ok, errors=[] if ok else ["Not a valid email format."],
                masked=(s[0] + "***@" + s.split("@")[1]) if ok else None)


VALIDATORS = {"aadhaar": v_aadhaar, "pan": v_pan, "gstin": v_gstin, "tan": v_tan, "ifsc": v_ifsc, "upi": v_upi,
              "mobile": v_mobile, "pin": v_pin, "vehicle": v_vehicle, "driving_licence": v_dl, "passport": v_passport,
              "voter_id": v_voter, "cin": v_cin, "llpin": v_llpin, "udyam": v_udyam, "card": v_card, "email": v_email}
ALIASES = {"aadhar": "aadhaar", "uid": "aadhaar", "gst": "gstin", "vpa": "upi", "upi_id": "upi", "phone": "mobile",
           "pincode": "pin", "pin_code": "pin", "dl": "driving_licence", "driving_license": "driving_licence",
           "epic": "voter_id", "voter": "voter_id", "rc": "vehicle", "vehicle_number": "vehicle", "msme": "udyam",
           "credit_card": "card", "debit_card": "card"}


# ------------------------------------------------------------------ detection
def detect(value):
    raw = str(value or "").strip()
    s = norm(raw, "-@.")
    digits = re.sub(r"[\s-]", "", raw)
    cands = []
    if "@" in raw:
        cands = ["email"] if re.search(r"\.[A-Za-z]{2,}$", raw.split("@")[-1]) else ["upi"]
    elif s.startswith("UDYAM"):
        cands = ["udyam"]
    elif re.fullmatch(r"\d{12}", digits):
        cands = ["aadhaar"]
    elif re.fullmatch(r"(\+?91|0)?[6-9]\d{9}", re.sub(r"[\s\-()]", "", raw)):
        cands = ["mobile"]
    elif re.fullmatch(r"\d{6}", digits):
        cands = ["pin"]
    elif re.fullmatch(r"\d{13,19}", digits):
        cands = ["card"]
    else:
        c = s.replace("-", "")
        rules = [("gstin", r"\d{2}[A-Z]{5}\d{4}[A-Z][0-9A-Z]{3}"), ("cin", r"[LU]\d{5}[A-Z]{2}\d{4}[A-Z]{3}\d{6}"),
                 ("pan", r"[A-Z]{5}\d{4}[A-Z]"), ("tan", r"[A-Z]{4}\d{5}[A-Z]"), ("ifsc", r"[A-Z]{4}0[A-Z0-9]{6}"),
                 ("driving_licence", r"[A-Z]{2}\d{13}"), ("voter_id", r"[A-Z]{3}\d{7}"), ("passport", r"[A-Z]\d{7}"),
                 ("vehicle", r"(\d{2}BH\d{4}[A-Z]{1,2})|([A-Z]{2}\d{1,2}[A-Z]{0,3}\d{1,4})")]
        cands = [t for t, rx in rules if re.fullmatch(rx, c)]
        if re.fullmatch(r"[A-Z]{3}-\d{4}", s):
            cands.append("llpin")
    out = []
    for t in cands:
        r = VALIDATORS[t](raw)
        out.append({"type": t, "valid": r["valid"]})
    out.sort(key=lambda x: not x["valid"])
    return {"value_preview": raw[:4] + "…" if cands and cands[0] in ("aadhaar", "card") else raw,
            "candidates": out, "best_guess": out[0]["type"] if out else None}


def validate(d):
    if "values" in d:
        return [validate({"value": v}) for v in d["values"]]
    t = d.get("type")
    t = ALIASES.get(str(t).lower(), str(t).lower()) if t else None
    if not t:
        t = detect(d["value"])["best_guess"]
        if not t:
            return {"value": d["value"], "valid": False, "errors": ["Could not recognise this as any supported Indian ID."]}
    if t not in VALIDATORS:
        return {"error": f"Unknown type '{t}'. Supported: {', '.join(VALIDATORS)}"}
    return v_pan(d["value"], d.get("name")) if t == "pan" else VALIDATORS[t](d["value"])


def mask(d):
    r = validate(d)
    return {"type": r.get("type"), "masked": r.get("masked") or (str(d["value"])[:2] + "****"), "valid": r.get("valid")}


# ------------------------------------------------------------------ redaction
REDACT_PATTERNS = [
    ("card", r"(?<!\d)(?:\d[ -]?){12,18}\d(?!\d)"),
    ("aadhaar", r"(?<!\d)[2-9]\d{3}[ -]?\d{4}[ -]?\d{4}(?!\d)"),
    ("gstin", r"\b\d{2}[A-Z]{5}\d{4}[A-Z][1-9A-Z]Z[0-9A-Z]\b"),
    ("pan", r"\b[A-Z]{3}[PCHFATBLJG][A-Z]\d{4}[A-Z]\b"),
    ("email", r"\b[A-Za-z0-9._%+\-]+@[A-Za-z0-9.\-]+\.[A-Za-z]{2,}\b"),
    ("upi", r"\b[A-Za-z0-9.\-_]{2,}@[A-Za-z][A-Za-z0-9]{1,30}\b"),
    ("mobile", r"(?<![\d+])(?:\+91[\s-]?|0)?[6-9]\d{4}[\s-]?\d{5}(?!\d)"),
    ("passport", r"\b[A-PR-WY][1-9]\d{6}\b"),
    ("voter_id", r"\b[A-Z]{3}\d{7}\b"),
]


def redact(d):
    text = str(d.get("text", ""))
    only = set(ALIASES.get(t, t) for t in d.get("types", [])) or None
    spans, found = [], []
    for t, rx in REDACT_PATTERNS:
        if only and t not in only:
            continue
        for m in re.finditer(rx, text):
            a, b = m.span()
            if any(not (b <= x or a >= y) for x, y, _ in spans):
                continue
            val = m.group(0)
            r = VALIDATORS[t](val)
            if t in ("aadhaar", "card", "gstin") and not r["valid"]:
                continue          # checksum guards against false positives
            if t == "card" and re.fullmatch(r"\d{12}", re.sub(r"[ -]", "", val)):
                continue
            rep = r.get("masked") or f"[{t.upper()} REDACTED]"
            if d.get("style") == "label":
                rep = f"[{t.upper()}]"
            spans.append((a, b, rep))
            found.append({"type": t, "masked": r.get("masked") or f"[{t.upper()}]"})
    out = text
    for a, b, rep in sorted(spans, reverse=True):
        out = out[:a] + rep + out[b:]
    counts = {}
    for f in found:
        counts[f["type"]] = counts.get(f["type"], 0) + 1
    return {"redacted_text": out, "found": counts, "items": found}


# ------------------------------------------------------------------ crosscheck
def crosscheck(d):
    checks = []
    pan = norm(d.get("pan", ""), "") or None
    if d.get("gstin"):
        g = v_gstin(d["gstin"])
        checks.append({"check": "GSTIN valid", "ok": g["valid"], "detail": "; ".join(g["errors"]) or "OK"})
        if pan:
            ok = g["value"][2:12] == pan
            checks.append({"check": "PAN inside GSTIN matches PAN", "ok": ok,
                           "detail": "OK" if ok else f"GSTIN contains {g['value'][2:12]}, PAN given is {pan}"})
        pan = pan or g["value"][2:12]
    if pan:
        p = v_pan(pan, d.get("name"))
        checks.append({"check": "PAN format", "ok": p["valid"], "detail": "; ".join(p["errors"] + p["warnings"]) or "OK"})
        if d.get("entity"):
            want = {"individual": "P", "company": "C", "firm": "F", "llp": "F", "huf": "H", "trust": "T"}.get(str(d["entity"]).lower())
            if want:
                ok = pan[3] == want
                checks.append({"check": "PAN holder type matches entity", "ok": ok,
                               "detail": "OK" if ok else f"PAN type is {PAN_ENTITY.get(pan[3])}, expected {d['entity']}"})
    if d.get("ifsc") and d.get("bank"):
        i = v_ifsc(d["ifsc"])
        ok = bool(i["valid"]) and str(d["bank"]).lower().split()[0] in str(i["details"].get("bank", "")).lower()
        checks.append({"check": "IFSC belongs to stated bank", "ok": ok, "detail": f"IFSC bank: {i['details'].get('bank')}"})
    if d.get("pin") and d.get("state"):
        p = v_pin(d["pin"])
        ls = p["details"].get("likely_state") or ""
        ok = str(d["state"]).lower() in ls.lower() or ls.lower() in str(d["state"]).lower()
        checks.append({"check": "PIN matches state", "ok": ok, "detail": f"PIN suggests {ls} (approximate)"})
    return {"all_ok": all(c["ok"] for c in checks) if checks else None, "checks": checks}


# ------------------------------------------------------------------ optional online lookup
def lookup(d):
    import urllib.request
    try:
        if d.get("ifsc"):
            code = norm(d["ifsc"], "")
            with urllib.request.urlopen(f"https://ifsc.razorpay.com/{code}", timeout=15) as r:
                j = json.loads(r.read())
            keys = ["BANK", "BRANCH", "ADDRESS", "CITY", "DISTRICT", "STATE", "MICR", "UPI", "NEFT", "RTGS", "IMPS"]
            return {"ifsc": code, "source": "ifsc.razorpay.com", **{k.lower(): j.get(k) for k in keys}}
        if d.get("pin"):
            pin = re.sub(r"\D", "", str(d["pin"]))
            with urllib.request.urlopen(f"https://api.postalpincode.in/pincode/{pin}", timeout=15) as r:
                j = json.loads(r.read())[0]
            pos = j.get("PostOffice") or []
            return {"pin": pin, "source": "api.postalpincode.in", "status": j.get("Status"),
                    "post_offices": [{k: p.get(k) for k in ("Name", "BranchType", "District", "State")} for p in pos]}
    except Exception as e:
        return {"error": f"Online lookup failed ({e}). The offline 'validate' result still applies."}
    return {"error": "Give 'ifsc' or 'pin'."}


# ------------------------------------------------------------------ CLI
def main():
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    if len(sys.argv) < 3:
        sys.exit(__doc__)
    cmd, arg = sys.argv[1], sys.argv[2]
    data = json.load(open(arg, encoding="utf-8")) if arg.endswith(".json") else json.loads(arg)
    fn = {"validate": validate, "detect": lambda d: detect(d["value"]), "mask": mask, "redact": redact,
          "crosscheck": crosscheck, "lookup": lookup}.get(cmd)
    if not fn:
        sys.exit(f"Unknown command '{cmd}'.\n" + __doc__)
    print(json.dumps(fn(data), indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
