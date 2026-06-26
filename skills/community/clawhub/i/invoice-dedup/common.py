#!/usr/bin/env python3
"""发票技能公共函数 - 供所有发票技能脚本共用"""

import io
import json
import os
import re
import sys
import urllib.request
import urllib.error
import uuid

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

BASE_URL = "https://skill.quandianfapiao.com"

MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB

def post(path: str, data: dict) -> dict:
    url = f"{BASE_URL}{path}"
    body = json.dumps(data).encode("utf-8")
    req = urllib.request.Request(
        url,
        data=body,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        body_text = e.read().decode("utf-8", errors="replace")
        try:
            return json.loads(body_text)
        except json.JSONDecodeError:
            return {"status": str(e.code), "message": body_text}
    except urllib.error.URLError as e:
        return {"status": "-1", "message": str(e.reason)}


def post_file(path: str, api_key: str, file_path: str) -> dict:
    file_size = os.path.getsize(file_path)
    if file_size > MAX_FILE_SIZE:
        return {"status": "-1",
                "message": f"文件过大: {file_size / 1024 / 1024:.1f}MB，上限 10MB"}
    boundary = uuid.uuid4().hex
    file_name = os.path.basename(file_path)
    with open(file_path, "rb") as f:
        file_data = f.read()
    parts = []
    parts.append(
        f"--{boundary}\r\n"
        f'Content-Disposition: form-data; name="apiKey"\r\n'
        f"\r\n{api_key}\r\n".encode()
    )
    parts.append(
        f"--{boundary}\r\n"
        f'Content-Disposition: form-data; name="file"; filename="{file_name}"\r\n'
        f"Content-Type: application/octet-stream\r\n"
        f"\r\n".encode()
    )
    parts.append(file_data)
    parts.append(f"\r\n--{boundary}--\r\n".encode())
    body = b"".join(parts)
    url = f"{BASE_URL}{path}"
    req = urllib.request.Request(
        url,
        data=body,
        headers={"Content-Type": f"multipart/form-data; boundary={boundary}"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        body_text = e.read().decode("utf-8", errors="replace")
        try:
            return json.loads(body_text)
        except json.JSONDecodeError:
            return {"status": str(e.code), "message": body_text}
    except urllib.error.URLError as e:
        return {"status": "-1", "message": str(e.reason)}


def is_error(result: dict) -> str:
    if result.get("status") != "200":
        return f"[错误] {result.get('message', '未知错误')} (status={result.get('status')})"
    return ""


def fmt_items(items: list) -> list:
    lines = []
    for i, item in enumerate(items, 1):
        lines.append(f"        [{i}] {item.get('projectName', '-')}")
        lines.append(
            f"            规格: {item.get('ggxh') or '-'}  "
            f"单位: {item.get('projectUnit') or '-'}  "
            f"数量: {item.get('projectCount') or '-'}"
        )
        lines.append(
            f"            单价: {item.get('projectPriceEt', '-')}  "
            f"金额: {item.get('projectJeEt', '-')}  "
            f"税率: {item.get('sl', '-')}  "
            f"税额: {item.get('se', '-')}"
        )
    return lines


def fmt_invoice_basic(d: dict) -> list:
    lines = [
        f"  发票类型: {d.get('invoiceType', '-')}",
        f"  发票代码: {d.get('invoiceCode') or '-'}",
        f"  发票号码: {d.get('invoiceNumber', '-')}",
        f"  开票日期: {d.get('invoiceDate', '-')}",
        f"  合计金额: {d.get('hjje', '-')}  合计税额: {d.get('hjse', '-')}  价税合计: {d.get('jshj', '-')}",
        f"  销方名称: {d.get('xsfMc', '-')}",
        f"  销方税号: {d.get('xsfNsrsbh', '-')}",
        f"  销方地址电话: {d.get('xsfAddressTel') or '-'}",
        f"  销方开户行: {d.get('xsfBankAccount') or '-'}",
        f"  购方名称: {d.get('gmfMc', '-')}",
        f"  购方税号: {d.get('gmfNsrsbh', '-')}",
        f"  购方地址电话: {d.get('gmfAddressTel') or '-'}",
        f"  购方开户行: {d.get('gmfBankAccount') or '-'}",
    ]
    return lines


_DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")


def validate_date(value: str, field: str = "日期") -> str:
    if not _DATE_RE.match(value):
        return f"[错误] {field}格式不正确: {value}，需要 YYYY-MM-DD"
    return ""
