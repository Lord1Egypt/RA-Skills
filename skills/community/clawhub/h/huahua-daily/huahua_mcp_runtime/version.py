"""Public runtime version and release location for HuahuaDaily MCP."""

__version__ = "4.1.14"

PUBLIC_REPOSITORY_URL = "https://github.com/baiye1997/HuaHuaDailyMCP"
PUBLIC_VERSION_SOURCE_URL = (
    "https://raw.githubusercontent.com/baiye1997/"
    "HuaHuaDailyMCP/main/huahua_mcp_runtime/version.py"
)
UPDATE_INSTRUCTIONS = {
    "uvx": (
        "在 MCP 配置的 uvx args 开头临时加入 --refresh，重启 MCP；"
        "确认版本更新后可移除 --refresh。"
    ),
    "pip": (
        "运行 python -m pip install --upgrade --force-reinstall "
        "git+https://github.com/baiye1997/HuaHuaDailyMCP，然后重启 MCP。"
    ),
    "restartRequired": True,
}
