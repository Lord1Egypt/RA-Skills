#!/usr/bin/env python3
"""
法规检索脚本 - 调用得理（法律）开放平台 API 检索法律法规

API 规范：POST https://platform.delilegal.com/api/v1/generice/law/list
请求字段：query, pageNo, pageSize, sortField, sortOrder
响应字段：data[].title/content/activeDate/id/issuedNo/publishDate/
          publisherName/timelinessName/levelName/highlights
响应结构：{success, code, msg, body: {data: [...], totalCount, totalPage, queryId}}

用法:
    # 基础语义检索（默认返回5条，按相关性排序）
    python3 search_laws.py "深圳市小产权房买卖合同相关的法律法规"

    # 指定返回条数
    python3 search_laws.py "借款合同纠纷" --size 10

    # 翻页
    python3 search_laws.py "借款合同纠纷" --page 2

    # 按时间排序（获取最新法规）
    python3 search_laws.py "劳动合同法" --sort-field time --sort-order desc

    # 按实施时间排序
    python3 search_laws.py "合同法" --sort-field activeDate --sort-order desc
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

# 默认占位值集合
PLACEHOLDER_VALS = {"YOUR_API_KEY", "YOUR_APP_KEY", "YOUR_APPID", "YOUR APPID", "YOUR_SECRET", "", None}


def load_config():
    """从 config.json 读取 API Key"""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    config_path = os.path.join(script_dir, "..", "config.json")
    if not os.path.exists(config_path):
        raise FileNotFoundError(
            f"配置文件不存在: {config_path}\n"
            f"请在技能目录下创建 config.json，内容如下：\n"
            f'{{"apikey": "YOUR_API_KEY"}}\n'
            f"请先前往 https://open.delilegal.com/personal/keys 创建 API Key"
        )
    with open(config_path, "r", encoding="utf-8") as f:
        cfg = json.load(f)
    apikey = cfg.get("apikey", "").strip()
    if apikey in PLACEHOLDER_VALS:
        raise FileNotFoundError(
            "config.json 中的 apikey 尚未配置，请按以下步骤操作：\n"
            "1. 前往 https://open.delilegal.com/personal/keys 注册/登录\n"
            "2. 创建应用并获取 API Key\n"
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
    调用得理法律开放平台 API 检索法律法规。

    参数说明（对应官方 API 规范）：
        query      : 法规名称、法规条款、法规内容等，用于语义检索
        page_no    : 检索页数，默认 1
        page_size  : 检索条数，默认 5
        sort_field : 排序字段：correlation(相关性) / time(时间) / activeDate(实施时间)，默认 correlation
        sort_order : 排序方式：desc(降序) / asc(升序)，默认 desc
    """
    apikey = load_config()

    payload: dict = {
        "pageNo": page_no,
        "pageSize": page_size,
        "sortField": sort_field,
        "sortOrder": sort_order,
    }
    if query:
        payload["query"] = query

    data = json.dumps(payload, ensure_ascii=False).encode("utf-8")

    req = urllib.request.Request(
        API_URL,
        data=data,
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
        return {"success": False, "code": -1, "msg": f"网络错误: {e.reason}", "body": None}


def strip_em(text: str) -> str:
    """去掉 <em> 标签"""
    return re.sub(r"</?em>", "", text)


def format_result(result: dict) -> str:
    """格式化 API 返回结果为用户可读的 Markdown（对齐官方响应字段）"""

    # 错误响应
    if result.get("code") and result["code"] != 200 and result["code"] != 0:
        return f"❌ 检索失败: {result.get('msg', '未知错误')} (code: {result['code']})"
    if result.get("success") is False:
        return f"❌ 检索失败: {result.get('msg', '未知错误')}"

    # 标准响应结构：数据在 body 字段下，body 内再有 data 列表
    # 兼容旧格式（直接在顶层 data 字段）
    body = result.get("body", result.get("data", {}))

    if isinstance(body, dict):
        total = body.get("totalCount", 0)
        total_page = body.get("totalPage", 1)
        items = body.get("data", [])
    elif isinstance(body, list):
        total = len(body)
        total_page = 1
        items = body
    else:
        return f"❌ 检索结果格式异常: {type(body)}\n原始返回：{json.dumps(result, ensure_ascii=False)[:500]}"

    if not items:
        return f"未找到相关法规（共 {total} 条）"

    lines = [f"共检索到 **{total}** 条相关法规（共 {total_page} 页），当前展示 {len(items)} 条：\n"]

    for i, law in enumerate(items, 1):
        title = strip_em(law.get("title", "无标题"))
        lines.append(f"### {i}. {title}")

        # 时效性（官方字段：timelinessName）
        timeliness = law.get("timelinessName", "")
        if timeliness:
            if "现行" in timeliness or "有效" in timeliness:
                lines.append(f"- **时效性：** ✅ {timeliness}")
            elif "废止" in timeliness:
                lines.append(f"- **时效性：** 🔴 {timeliness}")
            elif "修订" in timeliness:
                lines.append(f"- **时效性：** 🟡 {timeliness}")
            elif "部分" in timeliness or "失效" in timeliness:
                lines.append(f"- **时效性：** 🟠 {timeliness}")
            else:
                lines.append(f"- **时效性：** {timeliness}")

        # 效力等级（官方字段：levelName）
        level_name = law.get("levelName", "")
        if level_name:
            lines.append(f"- **效力等级：** {level_name}")

        # 发布机关（官方字段：publisherName）
        publisher = law.get("publisherName", "")
        if publisher:
            lines.append(f"- **发布机关：** {publisher}")

        # 发文字号（官方字段：issuedNo）
        issued_no = law.get("issuedNo", "")
        if issued_no:
            lines.append(f"- **发文字号：** {issued_no}")

        # 发布时间（官方字段：publishDate）
        publish_date = law.get("publishDate", "")
        if publish_date:
            lines.append(f"- **发布时间：** {publish_date}")

        # 生效时间（官方字段：activeDate）
        active_date = law.get("activeDate", "")
        if active_date:
            lines.append(f"- **施行时间：** {active_date}")

        # 命中法条（官方字段：highlights，为 list）
        highlights = law.get("highlights", [])
        if highlights:
            lines.append("- **命中法条：**")
            for h in highlights[:3]:  # 最多展示3条
                h_name = h.get("name", "")
                h_text = strip_em(h.get("text", ""))
                if len(h_text) > 150:
                    h_text = h_text[:150] + "..."
                if h_name:
                    lines.append(f"  - **{h_name}**：{h_text}")
                else:
                    lines.append(f"  - {h_text}")

        # 正文详情（官方字段：content）
        content = strip_em(law.get("content", ""))
        if content and not highlights:
            # 无命中法条时才展示内容摘要
            if len(content) > 200:
                content = content[:200] + "..."
            lines.append(f"- **内容摘要：** {content}")

        lines.append("")

    lines.append("---")
    lines.append("⚠️ 检索结果基于得理法律开放平台数据，法规时效性可能因最新立法动态而变化，重要决策前请核实最新官方文本。")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(
        description="法规检索 - 得理法律开放平台 API（/api/v1/generice/law/list）",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  %(prog)s "深圳小产权房买卖合同纠纷相关的法律法规"
  %(prog)s "民法典第11条" --size 5
  %(prog)s "劳动合同法" --sort-field time --sort-order desc
  %(prog)s "竞业限制" --sort-field activeDate
        """)

    parser.add_argument("keyword", help="检索关键词（法规名称、条款、内容均可）")
    parser.add_argument("--page", type=int, default=1, help="页码 (默认 1)")
    parser.add_argument("--size", type=int, default=5, help="每页条数 (默认 5)")
    parser.add_argument("--sort-field", dest="sort_field",
                        choices=["correlation", "time", "activeDate"],
                        default="correlation",
                        help="排序字段：correlation(相关性) / time(时间) / activeDate(实施时间)，默认 correlation")
    parser.add_argument("--sort-order", dest="sort_order",
                        choices=["desc", "asc"],
                        default="desc",
                        help="排序方式：desc(降序) / asc(升序)，默认 desc")

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
