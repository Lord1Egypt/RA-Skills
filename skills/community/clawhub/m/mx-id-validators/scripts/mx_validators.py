#!/usr/bin/env python3
"""Validadores mexicanos offline: CURP, RFC, NSS. Sin red, sin PII almacenada."""
import re

# Diccionario oficial SAT/RENAPO (nota: '&' ocupa la posicion 24 y desplaza a O..Z)
DICT = "0123456789ABCDEFGHIJKLMN&OPQRSTUVWXYZ"

ESTADOS = {
    "AS","BC","BS","CC","CL","CM","CS","CH","DF","DG","GT","GR","HG","JC",
    "MC","MN","MS","NT","NL","OC","PL","QT","QR","SP","SL","SR","TC","TS",
    "TL","VZ","YN","ZS","NE",
}

CURP_RE = re.compile(
    r"^[A-Z][AEIOUX][A-Z]{2}\d{6}[HM]"
    r"(AS|BC|BS|CC|CL|CM|CS|CH|DF|DG|GT|GR|HG|JC|MC|MN|MS|NT|NL|OC|PL|QT|QR|SP|SL|SR|TC|TS|TL|VZ|YN|ZS|NE)"
    r"[B-DF-HJ-NP-TV-Z]{3}[0-9A-Z]\d$"
)


def _days_in_month(year, month):
    if month == 2:
        leap = year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)
        return 29 if leap else 28
    return 30 if month in (4, 6, 9, 11) else 31


def _check_calendar_date(yy, mm, dd, century=None):
    """Valida fecha real, no solo rangos. century=1900|2000 fuerza el siglo;
    si es None se acepta si el dia existe en alguna de las dos centurias."""
    if not 1 <= mm <= 12:
        return {"valid": False, "error": "bad_month", "value": mm}
    if dd < 1:
        return {"valid": False, "error": "bad_day", "value": dd}
    if century is None:
        ok = any(dd <= _days_in_month(c + yy, mm) for c in (1900, 2000))
    else:
        ok = dd <= _days_in_month(century + yy, mm)
    if not ok:
        return {"valid": False, "error": "impossible_date",
                "value": f"{dd:02d}/{mm:02d}",
                "detail": "ese dia no existe en ese mes"}
    return None


# ---------------- CURP ----------------
def curp_check_digit(curp17):
    s = sum(DICT.index(ch) * (18 - i) for i, ch in enumerate(curp17))
    return (10 - (s % 10)) % 10


def validate_curp(curp):
    if not isinstance(curp, str):
        return {"valid": False, "error": "not_a_string"}
    c = curp.strip().upper()
    if len(c) != 18:
        return {"valid": False, "error": "bad_length", "expected": 18, "got": len(c)}
    if not CURP_RE.match(c):
        if not re.match(r"^[A-Z]{4}", c):
            return {"valid": False, "error": "bad_initial_block"}
        if not re.match(r"^[A-Z]{4}\d{6}", c):
            return {"valid": False, "error": "bad_birthdate_block"}
        if c[10] not in "HM":
            return {"valid": False, "error": "bad_sex"}
        if c[11:13] not in ESTADOS:
            return {"valid": False, "error": "bad_state_code", "value": c[11:13]}
        return {"valid": False, "error": "bad_format"}
    # El caracter 17 (indice 16) es digito si nacio antes de 2000, letra si nacio 2000+
    century = 2000 if c[16].isalpha() else 1900
    err = _check_calendar_date(int(c[4:6]), int(c[6:8]), int(c[8:10]), century)
    if err:
        return err
    exp = curp_check_digit(c[:17])
    act = int(c[17])
    if exp != act:
        return {"valid": False, "error": "checksum_mismatch",
                "expectedCheckDigit": exp, "actualCheckDigit": act}
    return {
        "valid": True, "curp": c,
        "birthDate": f"{c[4:6]}/{c[6:8]}/{c[8:10]}",
        "sex": "Hombre" if c[10] == "H" else "Mujer",
        "stateCode": c[11:13], "checkDigit": act,
    }


# ---------------- RFC ----------------
RFC_RE = re.compile(r"^[A-ZÑ&]{3,4}\d{6}[A-Z0-9]{3}$")


def rfc_check_digit(body):
    """body = los chars antes del digito verificador (11 si moral, 12 si fisica)."""
    s = 0
    for i, ch in enumerate(body):
        s += DICT.index(ch) * (13 - i)
    d = 11 - (s % 11)
    if d == 11:
        return "0"
    if d == 10:
        return "A"
    return str(d)


def validate_rfc(rfc):
    """Valida RFC de persona fisica (13) o moral (12) de Mexico."""
    if not isinstance(rfc, str):
        return {"valid": False, "error": "not_a_string"}
    c = rfc.strip().upper().replace("-", "").replace(" ", "")
    # RFC genericos oficiales del SAT: validos aunque no sigan el checksum.
    if c in ("XAXX010101000", "XEXX010101000"):
        return {
            "valid": True, "rfc": c, "personType": "generico",
            "note": "RFC generico autorizado por el SAT",
            "birthDate": "01/01/01", "checkDigit": c[-1],
        }
    if len(c) not in (12, 13):
        return {"valid": False, "error": "bad_length", "expected": "12 or 13", "got": len(c)}
    if not RFC_RE.match(c):
        if not re.match(r"^[A-ZÑ&]{3,4}", c):
            return {"valid": False, "error": "bad_initial_block"}
        if not re.match(r"^[A-ZÑ&]{3,4}\d{6}", c):
            return {"valid": False, "error": "bad_birthdate_block"}
        return {"valid": False, "error": "bad_format"}
    # persona moral: 3 letras + fecha (pos 3-8); fisica: 4 letras + fecha (pos 4-9)
    off = 3 if len(c) == 12 else 4
    err = _check_calendar_date(int(c[off:off+2]), int(c[off+2:off+4]), int(c[off+4:off+6]))
    if err:
        return err
    body, actual = c[:-1], c[-1]
    expected = rfc_check_digit(body)
    if expected != actual:
        return {"valid": False, "error": "checksum_mismatch",
                "expectedCheckDigit": expected, "actualCheckDigit": actual}
    persona = "fisica" if len(c) == 13 else "moral"
    out = {
        "valid": True, "rfc": c, "personType": persona,
        "checkDigit": actual,
    }
    if persona == "fisica":
        out["birthDate"] = f"{c[off:off+2]}/{c[off+2:off+4]}/{c[off+4:off+6]}"
    else:
        out["constitutionDate"] = f"{c[off:off+2]}/{c[off+2:off+4]}/{c[off+4:off+6]}"
    return out


# ---------------- NSS ----------------
NSS_RE = re.compile(r"^\d{11}$")


def nss_check_digit(first10):
    total = 0
    for i, ch in enumerate(first10, start=1):
        d = int(ch)
        if i % 2 == 0:            # posiciones 2,4,6,8,10
            v = d * 2
            if v > 9:
                v -= 9
            total += v
        else:                      # posiciones 1,3,5,7,9
            total += d
    return (10 - (total % 10)) % 10


def validate_nss(nss):
    """Valida Numero de Seguridad Social del IMSS (11 digitos)."""
    if not isinstance(nss, str):
        nss = str(nss)
    c = re.sub(r"[\s-]", "", nss)
    if not NSS_RE.match(c):
        return {"valid": False, "error": "bad_length_or_chars", "expected": "11 digits", "got": len(c)}
    exp = nss_check_digit(c[:10])
    act = int(c[10])
    if exp != act:
        return {"valid": False, "error": "checksum_mismatch",
                "expectedCheckDigit": exp, "actualCheckDigit": act}
    def to_year(yy):
        # El IMSS usa ventana deslizante: >30 se interpreta como 1900s.
        return 2000 + yy if yy <= 30 else 1900 + yy

    return {
        "valid": True, "nss": c,
        "subdelegation": c[0:2],
        "registrationYear": to_year(int(c[2:4])),
        "birthYear": to_year(int(c[4:6])),
        "consecutive": c[6:10],
        "checkDigit": act,
    }


# ---------------- CLI ----------------
def _cli():
    import json as _json
    import sys

    validators = {"curp": validate_curp, "rfc": validate_rfc, "nss": validate_nss}
    if len(sys.argv) < 3:
        print("usage: mx_validators.py {curp|rfc|nss} <value>", file=sys.stderr)
        print("       mx_validators.py {curp|rfc|nss} -   (read values from stdin, one per line)",
              file=sys.stderr)
        raise SystemExit(2)

    kind = sys.argv[1].lower()
    if kind not in validators:
        print(f"unknown kind '{kind}'; expected one of: {', '.join(validators)}", file=sys.stderr)
        raise SystemExit(2)

    fn = validators[kind]
    arg = sys.argv[2]
    values = [l.strip() for l in sys.stdin if l.strip()] if arg == "-" else [arg]

    out = [fn(v) for v in values]
    if len(out) == 1:
        print(_json.dumps(out[0], indent=1, ensure_ascii=False))
    else:
        print(_json.dumps(out, indent=1, ensure_ascii=False))

    # exit 1 si alguno es invalido, para uso en scripts
    raise SystemExit(0 if all(r.get("valid") for r in out) else 1)


if __name__ == "__main__":
    _cli()
