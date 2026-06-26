#!/usr/bin/env python3
"""
法规检索脚本 - 调用得理法律开放平台法规检索 API

用法:
    # 基础关键词检索（默认只返回有效法规）
    python3 search_laws.py "劳动合同法第四十六条"

    # 指定条数
    python3 search_laws.py "个人信息保护法" --size 10

    # 按时间排序（适合查最新法规）
    python3 search_laws.py "数据安全" --sort-field time --sort-order desc

    # 按生效日期排序
    python3 search_laws.py "民法典合同编" --sort-field activeDate --sort-order desc

    # 翻页
    python3 search_laws.py "行政处罚法" --page 2 --size 10

API 文档：得理法律开放平台
端点：https://platform.delilegal.com/api/v1/generice/law/list
响应结构：{success, code, msg, body: {data:[...], totalCount, totalPage, queryId}}
"""

import argparse
import json
import os
import re
import ssl
import sys
import urllib.request
import urllib.error

API_URL = "https://platform.delilegal.com/api/v1/generice/law/list"

# 占位值集合
PLACEHOLDER_VALS = {"YOUR_API_KEY", "YOUR_APP_KEY", "YOUR_APPID", "YOUR APPID", "YOUR_SECRET", "", None}


def load_config():
    """从 config.json 读取 API Key"""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    config_path = os.path.join(script_dir, "..", "config.json")
    if not os.path.exists(config_path):
        raise FileNotFoundError(
            f"配置文件不存在: {config_path}\n"
            f"请在技能根目录创建 config.json，格式如下：\n"
            f'{{"apikey": "YOUR_API_KEY"}}\n'
            f"请前往 https://open.delilegal.com/personal/keys 获取 API Key"
        )
    with open(config_path, "r", encoding="utf-8") as f:
        cfg = json.load(f)
    apikey = cfg.get("apikey", "").strip()
    if apikey in PLACEHOLDER_VALS:
        raise FileNotFoundError(
            "config.json 中的 apikey 尚未配置或为占位符，请：\n"
            "1. 前往 https://open.delilegal.com/personal/keys 注册/登录\n"
            "2. 在控制台生成 API Key\n"
            "3. 将 API Key 填入 config.json 的 \"apikey\" 字段"
        )
    return apikey


def search_laws(
    query: str,
    page_no: int = 1,
    page_size: int = 5,
    sort_field: str = "correlation",
    sort_order: str = "desc"
) -> dict:
    """
    调用得理法规检索 API 搜索法律法规

    参数：
        query      - 检索关键词（自然语言）
        page_no    - 页码，默认 1
        page_size  - 每页条数，默认 5
        sort_field - 排序字段：correlation（相关性）/ time（发布时间）/ activeDate（生效日期）
        sort_order - 排序方向：desc（降序）/ asc（升序）

    返回：
        API 原始响应 dict，结构为 {success, code, msg, body: {data, totalCount, totalPage, queryId}}
    """
    apikey = load_config()

    # 构造请求体（扁平结构，无 condition 嵌套）
    payload_dict = {
        "pageNo": page_no,
        "pageSize": page_size,
        "sortField": sort_field,
        "sortOrder": sort_order,
        "query": query,
    }

    payload = json.dumps(payload_dict, ensure_ascii=False).encode("utf-8")

    req = urllib.request.Request(
        API_URL,
        data=payload,
        headers={
            "Content-Type": "application/json",
            "Authorization": "Bearer " + apikey
        },
        method="POST",
    )

    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE

    try:
        with urllib.request.urlopen(req, timeout=30, context=ctx) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", errors="replace") if e.fp else ""
        return {"success": False, "code": e.code, "msg": f"HTTP {e.code}: {e.reason}", "body": body}
    except urllib.error.URLError as e:
        return {"success": False, "code": -1, "msg": f"网络连接失败: {e.reason}", "body": None}


def strip_em(text: str) -> str:
    """移除 <em> 高亮标签"""
    return re.sub(r"</?em>", "", str(text))


def format_result(result: dict) -> str:
    """将 API 响应格式化为可读 Markdown"""

    success = result.get("success", False)
    code = result.get("code", 0)

    if not success and code != 0:
        return f"❌ 检索失败: {result.get('msg', '未知错误')} (code: {code})"

    # 标准响应结构：数据在 body 字段下，body 内再有 data 列表
    # 兼容旧格式（直接在顶层 data 字段）
    body = result.get("body", result.get("data", {}))

    if isinstance(body, dict):
        total = body.get("totalCount", body.get("total", 0))
        data = body.get("data", body.get("list", body.get("records", [])))
    elif isinstance(body, list):
        total = len(body)
        data = body
    else:
        return f"❌ 响应数据格式异常，类型: {type(body)}"

    if not data:
        return f"未检索到相关法规（总数: {total}）"

    lines = [f"共检索到 **{total}** 条法规，当前显示第 1-{len(data)} 条\n"]

    for i, law in enumerate(data, 1):
        title = strip_em(law.get("title", law.get("name", "无标题")))
        lines.append(f"### {i}. {title}")

        # 时效性（官方字段：timelinessName）
        timeliness = law.get("timelinessName", law.get("timeliness", ""))
        if timeliness:
            if "有效" in timeliness or "现行" in timeliness:
                lines.append(f"- **时效状态：** ✅ {timeliness}")
            elif "失效" in timeliness:
                lines.append(f"- **时效状态：** ❌ {timeliness}")
            elif "废止" in timeliness:
                lines.append(f"- **时效状态：** ❌ {timeliness}")
            elif "修订" in timeliness or "修正" in timeliness:
                lines.append(f"- **时效状态：** ⚠️ {timeliness}")
            else:
                lines.append(f"- **时效状态：** {timeliness}")

        # 效力级别（官方字段：levelName）
        level = law.get("levelName", law.get("level", ""))
        if level:
            lines.append(f"- **效力级别：** {level}")

        # 发布机关（官方字段：publisherName）
        publisher = law.get("publisherName", law.get("publisher", ""))
        if publisher:
            lines.append(f"- **发布机关：** {publisher}")

        # 文号（官方字段：issuedNo）
        issued_no = law.get("issuedNo", "")
        if issued_no:
            lines.append(f"- **发文字号：** {issued_no}")

        # 发布日期（官方字段：publishDate）
        publish_date = law.get("publishDate", law.get("publishTime", ""))
        if publish_date:
            lines.append(f"- **发布日期：** {publish_date}")

        # 生效日期（官方字段：activeDate）
        active_date = law.get("activeDate", law.get("activeTime", ""))
        if active_date:
            lines.append(f"- **生效日期：** {active_date}")

        # 摘要/高亮内容（官方字段：highlights）
        highlights = law.get("highlights", "")
        content = law.get("content", "")
        summary = law.get("summary", law.get("abstract", ""))

        display_text = highlights or content or summary
        if display_text:
            display_text = strip_em(str(display_text))
            if len(display_text) > 200:
                display_text = display_text[:200] + "..."
            lines.append(f"- **相关摘录：** {display_text}")

        lines.append("")

    lines.append("---")
    lines.append("> 数据来源：得理法律数据库。引用法规前请核实时效性，以官方发布文本为准。")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(
        description="法规检索 - 调用得理法律开放平台 API",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  %(prog)s "劳动合同法第四十六条"
  %(prog)s "个人信息保护法" --size 10
  %(prog)s "数据安全" --sort-field time --sort-order desc
  %(prog)s "民法典合同编" --sort-field activeDate --sort-order desc --page 2
        """)

    parser.add_argument("keyword", help="检索关键词（自然语言）")
    parser.add_argument("--page", type=int, default=1, help="页码（默认 1）")
    parser.add_argument("--size", type=int, default=5, help="每页条数（默认 5）")
    parser.add_argument("--sort-field", dest="sort_field",
                        choices=["correlation", "time", "activeDate"],
                        default="correlation",
                        help="排序字段：correlation（相关性，默认）/ time（发布时间）/ activeDate（生效日期）")
    parser.add_argument("--sort-order", dest="sort_order",
                        choices=["desc", "asc"],
                        default="desc",
                        help="排序方向：desc（降序，默认）/ asc（升序）")

    args = parser.parse_args()

    result = search_laws(
        query=args.keyword,
        page_no=args.page,
        page_size=args.size,
        sort_field=args.sort_field,
        sort_order=args.sort_order,
    )
    print(format_result(result))


if __name__ == "__main__":
    main()
