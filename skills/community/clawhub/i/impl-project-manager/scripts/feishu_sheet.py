#!/usr/bin/env python3
"""飞书表格操作 — 读取和更新项目管理在线表格"""

import json
import os
import sys
import urllib.parse

# 导入基础 API
sys.path.insert(0, os.path.dirname(__file__))
from feishu_api import api_request, get_token

# 飞书表格 API
SHEET_API_BASE = "https://open.feishu.cn/open-apis/sheets/v3/spreadsheets"


def read_sheet(spreadsheet_token, sheet_id=None, range_str=None):
    """
    读取飞书在线表格数据

    Args:
        spreadsheet_token: 表格 token（从表格 URL 获取）
        sheet_id: 工作表 ID（可选，默认第一个）
        range_str: 读取范围（如 "A1:F10"），可选
    """
    url = f"{SHEET_API_BASE}/{spreadsheet_token}/values"

    params = {}
    if sheet_id:
        params["sheetId"] = sheet_id
    if range_str:
        if sheet_id:
            params["range"] = f"{sheet_id}!{range_str}"
        else:
            params["range"] = range_str

    if params:
        url += "?" + urllib.parse.urlencode(params)

    result = api_request(url)
    return result


def write_sheet(spreadsheet_token, sheet_id, range_str, values):
    """
    写入飞书在线表格数据

    Args:
        spreadsheet_token: 表格 token
        sheet_id: 工作表 ID
        range_str: 写入范围（如 "A1:F10"）
        values: 二维数组数据
    """
    url = f"{SHEET_API_BASE}/{spreadsheet_token}/values"

    body = {
        "valueRange": {
            "range": f"{sheet_id}!{range_str}" if sheet_id else range_str,
            "values": values
        }
    }

    result = api_request(url, method="PUT", body=body)
    return result


def batch_update(spreadsheet_token, requests):
    """
    批量更新表格（设置格式、公式等）

    Args:
        spreadsheet_token: 表格 token
        requests: 批量请求列表
    """
    url = f"{SHEET_API_BASE}/{spreadsheet_token}/batchUpdate"

    body = {"requests": requests}
    result = api_request(url, method="POST", body=body)
    return result


def create_spreadsheet(title):
    """
    创建新飞书表格，并自动设置编辑权限

    Args:
        title: 表格标题

    Returns:
        dict: 包含 spreadsheet_token, url, folder_token 等
    """
    # 创建表格
    result = api_request(SHEET_API_BASE, method="POST", body={"title": title})
    if result.get("code") != 0:
        return result

    spreadsheet = result.get("data", {}).get("spreadsheet", {})
    sp_token = spreadsheet.get("spreadsheet_token")

    # 自动设置编辑权限：组织内可编辑
    set_edit_permission(sp_token)

    return result


def set_edit_permission(spreadsheet_token):
    """
    设置表格为组织内可编辑权限

    Args:
        spreadsheet_token: 表格 token

    Returns:
        bool: 是否设置成功
    """
    import requests

    token = get_token()
    url = f"https://open.feishu.cn/open-apis/drive/v1/permissions/{spreadsheet_token}/public?type=sheet"
    resp = requests.patch(
        url,
        headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"},
        json={"link_share_entity": "tenant_editable"},
        timeout=10,
    )
    result = resp.json()
    success = result.get("code") == 0
    if not success:
        print(f"⚠️ 设置编辑权限失败: {result.get('msg')}", file=sys.stderr)
    return success


def create_project_sheets(spreadsheet_token):
    """
    为项目表格创建标准5个Sheet（项目总览、合同回款、分包付款、变更记录、风险清单）
    并自动设置编辑权限

    Args:
        spreadsheet_token: 表格 token

    Returns:
        dict: {sheet_name: sheet_id}
    """
    sheet_names = ["合同回款", "分包付款", "变更记录", "风险清单"]
    sheet_ids = {}

    for name in sheet_names:
        result = api_request(
            f"{SHEET_API_BASE}/{spreadsheet_token}/sheets",
            method="POST",
            body={"title": name},
        )
        if result.get("code") == 0:
            sheet_ids[name] = result["data"]["sheet"]["sheet_id"]

    return sheet_ids


def list_sheets(spreadsheet_token):
    """获取表格中的所有工作表信息"""
    url = f"{SHEET_API_BASE}/{spreadsheet_token}/sheets"
    result = api_request(url)
    return result


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("用法:")
        print("  python feishu_sheet.py read <spreadsheet_token> [range]")
        print("  python feishu_sheet.py list <spreadsheet_token>")
        print("  python feishu_sheet.py write <spreadsheet_token> <sheet_id> <range> <json_data>")
        sys.exit(1)

    action = sys.argv[1]
    token = sys.argv[2]

    if action == "read":
        range_str = sys.argv[3] if len(sys.argv) > 3 else None
        result = read_sheet(token, range_str=range_str)
        print(json.dumps(result, ensure_ascii=False, indent=2))

    elif action == "list":
        result = list_sheets(token)
        print(json.dumps(result, ensure_ascii=False, indent=2))

    elif action == "write":
        sheet_id = sys.argv[3]
        range_str = sys.argv[4]
        data = json.loads(sys.argv[5])
        result = write_sheet(token, sheet_id, range_str, data)
        print(json.dumps(result, ensure_ascii=False, indent=2))

    else:
        print(f"未知动作: {action}", file=sys.stderr)
        sys.exit(1)