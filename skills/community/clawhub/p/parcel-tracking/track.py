#!/usr/bin/env python3
import os
import sys
import json
import argparse
import requests
from typing import Any, Dict, List

def oc_print(obj: Any):
    print(json.dumps(obj, ensure_ascii=False, indent=2))

def get_api_base() -> str:
    return os.getenv("TRACK123_API_BASE", "https://api.track123.com/gateway/open-api/tk/v2")

def get_api_secret() -> str:
    secret = os.getenv("TRACK123_API_SECRET")
    if not secret:
        raise RuntimeError("TRACK123_API_SECRET not set")
    return secret

def api_headers() -> Dict[str, str]:
    return {
        "Track123-Api-Secret": get_api_secret(),  # Track123 Header[web:35]
        "accept": "application/json",
        "content-type": "application/json",
    }

def query_track123(tracking_number: str, postal_code: str | None) -> Dict[str, Any]:
    """
    Track123 /track/query – auto-detect mit leerem courierCode.[web:35]
    """
    url = f"{get_api_base()}/track/query"
    payload = {
        "trackNos": [tracking_number],
        "orderNos": [""],
        "queryPageSize": 1,
    }
    if postal_code:
        payload["postalCode"] = postal_code  # Für Filterung/Erweiterung[web:35]

    resp = requests.post(url, headers=api_headers(), json=payload)
    resp.raise_for_status()
    data = resp.json()
    if data.get("code") != "00000":
        raise RuntimeError(f"Track123 Error: {data.get('msg', 'Unknown')}")
    
    accepted = data["data"].get("accepted", {}).get("content", [])
    if not accepted:
        raise RuntimeError("Kein Tracking gefunden")
    
    return accepted[0]  # Erstes (und einziges) Ergebnis

def normalize_response(raw: Dict[str, Any]) -> Dict[str, Any]:
    """
    Normalisiert Track123-Response.[web:35]
    """
    checkpoints = []
    local_info = raw.get("localLogisticsInfo", {})
    for detail in local_info.get("trackingDetails", []):
        checkpoints.append({
            "time": detail.get("eventTime"),
            "location": detail.get("address", ""),
            "status": detail.get("eventDetail"),
            "substatus": detail.get("transitSubStatus"),
        })
    
    last_mile = raw.get("lastMileInfo", {})
    lm_track = last_mile.get("openApiWayBillInfo", {})
    lm_checkpoints = lm_track.get("trackingDetails", [])
    checkpoints.extend([{
        "time": d.get("eventTime"),
        "location": d.get("address", ""),
        "status": d.get("eventDetail"),
        "substatus": d.get("transitSubStatus"),
    } for d in lm_checkpoints])

    carrier = local_info.get("courierNameEN") or local_info.get("courierNameCN", "Unknown")

    return {
        "carrier": {"name": carrier, "code": local_info.get("courierCode")},
        "tracking_number": raw.get("trackNo"),
        "current_status": raw.get("trackingStatus", ""),
        "transit_status": raw.get("transitStatus"),
        "delivered": raw.get("deliveredTime") is not None,
        "eta": raw.get("expectedDelivery"),
        "checkpoints": checkpoints,
        "tracking_url": local_info.get("courierTrackingLink"),
        "raw": raw,
    }

def format_markdown(result: Dict[str, Any]) -> str:
    carrier = result["carrier"]["name"]
    tn = result["tracking_number"]
    status = result["current_status"]
    delivered = "Ja" if result["delivered"] else "Nein"
    eta = result["eta"] or "keine Angabe"
    url = result.get("tracking_url") or ""

    md = [
        f"**Paketdienst:** {carrier}",
        f"**Sendungsnummer:** {tn}",
        f"**Status:** {status} ({result.get('transit_status', '')})",
        f"**Zugestellt:** {delivered}",
        f"**ETA:** {eta}",
    ]
    if url:
        md.append(f"**Direktlink:** {url}")
    md.append("")

    if result["checkpoints"]:
        md.append("**Verlauf:**")
        md.append("| Zeit | Ort | Status |")
        md.append("|------|-----|--------|")
        for cp in result["checkpoints"][:10]:  # Max 10
            t = cp.get("time", "")[:16]  # Kürzen
            loc = cp.get("location", "")
            st = cp.get("status", "")[:50]
            md.append(f"| {t} | {loc} | {st} |")

    return "\n".join(md)

def main(argv: List[str]) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--tracking_number", required=True)
    parser.add_argument("--postal_code", required=False)
    args = parser.parse_args(argv)

    try:
        raw = query_track123(args.tracking_number, args.postal_code)
        normalized = normalize_response(raw)
        markdown = format_markdown(normalized)

        oc_print({
            "ok": True,
            "markdown": markdown,
            "carrier": normalized["carrier"],
            "status": normalized["current_status"],
            "delivered": normalized["delivered"],
            "eta": normalized["eta"],
            "checkpoints_count": len(normalized["checkpoints"]),
            "tracking_url": normalized.get("tracking_url"),
        })
        return 0
    except Exception as e:
        oc_print({"ok": False, "error": str(e)})
        return 1

if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
