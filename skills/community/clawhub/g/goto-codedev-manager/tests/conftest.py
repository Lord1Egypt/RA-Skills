"""测试公共 fixture：临时 config 目录 + 假执行器。"""

from __future__ import annotations

import pytest

from executor.base import ExecutionResult, ExecutorBase

ADAPTERS_YAML = """
adapters:
  codex:        { enabled: true, type: cli, command: codex, priority: 1 }
  claude_code:  { enabled: true, type: cli, command: claude, priority: 2 }
  qoer:
    enabled: true
    type: cli
    command: qoer
    priority: 3
    project_args: ["project", "read", "--workspace", "{repo_path}"]
    task_args: ["task", "run", "--workspace", "{repo_path}", "--prompt", "{prompt}"]
  lingma:
    enabled: true
    type: cli
    command: qoer
    priority: 4
    project_args: ["project", "read", "--workspace", "{repo_path}"]
    task_args: ["task", "run", "--workspace", "{repo_path}", "--prompt", "{prompt}"]
  trae:
    enabled: true
    type: cli
    command: trae
    priority: 5
    project_args: ["project", "read", "--workspace", "{repo_path}"]
    task_args: ["task", "run", "--workspace", "{repo_path}", "--prompt", "{prompt}"]
  vscode:       { enabled: true, type: cli, command: code, priority: 6 }
  cursor:       { enabled: true, type: cli, command: cursor, priority: 7 }
  qoder:        { enabled: true, type: cli, command: qoder, priority: 8 }
  generic:      { enabled: true, type: workspace, priority: 100 }
"""

STACKS_YAML = """
stacks:
  dotnet:
    name: .NET / EF Core
    migration_tool: efcore
    type_map:
      long: bigint
      int: int
      short: smallint
      byte: tinyint
      string: string
      decimal: decimal
      bool: boolean
      DateTime: datetime
      Guid: uuid
"""

POLICIES_YAML = """
policies:
  default:
    readonly_allowed:
      - list_adapters
      - read_project
      - read_project_context
      - detect_stack
      - analyze_git_diff
      - detect_entities
      - detect_database_changes
      - generate_schema_contract
      - generate_report
      - run_tests
      - run_build
    confirmation_required:
      - assign_coding_task
      - generate_migration
      - apply_migration_local
      - git_commit
    forbidden:
      - apply_migration_prod
      - force_push
      - reset_hard
  test:
    inherits: default
"""


def make_workspaces_yaml(path: str) -> str:
    return f"""
workspaces:
  - id: ws-test
    name: 测试工作区
    path: {path}
    git_repo: {path}
    stack: dotnet
    preferred_agent: codex
    fallback_agent: claude_code
    environment: test
    ef_project: src/App.Infrastructure
    db_context: AppDbContext
    test_db_connection: Server=localhost;Database=App_Test;
"""


@pytest.fixture
def config_dir(tmp_path):
    d = tmp_path / "config"
    d.mkdir()
    (d / "adapters.yaml").write_text(ADAPTERS_YAML, encoding="utf-8")
    (d / "stacks.yaml").write_text(STACKS_YAML, encoding="utf-8")
    (d / "policies.yaml").write_text(POLICIES_YAML, encoding="utf-8")
    (d / "workspaces.yaml").write_text(make_workspaces_yaml(str(tmp_path / "repo")), encoding="utf-8")
    (tmp_path / "repo").mkdir()
    return d


class FakeExecutor(ExecutorBase):
    """按命令前缀返回预设结果，记录调用历史。"""

    def __init__(self, responses: dict | None = None) -> None:
        self.responses = responses or {}
        self.calls: list = []

    def execute(self, command, cwd=None, timeout=120) -> ExecutionResult:
        self.calls.append(command)
        key = command if isinstance(command, str) else " ".join(command)
        for prefix, result in self.responses.items():
            if key.startswith(prefix):
                return result
        return ExecutionResult(stdout="", stderr="", exit_code=0)


@pytest.fixture
def fake_executor():
    return FakeExecutor()
