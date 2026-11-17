"""根据 action 路由到适配器 / 技术栈 / 分析器并执行。对上层屏蔽底层用的是哪个 IDE/Agent。"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

import structlog

from core.adapter_selector import AdapterSelector
from core.config_loader import ConfigLoader, WorkspaceConfig
from core.diff_analyzer import DiffAnalysis, analyze_porcelain
from core.entity_extractor import extract_entities
from core.policy_engine import (
    ConfirmationRequiredError,
    PolicyEngine,
    PolicyViolationError,
)
from core.report_generator import ReportGenerator
from core.schema_contract import SchemaContract
from executor.local_executor import LocalExecutor
from stacks.registry import resolve_stack

logger = structlog.get_logger(__name__)


@dataclass
class ActionResult:
    success: bool
    action: str
    workspace_id: str
    output: str = ""
    error: str = ""
    data: dict = field(default_factory=dict)

    def __bool__(self) -> bool:
        return self.success


class CodeDevManagerDispatcher:
    def __init__(
        self,
        config_loader: ConfigLoader | None = None,
        policy_engine: PolicyEngine | None = None,
        executor: LocalExecutor | None = None,
    ) -> None:
        self._config = config_loader or ConfigLoader()
        self._policy = policy_engine or PolicyEngine()
        self._executor = executor or LocalExecutor()
        self._selector = AdapterSelector(self._config, executor=self._executor)

    # ── 主入口 ────────────────────────────────────────────────────────────
    def dispatch(
        self,
        workspace_id: str,
        action: str,
        params: dict[str, Any] | None = None,
        confirmed: bool = False,
    ) -> ActionResult:
        params = params or {}
        ws = self._config.get_workspace(workspace_id)
        log = logger.bind(workspace_id=workspace_id, action=action, environment=ws.environment)

        try:
            self._policy.check(
                action=action,
                environment=ws.environment,
                plan={"workspace": workspace_id, "action": action, "params": params},
            )
        except PolicyViolationError as e:
            log.warning("action_forbidden", reason=str(e))
            return ActionResult(False, action, workspace_id, error=str(e))
        except ConfirmationRequiredError as e:
            if not confirmed:
                log.info("awaiting_confirmation")
                return ActionResult(
                    False, action, workspace_id,
                    error="需要用户确认后才能执行。",
                    data={"requires_confirmation": True, "plan": e.plan},
                )

        log.info("executing_action")
        try:
            return self._route(ws, action, params)
        except Exception as e:  # noqa: BLE001
            log.error("action_failed", error=str(e))
            return ActionResult(False, action, workspace_id, error=str(e))

    # ── 路由 ──────────────────────────────────────────────────────────────
    def _route(self, ws: WorkspaceConfig, action: str, params: dict) -> ActionResult:
        if action == "list_adapters":
            return self._list_adapters(ws)
        if action == "open_workspace":
            return self._open_workspace(ws, params)
        if action == "read_project":
            return self._read_project(ws, params)
        if action == "detect_stack":
            return self._detect_stack(ws)
        if action == "read_project_context":
            return self._read_project_context(ws, params)
        if action == "get_task_progress":
            return self._get_task_progress(ws, params)
        if action == "analyze_git_diff":
            return self._analyze_git_diff(ws)
        if action == "detect_entities":
            return self._detect_entities(ws)
        if action == "detect_database_changes":
            return self._detect_database_changes(ws)
        if action == "run_tests":
            return self._run_tests(ws)
        if action == "run_build":
            return self._run_build(ws)
        if action == "generate_schema_contract":
            return self._generate_schema_contract(ws, params)
        if action == "generate_report":
            return self._generate_report(ws, params)
        if action == "assign_coding_task":
            return self._assign_coding_task(ws, params)
        if action == "generate_migration":
            return self._generate_migration(ws, params)
        if action == "apply_migration_local":
            return self._apply_migration_local(ws)
        if action == "git_commit":
            return self._git_commit(ws, params)
        return ActionResult(False, action, ws.id, error=f"未知操作：'{action}'")

    # ── 只读动作 ──────────────────────────────────────────────────────────
    def _list_adapters(self, ws: WorkspaceConfig) -> ActionResult:
        return ActionResult(
            True, "list_adapters", ws.id, data={"adapters": self._selector.list_available()}
        )

    def _open_workspace(self, ws: WorkspaceConfig, params: dict) -> ActionResult:
        adapter = self._selector.select(ws, params.get("agent"))
        adapter.open_workspace(ws)
        return ActionResult(
            True,
            "open_workspace",
            ws.id,
            output=f"已通过 {adapter.name} CLI 请求打开工作区：{ws.path}",
            data={"path": ws.path, "agent": adapter.name},
        )

    def _read_project(self, ws: WorkspaceConfig, params: dict) -> ActionResult:
        from pathlib import Path
        root = Path(ws.path)
        exists = root.exists()
        cs_files = len(list(root.rglob("*.cs"))) if exists else 0
        adapter = self._selector.select(ws, params.get("agent")) if params.get("agent") else None
        ctx = adapter.read_project_context(ws) if adapter else None
        return ActionResult(
            True, "read_project", ws.id,
            output=f"工作区 {ws.name}：path={ws.path}，存在={exists}，.cs 文件数={cs_files}",
            data={
                "path": ws.path,
                "exists": exists,
                "cs_file_count": cs_files,
                "stack": ws.stack,
                "agent": adapter.name if adapter else "",
                "agent_summary": ctx.summary if ctx else "",
            },
        )

    def _detect_stack(self, ws: WorkspaceConfig) -> ActionResult:
        adapter = resolve_stack(ws, self._config, self._executor)
        return ActionResult(
            True, "detect_stack", ws.id,
            output=f"技术栈：{adapter.name}（迁移工具：{adapter.migration_tool}）",
            data={"stack": adapter.name, "migration_tool": adapter.migration_tool},
        )

    def _read_project_context(self, ws: WorkspaceConfig, params: dict) -> ActionResult:
        adapter = self._selector.select(ws, params.get("agent"))
        ctx = adapter.read_project_context(ws)
        return ActionResult(
            True, "read_project_context", ws.id,
            output=f"分支：{ctx.branch}；改动文件：{len(ctx.changed_files)} 个；技术栈：{ctx.stack}",
            data={"branch": ctx.branch, "changed_files": ctx.changed_files,
                  "stack": ctx.stack, "agent": adapter.name, "summary": ctx.summary},
        )

    def _get_task_progress(self, ws: WorkspaceConfig, params: dict) -> ActionResult:
        # MVP：本 Skill 不持久化任务，进度直接由 assign_coding_task 返回的 handle 字段反映
        return ActionResult(
            True, "get_task_progress", ws.id,
            output=params.get("status", "unknown"),
            data={"status": params.get("status", "unknown"), "output": params.get("output", "")},
        )

    def _analyze_git_diff(self, ws: WorkspaceConfig) -> ActionResult:
        analysis = self._collect_diff(ws)
        return ActionResult(
            True, "analyze_git_diff", ws.id,
            output=self._summarize_diff(analysis),
            data=self._diff_to_dict(analysis),
        )

    def _detect_entities(self, ws: WorkspaceConfig) -> ActionResult:
        analysis = self._collect_diff(ws)
        entities = extract_entities(ws, self._config, analysis.changed_files, self._executor)
        return ActionResult(
            True, "detect_entities", ws.id,
            output=f"识别到 {len(entities)} 个实体：" + ", ".join(e.name for e in entities),
            data={"entities": [self._entity_to_dict(e) for e in entities]},
        )

    def _detect_database_changes(self, ws: WorkspaceConfig) -> ActionResult:
        analysis = self._collect_diff(ws)
        entities = extract_entities(ws, self._config, analysis.changed_files, self._executor)
        needs = analysis.likely_db_change or bool(entities)
        return ActionResult(
            True, "detect_database_changes", ws.id,
            output=("检测到可能的数据库结构变更" if needs else "未检测到数据库结构变更"),
            data={
                "needs_db_change": needs,
                "entities": [self._entity_to_dict(e) for e in entities],
                "categories": self._diff_to_dict(analysis),
            },
        )

    def _run_tests(self, ws: WorkspaceConfig) -> ActionResult:
        result = resolve_stack(ws, self._config, self._executor).run_tests(ws)
        return ActionResult(result.succeeded, "run_tests", ws.id, output=result.stdout, error=result.stderr)

    def _run_build(self, ws: WorkspaceConfig) -> ActionResult:
        result = resolve_stack(ws, self._config, self._executor).run_build(ws)
        return ActionResult(result.succeeded, "run_build", ws.id, output=result.stdout, error=result.stderr)

    def _generate_schema_contract(self, ws: WorkspaceConfig, params: dict) -> ActionResult:
        analysis = self._collect_diff(ws)
        entities = extract_entities(ws, self._config, analysis.changed_files, self._executor)
        if not entities:
            return ActionResult(
                True, "generate_schema_contract", ws.id,
                output="未识别到实体变化，无需生成数据库变更交接单。",
                data={"changes": []},
            )
        database = params.get("database") or self._infer_database(ws)
        contract = SchemaContract.from_entities(
            entities, feature=params.get("feature", ""), database=database, environment=ws.environment,
        )
        written = contract.write(ws.repo_path)
        return ActionResult(
            True, "generate_schema_contract", ws.id,
            output=f"已生成数据库变更交接单：{written['pending_changes']}（{len(entities)} 张表）",
            data={
                "pending_changes": contract.to_pending_changes(),
                "unified_schema": contract.to_unified_schema(),
                "files": written,
            },
        )

    def _generate_report(self, ws: WorkspaceConfig, params: dict) -> ActionResult:
        report_type = params.get("type", "dev_sync_report")
        report = ReportGenerator().generate(report_type, workspace=ws, params=params, **params)
        return ActionResult(True, "generate_report", ws.id, output=report)

    # ── 需确认动作 ────────────────────────────────────────────────────────
    def _assign_coding_task(self, ws: WorkspaceConfig, params: dict) -> ActionResult:
        prompt = params.get("prompt", "")
        if not prompt:
            return ActionResult(False, "assign_coding_task", ws.id, error="缺少 prompt 参数")
        adapter = self._selector.select(ws, params.get("agent"))
        handle = adapter.assign_coding_task(ws, prompt, timeout=params.get("timeout", 1800))
        return ActionResult(
            handle.status in ("completed", "manual"),
            "assign_coding_task", ws.id,
            output=handle.output, error=handle.error,
            data={"agent": handle.agent, "handle_id": handle.id, "status": handle.status},
        )

    def _generate_migration(self, ws: WorkspaceConfig, params: dict) -> ActionResult:
        name = params.get("name", "")
        if not name:
            return ActionResult(False, "generate_migration", ws.id, error="缺少 name 参数（Migration 名称）")
        result = resolve_stack(ws, self._config, self._executor).generate_migration(ws, name)
        return ActionResult(result.succeeded, "generate_migration", ws.id, output=result.stdout, error=result.stderr)

    def _apply_migration_local(self, ws: WorkspaceConfig) -> ActionResult:
        result = resolve_stack(ws, self._config, self._executor).apply_migration_local(ws)
        return ActionResult(result.succeeded, "apply_migration_local", ws.id, output=result.stdout, error=result.stderr)

    def _git_commit(self, ws: WorkspaceConfig, params: dict) -> ActionResult:
        message = params.get("message", "")
        if not message:
            return ActionResult(False, "git_commit", ws.id, error="缺少 message 参数")
        add = self._executor.execute("git add -A", cwd=ws.repo_path)
        if not add.succeeded:
            return ActionResult(False, "git_commit", ws.id, error=add.stderr or "git add 失败")
        commit = self._executor.execute(["git", "commit", "-m", message], cwd=ws.repo_path)
        return ActionResult(commit.succeeded, "git_commit", ws.id, output=commit.stdout, error=commit.stderr)

    # ── 辅助 ──────────────────────────────────────────────────────────────
    def _collect_diff(self, ws: WorkspaceConfig) -> DiffAnalysis:
        porcelain = self._executor.execute("git status --porcelain", cwd=ws.repo_path).stdout
        return analyze_porcelain(porcelain)

    def _infer_database(self, ws: WorkspaceConfig) -> str:
        if ws.db_context:
            return ws.db_context.removesuffix("DbContext").removesuffix("Context") or ws.db_context
        return "AppDb"

    @staticmethod
    def _summarize_diff(a: DiffAnalysis) -> str:
        return (
            f"新增 {len(a.added)} / 修改 {len(a.modified)} / 删除 {len(a.deleted)}；"
            f"实体 {len(a.entities)}、Migration {len(a.migrations)}、Repository {len(a.repositories)}、"
            f"Controller {len(a.controllers)}、Service {len(a.services)}"
        )

    @staticmethod
    def _diff_to_dict(a: DiffAnalysis) -> dict:
        return {
            "added": a.added, "modified": a.modified, "deleted": a.deleted,
            "entities": a.entities, "migrations": a.migrations, "repositories": a.repositories,
            "controllers": a.controllers, "services": a.services, "others": a.others,
            "likely_db_change": a.likely_db_change,
        }

    @staticmethod
    def _entity_to_dict(e) -> dict:
        return {
            "name": e.name, "table": e.table, "source_file": e.source_file,
            "fields": [
                {"name": f.name, "type": f.unified_type, "nullable": f.nullable,
                 "length": f.length, "primary_key": f.primary_key, "auto_increment": f.auto_increment}
                for f in e.fields
            ],
        }
