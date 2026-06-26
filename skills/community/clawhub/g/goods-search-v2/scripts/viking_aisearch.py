#!/usr/bin/env python3
import argparse
import json
import sys
from typing import Any, Dict, List, Optional, Tuple

from aisearch import VikingAISearch


def _json_loads(raw: str) -> Any:
    if raw is None:
        return None
    s = raw.strip()
    if not s:
        return None
    return json.loads(s)


def _emit(payload: Any, *, code: int) -> None:
    sys.stdout.write(json.dumps(payload, ensure_ascii=False, indent=2) + "\n")
    raise SystemExit(code)


def _parse_output_fields(value: str) -> Optional[List[str]]:
    if value is None:
        return None
    s = value.strip()
    if not s:
        return None
    if s.startswith("["):
        parsed = json.loads(s)
        if isinstance(parsed, list):
            return [str(x) for x in parsed]
        raise ValueError("output_fields must be a JSON array or comma-separated string")
    return [part.strip() for part in s.split(",") if part.strip()]


def _build_chat_search_param(args) -> Optional[Dict[str, Any]]:
    if args.chat_search_param_json:
        return _json_loads(args.chat_search_param_json)
    payload: Dict[str, Any] = {}
    if args.chat_page_size and args.chat_page_size > 0:
        payload["page_size"] = args.chat_page_size
    if args.chat_dataset_ids:
        payload["dataset_ids"] = [part.strip() for part in args.chat_dataset_ids.split(",") if part.strip()]
    if args.chat_filters_json:
        payload["filters"] = _json_loads(args.chat_filters_json)
    if args.chat_output_fields_json:
        payload["output_fields"] = _json_loads(args.chat_output_fields_json)
    return payload or None


def _build_search_query(args) -> Tuple[Optional[Dict[str, Any]], Optional[str]]:
    if args.search_query_json:
        return _json_loads(args.search_query_json), None
    query: Dict[str, Any] = {}
    if args.search_text:
        query["text"] = args.search_text
    if args.search_image_url:
        query["image_url"] = args.search_image_url
    if args.search_image_query_instruction:
        query["image_query_instruction"] = args.search_image_query_instruction
    if not query or (not query.get("text") and not query.get("image_url")):
        return None, "缺少 query：请提供 --search-text 或 --search-image-url 或 --search-query-json"
    return query, None


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Viking AI 搜索（ChatSearch + Search）",
        formatter_class=argparse.RawTextHelpFormatter,
        epilog=(
            "接口概览:\n"
            "  chat : POST /api/v1/application/{application_id}/chat_search (流式)\n"
            "  search: POST /api/v1/application/{application_id}/search[/scene_id]\n"
            "\n"
            "通用参数（chat/search 通用）:\n"
            "  --session-id    chat 会话标识；search 可选透传\n"
            "  --text          文本查询\n"
            "  --image-url     图片（Data URI 或 URL），--image 为别名\n"
            "  --dataset-id    search 数据集 ID；chat 将写入 search_param.dataset_ids\n"
            "  --scene-id      search 策略 ID（可选）\n"
            "  --user-json     user JSON（chat/search 通用）\n"
            "  --context-json  context JSON（chat/search 通用）\n"
            "\n"
            "chat 专属:\n"
            "  --enable-suggestions   enable_suggestions=true\n"
            "  --search-param-json    chat search_param JSON\n"
            "\n"
            "search 专属:\n"
            "  --page-number          页码（从 1 开始）\n"
            "  --page-size            每页数量（<=0 表示不传；建议 <=100）\n"
            "  --filter-json          filter JSON\n"
            "  --output-fields        output_fields（JSON 数组或逗号分隔）\n"
            "  --sort-by/--sort-order sort_by + sort_order(asc/desc)\n"
            "  --conditional-boost-json / --disable-personalize\n"
            "\n"
            "返回结构（概览）:\n"
            "  chat  : data={request_id, content}, raw={request_id, chunk_count}\n"
            "  search: data={request_id, search_results, total_items, spell_correction}\n"
        ),
    )
    parser.add_argument(
        "--action",
        choices=["validate", "chat", "search"],
        default="validate",
        help="validate: 校验配置；chat: 对话搜索；search: 直接检索",
    )

    parser.add_argument("--base-url", default="", help="覆盖 VIKING_AISEARCH_API_BASE")
    parser.add_argument("--api-key", default="", help="覆盖 VIKING_AISEARCH_API_KEY")
    parser.add_argument("--application-id", default="", help="覆盖 VIKING_AISEARCH_APPLICATION_ID")

    parser.add_argument("--session-id", default="", help="chat 会话标识；search 可选透传")
    parser.add_argument("--text", default="", help="文本查询（chat/search 通用）")
    parser.add_argument("--image-url", default="", help="图片 Data URI 或图片 URL（与 --image 等价）")
    parser.add_argument("--image", default="", help="--image-url 的别名")
    parser.add_argument("--dataset-id", default="", help="search 数据集 ID；chat 将写入 search_param.dataset_ids")
    parser.add_argument("--scene-id", default="", help="search 策略 ID（可选）")

    parser.add_argument("--chat-session-id", default="", help=argparse.SUPPRESS)
    parser.add_argument("--chat-text", default="", help=argparse.SUPPRESS)
    parser.add_argument("--chat-image-url", default="", help=argparse.SUPPRESS)
    parser.add_argument("--chat-body-json", default="", help=argparse.SUPPRESS)
    parser.add_argument("--chat-user-json", default="", help=argparse.SUPPRESS)
    parser.add_argument("--chat-enable-suggestions", action="store_true", help=argparse.SUPPRESS)
    parser.add_argument("--chat-context-json", default="", help=argparse.SUPPRESS)

    parser.add_argument("--chat-search-param-json", default="", help=argparse.SUPPRESS)
    parser.add_argument("--chat-page-size", type=int, default=0, help=argparse.SUPPRESS)
    parser.add_argument("--chat-dataset-ids", default="", help=argparse.SUPPRESS)
    parser.add_argument("--chat-filters-json", default="", help=argparse.SUPPRESS)
    parser.add_argument("--chat-output-fields-json", default="", help=argparse.SUPPRESS)

    parser.add_argument("--search-dataset-id", default="", help=argparse.SUPPRESS)
    parser.add_argument("--search-scene-id", default="", help=argparse.SUPPRESS)
    parser.add_argument("--search-query-json", default="", help=argparse.SUPPRESS)
    parser.add_argument("--search-text", default="", help=argparse.SUPPRESS)
    parser.add_argument("--search-image-url", default="", help=argparse.SUPPRESS)
    parser.add_argument("--search-image-query-instruction", default="", help=argparse.SUPPRESS)
    parser.add_argument("--search-page-number", type=int, default=1, help=argparse.SUPPRESS)
    parser.add_argument("--search-page-size", type=int, default=0, help=argparse.SUPPRESS)
    parser.add_argument("--search-user-json", default="", help=argparse.SUPPRESS)
    parser.add_argument("--search-filter-json", default="", help=argparse.SUPPRESS)
    parser.add_argument("--search-context-json", default="", help=argparse.SUPPRESS)
    parser.add_argument("--search-conditional-boost-json", default="", help=argparse.SUPPRESS)
    parser.add_argument("--search-output-fields", default="", help=argparse.SUPPRESS)
    parser.add_argument("--search-sort-by", default="", help=argparse.SUPPRESS)
    parser.add_argument("--search-sort-order", default="", help=argparse.SUPPRESS)
    parser.add_argument("--search-disable-personalize", action="store_true", help=argparse.SUPPRESS)

    parser.add_argument("--page-number", type=int, default=1, help="search 页码，从 1 开始")
    parser.add_argument("--page-size", type=int, default=0, help="search 每页数量（<=0 表示不传）")
    parser.add_argument("--user-json", default="", help="user 对象 JSON（chat/search 通用）")
    parser.add_argument("--filter-json", default="", help="search filter JSON（可选）")
    parser.add_argument("--context-json", default="", help="context JSON（chat/search 通用，可选）")
    parser.add_argument("--conditional-boost-json", default="", help="search conditional_boost JSON（可选）")
    parser.add_argument("--output-fields", default="", help="search output_fields（JSON 数组或逗号分隔）")
    parser.add_argument("--sort-by", default="", help="search sort_by（可选）")
    parser.add_argument("--sort-order", default="", help="search sort_order: asc/desc（可选）")
    parser.add_argument("--disable-personalize", action="store_true", help="search disable_personalize=true")

    parser.add_argument("--enable-suggestions", action="store_true", help="chat enable_suggestions=true")
    parser.add_argument("--search-param-json", default="", help="chat search_param JSON（可选）")

    args = parser.parse_args()

    try:
        tool = VikingAISearch(
            base_url=args.base_url or None,
            api_key=args.api_key or None,
            application_id=args.application_id or None,
        )
    except Exception as e:
        _emit(
            {
                "ok": False,
                "message": "检测到环境配置缺失：请补充 VIKING_AISEARCH_API_BASE / VIKING_AISEARCH_API_KEY 等环境变量。",
                "error": {"detail": str(e)},
            },
            code=1,
        )

    if args.action == "validate":
        _emit(
            {
                "ok": True,
                "config": {
                    "base_url": tool.base_url,
                    "application_id": tool.application_id,
                    "has_api_key": bool(tool.api_key),
                    "extra_headers_keys": sorted(list((tool.extra_headers or {}).keys())),
                },
            },
            code=0,
        )

    if args.action == "chat":
        body = _json_loads(args.chat_body_json)
        user = _json_loads(args.user_json) if args.user_json else _json_loads(args.chat_user_json)
        context = _json_loads(args.context_json) if args.context_json else _json_loads(args.chat_context_json)
        search_param = _json_loads(args.search_param_json) if args.search_param_json else _build_chat_search_param(args)

        session_id = args.session_id or args.chat_session_id
        text = args.text or args.chat_text
        image_url = args.image_url or args.image or args.chat_image_url
        dataset_id = args.dataset_id

        if not session_id and body is None:
            _emit({"ok": False, "message": "缺少 chat_session_id 或 chat_body_json"}, code=2)

        resp = tool.chat(
            session_id=session_id,
            dataset_id=dataset_id,
            text=text,
            image_url=image_url,
            user=user,
            enable_suggestions=True if (args.enable_suggestions or args.chat_enable_suggestions) else None,
            search_param=search_param,
            context=context,
            body=body,
        )
        _emit(resp, code=0 if resp.get("success") else 1)

    args.search_text = args.search_text or args.text
    args.search_image_url = args.search_image_url or args.image_url or args.image
    args.search_scene_id = args.search_scene_id or args.scene_id
    args.search_dataset_id = args.search_dataset_id or args.dataset_id
    if args.search_page_number == 1 and args.page_number != 1:
        args.search_page_number = args.page_number
    if args.search_page_size == 0 and args.page_size != 0:
        args.search_page_size = args.page_size

    query, err = _build_search_query(args)
    if err:
        _emit({"ok": False, "message": err}, code=2)

    try:
        user = _json_loads(args.user_json) if args.user_json else _json_loads(args.search_user_json)
        filter_obj = _json_loads(args.filter_json) if args.filter_json else _json_loads(args.search_filter_json)
        context = _json_loads(args.context_json) if args.context_json else _json_loads(args.search_context_json)
        conditional_boost = _json_loads(args.conditional_boost_json) if args.conditional_boost_json else _json_loads(args.search_conditional_boost_json)
        output_fields = _parse_output_fields(args.output_fields) if args.output_fields else _parse_output_fields(args.search_output_fields)
    except Exception as e:
        _emit({"ok": False, "message": "参数 JSON 解析失败", "error": {"detail": str(e)}}, code=2)

    page_size = args.page_size if args.page_size and args.page_size > 0 else None
    disable_personalize = True if (args.disable_personalize or args.search_disable_personalize) else None
    sort_by = (args.sort_by.strip() if args.sort_by else args.search_sort_by.strip()) or None
    sort_order = (args.sort_order.strip() if args.sort_order else args.search_sort_order.strip()) or None

    resp = tool.search(
        application_id=args.application_id,
        scene_id=args.search_scene_id,
        dataset_id=args.search_dataset_id,
        session_id=args.session_id,
        query=query,
        page_number=args.page_number,
        page_size=page_size,
        user=user,
        filter=filter_obj,
        sort_by=sort_by,
        sort_order=sort_order,
        output_fields=output_fields,
        context=context,
        conditional_boost=conditional_boost,
        disable_personalize=disable_personalize,
    )
    _emit(resp, code=0 if resp.get("success") else 1)


if __name__ == "__main__":
    main()
