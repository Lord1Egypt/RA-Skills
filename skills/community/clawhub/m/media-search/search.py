#!/usr/bin/env python3
"""
媒体库搜索工具 — 快捷入口
供 Claude 或命令行直接调用。
"""

import argparse
import json
import logging
import os
import sys
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

# 添加scripts目录到Python路径
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), "scripts"))

from media_search import MediaSearchEngine, SearchParameters


def get_item_value(item: Union[Dict, Any], key: str, default: str = "") -> Any:
    """统一获取属性值，支持字典和 Pydantic 模型。"""
    if isinstance(item, dict):
        return item.get(key, default)
    # Pydantic 模型或普通对象
    return getattr(item, key, default)


logging.basicConfig(
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)


def format_media_item(media_item: Union[Dict, Any], index: int) -> List[str]:
    """格式化单条媒体搜索结果。"""
    lines = []
    title = get_item_value(media_item, "title", "无标题")
    url = get_item_value(media_item, "url", "")
    publish_time = get_item_value(media_item, "publish_time", "")
    source_name = get_item_value(media_item, "source_name", "")
    summary = get_item_value(media_item, "summary", "")
    content = get_item_value(media_item, "content", "")

    publish_time_str = f" ({publish_time})" if publish_time else ""
    lines.append(f"{index}. **{title}**{publish_time_str} - **{source_name}**")

    if url:
        lines.append(f"链接: {url}")

    if summary:
        lines.append(f"摘要: {summary}")

    if content:
        lines.append(f"正文: {content[:500]}{'...' if len(content) > 500 else ''}")

    return lines


def format_response(result: Dict[str, Any]) -> str:
    """将查询结果格式化为可读输出。"""
    if not result["success"]:
        return f"查询失败: {result['error']}"

    items: List[Dict] = result.get("items", [])
    items = items if isinstance(items, list) else []

    output_lines: List[str] = []

    output_lines.extend(
        [
            "**媒体库搜索结果**",
            "",
            f"|**查询**: {result.get('query', '')}",
            f"|**后端**: {result.get('backend', '媒体库搜索')}",
            f"|**时间**: {result.get('timestamp', '')}",
            f"|**数量**: {len(items)} 条 (共 {result.get('total', 0)} 条)",
            "",
            "---",
            "",
        ]
    )

    if items:
        for i, item in enumerate(items, 1):
            output_lines.extend(format_media_item(item, i))
            output_lines.append("")
    else:
        output_lines.append("无结果")

    return "\n".join(output_lines)


def save_to_sources(result: Dict[str, Any], query_keywords: str) -> Optional[str]:
    """
    保存搜索结果到 sources 文件夹

    Args:
        result: 搜索结果
        query_keywords: 查询关键词

    Returns:
        保存的文件路径，如果保存失败则返回None
    """
    try:
        # 确保sources目录存在
        sources_dir = Path("sources")
        sources_dir.mkdir(exist_ok=True)

        # 生成文件名
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        # 清理关键词作为文件名的一部分
        safe_keywords = "".join(c for c in query_keywords[:20] if c.isalnum() or c in "-_")
        filename = f"media_{timestamp}_{safe_keywords}.md"
        filepath = sources_dir / filename

        # 构建保存内容
        content_lines = [
            f"# 媒体库搜索结果 - {query_keywords}",
            "",
            f"**查询时间**: {result.get('timestamp', '')}",
            f"**查询关键词**: {query_keywords}",
            f"**后端**: {result.get('backend', '媒体库搜索')}",
            f"**总结果数**: {result.get('total', 0)}",
            "",
            "---",
            ""
        ]

        if result.get("success"):
            items = result.get("items", [])
            if items:
                for i, item in enumerate(items, 1):
                    title = item.get("title", "无标题")
                    publish_time = item.get("publish_time", "")
                    source_name = item.get("source_name", "")
                    url = item.get("url", "")
                    summary = item.get("summary", "")
                    content = item.get("content", "")
                    relevance_score = item.get("relevance_score", 0.0)

                    content_lines.extend([
                        f"## {i}. {title}",
                        "",
                        f"**发布时间**: {publish_time}" if publish_time else "",
                        f"**信源**: {source_name}" if source_name else "",
                        f"**相关性分数**: {relevance_score:.2f}" if relevance_score else "",
                        f"**链接**: {url}" if url else "",
                        "",
                        f"### 摘要",
                        summary if summary else "无摘要",
                        "",
                        f"### 正文",
                        content if content else "无正文内容",
                        "",
                        "---",
                        ""
                    ])
            else:
                content_lines.append("无搜索结果\n")
        else:
            content_lines.extend([
                "## 查询失败",
                "",
                f"**错误信息**: {result.get('error', '未知错误')}",
                ""
            ])

        # 写入文件
        filepath.write_text("\n".join(content_lines), encoding="utf-8")
        logger.info(f"已保存：媒体库检索到 {filepath.absolute()}")
        return str(filepath)

    except Exception as e:
        logger.error(f"保存搜索结果失败: {e}")
        return None


def parse_args() -> Dict[str, Any]:
    """解析 JSON 参数。"""
    parser = argparse.ArgumentParser(
        description="媒体库搜索工具",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python search.py --json-input '{"keywords": "人工智能 政策", "limit": 20}'
  python search.py --json-input '{"keywords": "乡村振兴", "limit": 10}' --output-file results.json
  python search.py --json-input '{"keywords": "人民日报 一带一路", "source_name": "人民日报"}' --output-console
        """,
    )
    parser.add_argument(
        "--json-input",
        dest="json_input",
        required=True,
        help="JSON 格式输入参数",
    )
    parser.add_argument(
        "--output-file",
        dest="output_file",
        help="将结果保存到指定JSON文件，如果不指定则输出到控制台",
    )
    parser.add_argument(
        "--output-console",
        dest="output_console",
        action="store_true",
        help="强制输出到控制台（默认行为）",
    )

    args = parser.parse_args()

    # 解析 JSON
    try:
        params = json.loads(args.json_input)
    except json.JSONDecodeError as e:
        logger.error(f"JSON 解析失败: {e}")
        raise ValueError(f"无效的 JSON 格式: {e}")

    return {
        "search_params": params,
        "output_file": args.output_file,
        "output_console": args.output_console
    }


def check_api_config() -> bool:
    """检查 API 配置是否完整。"""
    return bool(
        os.getenv("NEWS_BIGDATA_API_KEY") and os.getenv("NEWS_BIGDATA_API_SECRET")
    )


def main() -> int:
    """入口函数。"""
    if not check_api_config():
        logger.error("未配置 API Key，请至少配置一组：")
        logger.error("  NEWS_BIGDATA_API_KEY + NEWS_BIGDATA_API_SECRET")
        return 1

    try:
        parsed_args = parse_args()
        params = parsed_args["search_params"]
        output_file = parsed_args["output_file"]
        output_console = parsed_args["output_console"]
    except ValueError as e:
        logger.error(str(e))
        return 1

    # 提取查询参数
    keywords = params.get("keywords", "")
    keyword_position = params.get("keyword_position", "标题或正文")
    publish_time_start = params.get("publish_time_start")
    publish_time_end = params.get("publish_time_end")
    data_type = params.get("data_type")
    source_name = params.get("source_name")
    limit = params.get("limit", 10)
    timeout = params.get("timeout", 60)

    if not keywords:
        logger.error("请提供查询关键词 (keywords)")
        return 1

    # 验证limit范围
    if limit < 1 or limit > 50:
        logger.warning("结果数量超出范围，已自动调整为10条")
        limit = 10

    try:
        logger.info(f"查询中: {keywords}")

        # 创建搜索参数
        search_params = SearchParameters(
            keywords=keywords,
            keyword_position=keyword_position,
            publish_time_start=publish_time_start,
            publish_time_end=publish_time_end,
            data_type=data_type,
            source_name=source_name,
            limit=limit
        )

        # 执行搜索
        engine = MediaSearchEngine()
        result_obj = engine.search(search_params, timeout=timeout)

        # 转换为请求的JSON格式
        if result_obj.success:
            # 构建符合要求的JSON格式
            json_output = {
                "total": result_obj.total,
                "fallback_to_web": result_obj.fallback_to_web,
                "items": []
            }

            # 转换结果项为指定格式
            for item in result_obj.items:
                item_dict = {
                    "title": item.title,
                    "summary": item.summary,
                    "publish_time": item.publish_time,
                    "source_name": item.source_name,
                    "url": item.url
                }
                json_output["items"].append(item_dict)
        else:
            # 错误情况返回错误信息
            json_output = {
                "total": 0,
                "fallback_to_web": False,
                "items": [],
                "error": result_obj.error
            }

        # 保存结果到sources文件夹（使用完整信息）
        full_result_dict = {
            "success": result_obj.success,
            "total": result_obj.total,
            "from_cache": False,
            "fallback_to_web": result_obj.fallback_to_web,
            "items": [item.model_dump() for item in result_obj.items],
            "query": result_obj.query,
            "timestamp": result_obj.timestamp,
            "backend": result_obj.backend,
            "error": result_obj.error
        }
        # 根据参数决定输出方式
        if output_file:
            # 保存到JSON文件
            try:
                with open(output_file, 'w', encoding='utf-8') as f:
                    json.dump(json_output, f, ensure_ascii=False, indent=2)
                logger.info(f"结果已保存到JSON文件: {output_file}")
            except Exception as e:
                logger.error(f"保存文件失败: {e}")

    except Exception as e:
        logger.error(f"查询失败: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())