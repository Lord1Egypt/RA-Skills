#!/usr/bin/env python3
"""
案例检索脚本 - 调用得理（法律）开放平台 API 检索裁判文书案例

API 规范：POST https://platform.delilegal.com/api/v1/generice/case/list
请求字段：query, pageNo, pageSize, sortField, sortOrder
响应字段：data[].title/content/caseType/cause/judgementType/judgementDate/
          id/court/caseNumber/levelOfTrial/publishTypeName/publishType
响应结构：{success, code, msg, body: {data: [...], totalCount, totalPage, queryId}}

用法:
    # 基础语义检索
    python3 search_cases.py "离婚诉讼分居两年判决"

    # 指定返回条数和页码
    python3 search_cases.py "借款合同纠纷" --size 10 --page 2

    # 按时间排序
    python3 search_cases.py "劳动争议" --sort-field time --sort-order desc

    # 长文本语义检索
    python3 search_cases.py --long-text "原告与被告于2023年签订借款合同，约定年利率8%..."
"""

import argparse
import json
import os
import re
import ssl
import sys
import urllib.request
import urllib.error

API_URL = "https://platform.delilegal.com/api/v1/generice/case/list"

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


def search_cases(
    query: str = None,
    page_no: int = 1,
    page_size: int = 10,
    sort_field: str = "correlation",
    sort_order: str = "desc"
) -> dict:
    """
    调用得理法律开放平台 API 检索裁判文书案例。

    参数说明（对应官方 API 规范）：
        query      : 案情描述、争议焦点、法律问题，用于语义检索
        page_no    : 检索页数，默认 1
        page_size  : 检索条数，默认 10
        sort_field : 排序字段：correlation(相关性) / time(时间)，默认 correlation
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
        return f"未找到相关案例（共 {total} 条）"

    lines = [f"共检索到 **{total}** 条相关案例（共 {total_page} 页），当前展示 {len(items)} 条：\n"]

    for i, case in enumerate(items, 1):
        # 标题（官方字段：title）
        title = strip_em(case.get("title", "无标题"))
        lines.append(f"### {i}. {title}")

        # 案号（官方字段：caseNumber）
        case_number = case.get("caseNumber", "")
        if case_number:
            lines.append(f"- **案号：** {case_number}")

        # 诉讼案由（官方字段：cause）
        cause = case.get("cause", "")
        if cause:
            lines.append(f"- **案由：** {cause}")

        # 案件类型（官方字段：caseType）
        case_type = case.get("caseType", "")
        if case_type:
            lines.append(f"- **案件类型：** {case_type}")

        # 审理法院（官方字段：court）
        court = case.get("court", "")
        if court:
            lines.append(f"- **审理法院：** {court}")

        # 审理程序（官方字段：levelOfTrial）
        level_of_trial = case.get("levelOfTrial", "")
        if level_of_trial:
            lines.append(f"- **审理程序：** {level_of_trial}")

        # 判决类型（官方字段：judgementType）
        judgement_type = case.get("judgementType", "")
        if judgement_type:
            lines.append(f"- **判决类型：** {judgement_type}")

        # 判决时间（官方字段：judgementDate）
        judgement_date = case.get("judgementDate", "")
        if judgement_date:
            lines.append(f"- **判决时间：** {judgement_date}")

        # 案例类型（官方字段：publishTypeName / publishType）
        publish_type_name = case.get("publishTypeName", "")
        if publish_type_name:
            lines.append(f"- **案例类型：** {publish_type_name}")

        # 内容摘要（官方字段：content）
        content = strip_em(case.get("content", ""))
        if content:
            if len(content) > 300:
                content = content[:300] + "..."
            lines.append(f"- **内容摘要：** {content}")

        lines.append("")

    lines.append("---")
    lines.append("⚠️ 检索结果基于得理法律开放平台数据，裁判文书的公开性受法院公示范围限制，重要案件请以法院官方文书为准。")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(
        description="案例检索 - 得理法律开放平台 API（/api/v1/generice/case/list）",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  %(prog)s "离婚诉讼分居两年判决离婚"
  %(prog)s "民间借贷利率超过四倍LPR" --size 10
  %(prog)s "劳动合同解除违法赔偿" --sort-field time --sort-order desc
  %(prog)s --long-text "原告与被告签订借款合同..."
        """)

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("keyword", nargs="?", default=None,
                       help="检索关键词或案情描述（语义检索）")
    group.add_argument("--long-text", dest="long_text", default=None,
                       help="长文本输入，用于文件内容语义匹配")

    parser.add_argument("--page", type=int, default=1, help="页码 (默认 1)")
    parser.add_argument("--size", type=int, default=10, help="每页条数 (默认 10)")
    parser.add_argument("--sort-field", dest="sort_field",
                        choices=["correlation", "time"],
                        default="correlation",
                        help="排序字段：correlation(相关性) / time(时间)，默认 correlation")
    parser.add_argument("--sort-order", dest="sort_order",
                        choices=["desc", "asc"],
                        default="desc",
                        help="排序方式：desc(降序) / asc(升序)，默认 desc")

    args = parser.parse_args()

    query = args.long_text if args.long_text else args.keyword

    result = search_cases(
        query=query,
        page_no=args.page,
        page_size=args.size,
        sort_field=args.sort_field,
        sort_order=args.sort_order,
    )
    print(format_result(result))


if __name__ == "__main__":
    main()
