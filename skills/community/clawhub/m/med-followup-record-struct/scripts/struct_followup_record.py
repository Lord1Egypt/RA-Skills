#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import json
import argparse
from typing import Any, Dict

import urllib.error
import urllib.request


API_URL = "https://shangbao.yunzhisheng.cn/skills/record-struct/gen_abstract_by_his"


def _read_http_body(resp: Any) -> str:
    return resp.read().decode("utf-8", errors="replace")


def _post_json(url: str, payload: Dict[str, Any], *, timeout: int = 0) -> str:
    # 兼容部分服务端对非 ASCII JSON 处理不一致：这里使用 ASCII JSON（\uXXXX）编码
    data_bytes = json.dumps(payload, ensure_ascii=True).encode("utf-8")
    req = urllib.request.Request(
        url=url,
        data=data_bytes,
        method="POST",
        headers={
            "Content-Type": "application/json; charset=utf-8",
            "Accept": "application/json",
        },
    )
    try:
        if timeout and timeout > 0:
            ctx = urllib.request.urlopen(req, timeout=timeout)
        else:
            ctx = urllib.request.urlopen(req)
        with ctx as resp:
            return _read_http_body(resp)
    except urllib.error.HTTPError as e:
        detail = e.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"HTTP {e.code}: {detail}") from e
    except urllib.error.URLError as e:
        raise RuntimeError(f"Network error: {e}") from e


def call_followup_struct_api(
    his_record: str,
    *,
    diag_id: str = "skill-diag",
    department: str = "",
    timeout: int = 0,
) -> Dict[str, Any]:
    """
    调用公司接口，对复诊病历进行结构化。
    :param his_record: 门诊复诊病历文本（his_record）
    :param timeout: 超时时间（秒）
    :return: 结构化结果（字典）
    """
    if not isinstance(his_record, str) or not his_record.strip():
        raise ValueError("his_record is required and must be non-empty.")

    payload: Dict[str, Any] = {
        "his_record": his_record,
        "diag_id": diag_id or "skill-diag",
    }
    if department:
        payload["department"] = department

    body = _post_json(API_URL, payload, timeout=timeout)

    try:
        data = json.loads(body)
    except json.JSONDecodeError:
        raise ValueError(f"Unexpected non-JSON response: {body[:500]}") from None

    # 假定接口返回字段 'structured' / 'result' / 'data' 中包含结构化结果
    structured = data.get("structured") or data.get("result") or data.get("data")
    if structured is None:
        raise ValueError(f"Unexpected API response: {data}")

    return structured


def struct_followup_record(
    input_path: str,
    output_path: str,
    timeout: int = 0,
    diag_id: str = "skill-diag",
    department: str = "",
) -> str:
    """
    将复诊病历结构化并保存为 JSON。
    :param input_path: 输入病历文件路径
    :param output_path: 输出 JSON 文件路径
    :param timeout: 超时时间（秒）
    :return: 输出文件路径
    """
    if not os.path.exists(input_path):
        base_name = os.path.basename(input_path)
        fallback = os.path.join(os.path.dirname(__file__), "..", "..", "data", "med-followup-record-struct", base_name)
        if os.path.exists(fallback):
            input_path = fallback
        else:
            raise FileNotFoundError(f"Input file not found: {input_path}")

    with open(input_path, "r", encoding="utf-8") as f:
        record_text = f.read()

    print(f"Structuring follow-up outpatient record: {input_path}")
    structured = call_followup_struct_api(record_text, diag_id=diag_id, department=department, timeout=timeout)

    out_dir = os.path.dirname(output_path) or "."
    os.makedirs(out_dir, exist_ok=True)

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(structured, f, ensure_ascii=False, indent=2)

    print(f"✓ Structured record saved to: {output_path}")
    return output_path


def main():
    parser = argparse.ArgumentParser(
        description="Structure outpatient follow-up medical record into fine-grained fields."
    )

    parser.add_argument(
        "--input",
        required=True,
        help="Path to outpatient follow-up record text file (UTF-8)."
    )

    parser.add_argument(
        "--output",
        default="",
        help="Output path for structured JSON (default: ../runs/med-followup-record-struct/structured.json)."
    )

    parser.add_argument(
        "--timeout",
        type=int,
        default=0,
        help="HTTP request timeout seconds. 0 means wait forever (default: 0)."
    )
    parser.add_argument("--diag-id", default="skill-diag", help="diag_id (default: skill-diag)")
    parser.add_argument("--department", default="", help="department (optional)")

    args = parser.parse_args()

    try:
        default_out = os.path.join("..", "runs", "med-followup-record-struct", "structured.json")
        out_path = args.output or default_out
        struct_followup_record(
            input_path=args.input,
            output_path=out_path,
            timeout=args.timeout,
            diag_id=args.diag_id,
            department=args.department,
        )
        print("\n✓ Follow-up record structured successfully!")
        return 0
    except FileNotFoundError as e:
        print(f"✗ Error: {e}", file=sys.stderr)
        return 1
    except Exception as e:
        print(f"✗ Unexpected Error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())

