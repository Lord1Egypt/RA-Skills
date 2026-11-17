"""MemoryGuard Core: 本地优先的 Agent 治理引擎。

分层（对应 spec §1.1）:
- 触发层: Agent Skill (见 skill/ 目录)
- 核心层: CLI / Core (本包)
- 展示层: 静态 HTML + localhost GUI + MCP App
- 扩展层: Provider API / Policy Packs
- 持久层: 项目内 .memoryguard/ 文件
"""

__version__ = "0.1.0"
__all__ = ["__version__"]
