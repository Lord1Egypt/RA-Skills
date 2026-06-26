#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import argparse
from datetime import datetime

import json
import urllib.error
import urllib.request


RECORD_API_URL = "https://shangbao.yunzhisheng.cn/skills/record-gen/gen_record_by_diag_v1"


def call_record_api(diag_id: str, dialogue: str, timeout: int = 0) -> str:
    """
    调用公司接口，生成初诊门诊病历（最终记录）。
    """
    payload = {
        "diag_id": diag_id,
        "dep_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "diag": dialogue,
    }
    try:
        data_bytes = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        req = urllib.request.Request(
            url=RECORD_API_URL,
            data=data_bytes,
            method="POST",
            headers={"Content-Type": "application/json"},
        )
        if timeout and timeout > 0:
            resp_ctx = urllib.request.urlopen(req, timeout=timeout)
        else:
            resp_ctx = urllib.request.urlopen(req)
        with resp_ctx as resp:
            body = resp.read().decode("utf-8", errors="replace")

        # 优先按 JSON 解析，以便后续扩展
        data = json.loads(body)
        record = data.get("record") or data.get("result") or data.get("data")
        if record:
            return record
        return body
    except json.JSONDecodeError:
        # 非 JSON，直接返回文本
        return body
    except urllib.error.HTTPError as e:
        detail = e.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"HTTP {e.code}: {detail}") from e
    except urllib.error.URLError as e:
        raise RuntimeError(f"Network error: {e}") from e


def generate_initial_record(
    input_path: str,
    output_path: str,
    timeout: int = 0,
    diag_id: str = "skill-diag",
) -> str:
    """
    从输入对话文件生成门诊初诊病历并保存。
    :param input_path: 输入对话文本文件路径
    :param output_path: 输出病历文件路径
    :param timeout: 请求超时时间（秒）
    :return: 输出文件路径
    """
    if not os.path.exists(input_path):
        # 兼容：如果只传文件名且当前目录不存在，则尝试 skills/data/med-initial-record-gen/<name>
        base_name = os.path.basename(input_path)
        fallback = os.path.join(os.path.dirname(__file__), "..", "..", "data", "med-initial-record-gen", base_name)
        if os.path.exists(fallback):
            input_path = fallback
        else:
            raise FileNotFoundError(f"Input file not found: {input_path}")

    with open(input_path, "r", encoding="utf-8") as f:
        dialogue_text = f.read()

    print(f"Generating initial visit record from dialogue: {input_path}")
    # 直接调用生成病历接口
    record_text = call_record_api(diag_id=diag_id, dialogue=dialogue_text, timeout=timeout)

    out_dir = os.path.dirname(output_path) or "."
    os.makedirs(out_dir, exist_ok=True)

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(record_text)

    print(f"✓ Record saved to: {output_path}")
    return output_path


def main():
    parser = argparse.ArgumentParser(
        description="Generate outpatient initial visit medical record from doctor-patient dialogue."
    )

    parser.add_argument(
        "--input",
        required=True,
        help="Path to ASR dialogue text file (UTF-8)."
    )

    parser.add_argument(
        "--output",
        default="",
        help="Output path for generated medical record (default: ../runs/med-initial-record-gen/record.txt)."
    )

    parser.add_argument(
        "--diag-id",
        default="skill-diag",
        help="Dialogue ID used for backend services (default: skill-diag)."
    )

    parser.add_argument(
        "--timeout",
        type=int,
        default=0,
        help="HTTP request timeout seconds. 0 means wait forever (default: 0)."
    )

    args = parser.parse_args()

    try:
        default_out = os.path.join("..", "runs", "med-initial-record-gen", "record.txt")
        out_path = args.output or default_out
        generate_initial_record(
            input_path=args.input,
            output_path=out_path,
            timeout=args.timeout,
            diag_id=args.diag_id,
        )
        print("\n✓ Initial visit record generated successfully!")
        return 0
    except FileNotFoundError as e:
        print(f"✗ Error: {e}", file=sys.stderr)
        return 1
    except Exception as e:
        print(f"✗ Unexpected Error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())

