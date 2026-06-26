from __future__ import annotations

import argparse
import json
import math
import re
import statistics
import sys
import time
import urllib.parse
import urllib.request
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

WORKSPACE = Path(__file__).resolve().parents[3]
UPSTREAM = WORKSPACE / "tmp" / "naverland-scrapper"
SRC_ROOT = UPSTREAM / "src"
if str(UPSTREAM) not in sys.path:
    sys.path.insert(0, str(UPSTREAM))
if str(SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(SRC_ROOT))

UPSTREAM_IMPORT_ERROR: Exception | None = None
try:
    from src.core.parser import NaverURLParser
    from src.core.services.response_capture import normalize_article_payload
    from src.utils.helpers import PriceConverter, get_article_url
except Exception as exc:
    UPSTREAM_IMPORT_ERROR = exc

    class NaverURLParser:
        @staticmethod
        def extract_from_text(text: str) -> list[tuple[str, str]]:
            pairs: list[tuple[str, str]] = []
            for cid in RAW_COMPLEX_ID_RE.findall(text or ""):
                pairs.append(("", cid))
            return pairs

        @staticmethod
        def extract_complex_id(text: str | None) -> str | None:
            match = RAW_COMPLEX_ID_RE.search(text or "")
            return match.group(1) if match else None

        @staticmethod
        def fetch_complex_name(complex_id: str) -> str:
            _raise_missing_upstream()

    class PriceConverter:
        @staticmethod
        def to_int(value: Any) -> int:
            raw = str(value or "").strip()
            if not raw:
                return 0
            digits = re.sub(r"[^0-9]", "", raw)
            return int(digits) if digits else 0

        @staticmethod
        def to_string(value: Any) -> str:
            amount = PriceConverter.to_int(value)
            if amount <= 0:
                return "0"
            eok = amount // 100000000
            rem = amount % 100000000
            man = rem // 10000
            if eok and man:
                return f"{eok}억 {man:,}만"
            if eok:
                return f"{eok}억"
            return f"{man:,}만"

    def get_article_url(complex_id: str, article_id: str, real_estate_type: str = "APT") -> str:
        article = str(article_id or "").strip()
        if not article:
            return ""
        return f"https://new.land.naver.com/articles/{article}?complexNo={complex_id}&realEstateType={real_estate_type}"

    def normalize_article_payload(*args: Any, **kwargs: Any) -> dict[str, Any]:
        _raise_missing_upstream()


def _raise_missing_upstream() -> None:
    detail = f" ({UPSTREAM_IMPORT_ERROR})" if UPSTREAM_IMPORT_ERROR else ""
    raise RuntimeError(
        "필수 upstream clone(tmp/naverland-scrapper)이 없거나 불완전합니다. "
        "이 스킬은 해당 로컬 저장소의 src 패키지에 의존합니다. "
        f"경로를 확인한 뒤 다시 시도해 주세요{detail}"
    )

USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36"
SEARCH_URL = "https://search.naver.com/search.naver?where=nexearch&sm=top_hty&fbm=0&ie=utf8&query={query}"
COMPLEX_DETAIL_URL = "https://new.land.naver.com/api/complexes/{complex_id}?sameAddressGroup=false"
COMPLEX_ARTICLE_URL = (
    "https://new.land.naver.com/api/articles/complex/{complex_id}?"
    "realEstateType=APT%3AVL&tradeType={trade_codes}&tag=%3A%3A%3A%3A%3A%3A%3A%3A"
    "&rentPriceMin=0&rentPriceMax=900000000&priceMin=0&priceMax=900000000"
    "&areaMin=0&areaMax=900000000&oldBuildYears=&recentlyBuildYears=&minHouseHoldCount="
    "&maxHouseHoldCount=&showArticle=false&sameAddressGroup=false&minMaintenanceCost=&maxMaintenanceCost="
    "&priceType=RETAIL&directions=&page={page}&complexNo={complex_id}&buildingNos=&areaNos=&type=list&order=rank"
)
TRADE_CODE_MAP = {"매매": "A1", "전세": "B1", "월세": "B2"}
DEFAULT_QUERY_SUFFIX = " 네이버 부동산 아파트"
DEFAULT_BACKOFFS = [1.2, 2.5, 4.0]
STOPWORDS = [
    "네이버 부동산", "부동산", "시세", "매물", "가격", "가격대", "얼마", "비교", "정리", "요약", "알려줘", "찾아줘",
    "보여줘", "조회", "검색", "추천", "빌라", "오피스텔", "실거래가", "단지", "찾기", "브리핑", "아파트좀",
    "해줘", "해주세요", "알림", "감시", "체크", "체크해줘", "요청", "보고", "리포트", "채팅", "래퍼", "근처",
    "살펴봐", "알아봐", "부탁", "정도", "위주", "기준", "기반", "정도면", "좀", "그리고", "중에서", "해석",
]
TRADE_STOPWORDS = ["매매", "전세", "월세"]
COMPARE_TOKENS = ["비교", "대비", "vs", "VS"]
LOCATION_SUFFIXES = ("특별시", "광역시", "시", "도", "군", "구", "동", "읍", "면", "리", "가")
SIMPLE_KOREAN_TOKEN_RE = re.compile(r"[가-힣A-Za-z0-9]{2,}")
RAW_COMPLEX_ID_RE = re.compile(r"(?:complex(?:\s*id|no)?|단지(?:\s*id)?|id)\s*[:=#-]?\s*(\d{3,10})", re.I)
WATCH_STATE_FILE = WORKSPACE / "skills" / "naver-real-estate-search" / "data" / "watch-rules.json"
CANDIDATE_CACHE_FILE = WORKSPACE / "skills" / "naver-real-estate-search" / "data" / "candidate-cache.json"
DEFAULT_CANDIDATE_SEED_FILE = WORKSPACE / "skills" / "naver-real-estate-search" / "references" / "candidate-seeds.json"
DEFAULT_SEED_INPUT_FILE = WORKSPACE / "skills" / "naver-real-estate-search" / "references" / "seoul-major-complexes.seed-input.json"
APT_SUFFIX_RE = re.compile(r"(?:아파트|맨션|타운하우스|주상복합|오피스텔|빌라)$")
AREA_RANGE_RE = re.compile(r"(\d{1,2})\s*평\s*[~-]\s*(\d{1,2})\s*평")
AREA_BAND_RE = re.compile(r"(\d{1,2})\s*평대")
AREA_SINGLE_RE = re.compile(r"(\d{1,2})\s*평(?:형)?")
NOISE_TOKENS = set(STOPWORDS + TRADE_STOPWORDS + [
    "서울", "경기", "인천", "부산", "대구", "대전", "광주", "울산", "세종", "대한민국", "한국", "수도권"
])
REGION_ALIASES = {
    "서울": ["서울", "서울시", "서울특별시"],
    "부산": ["부산", "부산시", "부산광역시"],
    "인천": ["인천", "인천시", "인천광역시"],
    "대구": ["대구", "대구시", "대구광역시"],
    "광주": ["광주", "광주시", "광주광역시"],
    "대전": ["대전", "대전시", "대전광역시"],
    "울산": ["울산", "울산시", "울산광역시"],
    "세종": ["세종", "세종시", "세종특별자치시"],
    "경기": ["경기", "경기도"],
    "강원": ["강원", "강원도", "강원특별자치도"],
    "충북": ["충북", "충청북도"],
    "충남": ["충남", "충청남도"],
    "전북": ["전북", "전라북도", "전북특별자치도"],
    "전남": ["전남", "전라남도"],
    "경북": ["경북", "경상북도"],
    "경남": ["경남", "경상남도"],
    "제주": ["제주", "제주도", "제주특별자치도"],
}


class SearchError(RuntimeError):
    pass


@dataclass
class ParsedQuery:
    raw_query: str
    cleaned_query: str
    trade_types: list[str]
    min_pyeong: float | None
    max_pyeong: float | None
    compare_mode: bool
    candidate_keywords: list[str]
    location_hints: list[str]
    raw_subjects: list[str]
    direct_complex_ids: list[str]


RATE_LIMIT_STATE = {"active": False, "last_error": None}


def _record_rate_limit(message: str) -> None:
    RATE_LIMIT_STATE["active"] = True
    RATE_LIMIT_STATE["last_error"] = message


def _request_json(url: str, *, referer: str = "https://new.land.naver.com/", backoffs: list[float] | None = None) -> Any:
    backoffs = DEFAULT_BACKOFFS if backoffs is None else backoffs
    req = urllib.request.Request(url)
    req.add_header("User-Agent", USER_AGENT)
    req.add_header("Referer", referer)
    req.add_header("Accept", "application/json, text/plain, */*")
    attempts = len(backoffs) + 1
    for attempt in range(attempts):
        try:
            with urllib.request.urlopen(req, timeout=20) as response:
                RATE_LIMIT_STATE["active"] = False
                return json.loads(response.read().decode("utf-8"))
        except urllib.error.HTTPError as exc:
            body = exc.read().decode("utf-8", errors="ignore")
            if exc.code == 429 and attempt < len(backoffs):
                _record_rate_limit("429")
                time.sleep(backoffs[attempt])
                continue
            if exc.code == 429:
                _record_rate_limit("429")
                raise SearchError(
                    "네이버 부동산 API가 429(요청 제한)를 반환했습니다. 단일 단지 URL/ID를 우선 사용하거나, 후보 단지부터 1~3개로 좁혀 다시 시도해 주세요."
                )
            raise SearchError(f"네이버 부동산 API 호출 실패: HTTP {exc.code} {body[:200]}")
        except Exception as exc:
            raise SearchError(f"네이버 부동산 API 호출 실패: {exc}") from exc
    raise SearchError("네이버 부동산 API 호출 실패")


def _request_text(url: str) -> str:
    req = urllib.request.Request(url)
    req.add_header("User-Agent", USER_AGENT)
    req.add_header("Accept", "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8")
    try:
        with urllib.request.urlopen(req, timeout=20) as response:
            return response.read().decode("utf-8", errors="ignore")
    except urllib.error.HTTPError as exc:
        if exc.code in {403, 429}:
            raise SearchError(f"네이버 검색 HTML 후보 탐색이 차단되었습니다: HTTP {exc.code}")
        raise


def _read_json_file(path: Path, default: Any) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return default


def _write_json_file(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


def _read_candidate_cache() -> dict[str, Any]:
    data = _read_json_file(CANDIDATE_CACHE_FILE, {"version": 3, "updated_at": 0, "entries": []})
    if isinstance(data, list):
        data = {"version": 3, "updated_at": 0, "entries": data}
    data.setdefault("version", 3)
    data.setdefault("updated_at", 0)
    data.setdefault("entries", [])
    return data


def _write_candidate_cache(data: dict[str, Any]) -> None:
    data = dict(data)
    data["updated_at"] = int(time.time())
    _write_json_file(CANDIDATE_CACHE_FILE, data)


def normalize_keyword(text: str) -> str:
    value = str(text or "").strip()
    for token in STOPWORDS + TRADE_STOPWORDS:
        value = value.replace(token, " ")
    value = re.sub(r"\([^)]*\)", " ", value)
    value = AREA_RANGE_RE.sub(" ", value)
    value = AREA_BAND_RE.sub(" ", value)
    value = AREA_SINGLE_RE.sub(" ", value)
    value = re.sub(r"[?!.]", " ", value)
    value = re.sub(r"\s+", " ", value).strip(" ,/")
    return value


def normalize_complex_alias(text: str) -> str:
    value = normalize_keyword(text)
    value = APT_SUFFIX_RE.sub("", value.strip())
    value = re.sub(r"\s+", "", value)
    return value.strip()


def expand_region_aliases(value: str) -> list[str]:
    out: list[str] = []
    for canonical, aliases in REGION_ALIASES.items():
        if value in aliases or canonical == value:
            for alias in aliases + [canonical]:
                if alias not in out:
                    out.append(alias)
    return out


def expand_alias_variants(text: str) -> list[str]:
    raw = str(text or "").strip()
    normalized = normalize_complex_alias(raw)
    spaced = normalize_keyword(raw)
    variants: list[str] = []
    for value in [raw, spaced, normalized]:
        value = str(value or "").strip()
        if value and value not in variants:
            variants.append(value)
    if normalized:
        for suffix in ["아파트", "", "단지"]:
            value = f"{normalized}{suffix}" if suffix else normalized
            if value and value not in variants:
                variants.append(value)
    for token in list(variants):
        for alias in expand_region_aliases(token):
            if alias not in variants:
                variants.append(alias)
    return variants[:12]


def parse_trade_types(query: str) -> list[str]:
    hits = [trade for trade in ["매매", "전세", "월세"] if trade in query]
    return hits or ["전세"]


def parse_pyeong_range(query: str) -> tuple[float | None, float | None]:
    m = AREA_BAND_RE.search(query)
    if m:
        base = float(m.group(1))
        return max(0.0, base - 3), base + 3
    m = AREA_RANGE_RE.search(query)
    if m:
        return float(m.group(1)), float(m.group(2))
    single = AREA_SINGLE_RE.search(query)
    if single:
        base = float(single.group(1))
        return max(0.0, base - 1), base + 1
    return None, None


def _looks_like_location(token: str) -> bool:
    return any(token.endswith(suffix) for suffix in LOCATION_SUFFIXES) or token in REGION_ALIASES


def extract_location_hints(query: str) -> list[str]:
    seen: set[str] = set()
    results: list[str] = []
    spaced = normalize_keyword(query)
    for token in re.split(r"\s+", spaced):
        token = token.strip()
        if len(token) < 2 or token in NOISE_TOKENS:
            continue
        if _looks_like_location(token):
            for alias in [token, *expand_region_aliases(token)]:
                if alias not in seen:
                    results.append(alias)
                    seen.add(alias)
    for token in SIMPLE_KOREAN_TOKEN_RE.findall(spaced):
        if token in NOISE_TOKENS or len(token) < 2:
            continue
        if token.endswith("동") or token.endswith("구") or token.endswith("시") or token in {"잠실", "대치", "반포", "신월", "목동", "상계", "중계"}:
            if token not in seen:
                results.append(token)
                seen.add(token)
    return results[:8]


def split_query_subjects(query: str) -> list[str]:
    cleaned = normalize_keyword(query)
    if not cleaned:
        return []
    parts = [part.strip() for part in re.split(r"\s*(?:,|/|\||vs\.?|대비|와|과|랑|및)\s*", cleaned) if part.strip()]
    return parts[:6]


def split_candidate_keywords(query: str) -> list[str]:
    uniq: list[str] = []
    seen: set[str] = set()
    global_locations = extract_location_hints(query)
    removable_locations = list(global_locations)
    for location in list(global_locations):
        removable_locations.extend(expand_region_aliases(location))
    removable_locations.extend(["서울", "서울시", "서울특별시", "경기", "경기도"])
    for part in split_query_subjects(query):
        value = part.strip()
        for location in removable_locations:
            value = value.replace(location, " ")
        value = normalize_keyword(value)
        for variant in expand_alias_variants(value):
            norm = normalize_complex_alias(variant)
            if norm and norm not in seen:
                uniq.append(variant)
                seen.add(norm)
    return uniq[:10]


def extract_direct_complex_ids(text: str) -> list[str]:
    direct_complex_ids: list[str] = []
    seen: set[str] = set()
    for _, cid in NaverURLParser.extract_from_text(text or ""):
        if cid and cid not in seen:
            direct_complex_ids.append(cid)
            seen.add(cid)
    for match in RAW_COMPLEX_ID_RE.finditer(text or ""):
        cid = match.group(1)
        if cid and cid not in seen:
            direct_complex_ids.append(cid)
            seen.add(cid)
    text_clean = str(text or "").strip()
    if re.fullmatch(r"\d{3,10}", text_clean) and text_clean not in seen:
        direct_complex_ids.append(text_clean)
    return direct_complex_ids


def build_direct_lookup_payload(query: str | None, complex_id: str | None, url: str | None) -> dict[str, Any]:
    parts = [str(x or "") for x in [query, complex_id, url] if str(x or "").strip()]
    direct_ids = extract_direct_complex_ids("\n".join(parts))
    chosen = str(complex_id or "").strip() or (NaverURLParser.extract_complex_id(url) if url else None) or (direct_ids[0] if direct_ids else None)
    return {
        "query": query,
        "explicit_complex_id": complex_id,
        "explicit_url": url,
        "detected_complex_ids": direct_ids,
        "selected_complex_id": chosen,
        "canonical_complex_url": f"https://new.land.naver.com/complexes/{chosen}" if chosen else None,
    }


def parse_natural_query(query: str) -> ParsedQuery:
    min_pyeong, max_pyeong = parse_pyeong_range(query)
    subject_parts = split_query_subjects(query)
    location_hints = extract_location_hints(query)
    candidate_keywords = split_candidate_keywords(query)
    compare_mode = any(token in query for token in COMPARE_TOKENS) or len(subject_parts) >= 2
    cleaned_query = normalize_keyword(query)
    direct_complex_ids = extract_direct_complex_ids(query)
    return ParsedQuery(
        raw_query=query,
        cleaned_query=cleaned_query,
        trade_types=parse_trade_types(query),
        min_pyeong=min_pyeong,
        max_pyeong=max_pyeong,
        compare_mode=compare_mode,
        candidate_keywords=candidate_keywords or ([cleaned_query] if cleaned_query else []),
        location_hints=location_hints,
        raw_subjects=subject_parts,
        direct_complex_ids=direct_complex_ids,
    )


def extract_complex_candidates_from_web(query: str, limit: int = 5) -> list[dict[str, str]]:
    html = _request_text(SEARCH_URL.format(query=urllib.parse.quote(query + DEFAULT_QUERY_SUFFIX)))
    ids: list[str] = []
    seen: set[str] = set()
    patterns = [
        r"https://new\.land\.naver\.com/complexes/(\d+)",
        r"https://new\.land\.naver\.com/houses/(\d+)",
        r"complexNo=(\d+)",
    ]
    for pattern in patterns:
        for match in re.finditer(pattern, html):
            cid = match.group(1)
            if cid not in seen:
                ids.append(cid)
                seen.add(cid)
            if len(ids) >= limit:
                break
        if len(ids) >= limit:
            break
    return [{"complex_id": cid, "source": "web-search", "query": query} for cid in ids]


def fetch_complex_info(complex_id: str) -> dict[str, Any]:
    payload = _request_json(COMPLEX_DETAIL_URL.format(complex_id=complex_id))
    info = payload.get("complexDetail") or payload
    address = " ".join(filter(None, [str(info.get("cortarAddress") or "").strip(), str(info.get("roadAddressPrefix") or "").strip()])).strip()
    result = {
        "complex_id": complex_id,
        "name": str(info.get("complexName") or info.get("complexNm") or f"단지_{complex_id}"),
        "address": address,
        "household_count": info.get("totalHouseHoldCount") or info.get("houseHoldCount"),
        "complex_url": f"https://new.land.naver.com/complexes/{complex_id}",
    }
    remember_candidate(result)
    return result


def _tokenize_for_match(text: str) -> list[str]:
    normalized = normalize_keyword(text)
    return [token for token in re.split(r"\s+", normalized) if token and len(token) >= 2]


def _score_candidate(info: dict[str, Any], keyword: str, parsed: ParsedQuery | None) -> int:
    score = 0
    name = str(info.get("name") or "")
    address = str(info.get("address") or "")
    haystack = f"{name} {address}"
    normalized_name = normalize_complex_alias(name)
    normalized_keyword = normalize_complex_alias(keyword)
    query_alias = normalize_complex_alias(parsed.cleaned_query if parsed else keyword)
    keyword_tokens = _tokenize_for_match(keyword)
    query_tokens = _tokenize_for_match(parsed.cleaned_query if parsed else keyword)

    if normalized_keyword and normalized_keyword == normalized_name:
        score += 260
    elif normalized_keyword and normalized_keyword in normalized_name:
        score += 130
    if query_alias and query_alias == normalized_name:
        score += 180
    elif query_alias and query_alias in normalized_name:
        score += 85

    for token in keyword_tokens:
        if token == name:
            score += 120
        elif token in name:
            score += 55
        elif token in address:
            score += 22
        elif token in haystack:
            score += 10

    for token in query_tokens:
        if token in name:
            score += 14
        elif token in address:
            score += 8

    for alias in info.get("aliases") or []:
        alias_norm = normalize_complex_alias(alias)
        if query_alias and alias_norm == query_alias:
            score += 170
        elif query_alias and query_alias in alias_norm:
            score += 70
        if normalized_keyword and alias_norm == normalized_keyword:
            score += 140

    if parsed:
        for location in parsed.location_hints:
            if location and location in address:
                score += 32
            elif location and location in name:
                score += 16
        if parsed.raw_subjects:
            own = normalize_complex_alias(parsed.raw_subjects[0])
            if own and own == normalized_name:
                score += 50

    try:
        household_count = int(info.get("household_count") or 0)
    except Exception:
        household_count = 0
    if household_count >= 300:
        score += 4
    if household_count >= 800:
        score += 4
    if household_count >= 2000:
        score += 3
    return score


def remember_candidate(info: dict[str, Any], aliases: list[str] | None = None) -> dict[str, Any]:
    complex_id = str(info.get("complex_id") or "").strip()
    if not complex_id:
        return {}
    cache = _read_candidate_cache()
    entries = cache.get("entries") or []
    by_id = {str(row.get("complex_id") or ""): dict(row) for row in entries if row.get("complex_id")}
    row = by_id.get(complex_id, {})
    merged_aliases: list[str] = []
    for value in [row.get("name"), *(row.get("aliases") or []), info.get("name"), *(aliases or [])]:
        for variant in expand_alias_variants(str(value or "")):
            if variant and variant not in merged_aliases:
                merged_aliases.append(variant)
    note_items = [str(x).strip() for x in [row.get("note"), info.get("note")] if str(x or "").strip()]
    row.update(
        {
            "complex_id": complex_id,
            "name": str(info.get("name") or row.get("name") or f"단지_{complex_id}"),
            "address": str(info.get("address") or row.get("address") or ""),
            "household_count": info.get("household_count") or row.get("household_count"),
            "aliases": merged_aliases[:30],
            "updated_at": int(time.time()),
            "source": info.get("source") or row.get("source") or "runtime",
            "learned_from": info.get("learned_from") or row.get("learned_from"),
            "note": note_items[-1] if note_items else None,
        }
    )
    by_id[complex_id] = row
    rows = sorted(by_id.values(), key=lambda x: (-int(x.get("updated_at") or 0), str(x.get("name") or "")))
    cache["entries"] = rows[:500]
    _write_candidate_cache(cache)
    return row


def list_candidate_cache(*, limit: int = 50, keyword: str | None = None) -> list[dict[str, Any]]:
    rows = _read_candidate_cache().get("entries") or []
    if keyword:
        term = normalize_complex_alias(keyword)
        rows = [
            row for row in rows
            if term in normalize_complex_alias(row.get("name") or "")
            or any(term in normalize_complex_alias(alias) for alias in (row.get("aliases") or []))
            or term in normalize_complex_alias(row.get("address") or "")
        ]
    rows = sorted(rows, key=lambda row: (-int(row.get("updated_at") or 0), str(row.get("name") or "")))
    return rows[: max(1, limit)]


def seed_candidate_cache(entries: list[dict[str, Any]], *, source: str = "seed-file") -> list[dict[str, Any]]:
    saved: list[dict[str, Any]] = []
    for item in entries:
        complex_id = str(item.get("complex_id") or "").strip()
        if not complex_id:
            continue
        info = {
            "complex_id": complex_id,
            "name": item.get("name"),
            "address": item.get("address"),
            "household_count": item.get("household_count"),
            "source": item.get("source") or source,
            "learned_from": item.get("learned_from") or source,
            "note": item.get("note"),
        }
        saved.append(remember_candidate(info, aliases=[str(x) for x in (item.get("aliases") or []) if str(x).strip()]))
    return [row for row in saved if row]


def seed_candidate_from_file(path: str | Path | None = None) -> dict[str, Any]:
    target = Path(path) if path else DEFAULT_CANDIDATE_SEED_FILE
    payload = _read_json_file(target, {"entries": []})
    entries = payload.get("entries") if isinstance(payload, dict) else payload
    saved = seed_candidate_cache(entries or [], source=f"seed-file:{target.name}")
    return {"path": str(target), "saved_count": len(saved), "saved": saved}


def _load_reference_seed_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    target = _read_json_file(DEFAULT_CANDIDATE_SEED_FILE, {"entries": [], "manual_review_queue": []})
    if isinstance(target, dict):
        for row in target.get("entries") or []:
            rows.append({**row, "reference_kind": "production-entry"})
        for row in target.get("manual_review_queue") or []:
            rows.append({**row, "reference_kind": "manual-review"})
    seed_input = _read_json_file(DEFAULT_SEED_INPUT_FILE, {"seeds": []})
    if isinstance(seed_input, dict):
        for row in seed_input.get("seeds") or []:
            rows.append({**row, "reference_kind": "seed-input"})
    return rows


def search_reference_candidates(query: str, *, candidate_limit: int = 5, parsed: ParsedQuery | None = None) -> list[dict[str, Any]]:
    parsed = parsed or parse_natural_query(query)
    terms: list[str] = []
    for value in [query, parsed.cleaned_query, *parsed.candidate_keywords, *parsed.raw_subjects]:
        for variant in expand_alias_variants(value):
            norm = normalize_complex_alias(variant)
            if norm and norm not in terms:
                terms.append(norm)
    if not terms:
        return []

    scored: list[dict[str, Any]] = []
    seen_keys: set[str] = set()
    for row in _load_reference_seed_rows():
        name = str(row.get("name") or "").strip()
        if not name:
            continue
        aliases = [str(x) for x in (row.get("aliases") or []) if str(x).strip()]
        bag = [name, *aliases, row.get("district") or "", row.get("neighborhood") or "", row.get("address") or ""]
        bag_norms = [normalize_complex_alias(x) for x in bag if str(x or "").strip()]
        local_score = 0
        for term in terms:
            if term in bag_norms:
                local_score = max(local_score, 240)
            elif any(term and term in norm for norm in bag_norms):
                local_score = max(local_score, 170)
        if local_score <= 0:
            continue
        key = str(row.get("complex_id") or f"hint:{normalize_complex_alias(name)}:{row.get('reference_kind')}")
        if key in seen_keys:
            continue
        seen_keys.add(key)
        reference_score = local_score + _score_candidate(
            {
                "name": name,
                "address": row.get("address") or " ".join(filter(None, [row.get("district"), row.get("neighborhood")])),
                "household_count": row.get("household_count"),
                "aliases": aliases,
            },
            query,
            parsed,
        )
        cid = str(row.get("complex_id") or "")
        scored.append(
            {
                "complex_id": cid,
                "name": name,
                "address": row.get("address") or " ".join(filter(None, [row.get("district"), row.get("neighborhood")])),
                "household_count": row.get("household_count"),
                "aliases": aliases[:20],
                "match_score": reference_score,
                "source_term": row.get("reference_kind") or "reference-seed",
                "source": "reference-seed",
                "reference_kind": row.get("reference_kind"),
                "review_status": row.get("review_status"),
                "verification_status": row.get("verification_status"),
                "next_action": row.get("next_action"),
                "note": row.get("note") or row.get("reason"),
                "complex_url": f"https://new.land.naver.com/complexes/{cid}" if cid else None,
            }
        )
    scored.sort(key=lambda row: (-int(row.get("match_score") or 0), str(row.get("name") or ""), str(row.get("complex_id") or "")))
    return scored[:candidate_limit]


def search_cached_candidates(query: str, *, candidate_limit: int = 5, parsed: ParsedQuery | None = None) -> list[dict[str, Any]]:
    parsed = parsed or parse_natural_query(query)
    cache = _read_candidate_cache().get("entries") or []
    if not cache:
        return []
    terms: list[str] = []
    for value in [query, parsed.cleaned_query, *parsed.candidate_keywords, *parsed.location_hints]:
        for variant in expand_alias_variants(value):
            norm = normalize_complex_alias(variant)
            if norm and norm not in terms:
                terms.append(norm)
    scored: list[dict[str, Any]] = []
    for row in cache:
        aliases = row.get("aliases") or []
        alias_norms = [normalize_complex_alias(x) for x in aliases if x]
        alias_norms = [x for x in alias_norms if x]
        local_score = 0
        for term in terms:
            if term in alias_norms:
                local_score = max(local_score, 300)
            elif any(term in alias for alias in alias_norms):
                local_score = max(local_score, 210)
        if local_score <= 0:
            continue
        score = local_score + _score_candidate({**row, "aliases": aliases}, query, parsed)
        cid = str(row.get("complex_id") or "")
        scored.append({**row, "aliases": aliases, "match_score": score, "source_term": "candidate-cache", "source": "candidate-cache", "complex_url": f"https://new.land.naver.com/complexes/{cid}" if cid else None})
    scored.sort(key=lambda row: (-int(row.get("match_score") or 0), str(row.get("name") or ""), str(row.get("complex_id") or "")))
    return scored[:candidate_limit]


def build_search_terms(parsed: ParsedQuery) -> list[str]:
    terms: list[str] = []
    raw_values = [*parsed.raw_subjects, parsed.cleaned_query, *parsed.candidate_keywords, *parsed.location_hints]
    for value in raw_values:
        for variant in expand_alias_variants(value):
            variant = str(variant or "").strip()
            if variant and variant not in terms:
                terms.append(variant)
    if parsed.location_hints and parsed.candidate_keywords:
        for loc in parsed.location_hints[:3]:
            for kw in parsed.candidate_keywords[:3]:
                combo = f"{loc} {kw}".strip()
                if combo and combo not in terms:
                    terms.append(combo)
    return terms[:16]


def resolve_complex_ids(query: str | None, complex_id: str | None, url: str | None, *, candidate_limit: int = 5) -> list[str]:
    results: list[str] = []
    seen: set[str] = set()

    def _push(value: str | None):
        if value and value not in seen:
            results.append(value)
            seen.add(value)

    _push(complex_id)
    if url:
        _push(NaverURLParser.extract_complex_id(url))
    if query:
        parsed = parse_natural_query(query)
        for cid in parsed.direct_complex_ids:
            _push(cid)
        if not results:
            for item in search_cached_candidates(query, candidate_limit=max(candidate_limit * 2, 6), parsed=parsed):
                _push(item.get("complex_id"))
                if len(results) >= candidate_limit:
                    break
        if not results:
            for item in search_complex_candidates(query, candidate_limit=max(candidate_limit * 2, 6)):
                _push(item.get("complex_id"))
                if len(results) >= candidate_limit:
                    break
    return results[:candidate_limit]


def search_complex_candidates(query: str, *, candidate_limit: int = 5) -> list[dict[str, Any]]:
    parsed = parse_natural_query(query)
    merged: dict[str, dict[str, Any]] = {}

    def _merge_item(item: dict[str, Any]) -> None:
        key = str(item.get("complex_id") or "").strip() or f"hint:{normalize_complex_alias(item.get('name') or '')}:{item.get('source') or item.get('reference_kind') or 'unknown'}"
        prev = merged.get(key)
        if not prev or int(item.get("match_score") or 0) >= int(prev.get("match_score") or 0):
            merged[key] = dict(item)

    for item in search_cached_candidates(query, candidate_limit=max(candidate_limit * 2, 8), parsed=parsed):
        _merge_item(item)
    for item in search_reference_candidates(query, candidate_limit=max(candidate_limit * 2, 8), parsed=parsed):
        _merge_item(item)

    raw_ids: list[tuple[str, str]] = []
    seen_ids: set[str] = {str(row.get("complex_id") or "") for row in merged.values() if str(row.get("complex_id") or "").strip()}
    for term in build_search_terms(parsed):
        try:
            web_items = extract_complex_candidates_from_web(term, limit=max(candidate_limit * 2, 8))
        except SearchError:
            web_items = []
        for item in web_items:
            cid = str(item.get("complex_id") or "").strip()
            if cid and cid not in seen_ids:
                raw_ids.append((cid, term))
                seen_ids.add(cid)

    for cid, source_term in raw_ids:
        try:
            info = fetch_complex_info(cid)
        except Exception as exc:
            info = {"complex_id": cid, "name": f"단지_{cid}", "address": "", "error": str(exc), "source": "web-search-fallback"}
        score = _score_candidate(info, source_term, parsed)
        merged[cid] = {**info, "match_score": score, "source_term": source_term, "source": info.get("source") or "web-search", "complex_url": f"https://new.land.naver.com/complexes/{cid}"}

    scored = list(merged.values())
    scored.sort(key=lambda row: (-int(row.get("match_score") or 0), str(row.get("name") or ""), str(row.get("complex_id") or "")))
    return scored[:candidate_limit]


def fetch_articles(complex_id: str, trade_types: list[str], pages: int = 1) -> list[dict[str, Any]]:
    trade_codes = ":".join(TRADE_CODE_MAP[t] for t in trade_types if t in TRADE_CODE_MAP)
    if not trade_codes:
        trade_codes = "A1:B1:B2"
    complex_name = NaverURLParser.fetch_complex_name(complex_id)
    items: list[dict[str, Any]] = []
    for page in range(1, pages + 1):
        payload = _request_json(COMPLEX_ARTICLE_URL.format(complex_id=complex_id, trade_codes=trade_codes, page=page))
        article_list = payload.get("articleList") or payload.get("list") or []
        if not article_list:
            break
        for article in article_list:
            trade_type = str(article.get("tradeTypeName") or article.get("tradTpNm") or "").strip()
            normalized = normalize_article_payload(article, complex_name, complex_id, requested_trade_type=trade_type)
            normalized["매물URL"] = get_article_url(complex_id, normalized.get("매물ID", ""), normalized.get("자산유형", "APT"))
            normalized["complex_id"] = complex_id
            normalized["article_key"] = f"{complex_id}:{normalized.get('매물ID', '')}"
            items.append(normalized)
    return items


def filter_items(items: list[dict[str, Any]], min_pyeong: float | None, max_pyeong: float | None, limit: int) -> list[dict[str, Any]]:
    filtered = []
    for item in items:
        area = float(item.get("면적(평)") or 0)
        if min_pyeong is not None and area < min_pyeong:
            continue
        if max_pyeong is not None and area > max_pyeong:
            continue
        filtered.append(item)
    filtered.sort(key=lambda row: (row.get("거래유형", ""), PriceConverter.to_int(row.get("매매가") or row.get("보증금") or "0"), row.get("면적(평)", 0)))
    return filtered[:limit]


def _bucket_area(value: float | int | None) -> str:
    try:
        area = float(value or 0)
    except Exception:
        area = 0.0
    if area <= 0:
        return "미상"
    base = int(round(area))
    return f"{base}평"


def _extract_price_int(row: dict[str, Any]) -> int:
    return PriceConverter.to_int(row.get("매매가") or row.get("보증금") or "0")


def build_market_summary(items: list[dict[str, Any]]) -> dict[str, Any]:
    grouped: dict[str, list[dict[str, Any]]] = {}
    for item in items:
        grouped.setdefault(item.get("거래유형", "기타"), []).append(item)
    summary: dict[str, Any] = {}
    for trade_type, rows in grouped.items():
        prices = [_extract_price_int(r) for r in rows]
        prices = [p for p in prices if p > 0]
        area_groups: dict[str, list[dict[str, Any]]] = {}
        for row in rows:
            area_groups.setdefault(_bucket_area(row.get("면적(평)")), []).append(row)
        comparable_area_rows = []
        for area_key, area_items in area_groups.items():
            area_prices = [_extract_price_int(r) for r in area_items]
            area_prices = [p for p in area_prices if p > 0]
            comparable_area_rows.append({
                "area_key": area_key,
                "count": len(area_items),
                "min_price": min(area_prices) if area_prices else None,
                "avg_price": int(sum(area_prices) / len(area_prices)) if area_prices else None,
                "max_price": max(area_prices) if area_prices else None,
                "sample_items": area_items[:2],
            })
        comparable_area_rows.sort(key=lambda row: (-int(row.get("count") or 0), str(row.get("area_key") or "")))
        summary[trade_type] = {
            "count": len(rows),
            "min_price": min(prices) if prices else None,
            "max_price": max(prices) if prices else None,
            "avg_price": int(sum(prices) / len(prices)) if prices else None,
            "median_price": int(statistics.median(prices)) if prices else None,
            "sample_items": rows[:3],
            "area_summary": comparable_area_rows[:5],
        }
    return summary


def summarize(items: list[dict[str, Any]]) -> str:
    if not items:
        return "조건에 맞는 매물을 찾지 못했습니다."
    lines = []
    grouped: dict[str, list[dict[str, Any]]] = {}
    for item in items:
        grouped.setdefault(item.get("거래유형", "기타"), []).append(item)
    for trade_type, rows in grouped.items():
        lines.append(f"[{trade_type}] {len(rows)}건")
        prices = [_extract_price_int(r) for r in rows]
        prices = [p for p in prices if p > 0]
        if prices:
            lines.append(f"- 가격 범위: {PriceConverter.to_string(min(prices))} ~ {PriceConverter.to_string(max(prices))}")
            lines.append(f"- 평균/중앙값: {PriceConverter.to_string(int(sum(prices)/len(prices)))} / {PriceConverter.to_string(int(statistics.median(prices)))}")
        area_summary = build_market_summary(rows).get(trade_type, {}).get("area_summary", [])
        if area_summary:
            head = area_summary[0]
            lines.append(f"- 대표 동일 평형: {head.get('area_key')} {head.get('count')}건 | 평균 {PriceConverter.to_string(head.get('avg_price')) if head.get('avg_price') else '-'}")
        for row in rows[:5]:
            price = row.get("매매가") or row.get("보증금") or "-"
            if trade_type == "월세" and row.get("월세"):
                price = f"{price}/{row.get('월세')}"
            lines.append(f"- {row.get('단지명')} | {price} | {row.get('면적(평)', 0)}평 | {row.get('층/방향', '-') or '-'} | {row.get('매물URL', '')}")
    return "\n".join(lines)


def _brief_price(value: int | None) -> str:
    return PriceConverter.to_string(value) if value else "-"


def build_compare_insights(results: list[dict[str, Any]]) -> dict[str, Any]:
    trade_groups: dict[str, list[dict[str, Any]]] = {}
    area_match_groups: dict[str, dict[str, list[dict[str, Any]]]] = {}
    for result in results:
        info = result.get("complex_info", {})
        name = info.get("name", result.get("complex_id"))
        for trade_type, meta in (result.get("market_summary") or {}).items():
            trade_groups.setdefault(trade_type, []).append({"name": name, "avg_price": meta.get("avg_price"), "min_price": meta.get("min_price"), "count": meta.get("count", 0)})
            for area_row in meta.get("area_summary") or []:
                area_match_groups.setdefault(trade_type, {}).setdefault(area_row.get("area_key") or "미상", []).append({"name": name, **area_row})
    insights: dict[str, Any] = {"trade": {}, "same_area": {}}
    for trade_type, rows in trade_groups.items():
        valid = [row for row in rows if row.get("avg_price")]
        if len(valid) >= 2:
            valid.sort(key=lambda x: x["avg_price"])
            insights["trade"][trade_type] = {
                "cheapest": valid[0],
                "most_expensive": valid[-1],
                "gap": valid[-1]["avg_price"] - valid[0]["avg_price"],
            }
    for trade_type, area_rows in area_match_groups.items():
        for area_key, rows in area_rows.items():
            valid = [row for row in rows if row.get("avg_price")]
            if len(valid) >= 2:
                valid.sort(key=lambda x: x["avg_price"])
                insights["same_area"].setdefault(trade_type, []).append({
                    "area_key": area_key,
                    "cheapest": valid[0],
                    "most_expensive": valid[-1],
                    "gap": valid[-1]["avg_price"] - valid[0]["avg_price"],
                    "participant_count": len(valid),
                })
    for trade_type in list(insights["same_area"].keys()):
        insights["same_area"][trade_type].sort(key=lambda row: (-row.get("participant_count", 0), row.get("gap", 0)))
    return insights


def summarize_comparison(results: list[dict[str, Any]]) -> str:
    if not results:
        return "비교할 단지 결과가 없습니다."
    lines = ["[단지 비교 브리핑]"]
    insights = build_compare_insights(results)
    for result in results:
        info = result.get("complex_info", {})
        name = info.get("name", result.get("complex_id"))
        address = info.get("address") or "-"
        lines.append(f"- {name}")
        lines.append(f"  · 주소: {address}")
        for trade_type, meta in result.get("market_summary", {}).items():
            lines.append(f"  · {trade_type}: {meta.get('count', 0)}건 | 최저 {_brief_price(meta.get('min_price'))} | 평균 {_brief_price(meta.get('avg_price'))} | 중앙값 {_brief_price(meta.get('median_price'))} | 최고 {_brief_price(meta.get('max_price'))}")
            area_rows = meta.get("area_summary") or []
            if area_rows:
                head = area_rows[0]
                lines.append(f"    - 대표 동일 평형: {head.get('area_key')} {head.get('count')}건 | 평균 {_brief_price(head.get('avg_price'))}")
    for trade_type, meta in (insights.get("trade") or {}).items():
        lines.append(f"- 한줄 해석 ({trade_type}): {meta['cheapest']['name']} 쪽 평균이 가장 낮고 {meta['most_expensive']['name']} 쪽이 가장 높습니다. 전체 평균 격차는 {_brief_price(meta['gap'])} 정도입니다.")
    for trade_type, area_rows in (insights.get("same_area") or {}).items():
        if area_rows:
            head = area_rows[0]
            lines.append(f"- 동일 평형 비교 ({trade_type} {head['area_key']}): {head['cheapest']['name']} 쪽이 더 낮고 {head['most_expensive']['name']} 쪽이 더 높습니다. 같은 평형대 기준 격차는 {_brief_price(head['gap'])} 정도입니다.")
    return "\n".join(lines)


def run_query(*, query: str | None, complex_id: str | None, url: str | None, trade_types: list[str] | None, pages: int, limit: int, candidate_limit: int, min_pyeong: float | None, max_pyeong: float | None, compare: bool) -> dict[str, Any]:
    parsed = parse_natural_query(query or "") if query else None
    trade_types = list(trade_types or [])
    if not trade_types:
        trade_types = parsed.trade_types if parsed else ["전세"]
    min_pyeong = min_pyeong if min_pyeong is not None else (parsed.min_pyeong if parsed else None)
    max_pyeong = max_pyeong if max_pyeong is not None else (parsed.max_pyeong if parsed else None)

    complex_ids = resolve_complex_ids(query, complex_id, url, candidate_limit=max(1, candidate_limit))
    if not complex_ids:
        raise SearchError("단지 ID를 찾지 못했습니다. 더 구체적인 단지명/지역명을 주거나 단지 URL/ID를 직접 넣어 주세요.")

    compare_mode = compare or bool(parsed and parsed.compare_mode and len(complex_ids) >= 2)
    target_ids = complex_ids[: max(1, candidate_limit if compare_mode else 1)]
    meta = {"rate_limited": bool(RATE_LIMIT_STATE.get("active")), "rate_limit_message": RATE_LIMIT_STATE.get("last_error")}

    if compare_mode:
        results = []
        for cid in target_ids:
            items = fetch_articles(cid, trade_types, pages=max(1, pages))
            items = filter_items(items, min_pyeong, max_pyeong, max(1, limit))
            results.append({
                "complex_id": cid,
                "complex_info": fetch_complex_info(cid),
                "trade_types": trade_types,
                "count": len(items),
                "market_summary": build_market_summary(items),
                "items": items[:5],
            })
        compare_insights = build_compare_insights(results)
        return {"query": query, "parsed": asdict(parsed) if parsed else None, "compare_mode": True, "results": results, "compare_insights": compare_insights, "meta": meta}

    selected_complex_id = target_ids[0]
    items = fetch_articles(selected_complex_id, trade_types, pages=max(1, pages))
    items = filter_items(items, min_pyeong, max_pyeong, max(1, limit))
    return {
        "query": query,
        "parsed": asdict(parsed) if parsed else None,
        "selected_complex_id": selected_complex_id,
        "complex_info": fetch_complex_info(selected_complex_id),
        "trade_types": trade_types,
        "count": len(items),
        "market_summary": build_market_summary(items),
        "items": items,
        "meta": meta,
    }


def run_self_test() -> int:
    if not UPSTREAM.exists() or UPSTREAM_IMPORT_ERROR is not None:
        print(
            "SKIP: upstream clone(tmp/naverland-scrapper) 미구성 상태라 upstream 의존 self-test는 건너뜁니다.",
            file=sys.stderr,
        )
        return 0

    sample = {
        "articleNo": "123456789",
        "tradeTypeName": "전세",
        "dealOrWarrantPrc": "12억 5,000",
        "area1": 84.98,
        "floorInfo": "12/25",
        "direction": "남향",
        "articleFeatureDesc": "역세권, 학군우수",
        "realEstateTypeCode": "APT",
    }
    row = normalize_article_payload(sample, "테스트아파트", "99999", requested_trade_type="전세")
    assert row["단지명"] == "테스트아파트"
    assert row["거래유형"] == "전세"
    assert row["보증금"] == "12억 5,000"
    assert row["면적(평)"] > 0

    parsed = parse_natural_query("잠실 리센츠랑 엘스 전세 비교 30평대")
    assert parsed.compare_mode is True
    assert "전세" in parsed.trade_types
    assert parsed.min_pyeong is not None and parsed.max_pyeong is not None
    assert len(parsed.candidate_keywords) >= 2
    assert "잠실" in parsed.location_hints

    tricky = parse_natural_query("서울 양천구 신월동 신월시영아파트 전세")
    assert tricky.cleaned_query.startswith("서울 양천구 신월동 신월시영")
    assert any(normalize_complex_alias(x) == "신월시영" for x in tricky.candidate_keywords)
    assert normalize_complex_alias("신월시영아파트") == "신월시영"
    direct = build_direct_lookup_payload("complex 1147 리센츠", None, None)
    assert direct["selected_complex_id"] == "1147"
    assert direct["canonical_complex_url"].endswith("/1147")

    backup_cache = _read_candidate_cache()
    remember_candidate({"complex_id": "777", "name": "신월시영아파트", "address": "서울시 양천구 신월동", "household_count": 2256}, aliases=["신월시영", "양천 신월시영"])
    saved = seed_candidate_cache([
        {"complex_id": "778", "name": "리센츠", "address": "서울시 송파구 잠실동", "aliases": ["잠실 리센츠", "잠실리센츠"], "household_count": 5563}
    ], source="self-test")
    cached = search_cached_candidates("신월시영아파트", candidate_limit=3)
    assert cached and cached[0]["complex_id"] == "777"
    assert saved and any(row["complex_id"] == "778" for row in saved)
    assert list_candidate_cache(limit=5, keyword="리센츠")
    ref_candidates = search_reference_candidates("서울 양천구 신월동 신월시영아파트 전세", candidate_limit=3)
    assert ref_candidates and normalize_complex_alias(ref_candidates[0]["name"]) == "신월시영"
    _write_candidate_cache(backup_cache)

    score = _score_candidate({"name": "잠실리센츠", "address": "서울시 송파구 잠실동", "household_count": 5563}, "리센츠", parsed)
    assert score > 0

    summary = build_market_summary([
        {"거래유형": "전세", "보증금": "10억", "면적(평)": 33.0},
        {"거래유형": "전세", "보증금": "11억", "면적(평)": 33.2},
        {"거래유형": "전세", "보증금": "13억", "면적(평)": 44.0},
    ])
    assert summary["전세"]["area_summary"][0]["area_key"] in {"33평", "44평"}

    compare_insights = build_compare_insights([
        {"complex_info": {"name": "A"}, "market_summary": {"전세": {"avg_price": 100, "count": 2, "area_summary": [{"area_key": "33평", "avg_price": 100, "count": 2}]}}},
        {"complex_info": {"name": "B"}, "market_summary": {"전세": {"avg_price": 130, "count": 2, "area_summary": [{"area_key": "33평", "avg_price": 130, "count": 2}]}}},
    ])
    assert compare_insights["trade"]["전세"]["gap"] == 30

    print("SELF_TEST_OK")
    print(json.dumps({"parsed_query": asdict(parsed), "tricky_query": asdict(tricky), "cached_top": cached[:1], "sample_score": score, "compare_insights": compare_insights}, ensure_ascii=False, indent=2)[:3000])
    return 0


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="네이버 부동산 매물 검색/비교 래퍼")
    p.add_argument("--query", help="자연어 또는 지역/단지 키워드. 예: 잠실 리센츠 전세 30평대, 대치 은마와 래미안대치팰리스 비교")
    p.add_argument("--complex-id", help="네이버 부동산 단지 ID")
    p.add_argument("--url", help="네이버 부동산 단지/매물 URL")
    p.add_argument("--trade-types", default="", help="쉼표 구분 거래 유형. 비우면 query에서 추론하고, 없으면 전세")
    p.add_argument("--pages", type=int, default=1)
    p.add_argument("--limit", type=int, default=15)
    p.add_argument("--candidate-limit", type=int, default=3)
    p.add_argument("--min-pyeong", type=float)
    p.add_argument("--max-pyeong", type=float)
    p.add_argument("--list-candidates", action="store_true", help="매물 조회 대신 단지 후보만 출력")
    p.add_argument("--compare", action="store_true", help="후보 상위 단지들을 비교 모드로 조회")
    p.add_argument("--parse-only", action="store_true", help="자연어 파싱 결과만 출력")
    p.add_argument("--show-cache", action="store_true", help="candidate cache를 조회")
    p.add_argument("--resolve-direct", action="store_true", help="query/url/complex-id에서 direct ID와 canonical URL을 정리")
    p.add_argument("--lookup-complex", action="store_true", help="매물 조회 대신 단지 기본 정보만 direct lookup")
    p.add_argument("--seed-candidate-file", nargs="?", const="", help="candidate-cache에 seed할 JSON 파일 경로. 비우면 references/candidate-seeds.json")
    p.add_argument("--seed-candidate", action="store_true", help="단일 후보를 candidate-cache에 직접 저장")
    p.add_argument("--candidate-name", help="seed candidate 이름")
    p.add_argument("--candidate-address", help="seed candidate 주소")
    p.add_argument("--candidate-households", type=int, help="seed candidate 세대수")
    p.add_argument("--candidate-aliases", default="", help="쉼표 구분 alias 목록")
    p.add_argument("--candidate-note", help="seed candidate 메모")
    p.add_argument("--json", action="store_true")
    p.add_argument("--self-test", action="store_true")
    return p


def main() -> int:
    args = build_parser().parse_args()
    if args.self_test:
        return run_self_test()

    parsed = parse_natural_query(args.query or "") if args.query else None
    if args.parse_only:
        print(json.dumps(asdict(parsed) if parsed else {}, ensure_ascii=False, indent=2))
        return 0

    if args.seed_candidate_file is not None:
        result = seed_candidate_from_file(args.seed_candidate_file or None)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0

    if args.resolve_direct:
        print(json.dumps(build_direct_lookup_payload(args.query, args.complex_id, args.url), ensure_ascii=False, indent=2))
        return 0

    if args.seed_candidate:
        if not args.complex_id:
            raise SystemExit("--seed-candidate 는 --complex-id 와 함께 사용하세요.")
        aliases = [token.strip() for token in str(args.candidate_aliases or "").split(",") if token.strip()]
        saved = remember_candidate(
            {
                "complex_id": args.complex_id,
                "name": args.candidate_name,
                "address": args.candidate_address,
                "household_count": args.candidate_households,
                "source": "manual-seed",
                "learned_from": args.query or args.url or "manual-seed",
                "note": args.candidate_note,
            },
            aliases=aliases,
        )
        print(json.dumps({"saved": True, "candidate": saved}, ensure_ascii=False, indent=2))
        return 0

    if args.show_cache:
        rows = list_candidate_cache(limit=max(1, args.limit), keyword=args.query)
        print(json.dumps({"count": len(rows), "entries": rows}, ensure_ascii=False, indent=2))
        return 0

    if args.lookup_complex:
        payload = build_direct_lookup_payload(args.query, args.complex_id, args.url)
        selected = payload.get("selected_complex_id")
        if not selected:
            raise SystemExit("direct lookup용 complex ID를 찾지 못했습니다. --complex-id / --url / --query 중 하나에 direct 단서를 넣어 주세요.")
        payload["complex_info"] = fetch_complex_info(str(selected))
        print(json.dumps(payload, ensure_ascii=False, indent=2))
        return 0

    trade_types = [token.strip() for token in str(args.trade_types).split(",") if token.strip()]

    if args.list_candidates:
        if not args.query:
            raise SystemExit("--list-candidates 는 --query 와 함께 사용하세요.")
        candidates = search_complex_candidates(args.query, candidate_limit=max(1, args.candidate_limit))
        print(json.dumps({"query": args.query, "parsed": asdict(parsed), "candidates": candidates, "meta": {"rate_limited": RATE_LIMIT_STATE.get('active'), "rate_limit_message": RATE_LIMIT_STATE.get('last_error')}}, ensure_ascii=False, indent=2))
        return 0

    output = run_query(
        query=args.query,
        complex_id=args.complex_id,
        url=args.url,
        trade_types=trade_types,
        pages=max(1, args.pages),
        limit=max(1, args.limit),
        candidate_limit=max(1, args.candidate_limit),
        min_pyeong=args.min_pyeong,
        max_pyeong=args.max_pyeong,
        compare=bool(args.compare),
    )
    if args.json:
        print(json.dumps(output, ensure_ascii=False, indent=2))
    else:
        print(summarize_comparison(output.get("results", [])) if output.get("compare_mode") else summarize(output.get("items", [])))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
