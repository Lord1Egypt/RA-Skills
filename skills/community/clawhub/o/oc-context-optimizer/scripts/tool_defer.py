#!/usr/bin/env python3
"""
Tool Deferral - 工具延迟加载机制
参考 Claude Code 的 Tool Deferral 设计

核心思想：
- 大量工具时不膨胀 prompt
- shouldDefer 标记：需要 ToolSearch 先触发才加载
- alwaysLoad 标记：始终出现在初始 prompt
- ToolSearch：按关键词搜索可用工具，按需加载
"""

import json
import os
import sys
import re
import argparse
from pathlib import Path
from typing import Optional

CONFIG_PATH = Path(__file__).parent.parent / "tool_defer_config.json"
DEFAULT_CONFIG = {
    "always_load": [
        "exec", "read", "write", "edit", "web_search", "web_fetch",
        "message", "session_status", "sessions_spawn", "sessions_send"
    ],
    "deferred_categories": {
        "feishu_doc": {
            "description": "飞书文档管理工具",
            "tools": [
                "feishu_create_doc", "feishu_update_doc", "feishu_fetch_doc",
                "feishu_doc_comments", "feishu_doc_media"
            ],
            "keywords": ["文档", "doc", "document", "wiki", "知识库", "笔记"]
        },
        "feishu_sheet": {
            "description": "飞书电子表格工具",
            "tools": ["feishu_sheet"],
            "keywords": ["表格", "sheet", "excel", "spreadsheet", "数据表"]
        },
        "feishu_bitable": {
            "description": "飞书多维表格工具",
            "tools": [
                "feishu_bitable_app", "feishu_bitable_app_table",
                "feishu_bitable_app_table_field", "feishu_bitable_app_table_record",
                "feishu_bitable_app_table_view"
            ],
            "keywords": ["多维表格", "bitable", "数据表", "字段", "记录", "视图"]
        },
        "feishu_calendar": {
            "description": "飞书日历与日程管理",
            "tools": [
                "feishu_calendar_calendar", "feishu_calendar_event",
                "feishu_calendar_event_attendee", "feishu_calendar_freebusy"
            ],
            "keywords": ["日历", "calendar", "日程", "会议", "日程表", "忙闲", "安排"]
        },
        "feishu_task": {
            "description": "飞书任务管理",
            "tools": [
                "feishu_task_task", "feishu_task_tasklist",
                "feishu_task_comment", "feishu_task_subtask"
            ],
            "keywords": ["任务", "task", "待办", "to-do", "清单", "任务列表"]
        },
        "feishu_chat": {
            "description": "飞书群聊管理",
            "tools": [
                "feishu_chat", "feishu_chat_members",
                "feishu_im_user_message", "feishu_im_user_get_messages",
                "feishu_im_user_search_messages", "feishu_im_user_get_thread_messages",
                "feishu_im_bot_image", "feishu_im_user_fetch_resource"
            ],
            "keywords": ["群聊", "聊天", "chat", "消息", "message", "对话"]
        },
        "feishu_drive": {
            "description": "飞书云空间文件管理",
            "tools": ["feishu_drive_file", "feishu_search_doc_wiki"],
            "keywords": ["云盘", "文件", "drive", "文件夹", "上传", "下载"]
        },
        "feishu_wiki": {
            "description": "飞书知识库管理",
            "tools": ["feishu_wiki_space", "feishu_wiki_space_node"],
            "keywords": ["知识库", "wiki", "知识空间", "节点"]
        },
        "feishu_user": {
            "description": "飞书用户管理",
            "tools": ["feishu_get_user", "feishu_search_user"],
            "keywords": ["用户", "user", "员工", "搜索用户", "查找用户"]
        },
        "feishu_oauth": {
            "description": "飞书授权管理",
            "tools": ["feishu_oauth", "feishu_oauth_batch_auth"],
            "keywords": ["授权", "oauth", "登录", "认证", "token"]
        },
        "browser": {
            "description": "浏览器自动化工具",
            "tools": ["browser"],
            "keywords": ["浏览器", "browser", "网页", "页面", "web页面", "点击", "打开"]
        },
        "image_analysis": {
            "description": "图像分析工具",
            "tools": ["image"],
            "keywords": ["图片", "image", "图像", "看图", "分析图片"]
        },
        "pdf_analysis": {
            "description": "PDF文档分析工具",
            "tools": ["pdf"],
            "keywords": ["pdf", "PDF", "文档分析", "读取PDF"]
        },
        "tts": {
            "description": "语音合成工具",
            "tools": ["tts"],
            "keywords": ["语音", "tts", "说话", "朗读", "声音"]
        },
        "canvas": {
            "description": "画布展示工具",
            "tools": ["canvas"],
            "keywords": ["画布", "canvas", "展示", "渲染", "UI"]
        }
    },
    "search_weights": {
        "tool_name_match": 10,
        "keyword_match": 7,
        "description_match": 5,
        "category_match": 3
    }
}


def ensure_config():
    """确保配置文件存在"""
    if not CONFIG_PATH.exists():
        CONFIG_PATH.write_text(json.dumps(DEFAULT_CONFIG, ensure_ascii=False, indent=2))
        print(f"✅ 已创建默认配置: {CONFIG_PATH}")
    return json.loads(CONFIG_PATH.read_text())


class ToolDeferral:
    """工具延迟加载管理器"""

    def __init__(self, config: Optional[dict] = None):
        self.config = config or ensure_config()
        self.always_load = set(self.config.get("always_load", []))
        self.categories = self.config.get("deferred_categories", {})
        self.weights = self.config.get("search_weights", {})
        self._loaded_tools: set[str] = set()
        self._search_log: list[dict] = []

    @property
    def all_deferred_tools(self) -> set[str]:
        """获取所有延迟工具集合"""
        tools = set()
        for cat in self.categories.values():
            tools.update(cat["tools"])
        return tools

    @property
    def total_tool_count(self) -> int:
        """总工具数（always_load + deferred）"""
        return len(self.always_load) + len(self.all_deferred_tools)

    def search(self, query: str, top_k: int = 5) -> list[dict]:
        """
        ToolSearch：按关键词搜索可用工具

        返回匹配的工具及其描述，按相关性排序
        """
        query_lower = query.lower().strip()
        if not query_lower:
            return []

        results: list[dict] = []
        query_terms = set(re.split(r'[\s,，、]+', query_lower))

        for cat_name, cat_info in self.categories.items():
            score = 0
            matched_keywords = []

            # 1. 工具名匹配 (最高权重)
            for tool in cat_info["tools"]:
                if any(term in tool.lower() for term in query_terms):
                    score += self.weights.get("tool_name_match", 10)
                    matched_keywords.append(f"tool:{tool}")

            # 2. 关键词匹配
            for kw in cat_info["keywords"]:
                for term in query_terms:
                    if term in kw.lower() or kw.lower() in term:
                        score += self.weights.get("keyword_match", 7)
                        matched_keywords.append(f"keyword:{kw}")
                        break

            # 3. 描述匹配
            desc = cat_info.get("description", "")
            if any(term in desc.lower() for term in query_terms):
                score += self.weights.get("description_match", 5)
                matched_keywords.append(f"desc:{desc}")

            # 4. 分类名匹配
            if any(term in cat_name.lower() for term in query_terms):
                score += self.weights.get("category_match", 3)
                matched_keywords.append(f"cat:{cat_name}")

            if score > 0:
                results.append({
                    "category": cat_name,
                    "description": cat_info["description"],
                    "tools": cat_info["tools"],
                    "score": score,
                    "matched_keywords": list(set(matched_keywords))
                })

        results.sort(key=lambda x: x["score"], reverse=True)

        # 记录搜索日志
        self._search_log.append({
            "query": query,
            "results_count": len(results),
            "top_categories": [r["category"] for r in results[:top_k]]
        })

        return results[:top_k]

    def load_tools(self, tool_names: list[str]) -> dict:
        """
        按需加载工具描述

        返回工具的完整信息，用于注入 prompt
        """
        loaded = {}
        for name in tool_names:
            if name in self._loaded_tools:
                continue
            # 查找工具所在分类
            for cat_name, cat_info in self.categories.items():
                if name in cat_info["tools"]:
                    loaded[name] = {
                        "category": cat_name,
                        "description": cat_info["description"]
                    }
                    self._loaded_tools.add(name)
                    break
        return loaded

    def get_initial_prompt_tools(self) -> list[str]:
        """获取初始 prompt 中应包含的工具（always_load）"""
        return sorted(self.always_load)

    def get_deferred_tools(self) -> list[str]:
        """获取所有延迟加载的工具"""
        return sorted(self.all_deferred_tools - self._loaded_tools)

    def get_prompt_stats(self) -> dict:
        """获取 prompt 大小优化统计"""
        total = self.total_tool_count
        initial = len(self.always_load)
        deferred = len(self.all_deferred_tools)
        loaded = len(self._loaded_tools)

        # 估算：每个工具描述约 200 tokens
        tokens_per_tool = 200
        initial_tokens = initial * tokens_per_tool
        deferred_tokens = deferred * tokens_per_tool
        saved_tokens = (total - initial - loaded) * tokens_per_tool

        return {
            "total_tools": total,
            "initial_tools": initial,
            "deferred_tools": deferred,
            "loaded_on_demand": loaded,
            "remaining_deferred": deferred - loaded,
            "initial_token_estimate": initial_tokens,
            "full_token_estimate": total * tokens_per_tool,
            "saved_token_estimate": saved_tokens,
            "savings_percent": round(saved_tokens / (total * tokens_per_tool) * 100, 1) if total > 0 else 0,
            "search_queries_made": len(self._search_log)
        }

    def format_search_results(self, results: list[dict]) -> str:
        """格式化搜索结果为人类可读文本"""
        if not results:
            return "❌ 未找到匹配的工具。尝试其他关键词？"

        lines = [f"🔍 搜索到 {len(results)} 个匹配的工具类别：\n"]
        for i, r in enumerate(results, 1):
            lines.append(f"  {i}. [{r['category']}] {r['description']}")
            lines.append(f"     工具: {', '.join(r['tools'])}")
            lines.append(f"     相关度: {'⭐' * min(r['score'] // 3, 5)} (score={r['score']})")
            lines.append("")
        return "\n".join(lines)

    def format_stats(self) -> str:
        """格式化统计信息"""
        s = self.get_prompt_stats()
        lines = [
            "📊 Tool Deferral 统计",
            "─" * 30,
            f"  总工具数:        {s['total_tools']}",
            f"  初始加载:        {s['initial_tools']} (always_load)",
            f"  延迟加载:        {s['deferred_tools']} (shouldDefer)",
            f"  已按需加载:      {s['loaded_on_demand']}",
            f"  剩余未加载:      {s['remaining_deferred']}",
            "",
            f"  初始 Token 估算:  ~{s['initial_token_estimate']} tokens",
            f"  全量 Token 估算:  ~{s['full_token_estimate']} tokens",
            f"  节省 Token:       ~{s['saved_token_estimate']} tokens ({s['savings_percent']}%)",
            f"  搜索查询次数:    {s['search_queries_made']}",
        ]
        return "\n".join(lines)


def run_tests() -> bool:
    """运行测试"""
    print("🧪 Tool Deferral 测试模式\n")
    passed = 0
    failed = 0

    def check(name, condition, detail=""):
        nonlocal passed, failed
        if condition:
            print(f"  ✅ {name}")
            passed += 1
        else:
            print(f"  ❌ {name} {('- ' + detail) if detail else ''}")
            failed += 1

    td = ToolDeferral()

    # 基础属性测试
    print("1️⃣  基础属性")
    check("always_load 不为空", len(td.always_load) > 0)
    check("deferred_categories 不为空", len(td.categories) > 0)
    check("总工具数 > 0", td.total_tool_count > 0)
    check("always_load 是 deferred 的子集取反",
          len(td.always_load & td.all_deferred_tools) == 0)

    # 搜索测试
    print("\n2️⃣  ToolSearch 搜索")
    r1 = td.search("日历")
    check("搜索'日历'返回结果", len(r1) > 0)
    if r1:
        check("日历分类在结果中", r1[0]["category"] == "feishu_calendar")

    r2 = td.search("文档")
    check("搜索'文档'返回结果", len(r2) > 0)

    r3 = td.search("任务")
    check("搜索'任务'返回结果", len(r3) > 0)

    r4 = td.search("xyz_not_exist_123")
    check("搜索不存在的关键词返回空", len(r4) == 0)

    r5 = td.search("")
    check("空关键词返回空", len(r5) == 0)

    # 加载测试
    print("\n3️⃣  按需加载")
    loaded = td.load_tools(["feishu_calendar_event"])
    check("加载单个工具", len(loaded) == 1)
    check("工具已标记为已加载", "feishu_calendar_event" in td._loaded_tools)

    loaded2 = td.load_tools(["feishu_calendar_event"])
    check("重复加载不重复", len(loaded2) == 0)

    loaded3 = td.load_tools(["feishu_task_task", "feishu_task_tasklist"])
    check("批量加载", len(loaded3) == 2)

    # 统计测试
    print("\n4️⃣  统计信息")
    stats = td.get_prompt_stats()
    check("统计包含 total_tools", "total_tools" in stats)
    check("统计包含 savings_percent", "savings_percent" in stats)
    check("节省百分比 > 0", stats["savings_percent"] > 0)
    check("已按需加载数正确", stats["loaded_on_demand"] == 3)

    # 格式化测试
    print("\n5️⃣  格式化输出")
    fmt = td.format_search_results(r1)
    check("格式化搜索结果为字符串", isinstance(fmt, str) and len(fmt) > 0)

    stats_fmt = td.format_stats()
    check("格式化统计为字符串", isinstance(stats_fmt, str) and "Tool Deferral" in stats_fmt)

    # 总结
    print(f"\n{'─' * 30}")
    print(f"结果: {passed} 通过, {failed} 失败")
    if failed == 0:
        print("🎉 全部通过！")
    return failed == 0


def main():
    parser = argparse.ArgumentParser(
        description="Tool Deferral - 工具延迟加载机制",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  %(prog)s --search "日历"         搜索日历相关工具
  %(prog)s --search "文档管理"      搜索文档管理工具
  %(prog)s --load feishu_calendar_event  加载指定工具
  %(prog)s --stats                 查看统计信息
  %(prog)s --list-always           列出始终加载的工具
  %(prog)s --list-deferred         列出延迟加载的工具
  %(prog)s --test                  运行测试
        """
    )
    parser.add_argument("--search", "-s", type=str, help="搜索工具（按关键词）")
    parser.add_argument("--load", "-l", nargs="+", help="加载指定工具描述")
    parser.add_argument("--stats", action="store_true", help="显示 prompt 优化统计")
    parser.add_argument("--list-always", action="store_true", help="列出 always_load 工具")
    parser.add_argument("--list-deferred", action="store_true", help="列出 deferred 工具")
    parser.add_argument("--json", action="store_true", help="JSON 格式输出")
    parser.add_argument("--test", action="store_true", help="运行测试模式")
    parser.add_argument("--top-k", type=int, default=5, help="搜索返回结果数 (默认 5)")

    args = parser.parse_args()

    if args.test:
        success = run_tests()
        sys.exit(0 if success else 1)

    if not any([args.search, args.load, args.stats, args.list_always, args.list_deferred]):
        parser.print_help()
        sys.exit(0)

    td = ToolDeferral()

    if args.search:
        results = td.search(args.search, top_k=args.top_k)
        if args.json:
            print(json.dumps(results, ensure_ascii=False, indent=2))
        else:
            print(td.format_search_results(results))

    if args.load:
        loaded = td.load_tools(args.load)
        if args.json:
            print(json.dumps(loaded, ensure_ascii=False, indent=2))
        else:
            if loaded:
                print(f"✅ 已加载 {len(loaded)} 个工具：")
                for name, info in loaded.items():
                    print(f"  - {name}: {info['description']}")
            else:
                print("ℹ️  所有指定工具已加载或不存在")

    if args.stats:
        stats = td.get_prompt_stats()
        if args.json:
            print(json.dumps(stats, ensure_ascii=False, indent=2))
        else:
            print(td.format_stats())

    if args.list_always:
        tools = td.get_initial_prompt_tools()
        if args.json:
            print(json.dumps(tools, ensure_ascii=False, indent=2))
        else:
            print("📌 Always Load 工具（始终在初始 prompt 中）：")
            for t in tools:
                print(f"  - {t}")

    if args.list_deferred:
        tools = sorted(td.all_deferred_tools)
        if args.json:
            print(json.dumps(tools, ensure_ascii=False, indent=2))
        else:
            print("⏳ Should Defer 工具（延迟加载）：")
            for t in tools:
                loaded_mark = " ✅" if t in td._loaded_tools else ""
                print(f"  - {t}{loaded_mark}")


if __name__ == "__main__":
    main()
