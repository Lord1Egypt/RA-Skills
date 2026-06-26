"""
Memory Workflow 工具封装 - BaseTool 子类

每个操作对应一个 Tool，可直接注册到 Agent 工具注册表
"""
import json
import subprocess
import sys
import os
from pathlib import Path
from dataclasses import dataclass

SCRIPT_DIR = Path(__file__).parent


@dataclass
class ToolResult:
    """工具执行结果"""
    success: bool
    data: dict = None
    error: str = ""

    def __getitem__(self, key):
        return getattr(self, key)


class BaseMemoryTool:
    """Memory Tool 基类"""

    name: str = ""
    description: str = ""
    input_schema: dict = {}

    def validate_input(self, args: dict) -> tuple[bool, str]:
        """验证输入参数"""
        required = self.input_schema.get("required", [])
        for field in required:
            if field not in args:
                return False, f"缺少必需参数: {field}"
        return True, ""

    def call(self, args: dict, context: dict = None) -> ToolResult:
        """执行工具，子类实现"""
        raise NotImplementedError

    def _run_op(self, op: str, extra_args: list = None) -> dict:
        """运行 memory_ops.py，返回 JSON 结果"""
        cmd = [sys.executable, str(SCRIPT_DIR.parent / "memory_ops.py"), op]
        if extra_args:
            cmd.extend(extra_args)
        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=30,
                env={**os.environ, "PYTHONPATH": str(Path(__file__).parent.parent)}
            )
            if result.returncode != 0:
                return {"success": False, "error": result.stderr or result.stdout}
            try:
                return json.loads(result.stdout)
            except json.JSONDecodeError:
                return {"success": True, "output": result.stdout}
        except subprocess.TimeoutExpired:
            return {"success": False, "error": "操作超时"}
        except Exception as e:
            return {"success": False, "error": str(e)}


class MemorySearchTool(BaseMemoryTool):
    """语义搜索记忆库"""

    name = "MemorySearch"
    description = "语义搜索记忆库，支持 rerank 排序，返回最相关的记忆片段"
    input_schema = {
        "type": "object",
        "properties": {
            "query": {
                "type": "string",
                "description": "搜索查询，描述你想找的记忆内容"
            },
            "limit": {
                "type": "integer",
                "default": 3,
                "description": "返回结果数量，默认3条"
            }
        },
        "required": ["query"]
    }

    def call(self, args: dict, context: dict = None) -> ToolResult:
        valid, err = self.validate_input(args)
        if not valid:
            return ToolResult(success=False, error=err)

        query = args["query"]
        limit = args.get("limit", 3)
        result = self._run_op("search", [
            "--query", query,
            "--limit", str(limit),
            "--json"
        ])

        if result.get("success"):
            output = result.get("output", {})
            if isinstance(output, dict):
                return ToolResult(
                    success=True,
                    data={
                        "answer": output.get("answer", ""),
                        "results": output.get("results", []),
                        "count": len(output.get("results", []))
                    }
                )
            return ToolResult(success=True, data=output)
        return ToolResult(success=False, error=result.get("error", "搜索失败"))


class MemoryStoreTool(BaseMemoryTool):
    """存储记忆到记忆库"""

    name = "MemoryStore"
    description = "将重要信息存储到记忆库，自动按日期归档"
    input_schema = {
        "type": "object",
        "properties": {
            "content": {
                "type": "string",
                "description": "要记忆的内容，尽量完整描述"
            },
            "tags": {
                "type": "array",
                "items": {"type": "string"},
                "description": "标签，如 ['发哥', '工作']"
            }
        },
        "required": ["content"]
    }

    def call(self, args: dict, context: dict = None) -> ToolResult:
        valid, err = self.validate_input(args)
        if not valid:
            return ToolResult(success=False, error=err)

        content = args["content"]
        tags = args.get("tags", [])

        tag_args = []
        for tag in tags:
            tag_args.extend(["--tag", tag])

        result = self._run_op("store", ["--content", content, "--json"] + tag_args)

        if result.get("success"):
            return ToolResult(success=True, data=result.get("output", {}))
        return ToolResult(success=False, error=result.get("error", "存储失败"))


class MemoryDedupTool(BaseMemoryTool):
    """去除记忆库中的重复条目"""

    name = "MemoryDedup"
    description = "去除记忆库中的重复条目，基于语义相似度 > 0.85 判定为重复"
    input_schema = {
        "type": "object",
        "properties": {}
    }

    def call(self, args: dict = None, context: dict = None) -> ToolResult:
        result = self._run_op("dedup", ["--json"])
        if result.get("success"):
            return ToolResult(success=True, data=result)
        return ToolResult(success=False, error=result.get("error", "去重失败"))


class MemoryPruneTool(BaseMemoryTool):
    """清理过时记忆"""

    name = "MemoryPrune"
    description = "删除早于指定天数的记忆，默认为 30 天"
    input_schema = {
        "type": "object",
        "properties": {
            "days": {
                "type": "integer",
                "default": 30,
                "description": "删除多少天以前的记忆"
            }
        }
    }

    def call(self, args: dict = None, context: dict = None) -> ToolResult:
        days = (args or {}).get("days", 30)
        result = self._run_op("prune", ["--days", str(days), "--json"])
        if result.get("success"):
            return ToolResult(success=True, data=result)
        return ToolResult(success=False, error=result.get("error", "清理失败"))


class MemoryConsolidateTool(BaseMemoryTool):
    """合并相似的记忆片段"""

    name = "MemoryConsolidate"
    description = "合并相似的记忆片段，减少冗余，保留最完整的信息"
    input_schema = {
        "type": "object",
        "properties": {}
    }

    def call(self, args: dict = None, context: dict = None) -> ToolResult:
        result = self._run_op("consolidate", ["--json"])
        if result.get("success"):
            return ToolResult(success=True, data=result)
        return ToolResult(success=False, error=result.get("error", "合并失败"))


class MemoryListTool(BaseMemoryTool):
    """列出记忆文件"""

    name = "MemoryList"
    description = "列出记忆库中指定日期范围内的记忆文件"
    input_schema = {
        "type": "object",
        "properties": {
            "days": {
                "type": "integer",
                "default": 7,
                "description": "列出多少天以内的记忆"
            }
        }
    }

    def call(self, args: dict = None, context: dict = None) -> ToolResult:
        days = (args or {}).get("days", 7)
        result = self._run_op("list", ["--days", str(days), "--json"])
        if result.get("success"):
            return ToolResult(success=True, data=result)
        return ToolResult(success=False, error=result.get("error", "列出失败"))


# 所有工具列表（供注册用）
ALL_TOOLS = [
    MemorySearchTool,
    MemoryStoreTool,
    MemoryDedupTool,
    MemoryPruneTool,
    MemoryConsolidateTool,
    MemoryListTool,
]
