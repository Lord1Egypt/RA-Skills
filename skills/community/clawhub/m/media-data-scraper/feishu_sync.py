#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
飞书多维表格同步模块
支持: 首次安装配置询问、数据自动推送、配置持久化
兼容: lark-cli (本机有集成) 和 纯HTTP API (其他智能体)

设计原则:
- 配置环节的对话不占用 scrape_post 的使用次数计数
- 首次使用时输出一次性提示，由调用方（智能体）向用户展示并收集回复
- 提供参数化配置接口 setup_config()，供智能体传入用户提供的参数
- 保留交互式配置 setup_config_interactive() 供支持 input() 的环境使用
"""

import os
import json
import subprocess
import shutil
from typing import Dict, List, Optional

# 配置文件路径
CONFIG_DIR = os.path.expanduser("~/.social_media_scraper")
CONFIG_FILE = os.path.join(CONFIG_DIR, "feishu_config.json")

# 默认字段映射（飞书多维表格字段名）
DEFAULT_FIELDS = [
    "平台", "作品标题", "作者", "链接", "播放量", "点赞数",
    "评论数", "分享数", "收藏数", "发布时间", "抓取时间"
]


def _load_config() -> Dict:
    """加载飞书配置"""
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception:
            pass
    return {
        "enabled": False,
        "configured": False,
        "base_token": "",
        "table_id": "",
        "app_id": "",
        "app_secret": "",
        "use_cli": True,  # True=lark-cli, False=HTTP API
    }


def _save_config(config: Dict):
    """保存飞书配置"""
    os.makedirs(CONFIG_DIR, exist_ok=True)
    with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
        json.dump(config, f, ensure_ascii=False, indent=2)


def has_lark_cli() -> bool:
    """检查是否有 lark-cli 命令"""
    return shutil.which("lark-cli") is not None


def is_configured() -> bool:
    """检查是否已完成飞书配置并启用"""
    config = _load_config()
    return config.get("configured", False) and config.get("enabled", False)


def is_prompted() -> bool:
    """检查是否已经询问过用户（无论用户是否配置）"""
    config = _load_config()
    return config.get("configured", False)


def get_first_time_prompt() -> str:
    """
    获取首次安装时的提示文案。
    由调用方（智能体）展示给用户，并收集用户回复。
    """
    return """
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📋 飞书多维表格同步（可选）
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

您可以将抓取的数据自动同步到飞书多维表格，方便统一管理。

• 自动记录每次抓取的平台、标题、作者、互动数据
• 支持多平台数据汇总分析
• 随时查看历史抓取记录

此功能完全可选，不影响核心抓取功能。

👉 如需配置，请对我说"配置飞书"
👉 如不需要，直接开始抓取即可，此提示不会再次显示
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
""".strip()


def get_config_guide() -> str:
    """获取飞书配置指引文案（用户主动说"配置飞书"时展示）"""
    cli_available = "✅ 已检测到" if has_lark_cli() else "❌ 未检测到"
    return f"""
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📋 飞书多维表格配置指引
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

{cli_available} lark-cli 命令

配置方式一（推荐，有 lark-cli 时）:
  1. 确保已安装飞书 CLI 工具: pip install lark-cli
  2. 完成登录授权: lark-cli auth login
  3. 创建或选择一个多维表格，复制其链接
  4. 提供 base_token（链接中 /base/ 后的部分）

配置方式二（无 lark-cli 时，使用 HTTP API）:
  1. 前往飞书开放平台 (open.feishu.cn) 创建应用
  2. 获取 App ID 和 App Secret
  3. 为应用添加"多维表格"权限（bitable:record）
  4. 提供 App ID、App Secret 和 Base Token

配置完成后，每次抓取的数据将自动推送到多维表格。
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
""".strip()


def setup_config(
    base_url: str,
    table_id: str = "",
    app_id: str = "",
    app_secret: str = "",
) -> Dict:
    """
    参数化配置飞书多维表格。

    由智能体调用：收集用户提供的参数后，直接传入本函数完成配置。
    无需依赖 input()，适合所有智能体环境。

    Args:
        base_url: 多维表格链接（如 https://xxx.feishu.cn/base/XXXXXX）
                  或直接传入 base_token 字符串
        table_id: 数据表 ID（可从表格URL的 table= 参数获取，可选）
        app_id: 飞书应用 App ID（无 lark-cli 时必填）
        app_secret: 飞书应用 App Secret（无 lark-cli 时必填）

    Returns:
        {"success": bool, "message": str, "config": dict}
    """
    config = _load_config()

    # 自动检测 lark-cli
    if has_lark_cli():
        config["use_cli"] = True
    else:
        config["use_cli"] = False
        if not app_id or not app_secret:
            return {
                "success": False,
                "message": "未检测到 lark-cli，且未提供 App ID / App Secret，无法完成配置。",
                "config": config,
            }

    # 提取 base_token
    base_token = _extract_base_token(base_url)
    if not base_token:
        return {
            "success": False,
            "message": f"无法从链接提取 base_token，请检查链接格式: {base_url}",
            "config": config,
        }

    config["base_token"] = base_token
    if table_id:
        config["table_id"] = table_id
    if app_id:
        config["app_id"] = app_id
    if app_secret:
        config["app_secret"] = app_secret

    config["enabled"] = True
    config["configured"] = True
    _save_config(config)

    mode = "lark-cli" if config["use_cli"] else "HTTP API"
    return {
        "success": True,
        "message": f"飞书多维表格配置完成！推送方式: {mode}",
        "config": {
            "base_token": base_token[:20] + "...",
            "table_id": table_id or "默认",
            "use_cli": config["use_cli"],
        },
    }


def setup_config_interactive() -> bool:
    """
    交互式配置飞书多维表格（支持 input() 的环境使用）。
    内部调用 setup_config() 完成实际配置。
    """
    config = _load_config()

    if has_lark_cli():
        print("✅ 检测到 lark-cli，将使用 CLI 方式推送数据")
    else:
        print("⚠️ 未检测到 lark-cli，将使用 HTTP API 方式")
        print("   如需使用 CLI 方式，请先安装: pip install lark-cli")

    print("\n" + get_config_guide())
    print("\n请提供以下信息（按提示输入）：")

    base_url = input("多维表格链接（如 https://xxx.feishu.cn/base/XXXXXX）: ").strip()
    if not base_url:
        print("❌ 未提供链接，配置取消")
        return False

    table_id = input("数据表 ID（可从表格URL的 table= 参数获取，或留空使用默认表）: ").strip()

    app_id = ""
    app_secret = ""
    if not has_lark_cli():
        app_id = input("飞书应用 App ID: ").strip()
        app_secret = input("飞书应用 App Secret: ").strip()

    result = setup_config(base_url, table_id, app_id, app_secret)
    if result["success"]:
        print("\n✅ " + result["message"])
        print(f"   Base Token: {result['config']['base_token']}")
        print(f"   数据推送: 已启用")
        print("\n提示：抓取数据后将自动同步到飞书多维表格")
        return True
    else:
        print("\n❌ " + result["message"])
        return False


def _extract_base_token(url: str) -> Optional[str]:
    """从飞书多维表格链接提取 base_token"""
    import re
    # 匹配 /base/xxxx 或 /base/xxxx?table=yyy
    match = re.search(r'/base/([a-zA-Z0-9]+)', url)
    if match:
        return match.group(1)
    # 直接输入token的情况
    if re.match(r'^[a-zA-Z0-9]{10,}$', url):
        return url
    return None


def _result_to_record(result: Dict) -> Dict:
    """将抓取结果转换为飞书记录格式"""
    record = {
        "平台": result.get("platform", ""),
        "作品标题": result.get("title", "") or "",
        "作者": result.get("author", "") or "",
        "链接": result.get("url", ""),
        "播放量": _fmt_num(result.get("views")),
        "点赞数": _fmt_num(result.get("likes")),
        "评论数": _fmt_num(result.get("comments")),
        "分享数": _fmt_num(result.get("shares")),
        "收藏数": _fmt_num(result.get("collects")),
        "发布时间": result.get("publish_time", "") or "",
        "抓取时间": result.get("timestamp", ""),
    }
    return record


def _fmt_num(val) -> str:
    """格式化数字"""
    if val is None:
        return ""
    if isinstance(val, int):
        if val >= 10000:
            return f"{val / 10000:.1f}万"
        return str(val)
    return str(val)


def push_to_feishu(result: Dict) -> bool:
    """
    将抓取结果推送到飞书多维表格。
    自动选择 CLI 或 HTTP API 方式。
    """
    config = _load_config()
    if not config.get("enabled") or not config.get("configured"):
        return False

    base_token = config.get("base_token")
    if not base_token:
        return False

    record = _result_to_record(result)

    try:
        if config.get("use_cli") and has_lark_cli():
            return _push_via_cli(base_token, config.get("table_id"), record)
        else:
            return _push_via_api(config, record)
    except Exception as e:
        print(f"⚠️ 飞书推送失败: {e}")
        return False


def _push_via_cli(base_token: str, table_id: Optional[str], record: Dict) -> bool:
    """通过 lark-cli 推送数据"""
    cmd = ["lark-cli", "base", "+record-batch-create", "--base-token", base_token]
    if table_id:
        cmd.extend(["--table-id", table_id])
    cmd.extend(["--json", json.dumps({"records": [{"fields": record}]}, ensure_ascii=False)])

    result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
    if result.returncode == 0:
        print("✅ 数据已同步到飞书多维表格")
        return True
    else:
        print(f"⚠️ 飞书推送失败: {result.stderr[:200]}")
        return False


def _push_via_api(config: Dict, record: Dict) -> bool:
    """通过飞书开放平台 HTTP API 推送数据"""
    app_id = config.get("app_id")
    app_secret = config.get("app_secret")
    base_token = config.get("base_token")
    table_id = config.get("table_id")

    if not app_id or not app_secret:
        print("⚠️ 未配置 App ID/Secret，无法使用 API 方式推送")
        print("   请运行配置流程或安装 lark-cli")
        return False

    import requests

    # 1. 获取 tenant_access_token
    token_url = "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal"
    resp = requests.post(token_url, json={"app_id": app_id, "app_secret": app_secret}, timeout=10)
    token_data = resp.json()
    if token_data.get("code") != 0:
        print(f"⚠️ 获取飞书token失败: {token_data}")
        return False

    access_token = token_data["tenant_access_token"]

    # 2. 写入记录
    headers = {"Authorization": f"Bearer {access_token}", "Content-Type": "application/json"}
    # 如果没有 table_id，需要先获取默认表的 ID
    tbl_id = table_id or _get_default_table_id(access_token, base_token)
    if not tbl_id:
        return False

    api_url = f"https://open.feishu.cn/open-apis/bitable/v1/apps/{base_token}/tables/{tbl_id}/records"
    payload = {"fields": record}

    resp = requests.post(api_url, headers=headers, json=payload, timeout=10)
    data = resp.json()
    if data.get("code") == 0:
        print("✅ 数据已同步到飞书多维表格")
        return True
    else:
        print(f"⚠️ 飞书推送失败: {data.get('msg', 'unknown error')}")
        return False


def _get_default_table_id(access_token: str, base_token: str) -> Optional[str]:
    """获取多维表格中的第一个数据表 ID"""
    import requests
    headers = {"Authorization": f"Bearer {access_token}"}
    url = f"https://open.feishu.cn/open-apis/bitable/v1/apps/{base_token}/tables"
    resp = requests.get(url, headers=headers, timeout=10)
    data = resp.json()
    if data.get("code") == 0:
        items = data.get("data", {}).get("items", [])
        if items:
            return items[0].get("table_id")
    print(f"⚠️ 无法获取默认数据表 ID: {data.get('msg', 'unknown')}")
    return None


def check_and_prompt_config() -> Optional[str]:
    """
    检查是否需要提示用户配置飞书。

    在首次调用 scrape_post() 时执行（在赞赏检查之前）。
    - 如果已经询问过（configured=True），返回 None
    - 如果是首次使用，标记为已询问，并返回提示文案

    返回的文案应由调用方（智能体）展示给用户。
    此过程不占用 scrape_post 的使用次数。
    """
    config = _load_config()
    if config.get("configured"):
        return None

    # 标记为已询问（不再重复提示）
    config["configured"] = True
    config["enabled"] = False
    _save_config(config)

    return get_first_time_prompt()


def handle_config_command(user_input: str) -> Dict:
    """
    处理用户的飞书配置命令。

    当用户说"配置飞书"、"设置飞书"等时，由智能体调用。
    本函数仅判断用户意图并返回指引文案，不直接执行配置。
    智能体收集到用户参数后，应调用 setup_config() 完成配置。

    Returns:
        {"is_config_command": bool, "guide": str, "next_step": str}
    """
    keywords = ["配置飞书", "设置飞书", "飞书配置", "飞书推送", "同步飞书", "feishu"]
    if any(kw in user_input for kw in keywords):
        return {
            "is_config_command": True,
            "guide": get_config_guide(),
            "next_step": "请引导用户提供多维表格链接（base_url），以及必要时提供 App ID 和 App Secret，然后调用 setup_config() 完成配置。",
        }
    return {"is_config_command": False, "guide": "", "next_step": ""}
