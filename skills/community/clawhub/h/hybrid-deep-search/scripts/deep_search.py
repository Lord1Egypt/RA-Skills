#!/usr/bin/env python3
"""
Hybrid Deep Search
混合搜索系统 - Brave API + OpenAI Codex
"""

import os
import sys
import json
import argparse
from typing import Optional, Dict, Any
from router import QueryRouter

# 添加当前目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

class HybridSearch:
    """混合搜索系统"""

    def __init__(self):
        self.router = QueryRouter()
        self.openai_api_key = os.getenv("OPENAI_API_KEY")
        self.openai_base_url = os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1")

    def search(
        self,
        query: str,
        mode: str = "auto",
        focus: str = "web",
        max_results: int = 10,
        verbose: bool = False,
        format: str = "markdown"
    ) -> Dict[str, Any]:
        """
        执行搜索

        Args:
            query: 搜索查询
            mode: 'auto', 'quick' (Brave), 'codex' (OpenAI)
            focus: 'web', 'academic', 'news', 'youtube'
            max_results: 最大结果数
            verbose: 详细输出
            format: 输出格式 ('markdown', 'json', 'text')

        Returns:
            搜索结果字典
        """
        # 路由决策
        if mode == "auto":
            analysis = self.router.analyze(query)
            if verbose:
                self.router.print_analysis(analysis)
            mode = analysis["recommended_mode"]

        # 执行搜索
        if mode == "quick":
            return self._search_brave(query, focus, max_results, format)
        elif mode == "codex":
            return self._search_codex(query, focus, max_results, format)
        else:
            raise ValueError(f"无效的模式: {mode}")

    def _search_brave(
        self,
        query: str,
        focus: str,
        max_results: int,
        format: str
    ) -> Dict[str, Any]:
        """
        使用 Brave API 搜索 (通过 OpenClaw web_search 工具)

        注意: 这个脚本需要通过 OpenClaw 的 Bash 工具调用 web_search
        """
        # 构建搜索命令
        # 实际使用时,这里会调用 OpenClaw 的 web_search 工具
        # 例如: web_search(query, count=max_results)

        result = {
            "mode": "quick",
            "engine": "Brave API",
            "query": query,
            "focus": focus,
            "results": [],
            "status": "success",
            "message": "Brave API 搜索完成 (快速、免费)"
        }

        # 模拟结果 (实际使用时会替换为真实调用)
        if format == "markdown":
            result["output"] = self._format_markdown(result)
        elif format == "json":
            result["output"] = json.dumps(result, indent=2, ensure_ascii=False)
        else:
            result["output"] = self._format_text(result)

        return result

    def _search_codex(
        self,
        query: str,
        focus: str,
        max_results: int,
        format: str
    ) -> Dict[str, Any]:
        """
        使用 OpenAI Codex 搜索
        """
        if not self.openai_api_key:
            error_result = {
                "mode": "codex",
                "engine": "OpenAI Codex",
                "query": query,
                "status": "error",
                "message": "未设置 OPENAI_API_KEY 环境变量",
                "error": "请设置: export OPENAI_API_KEY='sk-...'"
            }
            # 添加格式化输出
            if format == "markdown":
                error_result["output"] = self._format_markdown(error_result)
            elif format == "json":
                error_result["output"] = json.dumps(error_result, indent=2, ensure_ascii=False)
            else:
                error_result["output"] = self._format_text(error_result)
            return error_result

        # 构建 prompt
        prompt = f"""
请对以下查询进行深度搜索和分析:
查询: {query}
聚焦领域: {focus}
最大结果数: {max_results}

要求:
1. 使用 web search 工具获取最新信息
2. 综合多个来源
3. 提供深度分析
4. 给出清晰的结构化回答

请开始搜索并分析...
"""

        result = {
            "mode": "codex",
            "engine": "OpenAI Codex (gpt-5-codex)",
            "query": query,
            "focus": focus,
            "results": [],
            "status": "success",
            "message": "OpenAI Codex 搜索执行中 (深度分析、可能产生费用)"
        }

        # 这里会调用 OpenAI API
        # 实际实现需要使用 openai 库

        # 模拟结果 (实际使用时会替换为真实调用)
        if format == "markdown":
            result["output"] = self._format_markdown(result)
        elif format == "json":
            result["output"] = json.dumps(result, indent=2, ensure_ascii=False)
        else:
            result["output"] = self._format_text(result)

        return result

    def _format_markdown(self, result: Dict) -> str:
        """格式化为 Markdown"""
        lines = []

        # 标题
        lines.append(f"# 🔍 搜索结果\n")
        lines.append(f"**模式:** {result['mode'].upper()}\n")
        lines.append(f"**引擎:** {result['engine']}\n")
        lines.append(f"**查询:** {result['query']}\n")

        # 状态
        if result.get("status") == "error":
            lines.append(f"\n❌ **错误:** {result.get('error', result.get('message'))}")
            return "\n".join(lines)

        # 结果 (模拟)
        lines.append(f"\n## 搜索结果\n")

        if result["mode"] == "quick":
            lines.append(f"⚡ **Brave API 快速搜索结果**\n")
            lines.append(f"\n{result['message']}")
            lines.append(f"\n> 💡 提示: 实际使用时会返回真实的搜索结果\n")
        else:
            lines.append(f"🧠 **OpenAI Codex 深度分析结果**\n")
            lines.append(f"\n{result['message']}")
            lines.append(f"\n> 💡 提示: 实际使用时会返回深度分析结果\n")

        return "\n".join(lines)

    def _format_text(self, result: Dict) -> str:
        """格式化为纯文本"""
        lines = []

        lines.append("="*60)
        lines.append("搜索结果")
        lines.append("="*60)
        lines.append(f"模式: {result['mode'].upper()}")
        lines.append(f"引擎: {result['engine']}")
        lines.append(f"查询: {result['query']}")

        if result.get("status") == "error":
            lines.append(f"\n错误: {result.get('error', result.get('message'))}")
            return "\n".join(lines)

        lines.append(f"\n状态: {result['message']}")
        lines.append("\n" + "-"*60)

        return "\n".join(lines)

def main():
    """命令行入口"""
    parser = argparse.ArgumentParser(
        description="Hybrid Deep Search - 混合搜索系统",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 自动模式 (推荐)
  python3 deep_search.py "what is OpenClaw?"

  # 快速搜索 (Brave API)
  python3 deep_search.py "latest AI news" --mode quick

  # 深度搜索 (OpenAI Codex)
  python3 deep_search.py "compare LangChain vs LlamaIndex" --mode codex

  # 聚焦学术
  python3 deep_search.py "AI agent frameworks" --mode codex --focus academic

  # JSON 输出
  python3 deep_search.py "query" --format json
        """
    )

    parser.add_argument(
        "query",
        help="搜索查询内容"
    )

    parser.add_argument(
        "--mode",
        choices=["auto", "quick", "codex"],
        default="auto",
        help="搜索模式 (默认: auto)"
    )

    parser.add_argument(
        "--focus",
        choices=["web", "academic", "news", "youtube"],
        default="web",
        help="搜索聚焦领域 (默认: web)"
    )

    parser.add_argument(
        "--max-results",
        type=int,
        default=10,
        help="最大结果数 (默认: 10)"
    )

    parser.add_argument(
        "--verbose",
        action="store_true",
        help="详细输出 (包括路由分析)"
    )

    parser.add_argument(
        "--format",
        choices=["markdown", "json", "text"],
        default="markdown",
        help="输出格式 (默认: markdown)"
    )

    args = parser.parse_args()

    # 创建搜索器
    search = HybridSearch()

    # 执行搜索
    result = search.search(
        query=args.query,
        mode=args.mode,
        focus=args.focus,
        max_results=args.max_results,
        verbose=args.verbose,
        format=args.format
    )

    # 输出结果
    print(result["output"])

    # 返回码
    return 0 if result.get("status") == "success" else 1

if __name__ == "__main__":
    sys.exit(main())
