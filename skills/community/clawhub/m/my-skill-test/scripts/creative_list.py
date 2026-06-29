#!/usr/bin/env python3
"""Call ZingAPI creative-list with signed production requests.

This script intentionally uses only Python's standard library so it can run in
minimal agent environments.
"""

from __future__ import annotations

import argparse
import hashlib
import hmac
import json
import os
import sys
import time
import uuid
from datetime import datetime, timezone
from typing import Any, Dict, Iterable, List, Mapping, MutableMapping, Optional
from urllib.error import HTTPError, URLError
from urllib.parse import quote
from urllib.request import Request, urlopen

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")


BASE_URL = "https://openapi.dataideaglobal.com"
HOST = "openapi.dataideaglobal.com"
ACTION = "creative-list"
VERSION = "v1"
ALGORITHM = "zf3-HMAC-SHA256"

APP_TYPE_MAP = {
    "game": 1,
    "games": 1,
    "游戏": 1,
    "tool": 2,
    "tools": 2,
    "app": 2,
    "工具": 2,
    "ecom": 3,
    "ecommerce": 3,
    "shop": 3,
    "电商": 3,
}

CREATIVE_TYPE_MAP = {
    "image": 1,
    "图片": 1,
    "video": 2,
    "视频": 2,
    "carousel": 3,
    "轮播": 3,
    "html": 4,
    "playable": 7,
    "试玩": 7,
    "试玩广告": 7,
}

SORT_MAP = {
    "latest": "-first_seen",
    "first_seen": "-first_seen",
    "最新": "-first_seen",
    "最新创意": "-first_seen",
    "首次发现": "-first_seen",
    "impression": "-impression",
    "展示": "-impression",
    "展现": "-impression",
    "展现估值": "-impression",
    "last_seen": "-last_seen",
    "最后发现": "-last_seen",
    "最后看见": "-last_seen",
    "days": "-days",
    "投放天数": "-days",
    "related_ads": "-related_ads_count",
    "关联广告": "-related_ads_count",
    "heat": "-heat_degree",
    "热度": "-heat_degree",
    "likes": "-like_count",
    "点赞": "-like_count",
    "comments": "-comment_count",
    "评论": "-comment_count",
    "shares": "-share_count",
    "分享": "-share_count",
}

DEDUPE_MAP = {
    "ad": 0,
    "ads": 0,
    "strict": 0,
    "广告": 0,
    "广告去重": 0,
    "material": 1,
    "creative": 1,
    "素材": 1,
    "创意": 1,
    "素材去重": 1,
    "创意去重": 1,
    "advertiser": 2,
    "广告主": 2,
    "广告主去重": 2,
}

PLATFORM_MAP = {
    "facebook": "facebook",
    "fb": "facebook",
    "脸书": "facebook",
    "instagram": "instagram",
    "ins": "instagram",
    "youtube": "youtube",
    "yt": "youtube",
    "tiktok": "tiktok",
    "tt": "tiktok",
    "x": "twitter",
    "twitter": "twitter",
    "unity": "unity_ads",
    "unityads": "unity_ads",
    "unity_ads": "unity_ads",
    "applovin": "applovin",
    "admob": "admob",
    "pangle": "pangle",
    "snapchat": "snapchat",
    "reddit": "reddit",
}

COUNTRY_MAP = {
    "美国": "USA",
    "us": "USA",
    "usa": "USA",
    "英国": "GBR",
    "日本": "JPN",
    "韩国": "KOR",
    "德国": "DEU",
    "法国": "FRA",
    "加拿大": "CAN",
    "澳大利亚": "AUS",
    "印度": "IND",
    "印尼": "IDN",
    "印度尼西亚": "IDN",
    "巴西": "BRA",
    "墨西哥": "MEX",
    "泰国": "THA",
    "越南": "VNM",
    "菲律宾": "PHL",
    "新加坡": "SGP",
    "马来西亚": "MYS",
    "土耳其": "TUR",
    "沙特": "SAU",
    "阿联酋": "ARE",
}

ADS_TYPE_LABELS = {
    1: "图片",
    2: "视频",
    3: "轮播",
    4: "HTML",
    7: "试玩广告",
}

APP_TYPE_LABELS = {
    1: "游戏",
    2: "工具",
    3: "电商",
}

PLATFORM_LABELS = {
    "facebook": "FB News Feed",
    "instagram": "Instagram",
    "audience_network": "Audience Network",
    "messenger": "Messenger",
    "youtube": "YouTube",
    "admob": "Admob",
    "adsense": "AdSense",
    "twitter": "X（原 Twitter）",
    "unity_ads": "UnityAds",
    "vungle": "Liftoff（原 Vungle）",
    "applovin": "AppLovin",
    "chartboost": "Chartboost",
    "pinterest": "Pinterest",
    "ironsource": "ironSource",
    "reddit": "Reddit",
    "tiktok": "TikTok",
    "topbuzz": "TopBuzz",
    "mobvista": "Mintegral(Mobvista)",
    "pangle": "Pangle(TikTok Audience Network)",
    "yahoo": "Yahoo!",
    "snapchat": "Snapchat",
    "tapjoy": "Tapjoy",
    "kwai": "Kwai",
    "inmobi": "InMobi",
    "asa": "Apple Search Ads",
    "naver": "NAVER(네이버)",
    "daum": "Daum(다음)",
    "nate": "Nate(네이트)",
    "ameba": "Ameba(アメーバ)",
    "yahoo_japan": "Yahoo! Japan",
    "gunosy": "Gunosy(グノシー)",
    "zucks": "Zucks",
    "smartnews": "SmartNews(スマートニュース)",
    "imobile": "i_mobile",
    "akane": "AkaNe",
    "nend": "Nend",
    "yandex": "Yandex",
    "vkontakte": "VKontakte",
    "moloco": "Moloco",
    "dt_exchange": "DtExchange",
    "bigoads": "BIGO Ads",
    "threads": "Threads",
    "whatsapp": "WhatsApp",
}

COUNTRY_LABELS = {
    "AGO": "安哥拉",
    "ARE": "阿联酋",
    "ARG": "阿根廷",
    "AUS": "澳大利亚",
    "AUT": "奥地利",
    "AZE": "阿塞拜疆",
    "BEL": "比利时",
    "BGD": "孟加拉国",
    "BHR": "巴林",
    "BRA": "巴西",
    "CAN": "加拿大",
    "CHE": "瑞士",
    "CHL": "智利",
    "CIV": "科特迪瓦",
    "COL": "哥伦比亚",
    "DEU": "德国",
    "DNK": "丹麦",
    "DZA": "阿尔及利亚",
    "EGY": "埃及",
    "GBR": "英国",
    "ESP": "西班牙",
    "FIN": "芬兰",
    "FRA": "法国",
    "GRC": "希腊",
    "HKG": "中国香港",
    "HUN": "匈牙利",
    "IDN": "印度尼西亚",
    "IND": "印度",
    "IRL": "爱尔兰",
    "IRQ": "伊拉克",
    "ISR": "以色列",
    "ITA": "意大利",
    "JPN": "日本",
    "KAZ": "哈萨克斯坦",
    "KEN": "肯尼亚",
    "KHM": "柬埔寨",
    "KOR": "韩国",
    "KWT": "科威特",
    "LBN": "黎巴嫩",
    "LBY": "利比亚",
    "LUX": "卢森堡",
    "MAC": "中国澳门",
    "MAR": "摩洛哥",
    "MEX": "墨西哥",
    "MMR": "缅甸",
    "MNG": "蒙古",
    "MYS": "马来西亚",
    "NGA": "尼日利亚",
    "NLD": "荷兰",
    "NOR": "挪威",
    "NZL": "新西兰",
    "OMN": "阿曼",
    "PAK": "巴基斯坦",
    "PAN": "巴拿马",
    "PER": "秘鲁",
    "PHL": "菲律宾",
    "POL": "波兰",
    "PRT": "葡萄牙",
    "PRY": "巴拉圭",
    "QAT": "卡塔尔",
    "ROU": "罗马尼亚",
    "RUS": "俄罗斯联邦",
    "SAU": "沙特阿拉伯",
    "SEN": "塞内加尔",
    "SGP": "新加坡",
    "SWE": "瑞典",
    "THA": "泰国",
    "TUR": "土耳其",
    "TWN": "中国台湾",
    "UKR": "乌克兰",
    "USA": "美国",
    "VEN": "委内瑞拉",
    "VNM": "越南",
    "ZAF": "南非",
    "SVN": "斯洛文尼亚",
    "GEO": "格鲁吉亚",
}


def _json_dumps(data: Any) -> str:
    return json.dumps(data, ensure_ascii=False, separators=(",", ":"), sort_keys=False)


def _sha256_hex(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def _utc_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _as_list(values: Optional[Iterable[str]]) -> List[str]:
    if not values:
        return []
    result: List[str] = []
    for value in values:
        for item in str(value).split(","):
            item = item.strip()
            if item:
                result.append(item)
    return result


def _normalize_aliases(values: Iterable[str], mapping: Mapping[str, str], upper_default: bool = False) -> List[str]:
    result: List[str] = []
    for value in values:
        raw = str(value).strip()
        key = raw.lower()
        normalized = mapping.get(key) or mapping.get(raw)
        if not normalized:
            normalized = raw.upper() if upper_default else key
        result.append(normalized)
    return result


def _map_one(value: str, mapping: Mapping[str, int], label: str) -> int:
    raw = str(value).strip()
    if raw.lstrip("-").isdigit():
        return int(raw)
    key = raw.lower()
    if key not in mapping:
        allowed = ", ".join(sorted(mapping))
        raise SystemExit(f"Unknown {label}: {value}. Allowed names: {allowed}")
    return mapping[key]


def _load_body(body_arg: str) -> Dict[str, Any]:
    if body_arg.startswith("@"):
        path = body_arg[1:]
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    return json.loads(body_arg)


def _build_payload(args: argparse.Namespace) -> Dict[str, Any]:
    if args.body:
        payload = _load_body(args.body)
    else:
        if not args.app_type:
            raise SystemExit("--app-type is required unless --body is used")

        payload = {
            "app_type": _map_one(args.app_type, APP_TYPE_MAP, "app type"),
            "page": args.page,
            "page_size": args.page_size,
            "sort_field": SORT_MAP.get(args.sort, args.sort),
            "duplicate_removal": _map_one(args.dedupe, DEDUPE_MAP, "dedupe"),
        }

        keywords = _as_list(args.keyword)
        if keywords:
            payload["keyword"] = keywords

        platforms = _normalize_aliases(_as_list(args.platform), PLATFORM_MAP)
        if platforms:
            payload["platform"] = platforms

        countries = _normalize_aliases(_as_list(args.geo), COUNTRY_MAP, upper_default=True)
        if countries:
            payload["geo"] = countries

        languages = _as_list(args.language)
        if languages:
            payload["language"] = languages

        creative_types = _as_list(args.creative_type)
        if creative_types:
            payload["ads_type"] = [
                _map_one(item, CREATIVE_TYPE_MAP, "creative type")
                for item in creative_types
            ]

        if args.seen_begin is not None:
            payload["seen_begin"] = args.seen_begin
        if args.seen_end is not None:
            payload["seen_end"] = args.seen_end
        if args.seen_days is not None and args.seen_begin is None:
            now = int(time.time())
            payload["seen_begin"] = now - args.seen_days * 86400
            payload["seen_end"] = args.seen_end or now

        if args.first_seen_begin is not None:
            payload["first_seen_begin"] = args.first_seen_begin
        if args.first_seen_end is not None:
            payload["first_seen_end"] = args.first_seen_end

        if args.include_ai_tags:
            payload["include_ai_tags"] = True
            payload["max_ai_tags_per_type"] = args.max_ai_tags_per_type

    if "page_size" in payload:
        payload["page_size"] = min(int(payload["page_size"]), 20)
    if "page" in payload:
        payload["page"] = max(1, min(int(payload["page"]), 500))

    return payload


def _canonical_uri(customer_name: str) -> str:
    return f"/zingapi/v1/creative/list/{quote(customer_name, safe='')}"


def _sign_headers(
    *,
    method: str,
    canonical_uri: str,
    body_text: str,
    access_key_id: str,
    access_key_secret: str,
) -> Dict[str, str]:
    body_hash = _sha256_hex(body_text)
    headers = {
        "content-type": "application/json; charset=utf-8",
        "x-zf-action": ACTION,
        "x-zf-content-sha256": body_hash,
        "x-zf-date": _utc_now(),
        "x-zf-nonce": str(uuid.uuid4()),
        "x-zf-version": VERSION,
    }

    signed_header_names = sorted(headers)
    canonical_headers = "".join(f"{name}:{headers[name].strip()}\n" for name in signed_header_names)
    signed_headers = ";".join(signed_header_names)
    canonical_request = "\n".join(
        [
            method.upper(),
            canonical_uri,
            "",
            canonical_headers,
            signed_headers,
            body_hash,
        ]
    )
    string_to_sign = "\n".join([ALGORITHM, _sha256_hex(canonical_request)])
    signature = hmac.new(
        access_key_secret.encode("utf-8"),
        string_to_sign.encode("utf-8"),
        hashlib.sha256,
    ).hexdigest()

    request_headers = {k: v for k, v in headers.items() if k != "host"}
    request_headers["Authorization"] = (
        f"{ALGORITHM} Credential={access_key_id},"
        f"SignedHeaders={signed_headers},Signature={signature}"
    )
    return request_headers


def _request_json(
    *,
    customer_name: str,
    access_key_id: str,
    access_key_secret: str,
    payload: Mapping[str, Any],
    timeout: int,
) -> Dict[str, Any]:
    body_text = _json_dumps(payload)
    canonical_uri = _canonical_uri(customer_name)
    url = f"{BASE_URL}{canonical_uri}"
    headers = _sign_headers(
        method="POST",
        canonical_uri=canonical_uri,
        body_text=body_text,
        access_key_id=access_key_id,
        access_key_secret=access_key_secret,
    )
    req = Request(
        url,
        data=body_text.encode("utf-8"),
        headers={
            **headers,
            "Accept": "application/json",
            "User-Agent": "ZingAPI-CreativeList-Skill/1.0",
        },
        method="POST",
    )
    try:
        with urlopen(req, timeout=timeout) as resp:
            text = resp.read().decode("utf-8")
            return json.loads(text)
    except HTTPError as exc:
        body = exc.read().decode("utf-8", "replace")
        raise SystemExit(f"HTTP {exc.code}: {body}") from exc
    except URLError as exc:
        raise SystemExit(f"Network error: {exc.reason}") from exc


def _compact_dict(data: Mapping[str, Any]) -> Dict[str, Any]:
    return {k: v for k, v in data.items() if v not in (None, "", [], {})}


def _format_code_label(value: Any, labels: Mapping[str, str]) -> Any:
    if isinstance(value, list):
        return [_format_code_label(item, labels) for item in value]
    if isinstance(value, tuple):
        return [_format_code_label(item, labels) for item in value]
    if value is None:
        return None

    code = str(value).strip()
    if "," in code:
        return [
            _format_code_label(item.strip(), labels)
            for item in code.split(",")
            if item.strip()
        ]

    label = labels.get(code) or labels.get(code.lower()) or labels.get(code.upper())
    return f"{label} ({code})" if label else value


def _format_compact_number(value: Any) -> Any:
    if value in (None, ""):
        return value
    try:
        number = float(value)
    except (TypeError, ValueError):
        return value

    sign = "-" if number < 0 else ""
    number = abs(number)
    units = [
        (1_000_000_000, "B"),
        (1_000_000, "M"),
        (1_000, "K"),
    ]
    for threshold, suffix in units:
        if number >= threshold:
            return f"{sign}{number / threshold:.1f}{suffix}"
    if isinstance(value, int):
        return value
    return int(number) if number.is_integer() else value


def _extract_ai_tags(creative: Mapping[str, Any]) -> Dict[str, Any]:
    result: Dict[str, Any] = {}
    for field, label in [
        ("ai_image_tags", "图片 AI 标签"),
        ("ai_video_tags", "视频 AI 标签"),
        ("ai_image_tags_new", "新版图片 AI 标签"),
        ("ai_video_tags_new", "新版视频 AI 标签"),
    ]:
        value = creative.get(field)
        if not isinstance(value, Mapping):
            continue
        result[label] = _compact_dict({
            "summary": value.get("summary"),
            "tags": value.get("tags"),
        })
    return result


def _summarize_creative(creative: Mapping[str, Any]) -> Dict[str, Any]:
    ads_type = creative.get("ads_type")
    app_type = creative.get("app_type")
    resource_urls = creative.get("resource_urls") or []

    return _compact_dict({
        "创意ID": creative.get("ad_key"),
        "查询标识": creative.get("search_flag"),
        "广告主": _compact_dict({
            "名称": creative.get("advertiser_name"),
            "ID或域名": creative.get("advertiser_id"),
            "开发者": creative.get("app_developer"),
            "Logo": creative.get("logo_url"),
            "分类": creative.get("category_tag"),
        }),
        "素材": _compact_dict({
            "类型": ADS_TYPE_LABELS.get(ads_type, ads_type),
            "类型编码": ads_type,
            "预览图": creative.get("preview_img_url"),
            "预览图尺寸": creative.get("preview_img_size"),
            "资源列表": resource_urls,
            "视频时长秒": creative.get("video_duration"),
            "视频转图片标识": creative.get("video2pic"),
            "图片Hash": creative.get("image_ahash_md5"),
            "素材ID": creative.get("material_id"),
            "NSFW": creative.get("is_nsfw"),
        }),
        "投放": _compact_dict({
            "行业": APP_TYPE_LABELS.get(app_type, app_type),
            "行业编码": app_type,
            "渠道": _format_code_label(creative.get("platform"), PLATFORM_LABELS),
            "国家地区": _format_code_label(creative.get("countries"), COUNTRY_LABELS),
            "文案语言": creative.get("language"),
            "首次投放时间": creative.get("first_seen"),
            "最后发现时间": creative.get("last_seen"),
            "投放天数": creative.get("days_count"),
            "原帖创建时间": creative.get("post_created_time"),
            "主页ID": creative.get("page_id"),
            "主页名称": creative.get("page_name"),
            "FB合并渠道": _format_code_label(creative.get("fb_merge_channel"), PLATFORM_LABELS),
        }),
        "指标": _compact_dict({
            "人气总值": _format_compact_number(creative.get("all_exposure_value")),
            "当周人气值总和": _format_compact_number(creative.get("new_week_exposure_value")),
            "展现估值": _format_compact_number(creative.get("impression")),
            "热度值": _format_compact_number(creative.get("heat")),
            "关联广告数": creative.get("related_ads_count"),
            "广告花费美元": creative.get("ad_cost"),
            "点赞数": creative.get("like_count"),
            "评论数": creative.get("comment_count"),
            "分享数": creative.get("share_count"),
            "浏览数": creative.get("view_count"),
            "人气值Top标签": creative.get("exposure_top"),
            "人气值Top标签周": creative.get("exposure_top_week"),
        }),
        "文案": _compact_dict({
            "标题": creative.get("title"),
            "正文": creative.get("body"),
            "Message": creative.get("message"),
            "CTA": creative.get("call_to_action"),
            "文案唯一标识": creative.get("text_md5"),
        }),
        "链接": _compact_dict({
            "落地页": creative.get("store_url"),
            "原帖链接": creative.get("source_url"),
            "结束卡片或关联视频": creative.get("html_url"),
            "媒体包名": creative.get("source_app"),
        }),
        "游戏标签": _compact_dict({
            "游戏核心赛道": creative.get("game_core_track"),
            "游戏IP": creative.get("game_ip"),
            "游戏玩法": creative.get("game_play"),
            "游戏主题": creative.get("game_theme"),
        }),
        "AI素材标签": _extract_ai_tags(creative),
        "原始字段": _compact_dict({
            "ad_key": creative.get("ad_key"),
            "search_flag": creative.get("search_flag"),
            "advertiser_name": creative.get("advertiser_name"),
            "advertiser_id": creative.get("advertiser_id"),
            "platform": creative.get("platform"),
            "app_type": app_type,
            "ads_type": ads_type,
            "all_exposure_value": creative.get("all_exposure_value"),
            "new_week_exposure_value": creative.get("new_week_exposure_value"),
            "impression": creative.get("impression"),
            "heat": creative.get("heat"),
        }),
    })


def _summarize_response(response: Mapping[str, Any]) -> Dict[str, Any]:
    data = response.get("data") or {}
    creative_list = data.get("creative_list") or []
    summarized = []
    for creative in creative_list:
        if not isinstance(creative, Mapping):
            continue
        summarized.append(_summarize_creative(creative))
    result = {
        "message": response.get("message"),
        "trace_id": response.get("trace_id") or response.get("id"),
        "remaining_volume": response.get("remaining_volume"),
        "total_count": data.get("total_count"),
        "fetch_count": response.get("fetch_count"),
        "字段说明": {
            "人气总值": "all_exposure_value，创意累计人气值；用户要求展示“人气值”时优先使用该字段。",
            "当周人气值总和": "new_week_exposure_value，创意当周人气值总和。",
            "展现估值": "impression，创意展现估值。",
            "热度值": "heat，创意热度值；该字段不是人气值。",
            "数值格式": "摘要中的大数字会使用 K/M/B 缩写并保留一位小数；原始数值保留在“原始字段”中。",
            "字典格式": "摘要中的渠道、国家/地区会显示为“名称 (编码)”；未知编码保持原值。",
        },
        "creative_list": summarized,
    }
    return {k: v for k, v in result.items() if v is not None}


def parse_args(argv: Optional[List[str]] = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Call ZingAPI creative-list.")
    parser.add_argument("--customer-name", default=os.getenv("ZINGAPI_CUSTOMER_NAME"))
    parser.add_argument("--access-key-id", default=os.getenv("ZINGAPI_ACCESS_KEY_ID"))
    parser.add_argument("--access-key-secret", default=os.getenv("ZINGAPI_ACCESS_KEY_SECRET"))
    parser.add_argument("--body", help="Raw JSON body string, or @path/to/request.json")
    parser.add_argument("--app-type", help="game, tool, ecom, or numeric 1/2/3")
    parser.add_argument("--keyword", action="append", help="Keyword. Repeat or comma-separate.")
    parser.add_argument("--platform", action="append", help="Channel code. Repeat or comma-separate.")
    parser.add_argument("--geo", action="append", help="Country/region code such as USA.")
    parser.add_argument("--language", action="append")
    parser.add_argument("--creative-type", action="append", help="image, video, carousel, html, playable.")
    parser.add_argument("--seen-days", type=int, default=7)
    parser.add_argument("--seen-begin", type=int)
    parser.add_argument("--seen-end", type=int)
    parser.add_argument("--first-seen-begin", type=int)
    parser.add_argument("--first-seen-end", type=int)
    parser.add_argument("--sort", default="latest", help="latest, impression, heat, last_seen, days, likes, comments, shares, or raw sort_field.")
    parser.add_argument("--dedupe", default="ad", help="ad, material, advertiser, or numeric 0/1/2.")
    parser.add_argument("--page", type=int, default=1)
    parser.add_argument("--page-size", type=int, default=20)
    parser.add_argument("--include-ai-tags", action="store_true")
    parser.add_argument("--max-ai-tags-per-type", type=int, default=5)
    parser.add_argument("--timeout", type=int, default=60)
    parser.add_argument("--output", choices=["summary", "raw"], default="summary")
    parser.add_argument("--dry-run", action="store_true", help="Print signed request preview without sending.")
    return parser.parse_args(argv)


def main(argv: Optional[List[str]] = None) -> int:
    args = parse_args(argv)
    missing = [
        name
        for name, value in [
            ("ZINGAPI_CUSTOMER_NAME", args.customer_name),
            ("ZINGAPI_ACCESS_KEY_ID", args.access_key_id),
            ("ZINGAPI_ACCESS_KEY_SECRET", args.access_key_secret),
        ]
        if not value
    ]
    if missing:
        raise SystemExit("Missing required environment/config: " + ", ".join(missing))

    payload = _build_payload(args)
    body_text = _json_dumps(payload)
    canonical_uri = _canonical_uri(args.customer_name)

    if args.dry_run:
        headers = _sign_headers(
            method="POST",
            canonical_uri=canonical_uri,
            body_text=body_text,
            access_key_id=args.access_key_id,
            access_key_secret=args.access_key_secret,
        )
        safe_headers = dict(headers)
        safe_headers["Authorization"] = safe_headers["Authorization"].split("Signature=")[0] + "Signature=<redacted>"
        print(_json_dumps({
            "url": f"{BASE_URL}{canonical_uri}",
            "headers": safe_headers,
            "body": payload,
        }))
        return 0

    response = _request_json(
        customer_name=args.customer_name,
        access_key_id=args.access_key_id,
        access_key_secret=args.access_key_secret,
        payload=payload,
        timeout=args.timeout,
    )
    output = response if args.output == "raw" else _summarize_response(response)
    print(_json_dumps(output))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
