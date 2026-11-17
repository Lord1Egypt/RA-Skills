from core.config_loader import ConfigLoader
from core.dispatcher import CodeDevManagerDispatcher
from core.policy_engine import PolicyEngine
from executor.base import ExecutionResult

from tests.conftest import FakeExecutor

ENTITY_CS = """
namespace App.Domain.Entities;
public class Customer
{
    [Key]
    public long Id { get; set; }
    [Required]
    public string Name { get; set; }
}
"""


def _dispatcher(config_dir, executor):
    return CodeDevManagerDispatcher(
        config_loader=ConfigLoader(config_dir=config_dir),
        policy_engine=PolicyEngine(config_dir=config_dir),
        executor=executor,
    )


def test_forbidden_action_blocked(config_dir, fake_executor):
    d = _dispatcher(config_dir, fake_executor)
    res = d.dispatch("ws-test", "apply_migration_prod")
    assert res.success is False
    assert "禁止" in res.error


def test_readonly_list_adapters(config_dir, fake_executor):
    d = _dispatcher(config_dir, fake_executor)
    res = d.dispatch("ws-test", "list_adapters")
    assert res.success is True
    names = {a["name"] for a in res.data["adapters"]}
    assert {"codex", "claude_code", "qoer", "lingma", "trae", "vscode"} <= names


def test_confirmation_required_without_confirm(config_dir, fake_executor):
    d = _dispatcher(config_dir, fake_executor)
    res = d.dispatch("ws-test", "generate_migration", {"name": "AddX"})
    assert res.success is False
    assert res.data.get("requires_confirmation") is True


def test_generate_migration_confirmed(config_dir):
    ex = FakeExecutor({"dotnet ef migrations add": ExecutionResult(stdout="Done.", exit_code=0)})
    d = _dispatcher(config_dir, ex)
    res = d.dispatch("ws-test", "generate_migration", {"name": "AddX"}, confirmed=True)
    assert res.success is True
    assert any("migrations add" in (c if isinstance(c, str) else " ".join(c)) for c in ex.calls)


def test_apply_migration_local_requires_test_connection(config_dir):
    # workspaces.yaml 的 ws-test 已配 test_db_connection，应放行到执行
    ex = FakeExecutor({"dotnet ef database update": ExecutionResult(stdout="Applied.", exit_code=0)})
    d = _dispatcher(config_dir, ex)
    res = d.dispatch("ws-test", "apply_migration_local", confirmed=True)
    assert res.success is True


def test_analyze_git_diff(config_dir):
    ex = FakeExecutor({
        "git status --porcelain": ExecutionResult(
            stdout=" M src/Domain/Entities/Customer.cs\nA  src/Api/Controllers/CustomerController.cs\n",
            exit_code=0,
        )
    })
    d = _dispatcher(config_dir, ex)
    res = d.dispatch("ws-test", "analyze_git_diff")
    assert res.success is True
    assert "src/Domain/Entities/Customer.cs" in res.data["entities"]
    assert res.data["likely_db_change"] is True


def test_generate_schema_contract_end_to_end(config_dir, tmp_path):
    repo = tmp_path / "repo"               # 与 fixture 中 workspaces.yaml 的 path 一致
    (repo / "Customer.cs").write_text(ENTITY_CS, encoding="utf-8")
    ex = FakeExecutor({
        "git status --porcelain": ExecutionResult(stdout=" M Customer.cs\n", exit_code=0)
    })
    d = _dispatcher(config_dir, ex)
    res = d.dispatch("ws-test", "generate_schema_contract", {"feature": "客户管理", "database": "GotoPlanDB"})
    assert res.success is True
    unified = res.data["unified_schema"]
    assert unified["database"] == "GotoPlanDB"
    assert unified["tables"][0]["name"] == "Customers"
    # 交接单已写入仓库 .db-contract/
    assert (repo / ".db-contract" / "pending-changes.json").exists()


def test_assign_coding_task_manual_fallback(config_dir, monkeypatch):
    import shutil
    monkeypatch.setattr(shutil, "which", lambda *_a, **_k: None)   # 无 CLI → 选 generic（manual）
    d = _dispatcher(config_dir, FakeExecutor())
    res = d.dispatch("ws-test", "assign_coding_task", {"prompt": "开发客户管理"}, confirmed=True)
    assert res.success is True
    assert res.data["status"] == "manual"


def test_lingma_dispatches_task_through_qoer_cli(config_dir):
    ex = FakeExecutor({"qoer task run": ExecutionResult(stdout="Qoer task accepted", exit_code=0)})
    d = _dispatcher(config_dir, ex)
    res = d.dispatch(
        "ws-test",
        "assign_coding_task",
        {"agent": "lingma", "prompt": "开发客户管理"},
        confirmed=True,
    )
    assert res.success is True
    assert res.data["agent"] == "lingma"
    assert res.data["status"] == "completed"
    assert any("qoer task run" in " ".join(c) for c in ex.calls if isinstance(c, list))


def test_trae_cli_reads_project_context(config_dir):
    ex = FakeExecutor({
        "git rev-parse": ExecutionResult(stdout="main\n", exit_code=0),
        "git status --porcelain": ExecutionResult(stdout=" M Customer.cs\n", exit_code=0),
        "trae project read": ExecutionResult(stdout="Trae project snapshot", exit_code=0),
    })
    d = _dispatcher(config_dir, ex)
    res = d.dispatch("ws-test", "read_project_context", {"agent": "trae"})
    assert res.success is True
    assert res.data["agent"] == "trae"
    assert res.data["summary"] == "Trae project snapshot"
    assert "Customer.cs" in res.data["changed_files"]


def test_dynamic_cli_adapter_can_assign_for_other_ide(config_dir):
    current = (config_dir / "adapters.yaml").read_text(encoding="utf-8")
    (config_dir / "adapters.yaml").write_text(
        current
        + """
  custom_ide:
    enabled: true
    type: cli
    command: custom-ide
    priority: 9
    project_args: ["project", "read", "--workspace", "{repo_path}"]
    task_args: ["task", "run", "--workspace", "{repo_path}", "--prompt", "{prompt}"]
""",
        encoding="utf-8",
    )
    ex = FakeExecutor({"custom-ide task run": ExecutionResult(stdout="accepted", exit_code=0)})
    d = _dispatcher(config_dir, ex)
    res = d.dispatch(
        "ws-test",
        "assign_coding_task",
        {"agent": "custom_ide", "prompt": "实现订单模块"},
        confirmed=True,
    )
    assert res.success is True
    assert res.data["agent"] == "custom_ide"
    assert any("custom-ide task run" in " ".join(c) for c in ex.calls if isinstance(c, list))
