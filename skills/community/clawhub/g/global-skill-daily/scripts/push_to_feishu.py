"""
push_to_feishu.py — 飞书推送（Card 2.0 + 可选云文档上传）

v1.5.0 自依赖改造：
  - lark-cli 从「必需依赖」降级为「可选依赖」
  - lark-cli 不可用时跳过云文档上传，仅推送 Card 2.0 卡片消息（含完整简报文本）
  - 卡片消息通道完全自依赖（仅依赖 Python 标准库 urllib）
  - 云文档上传仍是用户身份（铁律保留），但作为增强项

升级点（历史）：
  1. Card 2.0 schema=2.0，markdown 元素（非 lark_md）
  2. 标题含具体数字（区分度）
  3. 云文档用 lark-cli drive +import 用户身份（非 create_document）
  4. template=green（与旧 blue/purple 差异化）

环境变量：
  FEISHU_APP_ID / FEISHU_APP_SECRET / FEISHU_USER_OPEN_ID
"""
from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
import urllib.request
import urllib.error
from pathlib import Path


FEISHU_API_BASE = "https://open.feishu.cn/open-apis"


def _get_credentials() -> tuple[str, str, str]:
    """读取飞书凭证。"""
    app_id = os.environ.get("FEISHU_APP_ID", "")
    app_secret = os.environ.get("FEISHU_APP_SECRET", "")
    user_open_id = os.environ.get("FEISHU_USER_OPEN_ID", "")
    return app_id, app_secret, user_open_id


def _get_tenant_token(app_id: str, app_secret: str) -> str | None:
    """获取 tenant_access_token。"""
    url = f"{FEISHU_API_BASE}/auth/v3/tenant_access_token/internal"
    payload = {"app_id": app_id, "app_secret": app_secret}
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json"}, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            result = json.loads(resp.read().decode("utf-8"))
            return result.get("tenant_access_token")
    except (urllib.error.URLError, json.JSONDecodeError) as e:
        print(f"[push_to_feishu] get token failed: {e}")
        return None


def upload_to_drive_via_lark_cli(md_path: Path, title: str) -> dict:
    """用 lark-cli drive +import 以用户身份将 .md 导入为飞书在线 docx 文档。

    v1.2.0 安全修复：使用 argv list 而非 shell=True 字符串拼接，
    避免 AST4/OH1 finding（shell 注入风险）。

    - lark-cli user 模式要求相对路径，需要 cwd 到 md 文件所在目录
    - argv list 模式 + shutil.which 解析完整路径（Windows npm 全局命令是 .cmd，
      subprocess 不自动解析 PATHEXT，必须 which 出 lark-cli.cmd 完整路径）
    - +import 比 +upload 更适合：upload 只存原文件（点击只能下载），import 转为在线 docx（点击可查看）
    """
    try:
        lark_cli_bin = shutil.which("lark-cli")
        if not lark_cli_bin:
            return {"success": False, "error": "lark-cli not found in PATH"}
        md_dir = md_path.parent
        relative_name = md_path.name
        # 用 argv list 而非字符串命令，避免 shell=True
        cmd = [
            lark_cli_bin, "drive", "+import",
            "--file", relative_name,
            "--name", title,
            "--type", "docx",
        ]
        result = subprocess.run(
            cmd,
            capture_output=True, text=True, timeout=120, encoding="utf-8",
            cwd=str(md_dir),
        )
        if result.returncode == 0:
            output = result.stdout
            # lark-cli +import 输出格式：{"ok": true, "data": {"token": "...", "url": "...", "type": "docx"}}
            try:
                # 输出可能有 "Uploading..." 等前置行，找到第一个 { 开始的 JSON
                json_start = output.find("{")
                if json_start >= 0:
                    parsed = json.loads(output[json_start:])
                    if parsed.get("ok"):
                        data = parsed.get("data", {})
                        file_token = data.get("token") or data.get("file_token")
                        url = data.get("url")
                        if file_token and not url:
                            url = f"https://aipeanut.feishu.cn/docx/{file_token}"
                        return {"success": True, "url": url, "token": file_token, "type": "docx", "output": output[:800]}
            except json.JSONDecodeError:
                pass
            # fallback：正则匹配
            import re
            url_match = re.search(r"https?://[^\s\"]+\.feishu\.cn/[^\s\"]+", output)
            if not url_match:
                url_match = re.search(r"https?://[^\s\"]+", output)
            token_match = re.search(r"\"token\"\s*:\s*\"([^\"]+)\"", output)
            return {
                "success": True,
                "url": url_match.group(0) if url_match else None,
                "token": token_match.group(1) if token_match else None,
                "type": "docx",
                "output": output[:800],
            }
        else:
            return {"success": False, "error": (result.stderr or result.stdout)[:500], "returncode": result.returncode}
    except (subprocess.TimeoutExpired, FileNotFoundError) as e:
        return {"success": False, "error": f"lark-cli not available: {e}"}


def _column_block(content: str, bg_color: str | None = None) -> dict:
    """构造 column_set + column + markdown 元素（Card 2.0 必需结构）。"""
    column = {
        "tag": "column",
        "width": "weighted",
        "weight": 1,
        "vertical_align": "top",
        "elements": [{"tag": "markdown", "content": content}],
    }
    column_set = {
        "tag": "column_set",
        "flex_mode": "none",
        "columns": [column],
    }
    if bg_color:
        # 同时在 column 和 column_set 上设置 background_style（V7.4-V7.9 兼容）
        column["background_style"] = bg_color
        column_set["background_style"] = bg_color
    return column_set


def build_card_2_0(result: dict, date_str: str, doc_url: str | None = None) -> dict:
    """构建 Card 2.0 卡片（schema=2.0，markdown 元素 + column_set 结构）。"""
    title = f"🌐 全球Skill日报-{date_str}-推荐{result['recommendations_count']}个-跨平台{result['cross_platform_count']}个"

    from collections import defaultdict
    by_dim = defaultdict(list)
    for rec in result["recommendations"]:
        by_dim[rec["dimension"]].append(rec)

    dim_labels = {
        "trending_both": "🔥 双榜热装",
        "quality": "⭐ 口碑精品",
        "newcomers": "🚀 新星上线",
        "china_only": "🇨🇳 国内独火",
        "global_only": "🌍 全球独火",
        "active_developer": "👤 活跃开发者",
        "memory_collision": "🧠 记忆碰撞",
        "scene_match": "🎯 痛点匹配",
        "scene_match_extra": "🎯 痛点匹配",
        "verified": "🛡️ 安全审计",
        "panorama": "🏆 全景视角",
    }
    dim_order = ["trending_both", "quality", "newcomers", "china_only", "global_only",
                 "active_developer", "memory_collision", "scene_match", "scene_match_extra",
                 "verified", "panorama"]

    # 背景色映射（邻近色环：green 起始 → turquoise/blue 主推，yellow 亮点，grey 统计）
    dim_bg = {
        "trending_both": "green-50",     # 起始色
        "quality": "yellow-50",          # 亮点
        "newcomers": "blue-50",          # 主推
        "china_only": "turquoise-50",
        "global_only": "blue-50",        # 主推
        "active_developer": "grey-50",   # 统计
        "memory_collision": "yellow-50", # 亮点
        "scene_match": "green-50",       # 起始色（主推）
        "scene_match_extra": "green-50",
        "verified": "turquoise-50",
        "panorama": "grey-50",           # 统计
    }

    body_elements: list[dict] = []

    # TL;DR 区块（grey-50 统计背景）
    group_name = result.get("dimension_group_name", "")
    group_desc = result.get("dimension_group_desc", "")
    dedup_window = result.get("dedup_window_days", 14)

    tldr_md = (
        f"**📊 双榜扫描**：ClawHub {result['clawhub_count']} + SkillHub {result['skillhub_count']} → "
        f"合并去重 **{result['merged_count']}** 个（双榜共有 {result['both_count']} 个）\n\n"
        f"**🎯 今日推荐**：{result['recommendations_count']} 个 | 跨平台对比 {result['cross_platform_count']} 个 | "
        f"跳过 {dedup_window} 天去重 {result['dedup_skipped_count']} 个\n\n"
        f"**🔄 维度组**：{group_name}（{group_desc}）"
    )
    body_elements.append(_column_block(tldr_md, "grey-50"))
    body_elements.append({"tag": "hr"})

    # 跨平台生态洞察区块（v1.1 核心，yellow-50 亮点背景）
    insights = result.get("cross_platform_insights", {})
    if insights:
        summary_lines = insights.get("insights_summary", [])
        if summary_lines:
            insights_md = "**🌏 跨平台生态洞察**\n\n" + "\n".join(
                f"- {line}" for line in summary_lines[:4]
            )
            body_elements.append(_column_block(insights_md, "yellow-50"))
            body_elements.append({"tag": "hr"})

    # 各维度区块
    for dim in dim_order:
        recs = by_dim.get(dim, [])
        if not recs:
            continue
        md_lines = [f"### {dim_labels[dim]} × {len(recs)}"]
        for rec in recs[:2]:  # 每维度最多 2 个
            platforms = "/".join(rec["platforms_active"])
            md_lines.append(f"- **{rec['name']}** (`{rec['slug']}`) [{platforms}]")
            md_lines.append(f"  - 安装: CH={rec['installs']['clawhub']} SH={rec['installs']['skillhub']} 总={rec['installs']['total']}")
            md_lines.append(f"  - {rec.get('chinese_summary', '')[:120]}")
        body_elements.append(_column_block("\n".join(md_lines), dim_bg.get(dim)))

    # 按钮（Card 2.0：button 直接作为 body element，不要 action 包装）
    if doc_url:
        body_elements.append({"tag": "hr"})
        body_elements.append({
            "tag": "button",
            "text": {"tag": "plain_text", "content": "📄 查看完整简报"},
            "type": "primary",
            "width": "fill",
            "behaviors": [{"type": "open_url", "default_url": doc_url}],
        })

    card = {
        "schema": "2.0",
        "config": {"wide_screen_mode": True, "update_multi": True},
        "header": {
            "title": {"tag": "plain_text", "content": title},
            "template": "green",
        },
        "body": {
            "elements": body_elements,
        },
    }
    return card


def send_card_message(token: str, user_open_id: str, card: dict) -> dict:
    """发送 Card 2.0 互动卡片消息。"""
    url = f"{FEISHU_API_BASE}/im/v1/messages?receive_id_type=open_id"
    payload = {
        "receive_id": user_open_id,
        "msg_type": "interactive",
        "content": json.dumps(card, ensure_ascii=False),
    }
    data = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}",
    }
    req = urllib.request.Request(url, data=data, headers=headers, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except (urllib.error.URLError, urllib.error.HTTPError, json.JSONDecodeError) as e:
        return {"error": str(e)}


def push(json_path: Path, md_path: Path, date_str: str) -> dict:
    """完整推送流程：上传云文档 + 发卡片消息。"""
    app_id, app_secret, user_open_id = _get_credentials()

    if not all([app_id, app_secret, user_open_id]):
        return {
            "success": False,
            "error": "缺少凭证：FEISHU_APP_ID / FEISHU_APP_SECRET / FEISHU_USER_OPEN_ID 未设置",
        }

    # 加载推荐结果
    result = json.loads(json_path.read_text(encoding="utf-8"))

    # Step 1: 上传云文档（用户身份，可选依赖 lark-cli）
    # v1.5.0：lark-cli 不可用时降级为「仅卡片消息」，不阻断流程
    title = f"全球 Skill 生态日报 {date_str}"
    doc_url = None
    upload_result = upload_to_drive_via_lark_cli(md_path, title)
    if upload_result.get("success"):
        doc_url = upload_result.get("url")
        print(f"[push_to_feishu] uploaded to drive: {doc_url}")
    else:
        # 降级模式：lark-cli 不可用或上传失败，继续发卡片（卡片已含完整简报文本）
        print(f"[push_to_feishu] [v1.5.0 降级模式] 跳过云文档上传，仅推送卡片消息。原因: {upload_result.get('error')}")
        # 失败不阻断，继续发卡片

    # Step 2: 获取 tenant token
    token = _get_tenant_token(app_id, app_secret)
    if not token:
        return {"success": False, "error": "get tenant_access_token failed", "upload_result": upload_result}

    # Step 3: 构建 Card 2.0 并发送
    card = build_card_2_0(result, date_str, doc_url)
    send_result = send_card_message(token, user_open_id, card)

    if send_result.get("code") != 0:
        return {
            "success": False,
            "error": send_result.get("msg"),
            "upload_result": upload_result,
            "send_result": send_result,
        }

    return {
        "success": True,
        "doc_url": doc_url,
        "upload_result": upload_result,
        "card_title": card["header"]["title"]["content"],
        "send_result": send_result,
    }


def main():
    if len(sys.argv) < 4:
        print("Usage: python push_to_feishu.py <json_path> <md_path> <date_str>")
        sys.exit(1)

    json_path = Path(sys.argv[1])
    md_path = Path(sys.argv[2])
    date_str = sys.argv[3]

    if not json_path.exists() or not md_path.exists():
        print(f"[push_to_feishu] files not found: {json_path} / {md_path}")
        sys.exit(1)

    result = push(json_path, md_path, date_str)
    print(json.dumps(result, ensure_ascii=False, indent=2))

    if not result.get("success"):
        sys.exit(1)


if __name__ == "__main__":
    main()
