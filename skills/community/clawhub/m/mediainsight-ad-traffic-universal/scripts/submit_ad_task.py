from __future__ import annotations

import argparse
from datetime import datetime
import os
import json
import re
import sys
from pathlib import Path
from tempfile import NamedTemporaryFile
from typing import Any

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from mediainsight_client import (  # noqa: E402
    DEFAULT_MCP_URL,
    MediaInsightClient,
    MediaInsightError,
    resolve_media_insight_auth,
)

# Public shared demo token for ClawHub trial use. Keep its permissions narrow and assume
# anyone who can inspect this public skill package can also see and use this token.
DEFAULT_DEMO_TOKEN = (
    "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9."
    "eyJlbmMiOiJ6aGNEZ0cycGhYRWViTUdINVoyazFxdGZSWUloamI4ZFB2ZGwyMTFhVUVoRXhVWi0yWDNNaWVu"
    "WHhldVN6eExfc082M2p4UDUtcWlKS2hXNDlXUzEzUSIsImlhdCI6MTc3ODA0ODA3NDk3NH0."
    "I2k6xLVQ5Sn9kQ_FAM_eHFC48m9EoF9rIrL_pFi47Xs"
)

DEFAULT_CHARTS = [
    "freq-capping",
    "data",
    "total_metrics",
    "flow-distribution-media",
    "flow-distribution-platform",
    "flow-distribution-industry",
    "flow-distribution-ta",
    "flow-distribution-region",
    "frequency-saturation-freq-capping",
]
DEFAULT_INDICATORS = ["impPassion"]
DEFAULT_INDUSTRY_NAME = "美妆个护类"
DEFAULT_ADVERTISER_NAME = "明略集团"
DEFAULT_BRAND_NAME = "明略科技"
DEVICE_IDS = {
    "pc": 0,
    "mobile": 1,
    "pm": 2,
    "ott": 3,
}
GENDER_ALIASES = {
    "female": "女",
    "woman": "女",
    "women": "女",
    "f": "女",
    "male": "男",
    "man": "男",
    "men": "男",
    "m": "男",
    "all": "",
    "any": "",
}


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Submit a MediaInsight ad-traffic task from a MediaInsight MCP token plus user-visible dictionary resolution."
    )
    auth = parser.add_mutually_exclusive_group(required=False)
    auth.add_argument(
        "--token",
        dest="token",
        help="MediaInsight MCP token.",
    )
    auth.add_argument(
        "--token-file",
        dest="token_file",
        help="Path to a file containing the MediaInsight token.",
    )

    parser.add_argument("--base-url", default="https://mediainsight.cn.miaozhen.com/api_v2")
    parser.add_argument("--mcp-url", default=DEFAULT_MCP_URL, help="MediaInsight MCP streamable HTTP endpoint.")
    parser.add_argument(
        "--mcp-token-type",
        type=int,
        default=0,
        help="Pass-through type for MCP get_ttc_token. Use 1 only after an API 401.",
    )
    parser.add_argument("--tenant-id", type=int, help="Optional tenant id to switch to after login.")
    parser.add_argument("--task-name", required=True)
    parser.add_argument(
        "--task-name-unique",
        action="store_true",
        help="Append a timestamp suffix to the task name before submission.",
    )
    parser.add_argument("--industry-name", default=DEFAULT_INDUSTRY_NAME)
    parser.add_argument("--advertiser-name", default=DEFAULT_ADVERTISER_NAME)
    parser.add_argument("--brand-name", default=DEFAULT_BRAND_NAME)
    parser.add_argument("--gender", default="female")
    parser.add_argument("--age-range", default="20-49", help="Inclusive age range, e.g. 20-49.")
    parser.add_argument("--region-name", action="append", required=True, dest="region_names")
    parser.add_argument("--campaign-type-name", action="append", dest="campaign_type_names")
    parser.add_argument(
        "--device",
        action="append",
        dest="devices",
        help="pc, mobile, pm, ott. Defaults to pc + mobile; add --device ott to include OTT.",
    )
    parser.add_argument("--media-name", action="append", dest="media_names")
    parser.add_argument(
        "--all-media",
        action="store_true",
        help="Expand to all visible leaf media ids (type=3); actual count depends on token permissions.",
    )
    parser.add_argument("--dataset", action="append", dest="datasets", help="Explicit dataset id, repeatable.")
    parser.add_argument("--months-back", type=int, default=1, help="Use the latest N visible datasets if --dataset is omitted.")
    parser.add_argument("--indicator", action="append", dest="indicators")
    parser.add_argument("--chart", action="append", dest="charts")
    parser.add_argument("--ad-spot-type-name", action="append", dest="ad_spot_type_names")
    parser.add_argument("--payload-out", help="Optional path to write the resolved payload.")
    parser.add_argument("--session-file", help="Optional path to persist the login session.")
    parser.add_argument("--dry-run", action="store_true", help="Resolve payload and coin cost, but do not create the task.")
    return parser


def load_token(args: argparse.Namespace) -> str:
    if args.token:
        return args.token.strip()
    if args.token_file:
        return Path(args.token_file).read_text(encoding="utf-8").strip()
    env_token = os.environ.get("MEDIAINSIGHT_MCP_TOKEN", "").strip()
    if env_token:
        return env_token
    return DEFAULT_DEMO_TOKEN


def normalize_name(value: str) -> str:
    normalized = value.strip().lower().replace(" ", "")
    normalized = re.sub(r"[省市区县特别行政自治区回族维吾尔壮族土家族苗族蒙古族藏族朝鲜族哈萨克族柯尔克孜族傣族白族自治州盟]+$", "", normalized)
    return normalized


def flatten_tree(nodes: list[dict[str, Any]]) -> list[dict[str, Any]]:
    flattened: list[dict[str, Any]] = []
    for node in nodes:
        flattened.append(node)
        children = node.get("children")
        if isinstance(children, list) and children:
            flattened.extend(flatten_tree(children))
    return flattened


def collapse_same_id(items: list[dict[str, Any]]) -> list[dict[str, Any]]:
    deduped: dict[str, dict[str, Any]] = {}
    for item in items:
        item_id = str(item.get("id", ""))
        if not item_id:
            continue
        current = deduped.get(item_id)
        if current is None or int(item.get("type", -1)) > int(current.get("type", -1)):
            deduped[item_id] = item
    return list(deduped.values())


def flatten_ta(nodes: list[dict[str, Any]]) -> list[dict[str, Any]]:
    flattened = flatten_tree(nodes)
    return [node for node in flattened if isinstance(node.get("id"), str) and node.get("name")]


def collect_media_leaf_ids(nodes: list[dict[str, Any]]) -> list[str]:
    leaf_ids: list[str] = []
    for node in nodes:
        children = node.get("children")
        if isinstance(children, list) and children:
            leaf_ids.extend(collect_media_leaf_ids(children))
            continue
        node_id = node.get("id")
        node_type = node.get("type")
        if isinstance(node_id, str) and node_id and node_type == 3:
            leaf_ids.append(node_id)
    return leaf_ids


def collect_media_root_ids(nodes: list[dict[str, Any]]) -> list[str]:
    return [str(node["id"]) for node in nodes if isinstance(node, dict) and node.get("type") == 1 and node.get("id")]


def match_one(items: list[dict[str, Any]], target: str, label: str) -> dict[str, Any]:
    raw_target = target.strip()
    exact_raw = collapse_same_id([item for item in items if str(item.get("name", "")).strip() == raw_target])
    if len(exact_raw) == 1:
        return exact_raw[0]
    if len(exact_raw) > 1:
        raise MediaInsightError(f"{label} name '{target}' is ambiguous")

    normalized_target = normalize_name(target)
    exact = collapse_same_id(
        [item for item in items if normalize_name(str(item.get("name", ""))) == normalized_target]
    )
    if len(exact) == 1:
        return exact[0]
    if len(exact) > 1:
        raise MediaInsightError(f"{label} name '{target}' is ambiguous")

    partial = collapse_same_id(
        [item for item in items if normalized_target in normalize_name(str(item.get("name", "")))]
    )
    if len(partial) == 1:
        return partial[0]
    if not partial:
        raise MediaInsightError(f"{label} name '{target}' is not visible for the current token")
    raise MediaInsightError(f"{label} name '{target}' matches multiple visible options")


def match_many(items: list[dict[str, Any]], targets: list[str], label: str) -> list[dict[str, Any]]:
    return [match_one(items, target, label) for target in targets]


def pick_datasets(visible: list[str], requested: list[str] | None, months_back: int) -> str:
    if requested:
        missing = [dataset for dataset in requested if dataset not in visible]
        if missing:
            raise MediaInsightError(f"dataset(s) not visible for the current token: {', '.join(missing)}")
        return ",".join(requested)

    if months_back <= 0:
        raise MediaInsightError("--months-back must be positive")
    visible_datasets = sorted(
        [dataset for dataset in visible if isinstance(dataset, str) and dataset],
        reverse=True,
    )
    chosen = visible_datasets[:months_back]
    if not chosen:
        raise MediaInsightError("no visible datasets returned by task/data-set")
    return ",".join(sorted(chosen))


def parse_age_range(raw: str) -> tuple[int, int]:
    normalized = raw.strip().lower()
    if normalized in {"all", "any", "*"}:
        return 0, 200
    open_ended = re.fullmatch(r"\s*(\d{1,2})\s*(?:\+|岁及以上)\s*", raw)
    if open_ended:
        return int(open_ended.group(1)), 200
    match = re.fullmatch(r"\s*(\d{1,2})\s*-\s*(\d{1,2})\s*", raw)
    if not match:
        raise MediaInsightError("--age-range must look like 20-49, 20+, 20岁及以上, or be 'all'")
    start, end = int(match.group(1)), int(match.group(2))
    if start > end:
        raise MediaInsightError("--age-range start cannot be greater than end")
    return start, end


def parse_age_bucket(name: str) -> tuple[int, int] | None:
    closed_range = re.fullmatch(r"(\d{1,2})-(\d{1,2})岁", name)
    if closed_range:
        return int(closed_range.group(1)), int(closed_range.group(2))

    open_ended = re.fullmatch(r"(\d{1,2})岁及以上", name)
    if open_ended:
        start = int(open_ended.group(1))
        return start, 200

    under_cap = re.fullmatch(r"(\d{1,2})岁及以下", name)
    if under_cap:
        end = int(under_cap.group(1))
        return 0, end

    return None


def build_ta_info(ta_nodes: list[dict[str, Any]], gender: str, age_range: str) -> list[list[dict[str, Any]]]:
    flattened = flatten_ta(ta_nodes)
    gender_key = GENDER_ALIASES.get(gender.strip().lower(), gender.strip())
    ta_group: list[dict[str, Any]] = []

    if gender_key:
        gender_node = match_one(flattened, gender_key, "gender")
        ta_group.append({"id": gender_node["id"], "type": int(gender_node["type"])})
    else:
        all_gender_nodes = []
        for node in flattened:
            name = str(node.get("name", "")).strip()
            if name in {"男", "女"}:
                all_gender_nodes.append({"id": node["id"], "type": int(node["type"])})
        deduped: dict[tuple[str, int], dict[str, Any]] = {}
        for node in all_gender_nodes:
            deduped[(str(node["id"]), int(node["type"]))] = node
        ta_group.extend(deduped.values())

    start_age, end_age = parse_age_range(age_range)
    for node in flattened:
        name = str(node.get("name", ""))
        bucket = parse_age_bucket(name)
        if bucket is None:
            continue
        bucket_start, bucket_end = bucket
        if bucket_end < start_age or bucket_start > end_age:
            continue
        ta_group.append({"id": node["id"], "type": int(node["type"])})

    deduped_group: dict[tuple[str, int], dict[str, Any]] = {}
    for node in ta_group:
        deduped_group[(str(node["id"]), int(node["type"]))] = node

    if not deduped_group:
        raise MediaInsightError("TA resolution produced an empty audience group")
    return [list(deduped_group.values())]


def device_ids_from_args(raw_devices: list[str] | None) -> list[int]:
    requested = raw_devices or ["pc", "mobile"]
    resolved: list[int] = []
    for raw in requested:
        key = raw.strip().lower()
        if key not in DEVICE_IDS:
            raise MediaInsightError(f"unsupported device '{raw}'")
        resolved.append(DEVICE_IDS[key])
    return sorted(set(resolved))


def resolve_payload(client: MediaInsightClient, args: argparse.Namespace) -> dict[str, Any]:
    task_name = args.task_name
    if args.task_name_unique:
        suffix = datetime.now().strftime("%Y%m%d-%H%M%S")
        task_name = f"{task_name}-{suffix}"

    datasets_payload = client.task_data_set()
    visible_datasets = datasets_payload.get("data", [])
    if not isinstance(visible_datasets, list):
        raise MediaInsightError("task/data-set returned an unexpected payload")

    industries_payload = client.dict_industry()
    visible_industries = flatten_tree(industries_payload.get("data", []))
    industry = match_one(visible_industries, args.industry_name, "industry")

    advertisers_payload = client.dict_adviser()
    visible_advertisers = advertisers_payload.get("data", [])
    if not isinstance(visible_advertisers, list):
        raise MediaInsightError("dict/adviser returned an unexpected payload")
    advertiser = match_one(visible_advertisers, args.advertiser_name, "advertiser")

    brands_payload = client.dict_brand(advertiser["id"])
    visible_brands = brands_payload.get("data", [])
    if not isinstance(visible_brands, list):
        raise MediaInsightError("dict/brand returned an unexpected payload")
    brand = match_one(visible_brands, args.brand_name, "brand")

    regions_payload = client.dict_region()
    visible_regions = flatten_tree(regions_payload.get("data", []))
    regions = match_many(visible_regions, args.region_names, "region")

    ta_payload = client.dict_ta()
    visible_ta = ta_payload.get("data", [])
    if not isinstance(visible_ta, list):
        raise MediaInsightError("dict/ta returned an unexpected payload")

    media_payload = client.dict_media()
    media_nodes = media_payload.get("data", [])
    if not isinstance(media_nodes, list):
        raise MediaInsightError("dict/media returned an unexpected payload")
    visible_media = flatten_tree(media_nodes)
    media_leaf_ids = collect_media_leaf_ids(media_nodes)
    if args.all_media:
        resolved_media_ids = media_leaf_ids
    else:
        if not args.media_names:
            resolved_media_ids = collect_media_root_ids(media_nodes)
            if not resolved_media_ids:
                raise MediaInsightError("no visible top-level media categories returned by dict/media")
        else:
            matched_media = match_many(visible_media, args.media_names, "media")
            resolved_media_ids = [str(item["id"]) for item in matched_media]

    campaign_type_ids: list[str] = []
    if args.campaign_type_names:
        campaign_types_payload = client.dict_campaign_type()
        visible_campaign_types = campaign_types_payload.get("data", [])
        if not isinstance(visible_campaign_types, list):
            raise MediaInsightError("dict/campaign-type returned an unexpected payload")
        campaign_type_ids = [str(item["id"]) for item in match_many(visible_campaign_types, args.campaign_type_names, "campaign type")]

    ad_spot_type_ids: list[str] = []
    if args.ad_spot_type_names:
        ad_spot_types_payload = client.dict_ad_spot_type()
        visible_ad_spot_types = ad_spot_types_payload.get("data", [])
        if not isinstance(visible_ad_spot_types, list):
            raise MediaInsightError("dict/ad-spot-type returned an unexpected payload")
        ad_spot_type_ids = [str(item["id"]) for item in match_many(visible_ad_spot_types, args.ad_spot_type_names, "ad spot type")]

    payload = {
        "name": task_name,
        "advertiserStid": str(advertiser["id"]),
        "brandStidList": [str(brand["id"])],
        "regionInfo": {
            "list": [str(item["id"]) for item in regions],
            "isPackage": False,
        },
        "taInfoList": build_ta_info(visible_ta, args.gender, args.age_range),
        "reportArgsAd": {
            "dataSet": pick_datasets(visible_datasets, args.datasets, args.months_back),
            "industryInfo": {
                "list": [str(industry["id"])],
                "isPackage": False,
            },
            "campaignInfo": {
                "list": campaign_type_ids,
                "isPackage": False,
            },
            "deviceList": device_ids_from_args(args.devices),
            "mediaList": resolved_media_ids,
            "adSpotTypeList": {
                "list": ad_spot_type_ids,
                "isPackage": False,
            },
            "indicators": args.indicators or DEFAULT_INDICATORS,
            "charts": args.charts or DEFAULT_CHARTS,
        },
    }
    return payload


def ensure_success(response: Any, action: str) -> dict[str, Any]:
    if not isinstance(response, dict):
        raise MediaInsightError(f"{action} returned an unexpected payload")
    code = response.get("code")
    if code not in (0, "0", None):
        message = response.get("msg") or response.get("message") or "unknown error"
        raise MediaInsightError(f"{action} failed: {message}")
    return response


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    using_demo_token = not (
        args.token
        or args.token_file
        or os.environ.get("MEDIAINSIGHT_MCP_TOKEN", "").strip()
    )

    session_file = Path(args.session_file) if args.session_file else None
    if session_file is None:
        tmp = NamedTemporaryFile(prefix="mediainsight-skill-", suffix=".json", delete=False)
        tmp.close()
        session_file = Path(tmp.name)

    try:
        if using_demo_token:
            print(
                "Using the public shared demo token with limited permissions. It may expire at any time; switch to your own MEDIAINSIGHT_MCP_TOKEN or --token for broader coverage.",
                file=sys.stderr,
            )
        auth = resolve_media_insight_auth(load_token(args), mcp_url=args.mcp_url, mcp_token_type=args.mcp_token_type)
        client = MediaInsightClient(
            base_url=args.base_url,
            session_file=session_file,
            ttc_token=auth.get("token"),
        )
        login_payload: dict[str, Any] = {"code": 0, "msg": "success", "mode": auth["mode"], "tokenSource": "demo" if using_demo_token else "user"}
        if args.tenant_id:
            ensure_success(client.switch_tenant(args.tenant_id), "switch tenant")

        payload = resolve_payload(client, args)
        if args.payload_out:
            Path(args.payload_out).write_text(
                json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
                encoding="utf-8",
            )

        coin = ensure_success(client.task_calculate_coin(payload), "calculate coin")
        output: dict[str, Any] = {
            "login": login_payload,
            "session_file": str(session_file),
            "resolvedPayload": payload,
            "coin": coin,
        }
        if not args.dry_run:
            output["create"] = ensure_success(client.task_add(payload), "create task")
        print(json.dumps(output, ensure_ascii=False, indent=2))
        return 0
    except MediaInsightError as exc:
        print(str(exc), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
