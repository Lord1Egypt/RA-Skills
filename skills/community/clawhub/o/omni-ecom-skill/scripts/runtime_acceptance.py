#!/usr/bin/env python3
"""Run a real WorkBuddy candidate pipeline acceptance and verify its local receipts."""

from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from artifact_contract import validate_team_bootstrap_identity
from host_runtime import Runtime


ANALYSIS_AGENTS = (
    "data-analyst",
    "platform-ops",
    "content-live-growth",
    "ad-profit-optimizer",
)
REQUIRED_MEMBERS = (*ANALYSIS_AGENTS, "delivery-review")
TASK_ID_RE = re.compile(r"^agent-[0-9A-Za-z_-]+$")
ACCEPTANCE_SCOPE = "runtime-acceptance-no-client-data"


def resolve_command(cli_path: str | None = None) -> list[str] | None:
    if cli_path:
        cli = Path(cli_path).resolve()
        node = shutil.which('node')
        if not cli.is_file() or not node:
            raise ValueError('explicit_native_cli_unavailable')
        return [node, str(cli)]
    command = shutil.which("codebuddy.cmd") or shutil.which("codebuddy")
    if not command:
        return None
    command_path = Path(command)
    if command_path.suffix.casefold() == ".cmd":
        base = command_path.parent
        node = base / "node.exe"
        cli = base / "node_modules" / "@tencent-ai" / "codebuddy-code" / "bin" / "codebuddy"
        if not node.is_file():
            node_value = shutil.which("node")
            node = Path(node_value) if node_value else node
        if node.is_file() and cli.is_file():
            return [str(node), str(cli)]
    return [str(command_path)]


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8-sig"))


def build_card_instructions(version: str, run_id: str, team_name: str, run_dir: Path, scaffold_command: str) -> str:
    instructions = f"""这是 omni-ecom v{version} 的真实多专家安装验收，不读取任何客户业务文件，也不生成经营结论。请把本次验收视为 comprehensive 的 single_topic，并完成整个正式链路。

硬要求：
1. 第一个执行动作必须是实际 TeamCreate，名称精确为 `{team_name}`；client_scope 固定为 {ACCEPTANCE_SCOPE}；run_id 精确为 `{run_id}`；运行目录精确为 `{run_dir}`。
2. TeamCreate 成功后，第二个执行动作必须原样运行：`{scaffold_command}`。不得手写、改写或覆盖 team-bootstrap、host-orchestration-plan、report-inventory、report-clusters、chapter-plan、baseline-pack、task-cards 或 launch-manifest；固定程序失败立即停止。
3. 创建可见阶段任务并由团长维护 TaskUpdate；成员不要调用 TaskList/TaskUpdate。随后从 launch-manifest 连续创建四位分析 Agent，完整使用 dispatch_parameters（特别是精确 team_name）及逐字 launch_prompt；不得展开或改写 prompt，单条不超过 300 字。四位都取得真实 task_id 后才统一等待；四次调用之间不得等待、读回传或并稿。
4. 每位成员读取任务卡，首次 a1 亲自填写 expert_analysis_template 的业务分析、六个机制问题和自检，写入 paths.expert_analysis，再运行 finish_command 生成完整 `omni-ecom.expert-handoff@2.0` 与唯一 role-scoped return。程序仅装配固定字段，禁止团长代写专家内容。成员只回传真实状态、回执路径、handoff_sha256 一次并立即结束，不在消息中复述全文。attempt 精确为 a1；禁止简化健康回传或连续重派；真实失败才允许受控 a2，a3 禁止。
5. 创建四位成员后，原样执行 acceptance-scaffold-receipt.json 的 `wait_command`，禁止自行拼接等待参数或改写路径；若返回 waiting 状态，只能原样重试同一命令。四份 a1 合法后，读取 `analysis_binding_command_template`，仅替换四个 `<真实task_id>` 后原样执行；只能使用该程序产生的 `sealed/` 文件，禁止直接调用 seal_handoff.py。随后依次原样执行回执中的 `after_binding_commands`。claim-ledger.json、run-scope.json 和 team-lead-handoff.json 已由 scaffold 固定生成，禁止手写、改写或覆盖。
6. `after_binding_commands` 全部成功后，原样执行 scaffold 回执的 `review_prepare_command`；再逐字使用 review-launch-manifest.json 的 launch_prompt 创建 delivery-review（韦交达），随后原样执行其中的 `wait_command`，不得自行拼接复核回传路径。a1 回传若不合法、不是 passed 或含 required_changes，本轮立即 fail closed，不得临时猜字段或连续发起 a2/a3/a4。合法真实回传后，仅替换 finalize_command_template 的 `<真实review_task_id>` 并原样执行；不得手写复核证明、公域回执或候选完成凭证。该完成凭证只证明候选流水线通过，不得冒充已发布版本。
7. finalize 成功后，最终答复第一屏必须逐字复制 acceptance-finalize-receipt.json 的 `required_final_summary`，不得省略其中任何一行；它包含专家团 v{version}、run_id、team_name、candidate_pipeline_complete 和五位成员真实 agent_task_id。最终答复前 TaskList 中本次阶段任务必须全部 completed；若仍有悬空任务，继续处理，不得提前结束。
8. 若 TeamCreate/Agent/回传/复核/任一固定命令失败，立即报告实际错误并结束本轮验收，不继续猜字段、比较时间、遍历目录、查 SQLite、手写 Python 或调查哈希算法；诊断由维护者另行只读处理。严禁团长代写、模拟成员或编造 task_id。
"""
    if "-candidate." not in version:
        instructions = instructions.replace("候选完成凭证", "安装验收完成凭证").replace(
            "该完成凭证只证明候选流水线通过，不得冒充已发布版本。",
            "该凭证只证明本次无客户数据的安装验收通过，不证明任何客户经营结论。"
        ).replace("candidate_pipeline_complete", "formal_delivery_complete")
        instructions += "\n当前为正式版：completion_gate 不传 --candidate-acceptance，使用 completion-receipt.json；不得沿用历史候选回执。\n"
    return instructions


def write_lead_card(workdir: Path, runs_root: Path, plugin_dir: Path, version: str, prefix: str, label: str | None) -> tuple[Path, Path]:
    suffix = str(label or datetime.now(timezone.utc).strftime("%Y%m%d%H%M%S")).strip()
    if not re.fullmatch(r"[0-9A-Za-z_-]+", suffix):
        raise ValueError("acceptance_run_label_invalid")
    run_id = f"{prefix}{suffix}"
    team_name = f"omni-ecom-{run_id}"
    run_dir = (runs_root / run_id).resolve()
    if run_dir.exists():
        raise ValueError("acceptance_run_already_exists")
    card_path = (workdir / f"{run_id}.lead-card.json").resolve()
    scaffold_command = f'python -B "{plugin_dir.resolve() / "scripts" / "prepare_workbuddy_acceptance_scaffold.py"}" --lead-card "{card_path}" --plugin-dir "{plugin_dir.resolve()}"'
    payload = {
        "schema_version": "2.0",
        "artifact_type": "workbuddy_acceptance_lead_card",
        "version": version,
        "run_id": run_id,
        "team_name": team_name,
        "client_scope": ACCEPTANCE_SCOPE,
        "run_dir": str(run_dir),
        "created_at": datetime.now(timezone.utc).isoformat(),
        "immutable_after_launch": True,
        "permitted_reads": [
            str(card_path),
            "files generated inside run_dir",
            "native Team/Task/Agent results for this team only",
        ],
        "forbidden_exploration": ["script source", "--help", "unrelated references", "other runs"],
        "scaffold_command": scaffold_command,
        "instructions": build_card_instructions(version, run_id, team_name, run_dir, scaffold_command),
    }
    card_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return card_path, run_dir


def build_prompt(card_path: Path) -> str:
    return f"OMNI_ECOM_ACCEPTANCE_CARD\n读取并严格执行唯一验收任务卡：{card_path}。不要读取脚本源码、--help 或其他参考文件，不要扩写工具参数；失败按卡片 fail closed。"


def build_resume_prompt(version: str, run_dir: Path, allow_rebind: bool = False, after_maintenance: bool = False) -> str:
    rebind = ("若宿主报告 No active team / Not in a team，只允许调用一次 TeamCreate，team_name 必须与 team-bootstrap.json 完全相同，目的仅是把当前续跑会话重新绑定到磁盘上已存在的团队；不得换名、不得删除或覆盖团队文件、不得新建 run_id。TeamCreate 若拒绝同名重绑，立即停止。"
              if allow_rebind else "不得 TeamCreate；若宿主丢失现有团队绑定则如实停止。")
    prompt = f"""继续同一个 omni-ecom v{version} 真实验收，不得新建 run_id，也不得重复启动已经回传的分析专家。现有运行目录是 `{run_dir}`。{rebind} 先读取该目录的 SQLite 状态、四份 sealed handoff 和宿主阶段任务；从实际未完成阶段继续。若四位分析专家已完成，直接完成团长裁决、报告与图表 PDF，随后只创建尚未创建的 delivery-review；已有 review a1 真实失败时仅允许 a2。最后用 completion_gate.py --candidate-acceptance 生成 candidate-acceptance-receipt.json。最终保持候选身份，显示 candidate_pipeline_complete、原 team_name 和五位真实 agent_task_id；失败时如实停在未完成状态。"""
    if "-candidate." not in version:
        prompt = prompt.replace("completion_gate.py --candidate-acceptance", "completion_gate.py").replace("candidate-acceptance-receipt.json", "completion-receipt.json").replace("保持候选身份", "标注正式版安装验收身份（非客户报告）").replace("candidate_pipeline_complete", "formal_delivery_complete")
    if after_maintenance:
        scaffold = load_json(run_dir/'acceptance-scaffold-receipt.json')
        binding = load_json(run_dir/'analysis-binding-receipt.json')
        if scaffold.get('run_id') != binding.get('run_id') or binding.get('status') != 'analysis_returns_bound':
            raise ValueError('maintenance_resume_binding_invalid')
        if (run_dir/'report.json').exists() or (run_dir/'review-launch-manifest.json').exists():
            raise ValueError('maintenance_resume_requires_report_pending')
        completion_status = 'candidate_pipeline_complete' if '-candidate.' in version else 'formal_delivery_complete'
        prompt = f'''维护者已修复报告构建程序并完成专项检查，现在由你实际验证修复后的固定流程。不要自行诊断此前错误、猜字段、读源码、手写或改写任何 handoff。运行目录：{run_dir}。原四位专家已真实完成并封存，禁止重新派工、新建团队、新建 run_id。{rebind}
第一执行动作必须原样执行报告构建命令：{scaffold['after_binding_commands'][4]}
如果失败，报告真实错误并结束，不调查、不覆盖输入。
成功后原样执行：{scaffold['review_prepare_command']}
读取该程序生成的 review-launch-manifest.json，逐字使用 launch_prompt 创建唯一 delivery-review，记录真实 task_id；原样执行 wait_command。复核必须真实 passed 且 required_changes 为空；其他结果不放行。
只替换 finalize_command_template 中的真实 review_task_id 后原样执行。成功后由团长使用 TaskList/TaskUpdate 收尾所有五阶段任务（包括被成员错误认领的已有阶段，不能新建重复任务），再次 TaskList 确认全部 completed。
最终第一屏逐字复制 acceptance-finalize-receipt.json 的 required_final_summary，必须显示版本 {version}、原 run_id、原 team_name、{completion_status} 和五位真实 task_id。安装验收不是客户经营分析。不得手写完成凭证。'''
    return prompt


def inspect_run(run_dir: Path, version: str, stdout: str) -> tuple[list[str], dict[str, Any]]:
    errors: list[str] = []
    bootstrap_path = run_dir / "team-bootstrap.json"
    candidate_mode = "-candidate." in version
    completion_path = run_dir / ("candidate-acceptance-receipt.json" if candidate_mode else "completion-receipt.json")
    if not bootstrap_path.is_file():
        errors.append("team_bootstrap_missing")
        bootstrap: dict[str, Any] = {}
    else:
        bootstrap = load_json(bootstrap_path)
        try:
            validate_team_bootstrap_identity(bootstrap,version,bootstrap.get('run_id'),ACCEPTANCE_SCOPE)
        except ValueError as exc:
            errors.append(str(exc))
        if bootstrap.get("status") != "team_created":
            errors.append("team_not_created")
        if str(bootstrap.get("team_version")) != version:
            errors.append("bootstrap_version_mismatch")
        if not bootstrap.get("team_name"):
            errors.append("team_name_missing")

    if not completion_path.is_file():
        errors.append("completion_receipt_missing")
        completion: dict[str, Any] = {}
    else:
        completion = load_json(completion_path)
        expected_status = "candidate_pipeline_complete" if candidate_mode else "formal_delivery_complete"
        if completion.get("status") != expected_status:
            errors.append("candidate_pipeline_completion_missing" if candidate_mode else "formal_completion_missing")
        if str(completion.get("team_version")) != version:
            errors.append("completion_version_mismatch")
        if completion.get("collaboration_mode") != "comprehensive":
            errors.append("collaboration_mode_not_comprehensive")

    activity = {
        str(item.get("agent_id")): item
        for item in completion.get("expert_activity", [])
        if isinstance(item, dict)
    }
    for agent_id in REQUIRED_MEMBERS:
        item = activity.get(agent_id)
        if not item or item.get("participation_status") != "contributed":
            errors.append(f"member_not_contributed:{agent_id}")
            continue
        task_ids = [str(value) for value in item.get("agent_task_ids", [])]
        if not task_ids or any(not TASK_ID_RE.fullmatch(value) for value in task_ids):
            errors.append(f"member_task_id_invalid:{agent_id}")
        for task_id in task_ids:
            if task_id not in stdout:
                errors.append(f"task_id_not_visible_in_final:{agent_id}")

    runtime_status: dict[str, Any] = {}
    if (run_dir / "run-journal.sqlite").is_file() and bootstrap.get("run_id"):
        try:
            runtime = Runtime(run_dir, str(bootstrap["run_id"]), ACCEPTANCE_SCOPE)
            try:
                runtime_status = runtime.status()
            finally:
                runtime.close()
        except (OSError, ValueError):
            errors.append("runtime_status_unreadable")
    raw_dir = run_dir / "raw-handoffs"
    for agent_id in ANALYSIS_AGENTS:
        attempts = sorted(raw_dir.glob(f"handoff-{agent_id}-a*.json")) if raw_dir.is_dir() else []
        names = [path.name for path in attempts]
        if names == [f"handoff-{agent_id}-a1.json"]:
            continue
        if names == [f"handoff-{agent_id}-a1.json", f"handoff-{agent_id}-a2.json"]:
            rejected = any(item.get("role") == agent_id and item.get("state") in {"member_rejected", "member_failed"}
                           for item in runtime_status.get("members", []))
            selected = runtime_status.get("selected_returns", {}).get(agent_id, {})
            if rejected and str(selected.get("attempt_id") or "").endswith("a2"):
                continue
        errors.append(f"attempt_contract_not_met:{agent_id}:{','.join(names)}")

    visible_status = "candidate_pipeline_complete" if candidate_mode else "formal_delivery_complete"
    if visible_status not in stdout:
        errors.append("pipeline_status_not_visible_in_final")
    if f"v{version}" not in stdout:
        errors.append("version_not_visible_in_final")
    if bootstrap.get("team_name") and str(bootstrap["team_name"]) not in stdout:
        errors.append("team_name_not_visible_in_final")

    team_name = str(bootstrap.get("team_name") or "").strip()
    if team_name:
        native_config=Path(os.environ.get('CODEBUDDY_CONFIG_DIR') or str(Path.home()/'.codebuddy')).resolve()
        task_root = native_config / "tasks" / team_name
        task_files = sorted(task_root.glob("*.json")) if task_root.is_dir() else []
        if not task_files:
            errors.append("phase_task_records_missing")
        for path in task_files:
            try:
                task = load_json(path)
            except (OSError, UnicodeError, json.JSONDecodeError):
                errors.append(f"phase_task_record_invalid:{path.name}")
                continue
            if task.get("status") != "completed":
                errors.append(f"phase_task_not_completed:{path.stem}:{task.get('status', 'missing')}")

        inbox_root = native_config / "teams" / team_name / "inboxes"
        for agent_id in REQUIRED_MEMBERS:
            inbox = inbox_root / f"{agent_id}.json"
            if not inbox.is_file():
                errors.append(f"member_inbox_missing:{agent_id}")
                continue
            try:
                messages = json.loads(inbox.read_text(encoding="utf-8-sig"))
            except (OSError, UnicodeError, json.JSONDecodeError):
                errors.append(f"member_inbox_invalid:{agent_id}")
                continue
            if not isinstance(messages, list):
                errors.append(f"member_inbox_invalid:{agent_id}")
            elif messages:
                errors.append(f"peer_chatter_detected:{agent_id}:{len(messages)}")
    return errors, {"bootstrap": bootstrap, "completion": completion}


def discover_runs(runs_root: Path, workdir: Path, prefix: str) -> list[Path]:
    roots = [runs_root, workdir / ".omni-ecom-runs"]
    found: dict[str, Path] = {}
    for root in roots:
        if not root.is_dir():
            continue
        for path in root.glob(f"{prefix}*"):
            if path.is_dir():
                resolved = path.resolve()
                found[str(resolved).casefold()] = resolved
    return list(found.values())


def main() -> int:
    parser = argparse.ArgumentParser(description="Run real omni-ecom TeamCreate + five-member runtime acceptance")
    parser.add_argument("--plugin-dir", default=str(Path(__file__).resolve().parents[1]))
    parser.add_argument("--cli", help="Explicit target host bundled CLI path, instead of guessing from PATH")
    parser.add_argument("--workdir", default=str(Path.cwd()))
    parser.add_argument("--runs-root")
    parser.add_argument("--timeout", type=int, default=2700)
    parser.add_argument("--no-auto-approve", action="store_true")
    parser.add_argument("--inspect-run", help="Inspect an existing runtime run instead of launching a new session")
    parser.add_argument("--final-output-json", help="JSON file containing the captured final stdout for --inspect-run")
    parser.add_argument("--resume-session", help="Resume the same WorkBuddy session after an external interruption")
    parser.add_argument("--resume-run", help="Existing run directory paired with --resume-session")
    parser.add_argument("--resume-after-maintenance", action="store_true", help="Resume a repaired, analysis-bound run directly at its fixed report command")
    parser.add_argument("--model", help="Explicit WorkBuddy model for a resumed acceptance")
    parser.add_argument("--run-label", help="Stable suffix for the fresh acceptance run id")
    parser.add_argument("--allow-rebind-existing-team", action="store_true", help="Allow one exact-name TeamCreate only to recover a lost host team binding")
    parser.add_argument("--output")
    args = parser.parse_args()

    plugin_dir = Path(args.plugin_dir).resolve()
    workdir = Path(args.workdir).resolve()
    runs_root = Path(args.runs_root).resolve() if args.runs_root else workdir / "runs"
    manifest = load_json(plugin_dir / ".codebuddy-plugin" / "plugin.json")
    version = str(manifest.get("version") or "")
    prefix = f"acc-v{version.replace('.', '')}-"
    lead_card: Path | None = None
    if not args.inspect_run and not args.resume_session:
        workdir.mkdir(parents=True, exist_ok=True)
        runs_root.mkdir(parents=True, exist_ok=True)
        try:
            lead_card, _ = write_lead_card(workdir, runs_root, plugin_dir, version, prefix, args.run_label)
        except ValueError as exc:
            result = {"status": "FAIL", "reason": str(exc), "version": version}
            payload = json.dumps(result, ensure_ascii=False, indent=2) + "\n"
            if args.output:
                output = Path(args.output).resolve(); output.parent.mkdir(parents=True, exist_ok=True); output.write_text(payload, encoding="utf-8")
            print(payload, end="")
            return 1
    before = {path.resolve() for path in discover_runs(runs_root, workdir, prefix)}
    command = resolve_command(args.cli)
    result: dict[str, Any]
    if args.inspect_run:
        run_dir = Path(args.inspect_run).resolve()
        stdout = ""
        if args.final_output_json:
            stdout = str(load_json(Path(args.final_output_json).resolve()).get("stdout") or "")
        errors, evidence = inspect_run(run_dir, version, stdout)
        result = {
            "status": "PASS" if not errors else "FAIL",
            "mode": "inspect_existing_run",
            "environment": "live",
            "host": "workbuddy",
            "acceptance_domain": "workbuddy_native_multi_agent_pdf",
            "evidence_kind": "native_host_acceptance",
            "version": version,
            "run_dir": str(run_dir),
            "run_id": evidence["completion"].get("run_id") or evidence["bootstrap"].get("run_id"),
            "team_name": evidence["bootstrap"].get("team_name"),
            "errors": errors,
            "pipeline_completion_verified": not errors,
            "multi_agent_complete": not any(error.startswith("member_") or error.startswith("first_attempt_") for error in errors),
            "pdf_review_passed": not any("completion" in error or "review" in error for error in errors),
        }
    elif args.resume_session:
        if not command:
            result = {"status": "INCONCLUSIVE", "reason": "codebuddy_not_found", "version": version}
        elif not args.resume_run:
            result = {"status": "FAIL", "reason": "resume_run_required", "version": version}
        else:
            run_dir = Path(args.resume_run).resolve()
            invocation = [*command, "-p", "-y", "--plugin-dir", str(plugin_dir), "--resume", args.resume_session]
            if args.model:
                invocation.extend(["--model", args.model])
            invocation.append(build_resume_prompt(version, run_dir, args.allow_rebind_existing_team, args.resume_after_maintenance))
            try:
                completed = subprocess.run(invocation, cwd=workdir, capture_output=True, text=True,
                                           encoding="utf-8", errors="replace", timeout=args.timeout, check=False)
                stdout = (completed.stdout or "").strip(); stderr = (completed.stderr or "").strip()
                errors, evidence = inspect_run(run_dir, version, stdout)
                result = {
                    "status": "PASS" if completed.returncode == 0 and not errors else "FAIL",
                    "environment": "live", "host": "workbuddy",
                    "acceptance_domain": "workbuddy_native_multi_agent_pdf",
                    "evidence_kind": "native_host_acceptance", "version": version,
                    "mode": "resume_existing_session", "run_dir": str(run_dir),
                    "run_id": evidence["completion"].get("run_id") or evidence["bootstrap"].get("run_id"),
                    "team_name": evidence["bootstrap"].get("team_name"), "exit_code": completed.returncode,
                    "errors": errors,
                    "pipeline_completion_verified": completed.returncode == 0 and not errors,
                    "multi_agent_complete": not any(error.startswith("member_") or error.startswith("first_attempt_") for error in errors),
                    "pdf_review_passed": not any("completion" in error or "review" in error for error in errors),
                    "stdout": stdout, "stderr": stderr,
                }
            except subprocess.TimeoutExpired as exc:
                result = {"status": "INCONCLUSIVE", "reason": "runtime_acceptance_resume_timeout", "version": version,
                          "run_dir": str(run_dir), "stdout": (exc.stdout or "") if isinstance(exc.stdout, str) else "",
                          "stderr": (exc.stderr or "") if isinstance(exc.stderr, str) else ""}
            except OSError as exc:
                result = {"status": "INCONCLUSIVE", "reason": "resume_launch_error", "version": version, "message": str(exc)}
    elif not command:
        result = {"status": "INCONCLUSIVE", "reason": "codebuddy_not_found", "version": version}
    else:
        invocation = [*command, "-p"]
        if not args.no_auto_approve:
            invocation.append("-y")
        invocation.extend(["--plugin-dir", str(plugin_dir), "--agent", "omni-ecom-team-lead"])
        if args.model:
            invocation.extend(["--model", args.model])
        invocation.append(build_prompt(lead_card))
        try:
            completed = subprocess.run(
                invocation,
                cwd=workdir,
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
                timeout=args.timeout,
                check=False,
            )
            stdout = (completed.stdout or "").strip()
            stderr = (completed.stderr or "").strip()
            candidates = [path for path in discover_runs(runs_root, workdir, prefix) if path.resolve() not in before]
            candidates.sort(key=lambda path: path.stat().st_mtime, reverse=True)
            if not candidates:
                result = {
                    "status": "FAIL",
                    "reason": "acceptance_run_not_created",
                    "version": version,
                    "exit_code": completed.returncode,
                    "stdout": stdout,
                    "stderr": stderr,
                }
            else:
                run_dir = candidates[0].resolve()
                errors, evidence = inspect_run(run_dir, version, stdout)
                result = {
                    "status": "PASS" if completed.returncode == 0 and not errors else "FAIL",
                    "environment": "live",
                    "host": "workbuddy",
                    "acceptance_domain": "workbuddy_native_multi_agent_pdf",
                    "evidence_kind": "native_host_acceptance",
                    "version": version,
                    "run_dir": str(run_dir),
                    "run_id": evidence["completion"].get("run_id") or evidence["bootstrap"].get("run_id"),
                    "team_name": evidence["bootstrap"].get("team_name"),
                    "exit_code": completed.returncode,
                    "errors": errors,
                    "pipeline_completion_verified": completed.returncode == 0 and not errors,
                    "multi_agent_complete": not any(error.startswith("member_") or error.startswith("first_attempt_") for error in errors),
                    "pdf_review_passed": not any("completion" in error or "review" in error for error in errors),
                    "stdout": stdout,
                    "stderr": stderr,
                }
        except subprocess.TimeoutExpired as exc:
            candidates = [path for path in discover_runs(runs_root, workdir, prefix) if path.resolve() not in before]
            candidates.sort(key=lambda path: path.stat().st_mtime, reverse=True)
            partial_run = candidates[0].resolve() if candidates else None
            result = {
                "status": "INCONCLUSIVE",
                "reason": "runtime_acceptance_timeout",
                "version": version,
                "run_dir": str(partial_run) if partial_run else None,
                "stdout": (exc.stdout or "") if isinstance(exc.stdout, str) else "",
                "stderr": (exc.stderr or "") if isinstance(exc.stderr, str) else "",
            }
        except OSError as exc:
            result = {"status": "INCONCLUSIVE", "reason": "launch_error", "version": version, "message": str(exc)}

    payload = json.dumps(result, ensure_ascii=False, indent=2) + "\n"
    if args.output:
        output = Path(args.output).resolve()
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(payload, encoding="utf-8")
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    print(payload, end="")
    return 0 if result.get("status") == "PASS" else 2 if result.get("status") == "INCONCLUSIVE" else 1


if __name__ == "__main__":
    raise SystemExit(main())
