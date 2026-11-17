"""
工具护栏 (Tool Guard)
- 读操作：自动批准
- 写操作：需确认
- 危险操作：需明确授权
"""

from enum import Enum
from typing import Optional, Set


class PermissionLevel(Enum):
    """权限级别"""
    READ = "read"           # 读操作：自动批准
    WRITE = "write"         # 写操作：需确认
    DANGEROUS = "dangerous" # 危险操作：需明确授权


# 读操作工具（自动批准）
READ_TOOLS: Set[str] = {
    "read_file", "grep_search", "web_search", "list_files",
    "get_file_info", "search_code", "read", "list", "search",
    "fetch_url", "get_status", "query",
}

# 写操作工具（需确认）
WRITE_TOOLS: Set[str] = {
    "write_file", "edit_file", "execute_code", "create_file",
    "update_file", "append_file", "write", "edit", "create",
    "modify", "save",
}

# 危险操作工具（需明确授权）
DANGEROUS_TOOLS: Set[str] = {
    "delete_file", "execute_shell", "run_command", "shell",
    "exec", "system", "rm", "format", "drop_table",
    "delete", "remove", "format_disk",
}


class ToolGuard:
    """工具护栏：根据权限级别控制工具调用"""

    def __init__(self):
        self.read_tools = READ_TOOLS
        self.write_tools = WRITE_TOOLS
        self.dangerous_tools = DANGEROUS_TOOLS

    def check(self, tool_name: str, params: dict = None) -> "GuardrailResult":
        """
        检查工具调用

        Args:
            tool_name: 工具名称
            params: 工具参数（可选）

        Returns:
            GuardrailResult: 检查结果
        """
        from guardrail import GuardrailResult

        level = self.get_permission_level(tool_name)

        if level == PermissionLevel.READ:
            # 读操作：自动批准
            return GuardrailResult(
                allowed=True,
                reason="读操作，自动批准"
            )

        elif level == PermissionLevel.WRITE:
            # 写操作：需确认
            return GuardrailResult(
                allowed=True,
                requires_confirmation=True,
                reason="写操作，需要用户确认",
                message=f"工具 '{tool_name}' 是写操作，请确认是否执行"
            )

        elif level == PermissionLevel.DANGEROUS:
            # 危险操作：需明确授权
            return GuardrailResult(
                allowed=False,
                requires_authorization=True,
                reason="危险操作，需要明确授权",
                message=f"工具 '{tool_name}' 是危险操作，需要明确授权才能执行"
            )

        else:
            # 未知工具：默认需要确认
            return GuardrailResult(
                allowed=True,
                requires_confirmation=True,
                reason=f"未知工具 '{tool_name}'，需要确认",
                message=f"工具 '{tool_name}' 未在权限列表中，请确认是否允许执行"
            )

    def get_permission_level(self, tool_name: str) -> PermissionLevel:
        """获取工具的权限级别"""
        if tool_name in self.read_tools:
            return PermissionLevel.READ
        elif tool_name in self.write_tools:
            return PermissionLevel.WRITE
        elif tool_name in self.dangerous_tools:
            return PermissionLevel.DANGEROUS
        else:
            # 未知工具默认为写操作级别
            return PermissionLevel.WRITE

    def add_tool(self, tool_name: str, level: PermissionLevel):
        """动态添加工具到权限列表"""
        if level == PermissionLevel.READ:
            self.read_tools.add(tool_name)
        elif level == PermissionLevel.WRITE:
            self.write_tools.add(tool_name)
        elif level == PermissionLevel.DANGEROUS:
            self.dangerous_tools.add(tool_name)


if __name__ == "__main__":
    # 测试
    guard = ToolGuard()

    test_cases = [
        ("read", "read"),
        ("write_file", "write"),
        ("rm", "dangerous"),
        ("unknown_tool", "write"),  # 未知工具默认为写
    ]

    for tool, expected_level in test_cases:
        result = guard.check(tool)
        level = guard.get_permission_level(tool)
        print(f"工具 '{tool}': level={level.value}, allowed={result.allowed}, "
              f"requires_confirmation={result.requires_confirmation}, "
              f"requires_authorization={result.requires_authorization}")
