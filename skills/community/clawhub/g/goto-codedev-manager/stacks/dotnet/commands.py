"""dotnet / dotnet ef 命令拼装。集中放置便于按 workspace 的 ef_project 等参数定制。"""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from core.config_loader import WorkspaceConfig


def _project_flags(ws: "WorkspaceConfig") -> str:
    flags = ""
    if ws.ef_project:
        flags += f' --project "{ws.ef_project}"'
    if ws.ef_startup_project:
        flags += f' --startup-project "{ws.ef_startup_project}"'
    if ws.db_context:
        flags += f' --context {ws.db_context}'
    return flags


def migration_add(ws: "WorkspaceConfig", name: str) -> str:
    return f'dotnet ef migrations add {name}{_project_flags(ws)}'


def database_update(ws: "WorkspaceConfig") -> str:
    """对测试库执行 Migration。

    强制显式传 --connection（测试库连接串）；调用方必须保证 ws.test_db_connection 已设置，
    禁止回落到项目默认连接（可能指向生产库）。
    """
    cmd = f'dotnet ef database update{_project_flags(ws)}'
    if ws.test_db_connection:
        cmd += f' --connection "{ws.test_db_connection}"'
    return cmd


def test(ws: "WorkspaceConfig") -> str:
    return ws.test_command or "dotnet test"


def build(ws: "WorkspaceConfig") -> str:
    return ws.build_command or "dotnet build"
