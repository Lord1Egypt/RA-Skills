#!/usr/bin/env python3
"""Portable, dependency-free multi-source IP intelligence fusion CLI."""

from __future__ import annotations

import argparse
import base64
import concurrent.futures
import datetime as dt
import html
import ipaddress
import json
import os
import re
import ssl
import statistics
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Callable, Dict, Iterable, List, Mapping, Optional, Sequence, Tuple


VERSION = "1.3.1"
USER_AGENT = f"ip-intelligence-fusion/{VERSION} (+https://github.com/GetIPProxy/ip-intelligence-fusion)"
DEFAULT_TIMEOUT = 8.0
MAX_RESPONSE_BYTES = 2_000_000

FACT_FIELDS = (
    "country_code", "country", "region", "city", "asn", "organization", "isp",
    "network_type", "allocation_prefix", "route_prefix", "registry_country", "reverse_dns",
)
RISK_FLAGS = ("is_proxy", "is_vpn", "is_tor", "is_hosting", "is_abuser", "is_bot")
RISK_WEIGHTS = {
    "ipqs": 1.00, "scamalytics": 0.95, "abuseipdb": 0.95, "ipdata": 0.90,
    "proxycheck": 0.85, "ipapi-is": 0.80, "ipinfo": 0.75, "ping0": 0.70,
    "ip-api": 0.60,
}
RISK_PROVIDER_ORDER = (
    "ipqs", "abuseipdb", "scamalytics", "ipdata", "proxycheck", "ipapi-is", "ping0",
)
DETAIL_PROVIDER_GROUPS = (
    ("Risk and reputation", ("ipqs", "abuseipdb", "scamalytics", "ipdata", "proxycheck", "ipapi-is", "ping0")),
    ("Network and privacy", ("ipinfo", "ip-api")),
    ("Registry and routing", ("rdap", "ripestat")),
    ("Geolocation cross-check", ("geojs",)),
)
PUBLIC_PAGE_DOMAINS = {
    "ipinfo": {"ipinfo.io", "www.ipinfo.io"},
    "scamalytics": {"scamalytics.com", "www.scamalytics.com"},
    "ipqs": {"ipqualityscore.com", "www.ipqualityscore.com"},
    "ipdata": {"ipdata.co", "www.ipdata.co"},
    "ping0": {"ping0.cc", "www.ping0.cc", "ip.ping0.cc"},
}
EVIDENCE_FIELDS = set(FACT_FIELDS) | set(RISK_FLAGS) | {
    "risk_score", "abuse_score", "latitude", "longitude", "timezone", "hostname",
    "range", "company", "domain", "anycast", "privacy", "native_ip",
    "native_classification", "trust_score", "blocklist_reports", "recent_abuse",
    "is_mobile", "is_residential_proxy", "is_anonymous", "is_relay", "analysis",
}
EVIDENCE_BOOLEAN_FIELDS = set(RISK_FLAGS) | {
    "anycast", "privacy", "native_ip", "recent_abuse", "is_mobile",
    "is_residential_proxy", "is_anonymous", "is_relay",
}
LEVELS = ((30, "low"), (50, "guarded"), (70, "elevated"), (85, "high"), (101, "critical"))


class LookupError(RuntimeError):
    """An expected provider or input failure safe to display to the user."""


@dataclass(frozen=True)
class Provider:
    id: str
    name: str
    category: str
    lookup: Callable[[str, float], Dict[str, Any]]
    credential_env: Tuple[str, ...] = ()
    experimental: bool = False

    def configured(self) -> bool:
        return all(os.environ.get(key, "").strip() for key in self.credential_env)


@dataclass
class ProviderResult:
    id: str
    name: str
    category: str
    status: str
    elapsed_ms: int = 0
    source_url: Optional[str] = None
    data: Dict[str, Any] = field(default_factory=dict)
    raw: Any = None
    message: Optional[str] = None
    experimental: bool = False
    collection_method: str = "api"
    observed_at: Optional[str] = None

    def as_dict(self, include_raw: bool) -> Dict[str, Any]:
        result = {
            "id": self.id, "name": self.name, "category": self.category,
            "status": self.status, "elapsed_ms": self.elapsed_ms,
            "experimental": self.experimental,
            "collection_method": self.collection_method,
        }
        if self.source_url:
            result["source_url"] = self.source_url
        if self.data:
            result["data"] = self.data
        if self.message:
            result["message"] = self.message
        if self.observed_at:
            result["observed_at"] = self.observed_at
        if include_raw and self.raw is not None:
            result["raw"] = self.raw
        return result


def utc_now() -> str:
    return dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def compact(value: Any) -> Any:
    if value is None or value == "" or value == [] or value == {}:
        return None
    if isinstance(value, str) and value.strip().casefold() in ("nil", "null", "none", "n/a", "unknown", "undefined"):
        return None
    return value


def first(mapping: Mapping[str, Any], *keys: str) -> Any:
    for key in keys:
        value = mapping.get(key)
        if compact(value) is not None:
            return value
    return None


def nested(mapping: Mapping[str, Any], *path: str) -> Mapping[str, Any]:
    current: Any = mapping
    for key in path:
        if not isinstance(current, Mapping):
            return {}
        current = current.get(key, {})
    return current if isinstance(current, Mapping) else {}


def text_value(value: Any) -> Optional[str]:
    if value is None or isinstance(value, (dict, list)):
        return None
    value = str(value).strip()
    return value if compact(value) is not None else None


def number(value: Any) -> Optional[float]:
    if value is None or isinstance(value, bool):
        return None
    try:
        result = float(value)
        return max(0.0, min(100.0, result))
    except (TypeError, ValueError):
        return None


def boolean(value: Any) -> Optional[bool]:
    if isinstance(value, bool):
        return value
    if isinstance(value, (int, float)) and value in (0, 1):
        return bool(value)
    if isinstance(value, str):
        lowered = value.strip().lower()
        if lowered in ("true", "yes", "y", "1", "enabled", "detected"):
            return True
        if lowered in ("false", "no", "n", "0", "disabled", "not detected"):
            return False
    return None


def normalize_asn(value: Any) -> Optional[str]:
    value = text_value(value)
    if not value:
        return None
    match = re.search(r"(?:AS)?\s*(\d+)", value, re.I)
    return f"AS{match.group(1)}" if match else value


def clean_data(**values: Any) -> Dict[str, Any]:
    return {key: value for key, value in values.items() if compact(value) is not None}


def public_ip(value: str) -> str:
    try:
        address = ipaddress.ip_address(value.strip())
    except ValueError as exc:
        raise LookupError(f"Invalid IP address: {value!r}") from exc
    if not address.is_global:
        raise LookupError(f"Refusing remote lookup for non-public IP address: {address.compressed}")
    return address.compressed


def safe_error(exc: BaseException) -> str:
    if isinstance(exc, urllib.error.HTTPError):
        return f"HTTP {exc.code} {exc.reason}".strip()
    if isinstance(exc, urllib.error.URLError):
        reason = getattr(exc, "reason", exc)
        return f"Network error: {reason}"
    message = str(exc)
    message = re.sub(r"https?://[^\s]+", "<upstream-url>", message)
    return message[:300] or exc.__class__.__name__


def load_public_page_evidence(paths: Sequence[str], target_ip: str) -> Dict[str, ProviderResult]:
    providers = {provider.id: provider for provider in PROVIDERS}
    loaded: Dict[str, ProviderResult] = {}
    for path_text in paths:
        path = Path(path_text).expanduser()
        try:
            payload = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise LookupError(f"Cannot read evidence file {path}: {safe_error(exc)}") from exc
        items = payload.get("evidence") if isinstance(payload, Mapping) else payload
        if isinstance(items, Mapping):
            items = [items]
        if not isinstance(items, list):
            raise LookupError(f"Evidence file {path} must contain an object, list, or evidence list")
        for index, item in enumerate(items):
            if not isinstance(item, Mapping):
                raise LookupError(f"Evidence item {index} in {path} must be an object")
            provider_id = text_value(item.get("provider"))
            if provider_id not in PUBLIC_PAGE_DOMAINS or provider_id not in providers:
                raise LookupError(f"Evidence item {index} has unsupported provider: {provider_id!r}")
            try:
                item_ip = ipaddress.ip_address(str(item.get("target_ip", "")).strip()).compressed
            except ValueError as exc:
                raise LookupError(f"Evidence item {index} has invalid target_ip") from exc
            if item_ip != target_ip:
                raise LookupError(f"Evidence target {item_ip} does not match requested IP {target_ip}")
            source_url = text_value(item.get("source_url"))
            parsed = urllib.parse.urlsplit(source_url or "")
            hostname = (parsed.hostname or "").lower()
            if parsed.scheme != "https" or hostname not in PUBLIC_PAGE_DOMAINS[provider_id]:
                raise LookupError(f"Evidence for {provider_id} must use its official HTTPS domain")
            decoded_path = urllib.parse.unquote(parsed.path).casefold()
            if target_ip.casefold() not in decoded_path:
                raise LookupError(f"Evidence URL for {provider_id} must contain the target IP")
            data = item.get("data")
            if not isinstance(data, Mapping) or not data:
                raise LookupError(f"Evidence for {provider_id} has no data object")
            unknown = sorted(set(data) - EVIDENCE_FIELDS)
            if unknown:
                raise LookupError(f"Evidence for {provider_id} has unsupported field(s): {', '.join(unknown)}")
            normalized: Dict[str, Any] = {}
            for key, value in data.items():
                if key in EVIDENCE_BOOLEAN_FIELDS:
                    parsed_bool = boolean(value)
                    if parsed_bool is None:
                        raise LookupError(f"Evidence field {key} for {provider_id} must be boolean")
                    normalized[key] = parsed_bool
                elif key in ("risk_score", "abuse_score", "trust_score"):
                    parsed_number = number(value)
                    if parsed_number is None:
                        raise LookupError(f"Evidence field {key} for {provider_id} must be between 0 and 100")
                    normalized[key] = parsed_number
                elif key == "asn":
                    parsed_asn = normalize_asn(value)
                    if not parsed_asn or not re.fullmatch(r"AS\d+", parsed_asn):
                        raise LookupError(f"Evidence field asn for {provider_id} is invalid")
                    normalized[key] = parsed_asn
                elif key in ("allocation_prefix", "route_prefix", "range"):
                    try:
                        normalized[key] = str(ipaddress.ip_network(str(value).strip(), strict=False))
                    except ValueError as exc:
                        raise LookupError(f"Evidence field {key} for {provider_id} is invalid") from exc
                else:
                    parsed_text = text_value(value)
                    if parsed_text is None or len(parsed_text) > 500:
                        raise LookupError(f"Evidence field {key} for {provider_id} must be concise text")
                    normalized[key] = parsed_text
            if provider_id == "ipdata" and "trust_score" in normalized:
                derived = round(100.0 - normalized["trust_score"], 1)
                if "risk_score" in normalized and abs(normalized["risk_score"] - derived) > 1:
                    raise LookupError("ipdata risk_score conflicts with its trust_score")
                normalized.setdefault("risk_score", derived)
            observed_at = text_value(item.get("observed_at")) or utc_now()
            try:
                dt.datetime.fromisoformat(observed_at.replace("Z", "+00:00"))
            except ValueError as exc:
                raise LookupError(f"Evidence observed_at for {provider_id} must be ISO 8601") from exc
            if provider_id in loaded:
                raise LookupError(f"Duplicate public-page evidence for provider: {provider_id}")
            provider = providers[provider_id]
            loaded[provider_id] = ProviderResult(
                provider.id, provider.name, provider.category, "success", source_url=source_url,
                data=normalized, message="Public lookup page read with host-provided web tooling.",
                experimental=provider.experimental, collection_method="browser-public-page",
                observed_at=observed_at,
            )
    return loaded


def merge_evidence(results: Sequence[ProviderResult], evidence: Mapping[str, ProviderResult]) -> List[ProviderResult]:
    merged = []
    seen = set()
    for result in results:
        replacement = evidence.get(result.id)
        if replacement and result.status != "success":
            merged.append(replacement)
        else:
            merged.append(result)
        seen.add(result.id)
    return merged


def request_bytes(
    url: str,
    timeout: float,
    headers: Optional[Mapping[str, str]] = None,
    method: str = "GET",
) -> Tuple[bytes, Mapping[str, str]]:
    request_headers = {"User-Agent": USER_AGENT, "Accept": "application/json, text/html;q=0.8"}
    request_headers.update(headers or {})
    request = urllib.request.Request(url, headers=request_headers, method=method)
    context = ssl.create_default_context()
    with urllib.request.urlopen(request, timeout=timeout, context=context) as response:
        length = response.headers.get("Content-Length")
        if length and int(length) > MAX_RESPONSE_BYTES:
            raise LookupError("Upstream response exceeds size limit")
        body = response.read(MAX_RESPONSE_BYTES + 1)
        if len(body) > MAX_RESPONSE_BYTES:
            raise LookupError("Upstream response exceeds size limit")
        return body, dict(response.headers.items())


def request_json(
    url: str,
    timeout: float,
    headers: Optional[Mapping[str, str]] = None,
) -> Any:
    body, _ = request_bytes(url, timeout, headers)
    try:
        return json.loads(body.decode("utf-8-sig"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise LookupError("Upstream returned invalid JSON") from exc


def with_query(url: str, params: Mapping[str, Any]) -> str:
    parsed = urllib.parse.urlsplit(url)
    query = dict(urllib.parse.parse_qsl(parsed.query, keep_blank_values=True))
    query.update({key: str(value) for key, value in params.items() if value is not None})
    return urllib.parse.urlunsplit((parsed.scheme, parsed.netloc, parsed.path,
                                    urllib.parse.urlencode(query), parsed.fragment))


def risk_fields(payload: Mapping[str, Any]) -> Dict[str, Any]:
    return clean_data(
        risk_score=number(first(payload, "risk_score", "fraud_score", "score", "abuse_score")),
        is_proxy=boolean(first(payload, "is_proxy", "proxy")),
        is_vpn=boolean(first(payload, "is_vpn", "vpn")),
        is_tor=boolean(first(payload, "is_tor", "tor")),
        is_hosting=boolean(first(payload, "is_hosting", "hosting", "is_datacenter", "datacenter")),
        is_abuser=boolean(first(payload, "is_abuser", "abuser", "abuse")),
        is_bot=boolean(first(payload, "is_bot", "bot", "is_crawler", "crawler")),
    )


def lookup_ip_api(ip: str, timeout: float) -> Dict[str, Any]:
    fields = "status,message,country,countryCode,regionName,city,isp,org,as,asname,reverse,mobile,proxy,hosting,query"
    url = f"http://ip-api.com/json/{urllib.parse.quote(ip)}?fields={fields}"
    raw = request_json(url, timeout)
    if raw.get("status") != "success" or raw.get("query") != ip:
        raise LookupError(text_value(raw.get("message")) or "IP-API lookup failed")
    data = clean_data(
        country_code=raw.get("countryCode"), country=raw.get("country"), region=raw.get("regionName"),
        city=raw.get("city"), asn=normalize_asn(raw.get("as")), organization=first(raw, "asname", "org"),
        isp=raw.get("isp"), reverse_dns=raw.get("reverse"), is_mobile=boolean(raw.get("mobile")),
        is_proxy=boolean(raw.get("proxy")), is_hosting=boolean(raw.get("hosting")),
    )
    return {"data": data, "raw": raw, "source_url": f"https://ip-api.com/#{ip}"}


def lookup_geojs(ip: str, timeout: float) -> Dict[str, Any]:
    url = f"https://get.geojs.io/v1/ip/geo/{urllib.parse.quote(ip)}.json"
    raw = request_json(url, timeout)
    if text_value(raw.get("ip")) != ip:
        raise LookupError("GeoJS response did not echo the target IP")
    data = clean_data(
        country_code=raw.get("country_code"), country=raw.get("country"), region=raw.get("region"),
        city=raw.get("city"), asn=normalize_asn(raw.get("asn")), organization=raw.get("organization"),
        latitude=compact(raw.get("latitude")), longitude=compact(raw.get("longitude")),
        timezone=compact(raw.get("timezone")),
    )
    return {"data": data, "raw": raw, "source_url": f"https://get.geojs.io/v1/ip/geo/{ip}.json"}


def rdap_vcard(entity: Mapping[str, Any]) -> Dict[str, str]:
    result: Dict[str, str] = {}
    vcard = entity.get("vcardArray")
    if not isinstance(vcard, list) or len(vcard) < 2 or not isinstance(vcard[1], list):
        return result
    for item in vcard[1]:
        if not isinstance(item, list) or len(item) < 4:
            continue
        key, value = text_value(item[0]), text_value(item[3])
        if key and value and key in ("fn", "email", "org"):
            result.setdefault(key, value)
    return result


def prefix_from_range(start: Any, end: Any) -> Optional[str]:
    try:
        ranges = list(ipaddress.summarize_address_range(ipaddress.ip_address(str(start)), ipaddress.ip_address(str(end))))
        return str(ranges[0]) if len(ranges) == 1 else f"{start} - {end}"
    except ValueError:
        return None


def lookup_rdap(ip: str, timeout: float) -> Dict[str, Any]:
    rdap_urls = (
        f"https://rdap.org/ip/{urllib.parse.quote(ip)}",
        f"https://rdap-bootstrap.arin.net/bootstrap/ip/{urllib.parse.quote(ip)}",
    )
    raw = None
    source_url = rdap_urls[0]
    failures = []
    deadline = time.monotonic() + timeout
    for index, candidate in enumerate(rdap_urls):
        remaining = deadline - time.monotonic()
        remaining_candidates = len(rdap_urls) - index
        if remaining <= 0:
            failures.append("timeout budget exhausted")
            break
        try:
            raw = request_json(candidate, max(1.0, remaining / remaining_candidates))
            source_url = candidate
            break
        except (LookupError, urllib.error.URLError, urllib.error.HTTPError, TimeoutError, OSError) as exc:
            failures.append(safe_error(exc))
    if not isinstance(raw, Mapping):
        raise LookupError("RDAP endpoints unavailable: " + "; ".join(failures))
    entities = raw.get("entities") if isinstance(raw.get("entities"), list) else []
    names, abuse_emails = [], []
    for entity in entities:
        if not isinstance(entity, Mapping):
            continue
        card = rdap_vcard(entity)
        if card.get("fn"):
            names.append(card["fn"])
        roles = entity.get("roles") if isinstance(entity.get("roles"), list) else []
        if "abuse" in roles and card.get("email"):
            abuse_emails.append(card["email"])
    events = {}
    for event in raw.get("events", []):
        if isinstance(event, Mapping) and event.get("eventAction") and event.get("eventDate"):
            events[str(event["eventAction"])] = event["eventDate"]
    allocation = first(raw, "cidr0_cidrs", "cidr")
    if isinstance(allocation, list) and allocation and isinstance(allocation[0], Mapping):
        item = allocation[0]
        allocation = f"{item.get('v4prefix') or item.get('v6prefix')}/{item.get('length')}"
    if not isinstance(allocation, str):
        allocation = prefix_from_range(raw.get("startAddress"), raw.get("endAddress"))
    data = clean_data(
        allocation_prefix=allocation, registry_country=raw.get("country"), registry=raw.get("port43"),
        network_name=raw.get("name"), network_handle=raw.get("handle"),
        organization=names[0] if names else None, abuse_contacts=sorted(set(abuse_emails)),
        registration_date=events.get("registration"), last_changed=events.get("last changed"),
    )
    return {"data": data, "raw": raw, "source_url": source_url}


def lookup_ripestat(ip: str, timeout: float) -> Dict[str, Any]:
    url = with_query("https://stat.ripe.net/data/routing-status/data.json", {"resource": ip})
    raw = request_json(url, timeout)
    data_raw = raw.get("data") if isinstance(raw.get("data"), Mapping) else {}
    origins = data_raw.get("origins") if isinstance(data_raw.get("origins"), list) else []
    origin = origins[0] if origins and isinstance(origins[0], Mapping) else {}
    prefixes = data_raw.get("announced_space") if isinstance(data_raw.get("announced_space"), Mapping) else {}
    last_seen = data_raw.get("last_seen") if isinstance(data_raw.get("last_seen"), Mapping) else {}
    route_prefix = first(data_raw, "prefix") or first(prefixes, "v4", "v6") or last_seen.get("prefix")
    data = clean_data(
        route_prefix=route_prefix, asn=normalize_asn(first(origin, "origin", "asn")),
        organization=first(origin, "holder", "name"), visibility=data_raw.get("visibility"),
        first_seen=data_raw.get("first_seen"), last_seen=data_raw.get("last_seen"),
    )
    if not data:
        raise LookupError("RIPEstat returned no routing data")
    return {"data": data, "raw": raw, "source_url": f"https://stat.ripe.net/{ip}"}


def lookup_ipapi_is(ip: str, timeout: float) -> Dict[str, Any]:
    raw = request_json(with_query("https://api.ipapi.is/", {"q": ip}), timeout)
    if raw.get("error"):
        raise LookupError(text_value(raw.get("reason")) or "ipapi.is lookup failed")
    echoed_ip = text_value(raw.get("ip"))
    if not echoed_ip:
        raise LookupError("ipapi.is response did not echo the target IP")
    try:
        echoed_ip = ipaddress.ip_address(echoed_ip).compressed
    except ValueError as exc:
        raise LookupError("ipapi.is returned an invalid target IP") from exc
    if echoed_ip != ip:
        raise LookupError("ipapi.is response did not echo the target IP")
    company = nested(raw, "company")
    asn = nested(raw, "asn")
    location = nested(raw, "location")
    data = clean_data(
        country_code=first(location, "country_code", "country") or raw.get("cc"),
        country=location.get("country") or raw.get("country"),
        region=first(location, "state", "region"), city=location.get("city"),
        asn=normalize_asn(first(asn, "asn", "number") or raw.get("asn_num")),
        organization=first(asn, "org", "name") or raw.get("asn_org"),
        isp=first(company, "name", "domain") or raw.get("company_name"),
        network_type=first(company, "type", "network") or raw.get("company_type"),
        route_prefix=first(asn, "route", "prefix"),
        latitude=first(location, "latitude", "lat") or raw.get("lat"),
        longitude=first(location, "longitude", "lon") or raw.get("lon"),
        is_proxy=boolean(raw.get("is_proxy")), is_vpn=boolean(raw.get("is_vpn")),
        is_tor=boolean(raw.get("is_tor")), is_hosting=boolean(raw.get("is_datacenter")),
        is_abuser=boolean(raw.get("is_abuser")), is_bot=boolean(raw.get("is_crawler")),
        abuse_score=number(first(raw, "abuse_score", "risk_score")),
    )
    return {"data": data, "raw": raw, "source_url": f"https://ipapi.is/?q={ip}"}


def lookup_proxycheck(ip: str, timeout: float) -> Dict[str, Any]:
    params = {"vpn": 1, "asn": 1, "risk": 1}
    if os.environ.get("PROXYCHECK_API_KEY"):
        params["key"] = os.environ["PROXYCHECK_API_KEY"]
    raw = request_json(with_query(f"https://proxycheck.io/v2/{urllib.parse.quote(ip)}", params), timeout)
    if raw.get("status") != "ok" or not isinstance(raw.get(ip), Mapping):
        raise LookupError(text_value(raw.get("message")) or "proxycheck.io lookup failed")
    item = raw[ip]
    operator = nested(item, "operator")
    data = clean_data(
        country_code=item.get("isocode"), country=item.get("country"), region=item.get("region"),
        city=item.get("city"), asn=normalize_asn(item.get("asn")), organization=first(operator, "name", "url"),
        network_type=item.get("type"), is_proxy=boolean(item.get("proxy")),
        is_vpn=True if str(item.get("type", "")).lower() == "vpn" else None,
        risk_score=number(item.get("risk")),
    )
    return {"data": data, "raw": raw, "source_url": f"https://proxycheck.io/v2/{ip}"}


def lookup_ping0(ip: str, timeout: float) -> Dict[str, Any]:
    # Ping0's documented /geo endpoint only supports the caller's own IP. Its public
    # arbitrary-IP page is therefore best-effort and intentionally isolated here.
    url = f"https://ping0.cc/ip/{urllib.parse.quote(ip)}"
    body, headers = request_bytes(url, timeout, {"Accept": "text/html"})
    charset_match = re.search(r"charset=([^;]+)", headers.get("Content-Type", ""), re.I)
    charset = charset_match.group(1).strip() if charset_match else "utf-8"
    try:
        page = body.decode(charset, "replace")
    except LookupError:
        page = body.decode("utf-8", "replace")
    visible = html.unescape(re.sub(r"<[^>]+>", " ", page))
    visible = re.sub(r"\s+", " ", visible)
    if ip not in visible and ip not in page:
        raise LookupError("Ping0.cc response did not echo the target IP")
    def capture(pattern: str) -> Optional[str]:
        match = re.search(pattern, visible, re.I)
        return match.group(1).strip() if match else None
    risk = capture(r"(?:风控值|risk)[^0-9]{0,40}(\d{1,3})\s*%")
    asn = capture(r"\b(AS\d{1,10})\b")
    location = capture(r"(?:IP\s*位置|location)\s*[:：]?\s*([^|]{2,100}?)(?:探测时间|ASN|风险|risk)")
    page_type = capture(r"(?:IP\s*类型|type)\s*[:：]?\s*([^|]{2,80}?)(?:为什么|风控值|risk)")
    native_class = capture(r"原生\s*IP\s*(?:[（(]?\s*说明\s*[?？]?\s*[)）]?)?\s*([^|]{2,60}?)(?:大模型检测|AI)")
    location = re.sub(r"^[\s,，:：?？()（）]+|[\s,，:：?？()（）]+$", "", location or "") or None
    page_type = re.sub(r"[（(]?\s*说明\s*[?？]?\s*[)）]?", "", page_type or "").strip(" ,，:：") or None
    native_class = re.sub(r"[（(]?\s*说明\s*[?？]?\s*[)）]?", "", native_class or "").strip(" ,，:：") or None
    native_bool = None
    if native_class:
        if re.search(r"(?:非原生|广播|not\s+native)", native_class, re.I):
            native_bool = False
        elif re.search(r"(?:原生|native)", native_class, re.I):
            native_bool = True
    lowered = visible.lower()
    data = clean_data(
        asn=normalize_asn(asn), location_text=location, network_type=page_type,
        risk_score=number(risk), is_hosting=True if any(x in lowered for x in ("idc机房 ip", "datacenter ip")) else None,
        is_vpn=True if re.search(r"\bVPN\b", visible, re.I) else None,
        is_proxy=True if re.search(r"(?:代理|proxy)\s*IP", visible, re.I) else None,
        native_classification=native_class, native_ip=native_bool,
    )
    if len(data) < 2:
        raise LookupError("Ping0.cc page layout was not parseable")
    return {"data": data, "raw": {"title": capture(r"<title>(.*?)</title>")}, "source_url": url}


def lookup_ipinfo(ip: str, timeout: float) -> Dict[str, Any]:
    token = os.environ["IPINFO_TOKEN"]
    raw = request_json(with_query(f"https://api.ipinfo.io/lite/{urllib.parse.quote(ip)}", {"token": token}), timeout)
    privacy = raw.get("privacy") if isinstance(raw.get("privacy"), Mapping) else {}
    asn_obj = raw.get("asn") if isinstance(raw.get("asn"), Mapping) else {}
    loc = text_value(raw.get("loc"))
    latitude, longitude = (loc.split(",", 1) if loc and "," in loc else (None, None))
    data = clean_data(
        country_code=first(raw, "country_code", "country"), country=first(raw, "country_name"),
        region=raw.get("region"), city=raw.get("city"), asn=normalize_asn(first(raw, "asn", "as_number") or asn_obj.get("asn")),
        organization=first(raw, "as_name", "org") or first(asn_obj, "name", "domain"),
        network_type=first(raw, "as_type") or asn_obj.get("type"), reverse_dns=raw.get("hostname"),
        latitude=latitude, longitude=longitude, is_proxy=boolean(privacy.get("proxy")),
        is_vpn=boolean(privacy.get("vpn")), is_tor=boolean(privacy.get("tor")),
        is_hosting=boolean(privacy.get("hosting")),
    )
    return {"data": data, "raw": raw, "source_url": f"https://ipinfo.io/{ip}"}


def lookup_ipqs(ip: str, timeout: float) -> Dict[str, Any]:
    key = urllib.parse.quote(os.environ["IPQS_API_KEY"], safe="")
    url = with_query(f"https://www.ipqualityscore.com/api/json/ip/{key}/{urllib.parse.quote(ip)}", {
        "strictness": 1, "allow_public_access_points": "true", "fast": "false",
        "lighter_penalties": "true",
    })
    raw = request_json(url, timeout)
    if raw.get("success") is False:
        raise LookupError(text_value(raw.get("message")) or "IPQualityScore lookup failed")
    data = clean_data(
        country_code=raw.get("country_code"), region=raw.get("region"), city=raw.get("city"),
        asn=normalize_asn(raw.get("ASN")), organization=raw.get("organization"), isp=raw.get("ISP"),
        network_type=raw.get("connection_type"), risk_score=number(raw.get("fraud_score")),
        is_proxy=boolean(raw.get("proxy")), is_vpn=boolean(raw.get("vpn")), is_tor=boolean(raw.get("tor")),
        is_hosting=boolean(raw.get("hosting")), is_bot=boolean(first(raw, "bot_status", "is_crawler")),
        is_abuser=boolean(raw.get("recent_abuse")), recent_abuse=boolean(raw.get("recent_abuse")),
        active_vpn=boolean(raw.get("active_vpn")),
        active_tor=boolean(raw.get("active_tor")), abuse_velocity=raw.get("abuse_velocity"),
    )
    return {"data": data, "raw": raw, "source_url": f"https://www.ipqualityscore.com/free-ip-lookup-proxy-vpn-test/lookup/{ip}"}


def lookup_ipdata(ip: str, timeout: float) -> Dict[str, Any]:
    raw = request_json(with_query(f"https://api.ipdata.co/{urllib.parse.quote(ip)}", {"api-key": os.environ["IPDATA_API_KEY"]}), timeout)
    if raw.get("message") and not raw.get("ip"):
        raise LookupError(text_value(raw.get("message")) or "ipdata lookup failed")
    threat = raw.get("threat") if isinstance(raw.get("threat"), Mapping) else {}
    asn = raw.get("asn") if isinstance(raw.get("asn"), Mapping) else {}
    data = clean_data(
        country_code=raw.get("country_code"), country=raw.get("country_name"), region=raw.get("region"),
        city=raw.get("city"), asn=normalize_asn(first(asn, "asn", "number")), organization=first(asn, "name", "domain"),
        network_type=asn.get("type"), route_prefix=asn.get("route"),
        is_proxy=boolean(threat.get("is_proxy")), is_vpn=boolean(threat.get("is_vpn")),
        is_tor=boolean(threat.get("is_tor")), is_hosting=boolean(threat.get("is_datacenter")),
        is_abuser=boolean(first(threat, "is_known_abuser", "is_abuser")),
        is_bot=boolean(first(threat, "is_known_attacker", "is_bogon")),
        threat_scores=threat.get("scores") if isinstance(threat.get("scores"), Mapping) else None,
    )
    scores = data.get("threat_scores")
    if isinstance(scores, Mapping):
        data["risk_score"] = number(first(scores, "threat", "risk", "fraud"))
    return {"data": data, "raw": raw, "source_url": f"https://ipdata.co/{ip}"}


def lookup_scamalytics(ip: str, timeout: float) -> Dict[str, Any]:
    base = os.environ["SCAMALYTICS_API_URL"].strip()
    key = os.environ["SCAMALYTICS_API_KEY"]
    if not base.lower().startswith("https://"):
        raise LookupError("SCAMALYTICS_API_URL must use HTTPS")
    if "{ip}" in base or "{key}" in base:
        url = base.replace("{ip}", urllib.parse.quote(ip)).replace("{key}", urllib.parse.quote(key, safe=""))
    else:
        url = with_query(base, {"ip": ip, "key": key})
    raw = request_json(url, timeout)
    scam = raw.get("scamalytics") if isinstance(raw.get("scamalytics"), Mapping) else {}
    proxy = scam.get("scamalytics_proxy") if isinstance(scam.get("scamalytics_proxy"), Mapping) else {}
    external = raw.get("external_datasources") if isinstance(raw.get("external_datasources"), Mapping) else {}
    ipinfo = external.get("ipinfo") if isinstance(external.get("ipinfo"), Mapping) else {}
    risk = first(raw, "score", "fraud_score", "risk_score", "scamalytics_score")
    risk = risk if risk is not None else first(scam, "scamalytics_score", "score", "fraud_score", "risk_score")
    data = clean_data(
        country_code=first(raw, "ip_country_code", "country_code") or first(ipinfo, "ip_country_code", "country_code"),
        country=first(raw, "ip_country_name", "country_name", "country"), region=first(raw, "ip_region", "region"),
        city=first(raw, "ip_city", "city"), asn=normalize_asn(first(raw, "asn", "ip_asn") or first(ipinfo, "asn", "ip_asn")),
        organization=first(raw, "organization", "as_name", "isp_name") or first(scam, "scamalytics_org", "organization"),
        isp=first(raw, "isp", "isp_name") or first(scam, "scamalytics_isp", "isp"),
        risk_score=number(risk), is_proxy=boolean(first(raw, "is_proxy", "proxy")),
        is_vpn=boolean(first(raw, "is_vpn", "vpn") if first(raw, "is_vpn", "vpn") is not None else proxy.get("is_vpn")),
        is_tor=boolean(first(raw, "is_tor", "tor") if first(raw, "is_tor", "tor") is not None else proxy.get("is_tor")),
        is_hosting=boolean(first(raw, "is_datacenter", "datacenter", "is_hosting") if first(raw, "is_datacenter", "datacenter", "is_hosting") is not None else proxy.get("is_datacenter")),
    )
    return {"data": data, "raw": raw, "source_url": f"https://scamalytics.com/ip/{ip}"}


def lookup_abuseipdb(ip: str, timeout: float) -> Dict[str, Any]:
    url = with_query("https://api.abuseipdb.com/api/v2/check", {"ipAddress": ip, "maxAgeInDays": 90, "verbose": "true"})
    raw = request_json(url, timeout, {"Key": os.environ["ABUSEIPDB_API_KEY"], "Accept": "application/json"})
    item = raw.get("data") if isinstance(raw.get("data"), Mapping) else {}
    if item.get("ipAddress") != ip:
        raise LookupError("AbuseIPDB response did not echo the target IP")
    data = clean_data(
        country_code=item.get("countryCode"), isp=item.get("isp"), organization=item.get("domain"),
        network_type=item.get("usageType"), risk_score=number(item.get("abuseConfidenceScore")),
        is_abuser=True if (number(item.get("abuseConfidenceScore")) or 0) >= 50 else False,
        total_reports=item.get("totalReports"), distinct_users=item.get("numDistinctUsers"),
        last_reported_at=item.get("lastReportedAt"), is_whitelisted=boolean(item.get("isWhitelisted")),
        is_tor=boolean(item.get("isTor")),
    )
    return {"data": data, "raw": raw, "source_url": f"https://www.abuseipdb.com/check/{ip}"}


PROVIDERS: Tuple[Provider, ...] = (
    Provider("ip-api", "IP-API", "geo-risk", lookup_ip_api),
    Provider("geojs", "GeoJS", "geo", lookup_geojs),
    Provider("rdap", "RDAP.org", "registry", lookup_rdap),
    Provider("ripestat", "RIPEstat", "routing", lookup_ripestat),
    Provider("ipapi-is", "ipapi.is", "risk-network", lookup_ipapi_is),
    Provider("proxycheck", "proxycheck.io", "risk", lookup_proxycheck),
    Provider("ping0", "Ping0.cc", "risk-network", lookup_ping0, experimental=True),
    Provider("ipinfo", "IPinfo", "geo-network-risk", lookup_ipinfo, ("IPINFO_TOKEN",)),
    Provider("scamalytics", "Scamalytics", "risk", lookup_scamalytics,
             ("SCAMALYTICS_API_URL", "SCAMALYTICS_API_KEY")),
    Provider("ipqs", "IPQualityScore", "risk", lookup_ipqs, ("IPQS_API_KEY",)),
    Provider("ipdata", "ipdata", "geo-network-risk", lookup_ipdata, ("IPDATA_API_KEY",)),
    Provider("abuseipdb", "AbuseIPDB", "abuse", lookup_abuseipdb, ("ABUSEIPDB_API_KEY",)),
)


def run_provider(provider: Provider, ip: str, timeout: float) -> ProviderResult:
    if provider.credential_env and not provider.configured():
        missing = [name for name in provider.credential_env if not os.environ.get(name, "").strip()]
        return ProviderResult(provider.id, provider.name, provider.category, "skipped",
                              message=f"Missing credentials: {', '.join(missing)}",
                              experimental=provider.experimental)
    started = time.monotonic()
    try:
        response = provider.lookup(ip, timeout)
        elapsed = round((time.monotonic() - started) * 1000)
        data = response.get("data", {})
        if not isinstance(data, dict) or not data:
            raise LookupError("Provider returned no usable fields")
        return ProviderResult(provider.id, provider.name, provider.category, "success", elapsed,
                              response.get("source_url"), data, response.get("raw"),
                              experimental=provider.experimental)
    except (LookupError, urllib.error.URLError, urllib.error.HTTPError, TimeoutError,
            json.JSONDecodeError, OSError, ValueError) as exc:
        elapsed = round((time.monotonic() - started) * 1000)
        status = "unavailable" if provider.experimental else "error"
        return ProviderResult(provider.id, provider.name, provider.category, status, elapsed,
                              message=safe_error(exc), experimental=provider.experimental)
    except Exception as exc:  # isolate unexpected adapter failures without hiding their class
        elapsed = round((time.monotonic() - started) * 1000)
        return ProviderResult(provider.id, provider.name, provider.category, "error", elapsed,
                              message=f"Unexpected {exc.__class__.__name__}: {safe_error(exc)}",
                              experimental=provider.experimental)


def normalized_key(field: str, value: Any) -> str:
    text = str(value).strip()
    if field in ("country_code", "asn"):
        return text.upper()
    return re.sub(r"\s+", " ", text).casefold()


def compatible_fact(field: str, left: Any, right: Any) -> bool:
    if field not in ("city", "region", "organization", "isp"):
        return False
    a, b = normalized_key(field, left), normalized_key(field, right)
    # Parenthetical locality qualifiers and legal suffix/detail frequently vary
    # without representing a real contradiction.
    base_a = re.sub(r"\s*[（(][^）)]*[）)]\s*$", "", a).strip()
    base_b = re.sub(r"\s*[（(][^）)]*[）)]\s*$", "", b).strip()
    return bool(base_a and base_b and (base_a == base_b or base_a in base_b or base_b in base_a))


def fuse_facts(results: Sequence[ProviderResult]) -> Dict[str, Any]:
    fused: Dict[str, Any] = {}
    for field_name in FACT_FIELDS:
        groups: Dict[str, Dict[str, Any]] = {}
        for result in results:
            if result.status != "success" or compact(result.data.get(field_name)) is None:
                continue
            value = result.data[field_name]
            key = normalized_key(field_name, value)
            for existing_key, existing in groups.items():
                if compatible_fact(field_name, existing["value"], value):
                    key = existing_key
                    break
            group = groups.setdefault(key, {"value": value, "sources": []})
            group["sources"].append(result.id)
        if not groups:
            continue
        ranked = sorted(groups.values(), key=lambda item: (-len(item["sources"]), str(item["value"])))
        top_count = len(ranked[0]["sources"])
        tied = len(ranked) > 1 and len(ranked[1]["sources"]) == top_count
        fused[field_name] = {
            "value": ranked[0]["value"], "sources": ranked[0]["sources"],
            "status": "consensus" if top_count >= 2 and not tied else ("disputed" if len(ranked) > 1 else "single-source"),
            "alternatives": ranked[1:],
        }
    return fused


def provider_risk_estimate(result: ProviderResult) -> Optional[Dict[str, Any]]:
    if result.status != "success" or result.id not in RISK_WEIGHTS:
        return None
    data = result.data
    score = number(first(data, "risk_score", "abuse_score"))
    if score is None:
        return None
    derived_from_trust = result.id == "ipdata" and number(data.get("trust_score")) is not None
    score_origin = "derived-from-trust-score" if derived_from_trust else "native"
    weight = RISK_WEIGHTS[result.id]
    if result.collection_method == "browser-public-page":
        weight *= 0.90
    return {"provider": result.id, "score": round(score, 1), "weight": round(weight, 3),
            "score_origin": score_origin,
            "reasons": ["100 - trust score"] if derived_from_trust else ["native score"]}


def fuse_unscored_signals(results: Sequence[ProviderResult]) -> List[Dict[str, Any]]:
    signal_fields = ("is_abuser", "recent_abuse", "is_bot")
    signals: List[Dict[str, Any]] = []
    for field_name in signal_fields:
        positive, negative = [], []
        for result in results:
            if result.status != "success":
                continue
            value = result.data.get(field_name)
            if value is True:
                positive.append(result.id)
            elif value is False:
                negative.append(result.id)
        if not positive:
            continue
        state = "disputed" if negative else ("corroborated" if len(positive) >= 2 else "single-source")
        signals.append({
            "signal": field_name.removeprefix("is_"),
            "positive_sources": positive,
            "negative_sources": negative,
            "state": state,
        })
    return signals


def score_level(score: Optional[float]) -> str:
    if score is None:
        return "unknown"
    for ceiling, level in LEVELS:
        if score < ceiling:
            return level
    return "critical"


def fuse_risk(results: Sequence[ProviderResult]) -> Dict[str, Any]:
    estimates = [estimate for result in results if (estimate := provider_risk_estimate(result))]
    rank = {provider_id: index for index, provider_id in enumerate(RISK_PROVIDER_ORDER)}
    estimates.sort(key=lambda item: rank.get(item["provider"], len(rank)))
    unscored_signals = fuse_unscored_signals(results)
    if not estimates:
        return {"score": None, "level": "unknown", "confidence": "none", "estimates": [],
                "unscored_signals": unscored_signals,
                "summary": "No usable risk estimate was returned; absence of evidence is not low risk."}
    weighted = sum(item["score"] * item["weight"] for item in estimates) / sum(item["weight"] for item in estimates)
    high_count = sum(1 for item in estimates if item["score"] >= 70)
    uplift = 15 if high_count >= 3 else (8 if high_count == 2 else 0)
    score = round(min(100.0, weighted + uplift), 1)
    spread = statistics.pstdev([item["score"] for item in estimates]) if len(estimates) > 1 else 0.0
    if len(estimates) == 1:
        confidence = "low"
    elif len(estimates) == 2:
        confidence = "low" if spread > 30 else "medium"
    else:
        confidence = "high" if spread <= 20 else ("medium" if spread <= 35 else "low")
    level = score_level(score)
    summary = (f"{level.title()} risk ({score}/100) from {len(estimates)} independent risk source(s); "
               f"confidence is {confidence}.")
    return {"score": score, "level": level, "confidence": confidence, "spread": round(spread, 1),
            "corroboration_uplift": uplift, "estimates": estimates,
            "unscored_signals": unscored_signals, "summary": summary}


def fuse_exposure(results: Sequence[ProviderResult]) -> Dict[str, Any]:
    indicators = {flag: {"positive": [], "negative": []}
                  for flag in ("is_proxy", "is_vpn", "is_tor", "is_hosting", "is_bot")}
    for result in results:
        if result.status != "success":
            continue
        for flag in indicators:
            value = result.data.get(flag)
            if value is True:
                indicators[flag]["positive"].append(result.id)
            elif value is False:
                indicators[flag]["negative"].append(result.id)
    indicators = {key: value for key, value in indicators.items()
                  if value["positive"] or value["negative"]}
    confirmed = [flag for flag, sources in indicators.items()
                 if sources["positive"] and not sources["negative"]]
    disputed = [flag for flag, sources in indicators.items()
                if sources["positive"] and sources["negative"]]
    severe = any(flag in confirmed for flag in ("is_tor", "is_proxy"))
    level = "high" if severe and len(confirmed) >= 2 else (
        "elevated" if severe or len(confirmed) >= 2 else
        ("notable" if confirmed else ("uncertain" if disputed else "none-detected"))
    )
    if not indicators:
        level = "unknown"
    return {
        "level": level,
        "positive_indicators": [flag.removeprefix("is_") for flag in confirmed],
        "disputed_indicators": [flag.removeprefix("is_") for flag in disputed],
        "indicators": indicators,
        "summary": ("No network-trait evidence was returned." if level == "unknown" else
                    ("No proxy, VPN, Tor, hosting, or bot trait was detected by reporting sources."
                     if not confirmed and not disputed else
                     "; ".join(part for part in (
                         (f"Detected contextual traits: {', '.join(flag.removeprefix('is_') for flag in confirmed)}"
                          if confirmed else ""),
                         (f"Disputed traits: {', '.join(flag.removeprefix('is_') for flag in disputed)}"
                          if disputed else ""),
                     ) if part) + ".")),
    }


def find_conflicts(facts: Mapping[str, Any], results: Sequence[ProviderResult]) -> List[str]:
    conflicts = []
    for field_name, item in facts.items():
        if item.get("status") == "disputed":
            values = [f"{item['value']} ({', '.join(item['sources'])})"]
            values.extend(f"{alt['value']} ({', '.join(alt['sources'])})" for alt in item.get("alternatives", []))
            conflicts.append(f"{field_name}: " + " vs ".join(values))
    estimates = [item for result in results if (item := provider_risk_estimate(result))]
    if len(estimates) >= 2:
        scores = [item["score"] for item in estimates]
        if max(scores) - min(scores) >= 40:
            conflicts.append("risk scores diverge by at least 40 points across providers")
    for signal in fuse_unscored_signals(results):
        sources = ", ".join(signal["positive_sources"])
        suffix = (f"; contradicted by {', '.join(signal['negative_sources'])}"
                  if signal["negative_sources"] else "; not converted to a numeric score")
        conflicts.append(f"unscored {signal['signal']} signal from {sources}{suffix}")
    return conflicts


def provider_risk_state(result: ProviderResult) -> str:
    """Return a presentation state without treating missing evidence as zero."""
    if provider_risk_estimate(result):
        return "numeric"
    if result.id == "ipqs" and result.status != "success":
        return "public-page-score-unavailable"
    if (result.id == "abuseipdb" and result.status == "skipped"
            and "Missing credentials" in result.message):
        return "credential-required"
    if result.status != "success":
        return result.status
    reputation_booleans = ("is_abuser", "recent_abuse", "is_bot")
    if any(isinstance(result.data.get(field_name), bool) for field_name in reputation_booleans):
        return "boolean-only"
    return "no-numeric-score"


def build_report(ip: str, results: Sequence[ProviderResult], include_raw: bool) -> Dict[str, Any]:
    facts = fuse_facts(results)
    risk = fuse_risk(results)
    counts = {status: sum(1 for result in results if result.status == status)
              for status in ("success", "skipped", "unavailable", "error")}
    return {
        "schema_version": "1.1", "tool_version": VERSION,
        "target": {"ip": ip, "version": ipaddress.ip_address(ip).version},
        "generated_at": utc_now(), "coverage": {"total": len(results), **counts},
        "assessment": {"risk": risk, "network_exposure": fuse_exposure(results),
                       "conflicts": find_conflicts(facts, results),
                       "limitations": [
                           "IP intelligence changes over time; this is a point-in-time assessment.",
                           "Hosting, VPN, or proxy classification is contextual and is not proof of abuse.",
                           "A failed or skipped source provides no negative evidence.",
                       ]},
        "presentation": {
            "risk_provider_order": list(RISK_PROVIDER_ORDER),
            "risk_provider_states": {
                result.id: provider_risk_state(result)
                for result in results if result.id in RISK_PROVIDER_ORDER
            },
            "detail_provider_groups": [
                {"label": label, "providers": list(provider_ids)}
                for label, provider_ids in DETAIL_PROVIDER_GROUPS
            ],
        },
        "facts": facts,
        "sources": [result.as_dict(include_raw) for result in results],
    }


def md_value(value: Any) -> str:
    if value is True:
        return "yes"
    if value is False:
        return "no"
    if isinstance(value, (list, dict)):
        return json.dumps(value, ensure_ascii=False, sort_keys=True)
    return str(value).replace("|", "\\|").replace("\n", " ")


def render_markdown(report: Mapping[str, Any]) -> str:
    target = report["target"]
    coverage = report["coverage"]
    assessment = report["assessment"]
    risk = assessment["risk"]
    exposure = assessment["network_exposure"]
    lines = [
        f"# IP Intelligence Report: {target['ip']}", "",
        f"- Generated: `{report['generated_at']}`",
        f"- IP version: IPv{target['version']}",
        (f"- Sources: {coverage['success']} successful, {coverage['skipped']} skipped, "
         f"{coverage['unavailable']} unavailable, {coverage['error']} failed"), "",
        "## Comprehensive assessment", "",
        f"**Reputation risk: {str(risk['level']).upper()}**",
    ]
    if risk["score"] is not None:
        lines.extend([f"- Fused triage score: **{risk['score']}/100**", f"- Confidence: **{risk['confidence']}**"])
    else:
        lines.append("- Fused triage score: **unknown (insufficient evidence)**")
    lines.append(f"- Summary: {risk['summary']}")
    lines.extend([f"- Network exposure: **{str(exposure['level']).upper()}**",
                  f"- Exposure summary: {exposure['summary']}"])
    if risk.get("estimates"):
        lines.extend(["", "### Risk evidence", "", "| Source | Estimate | Weight | Evidence |", "|---|---:|---:|---|"])
        for item in risk["estimates"]:
            lines.append(f"| {item['provider']} | {item['score']} | {item['weight']:.2f} | {item['score_origin']}: {', '.join(item['reasons'])} |")
    if risk.get("unscored_signals"):
        lines.extend(["", "### Unscored risk signals", "",
                      "| Signal | Positive sources | Negative sources | State |", "|---|---|---|---|"])
        for item in risk["unscored_signals"]:
            lines.append(
                f"| {item['signal']} | {', '.join(item['positive_sources'])} | "
                f"{', '.join(item['negative_sources']) or '-'} | {item['state']} |"
            )
    if exposure.get("indicators"):
        lines.extend(["", "### Network exposure evidence", "",
                      "| Trait | Positive sources | Negative sources |", "|---|---|---|"])
        for flag, evidence in exposure["indicators"].items():
            lines.append(f"| {flag.removeprefix('is_')} | {', '.join(evidence['positive']) or '-'} | {', '.join(evidence['negative']) or '-'} |")
    lines.extend(["", "### Key facts", "", "| Field | Fused value | Status | Supporting sources |", "|---|---|---|---|"])
    for field_name, item in report["facts"].items():
        lines.append(f"| {field_name} | {md_value(item['value'])} | {item['status']} | {', '.join(item['sources'])} |")
        for alt in item.get("alternatives", []):
            lines.append(f"| {field_name} (alternative) | {md_value(alt['value'])} | conflict | {', '.join(alt['sources'])} |")
    if assessment.get("conflicts"):
        lines.extend(["", "### Material conflicts", ""])
        lines.extend(f"- {item}" for item in assessment["conflicts"])
    lines.extend(["", "## Source details", ""])
    for source in report["sources"]:
        label = f"{source['name']} (`{source['id']}`)"
        if source.get("experimental"):
            label += " [experimental]"
        lines.extend([f"### {label}", "", f"- Status: **{source['status']}**", f"- Latency: {source['elapsed_ms']} ms"])
        if source.get("source_url"):
            lines.append(f"- Source page: {source['source_url']}")
        lines.append(f"- Collection: {source.get('collection_method', 'api')}")
        if source.get("observed_at"):
            lines.append(f"- Observed: {source['observed_at']}")
        if source.get("message"):
            lines.append(f"- Note: {source['message']}")
        if source.get("data"):
            lines.extend(["", "| Field | Value |", "|---|---|"])
            for key, value in sorted(source["data"].items()):
                lines.append(f"| {key} | {md_value(value)} |")
        if "raw" in source:
            lines.extend(["", "<details><summary>Raw upstream payload</summary>", "", "```json",
                          json.dumps(source["raw"], ensure_ascii=False, indent=2, sort_keys=True), "```", "", "</details>"])
        lines.append("")
    lines.extend(["## Limitations", ""])
    lines.extend(f"- {item}" for item in assessment["limitations"])
    return "\n".join(lines).rstrip() + "\n"


def render_html(report: Mapping[str, Any], language: str = "en") -> str:
    template_path = Path(__file__).resolve().parents[1] / "assets" / "report-template.html"
    try:
        template = template_path.read_text(encoding="utf-8")
    except OSError as exc:
        raise LookupError(f"Cannot read HTML report template: {safe_error(exc)}") from exc
    payload = json.dumps(report, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
    encoded = base64.b64encode(payload).decode("ascii")
    if "__REPORT_DATA_BASE64__" not in template or "__REPORT_LANGUAGE__" not in template:
        raise LookupError("HTML report template is missing required placeholders")
    return (template.replace("__REPORT_DATA_BASE64__", encoded)
            .replace("__REPORT_LANGUAGE__", language))


def select_providers(include: Optional[str], exclude: Optional[str]) -> List[Provider]:
    by_id = {provider.id: provider for provider in PROVIDERS}
    if include:
        requested = [item.strip() for item in include.split(",") if item.strip()]
        unknown = sorted(set(requested) - set(by_id))
        if unknown:
            raise LookupError(f"Unknown provider(s): {', '.join(unknown)}")
        selected = [by_id[item] for item in requested]
    else:
        selected = list(PROVIDERS)
    if exclude:
        excluded = {item.strip() for item in exclude.split(",") if item.strip()}
        unknown = sorted(excluded - set(by_id))
        if unknown:
            raise LookupError(f"Unknown provider(s): {', '.join(unknown)}")
        selected = [provider for provider in selected if provider.id not in excluded]
    if not selected:
        raise LookupError("No providers selected")
    return selected


def resolve_self_ip(timeout: float) -> str:
    body, _ = request_bytes("https://api64.ipify.org", timeout, {"Accept": "text/plain"})
    return public_ip(body.decode("ascii", "strict").strip())


def lookup(ip: str, providers: Sequence[Provider], timeout: float, include_raw: bool,
           evidence: Optional[Mapping[str, ProviderResult]] = None) -> Dict[str, Any]:
    workers = min(12, max(1, len(providers)))
    result_by_id: Dict[str, ProviderResult] = {}
    with concurrent.futures.ThreadPoolExecutor(max_workers=workers, thread_name_prefix="ipintel") as pool:
        futures = {pool.submit(run_provider, provider, ip, timeout): provider.id for provider in providers}
        for future in concurrent.futures.as_completed(futures):
            result = future.result()
            result_by_id[result.id] = result
    ordered = merge_evidence([result_by_id[provider.id] for provider in providers], evidence or {})
    return build_report(ip, ordered, include_raw)


def list_providers() -> str:
    lines = ["ID\tSTATUS\tCATEGORY\tCREDENTIALS"]
    for provider in PROVIDERS:
        if provider.id in PUBLIC_PAGE_DOMAINS:
            status = "ready" if provider.configured() else "public-page"
        else:
            status = "ready" if provider.configured() else ("missing-key" if provider.credential_env else "ready")
        if provider.experimental:
            status += ",experimental"
        lines.append(f"{provider.id}\t{status}\t{provider.category}\t{','.join(provider.credential_env) or '-'}")
    return "\n".join(lines)


def parser() -> argparse.ArgumentParser:
    argp = argparse.ArgumentParser(description="Fuse multiple IP intelligence sources into an auditable report.")
    argp.add_argument("ip", nargs="?", help="Public IPv4 or IPv6 address")
    argp.add_argument("--self", action="store_true", dest="lookup_self", help="Look up this machine's public IP")
    argp.add_argument("--format", choices=("markdown", "json", "html"), default="markdown")
    argp.add_argument("--output", help="Write the report to this file (UTF-8)")
    argp.add_argument("--report-dir", help="Write JSON and self-contained HTML reports to this directory")
    argp.add_argument("--language", choices=("en", "zh-CN"), default="en", help="HTML report language")
    argp.add_argument("--include-raw", action="store_true", help="Include raw provider payloads")
    argp.add_argument("--evidence", action="append", default=[], metavar="FILE",
                      help="Import validated public-page evidence JSON (repeatable)")
    argp.add_argument("--providers", help="Comma-separated provider IDs to run")
    argp.add_argument("--exclude", help="Comma-separated provider IDs to omit")
    argp.add_argument("--timeout", type=float, default=DEFAULT_TIMEOUT, help="Per-provider timeout in seconds")
    argp.add_argument("--list-providers", action="store_true")
    argp.add_argument("--version", action="version", version=f"%(prog)s {VERSION}")
    return argp


def main(argv: Optional[Sequence[str]] = None) -> int:
    args = parser().parse_args(argv)
    try:
        if args.list_providers:
            print(list_providers())
            return 0
        if args.lookup_self and args.ip:
            raise LookupError("Provide either an IP or --self, not both")
        if not args.lookup_self and not args.ip:
            raise LookupError("Provide a public IP address or use --self")
        if not 1 <= args.timeout <= 60:
            raise LookupError("--timeout must be between 1 and 60 seconds")
        target = resolve_self_ip(args.timeout) if args.lookup_self else public_ip(args.ip)
        selected = select_providers(args.providers, args.exclude)
        evidence = load_public_page_evidence(args.evidence, target) if args.evidence else {}
        report = lookup(target, selected, args.timeout, args.include_raw, evidence)
        # ASCII-safe JSON remains parseable in Windows PowerShell 5, whose
        # default Get-Content encoding is not UTF-8. Markdown keeps native text.
        if args.report_dir:
            report_dir = Path(args.report_dir).expanduser()
            report_dir.mkdir(parents=True, exist_ok=True)
            stem = f"ip-intelligence-{target.replace(':', '-')}"
            json_path = (report_dir / f"{stem}.json").resolve()
            html_path = (report_dir / f"{stem}.html").resolve()
            json_path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
            html_path.write_text(render_html(report, args.language), encoding="utf-8")
            print(json.dumps({"json": str(json_path), "html": str(html_path)}, ensure_ascii=False))
            return 0
        output = (json.dumps(report, ensure_ascii=True, indent=2, sort_keys=False) + "\n"
                  if args.format == "json" else
                  (render_html(report, args.language) if args.format == "html" else render_markdown(report)))
        if args.output:
            path = Path(args.output).expanduser()
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(output, encoding="utf-8")
            print(str(path.resolve()))
        else:
            try:
                sys.stdout.write(output)
            except UnicodeEncodeError:
                sys.stdout.buffer.write(output.encode("utf-8"))
        return 0
    except LookupError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    except KeyboardInterrupt:
        print("error: interrupted", file=sys.stderr)
        return 130


if __name__ == "__main__":
    raise SystemExit(main())
