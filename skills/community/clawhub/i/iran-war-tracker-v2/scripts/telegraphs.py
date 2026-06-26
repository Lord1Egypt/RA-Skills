#!/usr/bin/env python3
"""Fetch full CLS Telegraph and Jin10 flash content without filtering."""

from __future__ import annotations

import argparse
import hashlib
import io
import json
import sys
import time
from pathlib import Path
from typing import Any

import pandas as pd
import requests


DEFAULT_TIMEOUT = 20
DEFAULT_RN = 2000
CLS_URL = "https://www.cls.cn/nodeapi/telegraphList"
JIN10_URL = "https://flash-api.jin10.com/get_flash_list?channel=-8200&vip=1"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Fetch full CLS Telegraph and Jin10 flash records without filtering."
    )
    parser.add_argument("--output", help="Optional path to write JSON output.")
    parser.add_argument(
        "--limit", type=int, help="Optional limit for the number of records to return."
    )
    parser.add_argument(
        "--rn",
        type=int,
        default=DEFAULT_RN,
        help="CLS API rn parameter. Default: 2000.",
    )
    parser.add_argument(
        "--timeout",
        type=int,
        default=DEFAULT_TIMEOUT,
        help="Request timeout in seconds.",
    )
    parser.add_argument(
        "--source",
        choices=["all", "cls", "jin10"],
        default="all",
        help="Select data source. Default: all.",
    )
    parser.add_argument(
        "--format",
        choices=["raw", "normalized"],
        default="raw",
        help="Output raw payloads or normalized fields. Default: raw.",
    )
    parser.add_argument(
        "--hours",
        type=int,
        default=2,
        help="Filter records from the last N hours. Default: 2 (0 means no time limit).",
    )
    return parser.parse_args()


def get_session() -> requests.Session:
    session = requests.Session()
    session.headers.update({"User-Agent": "market-telegraph-fullfeed/0.1"})
    return session


def build_signed_params(
    session: requests.Session, rn: int, timeout: int
) -> dict[str, Any]:
    current_time = int(time.time())
    params: dict[str, Any] = {
        "app": "CailianpressWeb",
        "category": "",
        "lastTime": current_time,
        "last_time": current_time,
        "os": "web",
        "refresh_type": "1",
        "rn": str(rn),
        "sv": "7.7.5",
    }
    query_string = session.get(CLS_URL, params=params, timeout=timeout).url.split(
        "?", 1
    )[1]
    sha1 = hashlib.sha1(query_string.encode("utf-8")).hexdigest()
    params["sign"] = hashlib.md5(sha1.encode("utf-8")).hexdigest()
    return params


def fetch_raw_records(
    session: requests.Session, rn: int, timeout: int
) -> list[dict[str, Any]]:
    params = build_signed_params(session, rn=rn, timeout=timeout)
    response = session.get(
        CLS_URL,
        params=params,
        headers={
            "Accept": "application/json, text/plain, */*",
            "Referer": "https://www.cls.cn/telegraph",
            "User-Agent": "Mozilla/5.0",
        },
        timeout=timeout,
    )
    response.raise_for_status()
    payload = response.json()
    data = payload.get("data", {})
    records = data.get("roll_data", [])
    if not isinstance(records, list):
        raise ValueError("Unexpected CLS response: data.roll_data is not a list")
    return [record for record in records if isinstance(record, dict)]


def fetch_jin10_payload(session: requests.Session, timeout: int) -> dict[str, Any]:
    headers = {
        "accept": "application/json, text/plain, */*",
        "accept-language": "zh-CN,zh;q=0.9,en;q=0.8,zh-TW;q=0.7",
        "content-type": "application/x-www-form-urlencoded",
        "cookie": "kind_g=%5B%223%22%5D; trend=1; Hm_lvt_522b01156bb16b471a7e2e6422d272ba=1774666362; HMACCOUNT=A36A0D3680700ED3; UM_distinctid=19d325bac30a26-0656d1d154b8928-26061f51-295d29-19d325bac3120d4; x-token=; env=prod; did=ebd69ed7-4348-4fdc-9cfe-35ddfaee42bc; CALENDAR_FAVOR_INDEX_LIST=%5B%5D; Hm_lpvt_522b01156bb16b471a7e2e6422d272ba=1774667075",
        "handleerror": "true",
        "origin": "https://www.jin10.com",
        "priority": "u=1, i",
        "referer": "https://www.jin10.com/",
        "sec-ch-ua": '"Chromium";v="146", "Not-A.Brand";v="24", "Google Chrome";v="146"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-site",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36",
        "x-app-id": "bVBF4FyRTn5NJF5n",
        "x-version": "1.0.0",
    }
    response = session.get(JIN10_URL, headers=headers, timeout=timeout)
    response.raise_for_status()
    payload = response.json()
    if not isinstance(payload, dict):
        raise ValueError("Unexpected Jin10 response: payload is not an object")
    return payload


def normalize_records(
    records: list[dict[str, Any]], hours: int = 0
) -> list[dict[str, Any]]:
    if not records:
        return []

    df = pd.DataFrame(records)
    for column in ["title", "content", "level", "subjects", "ctime"]:
        if column not in df.columns:
            df[column] = None

    normalized = df[["title", "content", "level", "subjects", "ctime"]].copy()
    normalized["ctime"] = pd.to_datetime(
        normalized["ctime"], unit="s", utc=True, errors="coerce"
    ).dt.tz_convert("Asia/Shanghai")

    if hours > 0:
        cutoff_time = pd.Timestamp.now(tz="Asia/Shanghai") - pd.Timedelta(hours=hours)
        normalized = normalized[normalized["ctime"] >= cutoff_time]

    normalized["tags"] = [
        [tag.get("subject_name", "") for tag in subjects if isinstance(tag, dict)]
        if isinstance(subjects, list)
        else []
        for subjects in normalized["subjects"].tolist()
    ]
    normalized["date"] = normalized["ctime"].dt.strftime("%Y-%m-%d")
    normalized["time"] = normalized["ctime"].dt.strftime("%H:%M:%S")
    normalized["ctime"] = normalized["ctime"].dt.strftime("%Y-%m-%dT%H:%M:%S%z")
    normalized = normalized.drop(columns=["subjects"])
    return normalized.where(pd.notna(normalized), None).to_dict("records")


def normalize_jin10_payload(
    payload: dict[str, Any], limit: int | None = None, hours: int = 0
) -> dict[str, Any]:
    records = payload.get("data", [])
    if not isinstance(records, list):
        raise ValueError("Unexpected Jin10 response: data is not a list")

    cutoff_time = None
    if hours > 0:
        cutoff_time = pd.Timestamp.now(tz="Asia/Shanghai") - pd.Timedelta(hours=hours)

    flash_list: list[dict[str, Any]] = []
    for item in records:
        if not isinstance(item, dict):
            continue
        item_time = item.get("time")

        if hours > 0 and item_time and cutoff_time is not None:
            try:
                item_ts = pd.to_datetime(
                    item_time, utc=True, errors="coerce"
                ).tz_convert("Asia/Shanghai")
                if pd.isna(item_ts) or item_ts < cutoff_time:
                    continue
            except Exception:
                pass

        item_data = item.get("data", {})
        if not isinstance(item_data, dict):
            item_data = {}
        flash_list.append(
            {
                "id": item.get("id"),
                "time": item.get("time"),
                "type": item.get("type"),
                "important": item.get("important"),
                "channel": item.get("channel", []),
                "tags": item.get("tags", []),
                "title": item_data.get("title"),
                "content": item_data.get("content"),
                "source": item_data.get("source"),
                "source_link": item_data.get("source_link"),
                "pic": item_data.get("pic"),
                "remark": item.get("remark", []),
                "extras": item.get("extras", {}),
            }
        )

    if limit is not None:
        flash_list = flash_list[:limit]

    return {
        "status": payload.get("status"),
        "message": payload.get("message"),
        "items": flash_list,
        "item_count": len(flash_list),
    }


def limit_jin10_raw_payload(
    payload: dict[str, Any], limit: int | None = None
) -> dict[str, Any]:
    if limit is None:
        return payload
    copied = dict(payload)
    data = copied.get("data", [])
    if isinstance(data, list):
        copied["data"] = data[:limit]
    return copied


def build_payload(
    session: requests.Session,
    source: str,
    output_format: str,
    rn: int,
    timeout: int,
    limit: int | None,
    hours: int,
) -> Any:
    payload: dict[str, Any] = {"source": source, "format": output_format}

    if source in {"all", "cls"}:
        cls_records = fetch_raw_records(session, rn=rn, timeout=timeout)
        if limit is not None:
            cls_records = cls_records[:limit]
        payload["cls"] = (
            normalize_records(cls_records, hours=hours)
            if output_format == "normalized"
            else cls_records
        )

    if source in {"all", "jin10"}:
        jin10_payload = fetch_jin10_payload(session, timeout=timeout)
        payload["jin10"] = (
            normalize_jin10_payload(jin10_payload, limit=limit, hours=hours)
            if output_format == "normalized"
            else limit_jin10_raw_payload(jin10_payload, limit=limit)
        )

    if source == "cls":
        return payload["cls"]
    if source == "jin10":
        return payload["jin10"]
    return payload


def emit_output(payload: Any, output: str | None) -> None:
    content = json.dumps(payload, ensure_ascii=False, indent=2)
    if output:
        output_path = Path(output)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(content, encoding="utf-8")
        return
    print(content)


def main() -> int:
    args = parse_args()
    session = get_session()
    payload = build_payload(
        session=session,
        source=args.source,
        output_format=args.format,
        rn=args.rn,
        timeout=args.timeout,
        limit=args.limit,
        hours=args.hours,
    )
    emit_output(payload, args.output)
    return 0


if __name__ == "__main__":
    if sys.platform == "win32":
        sys.stdout = io.TextIOWrapper(
            sys.stdout.buffer, encoding="utf-8", errors="replace"
        )
    raise SystemExit(main())
