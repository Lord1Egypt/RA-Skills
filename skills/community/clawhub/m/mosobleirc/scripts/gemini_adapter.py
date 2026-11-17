from __future__ import annotations

import json
import math
from copy import deepcopy


class GeminiResultError(ValueError):
    pass


REQUIRED_FIELDS = (
    "same_meter",
    "meter_type",
    "serial_visible",
    "serial",
    "reading_raw",
    "integer_part",
    "decimal_part",
    "digit_confidence",
    "image_quality",
    "glare",
    "blur",
    "rotation",
    "ambiguous",
)


def build_prompt(profile: dict) -> str:
    meter_id = profile.get("meter_id")
    serial = str(profile.get("serial") or "")
    meter_type = str(profile.get("meter_type") or "")
    apartment = str(profile.get("apartment") or "")
    return f"""You are an image extraction component for a water meter workflow.
Expected meter_id: {meter_id}
Expected apartment: {apartment}
Expected serial: {serial}
Expected meter type: {meter_type}

Inspect only the attached image. Do not submit, update, call APIs, or infer an action.
Return exactly one JSON object with these fields:
same_meter, meter_type, serial_visible, serial, reading_raw,
integer_part, decimal_part, digit_confidence, image_quality,
glare, blur, rotation, ambiguous.

Rules:
- integer_part must contain only the whole-number reading.
- decimal_part may be null if no decimal digits are visible.
- digit_confidence is an array of numbers from 0 to 1.
- image_quality is one of good, fair, poor.
- same_meter must be false when visual identity conflicts with the expected meter.
- ambiguous must be true whenever any reading digit is uncertain.
"""


def _parse_raw(raw) -> dict:
    if isinstance(raw, dict):
        return deepcopy(raw)
    if not isinstance(raw, str):
        raise GeminiResultError("result must be a JSON object or JSON string")
    text = raw.strip()
    if text.startswith("```"):
        lines = text.splitlines()
        if lines and lines[0].startswith("```"):
            lines = lines[1:]
        if lines and lines[-1].strip() == "```":
            lines = lines[:-1]
        text = "\n".join(lines).strip()
    try:
        parsed = json.loads(text)
    except json.JSONDecodeError as exc:
        raise GeminiResultError("invalid JSON result") from exc
    if not isinstance(parsed, dict):
        raise GeminiResultError("result JSON must be an object")
    return parsed

def _require_bool(data: dict, key: str) -> bool:
    value = data.get(key)
    if type(value) is not bool:
        raise GeminiResultError(f"{key} must be boolean")
    return value


def _require_integer(value, key: str, *, allow_none: bool = False):
    if value is None and allow_none:
        return None
    if isinstance(value, bool):
        raise GeminiResultError(f"{key} must be integer")
    if not isinstance(value, int):
        raise GeminiResultError(f"{key} must be integer")
    if value < 0:
        raise GeminiResultError(f"{key} must be non-negative")
    return value


def normalize_result(raw) -> dict:
    data = _parse_raw(raw)
    missing = [key for key in REQUIRED_FIELDS if key not in data]
    if missing:
        raise GeminiResultError("missing required fields: " + ", ".join(missing))

    same_meter = _require_bool(data, "same_meter")
    serial_visible = _require_bool(data, "serial_visible")
    glare = _require_bool(data, "glare")
    blur = _require_bool(data, "blur")
    ambiguous = _require_bool(data, "ambiguous")

    meter_type = str(data["meter_type"]).strip().lower()
    if meter_type not in {"cold_water", "hot_water", "unknown"}:
        raise GeminiResultError("meter_type is invalid")
    serial = str(data["serial"] or "").strip()
    reading_raw = str(data["reading_raw"] or "").strip()
    integer_part = _require_integer(data["integer_part"], "integer_part")
    decimal_part = _require_integer(data["decimal_part"], "decimal_part", allow_none=True)

    confidences = data["digit_confidence"]
    if not isinstance(confidences, list) or not confidences:
        raise GeminiResultError("digit_confidence must be a non-empty list")
    normalized_confidence = []
    for value in confidences:
        if isinstance(value, bool) or not isinstance(value, (int, float)):
            raise GeminiResultError("digit_confidence values must be numbers")
        number = float(value)
        if not math.isfinite(number) or not 0.0 <= number <= 1.0:
            raise GeminiResultError("digit_confidence values must be between 0 and 1")
        normalized_confidence.append(number)

    image_quality = str(data["image_quality"]).strip().lower()
    if image_quality not in {"good", "fair", "poor"}:
        raise GeminiResultError("image_quality is invalid")
    rotation = data["rotation"]
    if isinstance(rotation, bool) or not isinstance(rotation, (int, float)):
        raise GeminiResultError("rotation must be numeric")
    rotation = float(rotation)
    if not math.isfinite(rotation):
        raise GeminiResultError("rotation must be finite")

    return {
        "same_meter": same_meter,
        "meter_type": meter_type,
        "serial_visible": serial_visible,
        "serial": serial,
        "reading_raw": reading_raw,
        "integer_part": integer_part,
        "decimal_part": decimal_part,
        "digit_confidence": normalized_confidence,
        "image_quality": image_quality,
        "glare": glare,
        "blur": blur,
        "rotation": rotation,
        "ambiguous": ambiguous,
    }


def compare_passes(first: dict, second: dict) -> dict:
    a = normalize_result(first)
    b = normalize_result(second)
    agree = (
        a["same_meter"] == b["same_meter"]
        and a["meter_type"] == b["meter_type"]
        and a["serial_visible"] == b["serial_visible"]
        and (not a["serial_visible"] or a["serial"].lower() == b["serial"].lower())
        and a["integer_part"] == b["integer_part"]
        and a["decimal_part"] == b["decimal_part"]
    )
    merged = deepcopy(a)
    merged["passes_agree"] = bool(agree)
    if not agree:
        merged["ambiguous"] = True
    else:
        merged["ambiguous"] = bool(a["ambiguous"] or b["ambiguous"])
        merged["glare"] = bool(a["glare"] or b["glare"])
        merged["blur"] = bool(a["blur"] or b["blur"])
        merged["digit_confidence"] = [
            min(x, y) for x, y in zip(a["digit_confidence"], b["digit_confidence"])
        ] if len(a["digit_confidence"]) == len(b["digit_confidence"]) else a["digit_confidence"]
        quality_rank = {"good": 0, "fair": 1, "poor": 2}
        merged["image_quality"] = max(
            (a["image_quality"], b["image_quality"]),
            key=lambda x: quality_rank[x],
        )
    return merged

def _identity_key(value) -> str:
    return "".join(ch for ch in str(value or "").lower() if ch.isalnum())

def _type_key(value) -> str:
    key=_identity_key(value)
    return {"coldwater":"coldwater","hotwater":"hotwater","хвс":"coldwater","гвс":"hotwater"}.get(key,key)

def _digits_only(value) -> str:
    return "".join(ch for ch in str(value or "") if ch.isdigit())

def build_deep_prompt(profile: dict) -> str:
    return f"""Read only the display of the already identified water meter {profile.get('meter_id')}.
Return JSON only: same_meter, meter_type, serial_visible, serial, black_digits, red_digits,
display_bbox, digit_confidence, ambiguous. Do not infer a decimal point from magnitude.
black_digits are the whole-m3 wheels; red_digits are the fractional wheels. Preserve leading zeros.
Expected layout: {profile.get('integer_digits')} black digits and {profile.get('decimal_digits')} red digits.
Do not call APIs and do not submit anything."""

def validate_deep_reading(profile: dict, first: dict, second: dict, local_ocr_candidates: list[str], *, third: dict | None = None, previous_value: float | None = None) -> dict:
    reasons=[]; warnings=[]
    int_digits=int(profile.get('integer_digits') or 0); dec_digits=int(profile.get('decimal_digits') or 0)
    if int_digits <= 0 or dec_digits < 0:
        return {'ok':False,'status':'RED','reasons':['meter_layout_not_calibrated'],'canonical_digits':None}
    expected_type=_type_key(profile.get('meter_type'))
    expected_ids={_identity_key(profile.get('serial')),_identity_key(profile.get('physical_serial'))}; expected_ids.discard('')
    total_digits=int_digits+dec_digits

    def parsed(obj):
        black=_digits_only(obj.get('black_digits')); red=_digits_only(obj.get('red_digits'))
        identity_ok=obj.get('same_meter') is not False and obj.get('ambiguous') is not True
        meter_type=_type_key(obj.get('meter_type'))
        if meter_type not in {'', 'unknown', expected_type}: identity_ok=False
        layout_ok=len(black)==int_digits and len(red)==dec_digits
        return {'black':black,'red':red,'canonical':black+red,'identity_ok':identity_ok,'layout_ok':layout_ok}

    passes=[parsed(first),parsed(second)]
    if third is not None: passes.append(parsed(third))
    valid=[x for x in passes if x['identity_ok'] and x['layout_ok']]
    if len(valid)<2:
        if any(not x['layout_ok'] for x in passes): reasons.append('digit_layout_mismatch')
        reasons.append('vision_identity_or_quality_uncertain')
        return {'ok':False,'status':'RED','reasons':list(dict.fromkeys(reasons)),'canonical_digits':None}

    counts={}
    for x in valid: counts[x['canonical']]=counts.get(x['canonical'],0)+1
    canonical,max_count=max(counts.items(),key=lambda kv:kv[1])
    if max_count < 2:
        reasons.append('no_vision_consensus' if third is not None else 'vision_pass_disagreement')
    if third is None and len(valid)>=2 and valid[0]['canonical']!=valid[1]['canonical']:
        reasons.append('vision_pass_disagreement')

    valid_ocr={_digits_only(x) for x in (local_ocr_candidates or []) if len(_digits_only(x))==total_digits}
    if valid_ocr and canonical not in valid_ocr:
        if third is not None and max_count == 3:
            warnings.append('local_ocr_disagreed')
        else:
            reasons.append('local_ocr_not_confirmed')

    integer_part=int(canonical[:int_digits]); decimal_part=int(canonical[int_digits:]) if dec_digits else 0
    if previous_value is not None and integer_part < int(float(previous_value)):
        reasons.append('reading_decreased')
    reasons=list(dict.fromkeys(reasons))
    if reasons:
        return {'ok':False,'status':'RED','reasons':reasons,'canonical_digits':canonical,
                'integer_part':integer_part,'decimal_part':decimal_part,'warnings':warnings}
    reading_value=integer_part + (decimal_part/(10**dec_digits) if dec_digits else 0.0)
    return {'ok':True,'status':'GREEN','reasons':[],'canonical_digits':canonical,
            'integer_part':integer_part,'decimal_part':decimal_part,'reading_value':reading_value,
            'vision_consensus_count':max_count,'warnings':warnings}

def route_photo_observation(observation: dict, profiles: list[dict], *, explicit_meter_id: int | None = None) -> dict:
    """Only known or explicitly bound meters enter the deep meter pipeline."""
    generic={"route":"generic_photo","meter_id":None,"provider_contacted":False,"deep_check_required":False}
    if not isinstance(observation,dict) or observation.get("is_water_meter") is not True:
        return generic
    observed_type=_type_key(observation.get("meter_type"))
    if explicit_meter_id is not None:
        candidates=[p for p in profiles if int(p.get('meter_id') or -1)==int(explicit_meter_id)]
        if len(candidates)!=1: return generic
        expected=_type_key(candidates[0].get('meter_type'))
        if observed_type and observed_type not in {'unknown',expected}: return generic
        return {"route":"known_meter","meter_id":int(explicit_meter_id),"binding":"user_explicit",
                "provider_contacted":False,"deep_check_required":True}
    serial=_identity_key(observation.get("serial")) if observation.get("serial_visible") is True else ""
    matches=[]
    if serial:
        for profile in profiles:
            ids={_identity_key(profile.get("serial")),_identity_key(profile.get("physical_serial"))}; ids.discard("")
            expected=_type_key(profile.get("meter_type"))
            if serial in ids and (not observed_type or observed_type in {'unknown',expected}): matches.append(int(profile['meter_id']))
    if len(set(matches))!=1: return generic
    return {"route":"known_meter","meter_id":matches[0],"binding":"database_serial",
            "provider_contacted":False,"deep_check_required":True}
