#!/usr/bin/env python3
"""Create compact, immutable task cards for native host Agent launches."""

from __future__ import annotations

import argparse
import hashlib
import json
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from artifact_contract import native_handoff_identity, native_analysis_identity
from analysis_depth_guard import SELF_CHECK_KEYS
from analysis_work_plan import plan as work_plan, published_cards
from task_input_projection import role_packet, project
from role_analysis_contract import questions, contract


ANALYSIS_AGENTS = (
    "data-analyst",
    "platform-ops",
    "content-live-growth",
    "ad-profit-optimizer",
)


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8-sig"))


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def resolved_file(value: str, label: str) -> Path:
    path = Path(value).resolve()
    if not path.is_file():
        raise SystemExit(f"{label}_missing:{path}")
    return path


def write_card(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("x", encoding="utf-8") as stream:
        stream.write(json.dumps(payload, ensure_ascii=False, indent=2) + "\n")


def analysis_cards(args: argparse.Namespace) -> dict[str, Any]:
    run_dir = Path(args.run_dir).resolve()
    plugin_dir = Path(args.plugin_dir).resolve()
    host = str(getattr(args, "host", None) or "workbuddy")
    if host not in {"workbuddy", "codex"}:
        raise SystemExit("task_card_host_invalid")
    identity_name = "team-bootstrap.json" if host == "workbuddy" else "host-orchestration-plan.json"
    identity_label = "team_bootstrap" if host == "workbuddy" else "host_orchestration_plan"
    identity_path = resolved_file(str(run_dir / identity_name), identity_label)
    baseline_path = resolved_file(args.baseline or str(run_dir / "baseline-pack.json"), "baseline")
    chapter_path = resolved_file(args.chapter_plan or str(run_dir / "chapter-plan.json"), "chapter_plan")
    inventory_path = resolved_file(args.inventory or str(run_dir / "report-inventory.json"), "report_inventory")
    identity = load_json(identity_path)
    run_id = str(identity.get("run_id") or "")
    client_scope = str(identity.get("client_scope") or "")
    team_version = str(identity.get("team_version") or "")
    if not run_id or not client_scope or not team_version:
        raise SystemExit(f"{identity_label}_identity_missing")
    if host == "workbuddy":
        if identity.get("host") != "workbuddy" or identity.get("status") != "team_created":
            raise SystemExit("team_bootstrap_identity_invalid")
    else:
        if (identity.get("host") != "codex" or identity.get("status") != "planned_not_executed"
                or identity.get("bootstrap_mode") != "codex_native_subagents"):
            raise SystemExit("host_orchestration_plan_identity_invalid")
    attempt = args.attempt
    if attempt not in {"a1", "a2"}:
        raise SystemExit("task_card_attempt_invalid")

    # Read and fingerprint each shared source once for the whole dispatch batch.
    packet_paths = {'baseline': baseline_path, 'inventory': inventory_path, 'chapter_plan': chapter_path}
    packet = {}
    for label, path in packet_paths.items():
        before = sha256(path)
        content = load_json(path)
        if sha256(path) != before:
            raise ValueError('task_packet_source_changed')
        if any(content.get(k) != identity.get(k) for k in ('run_id', 'client_scope', 'team_version')):
            raise ValueError('task_packet_identity_mismatch')
        packet[label] = {'path': str(path), 'sha256': before, 'content': content}
    baseline = packet['baseline']['content']
    chapter_plan = packet['chapter_plan']['content']
    roles = list(getattr(args, 'roles', None) or ANALYSIS_AGENTS)
    if len(set(roles)) != len(roles) or set(roles) - set(ANALYSIS_AGENTS):
        raise ValueError('task_card_roles_invalid')
    task_type=getattr(args,'task_type',None) or baseline.get('task_type') or 'store_diagnosis'
    single_point=task_type in ('single_topic','data_quality_audit') and getattr(args,'collaboration_mode',None)=='single_point'
    if attempt == 'a1' and tuple(roles) != ANALYSIS_AGENTS and not single_point:
        raise ValueError('initial_comprehensive_dispatch_requires_all_roles')
    if single_point and not getattr(args,'roles',None):
        raise ValueError('single_point_requires_explicit_roles')
    if attempt == 'a2':
        if not getattr(args, 'roles', None):
            raise ValueError('retry_requires_explicit_failed_roles')
        from host_runtime import Runtime
        runtime = Runtime(run_dir, run_id, client_scope, read_only=True)
        try:
            if runtime.identity()['team_version'] != team_version:
                raise ValueError('retry_version_mismatch')
            current = runtime.status()
            latest = {r['role']: r for r in current['members']}
            for role in roles:
                previous = latest.get(role, {})
                if previous.get('state') not in ('member_failed', 'member_rejected') or previous.get('attempt_id') != 'a1':
                    raise ValueError('retry_without_recorded_terminal_failure:'+role)
                observation = runtime.path(previous['observation_file'])
                if sha256(observation) != previous['observation_sha256']:
                    raise ValueError('retry_terminal_observation_changed:'+role)
        finally:
            runtime.close()

    attempt_dir = run_dir / "task-cards" / "analysis" / attempt
    card_dir = attempt_dir if attempt == 'a1' else attempt_dir / ('batch-' + '--'.join(sorted(roles)))
    raw_dir = run_dir / "raw-handoffs"
    return_dir = run_dir / "agent-returns"
    cards: list[dict[str, str]] = []
    pending_cards = []
    chapters = chapter_plan.get("chapters", [])
    plans = {role: work_plan(role, chapters, packet['inventory']['content']) for role in roles}
    for role in roles:
        if published_cards(attempt_dir, role, attempt):
            raise ValueError('task_card_already_exists:'+role)
    if card_dir.exists():
        raise ValueError('task_card_batch_already_exists')
    for role in roles:
        assigned = [item for item in chapters if isinstance(item, dict) and item.get("owner_agent") == role]
        card_path = card_dir / f"{role}-{attempt}.json"
        raw_path = raw_dir / f"handoff-{role}-{attempt}.json"
        role_return_dir = return_dir / role
        return_path = role_return_dir / f"{attempt}.return.json"
        payload = {
            "schema_version": "2.0",
            "artifact_type": "agent_task_card",
            "contract_name": "omni-ecom.agent-task-card",
            "contract_version": "2.0",
            "created_by_team_version": team_version,
            "issued_at": datetime.now(timezone.utc).isoformat(),
            "immutable_after_launch": True,
            "run_id": run_id,
            "client_scope": client_scope,
            "team_version": team_version,
            "host": host,
            "agent_id": role,
            "attempt_id": attempt,
            "scope": str(baseline.get("scope") or ""),
            "paths": {
                "plugin_dir": str(plugin_dir),
                "run_dir": str(run_dir),
                "host_identity": str(identity_path),
                "baseline": str(baseline_path),
                "chapter_plan": str(chapter_path),
                "report_inventory": str(inventory_path),
                "raw_handoff": str(raw_path),
                "return_dir": str(role_return_dir),
                "return_file": str(return_path),
                "validate_handoff": str(plugin_dir / "skills" / "ecom-diagnosis-core" / "scripts" / "validate_handoff.py"),
                "analysis_depth_guard": str(plugin_dir / "scripts" / "analysis_depth_guard.py"),
            },
            "baseline_sha256": packet['baseline']['sha256'],
            "analysis_work_plan": plans[role],
            "raw_handoff_template": {
                **native_handoff_identity(team_version),
                "run_id": run_id, "client_scope": client_scope, "agent_id": role,
                "agent_version": team_version, "attempt_id": attempt,
                "scope": baseline.get("scope"), "contribution_summary": "",
                "gate_status": "BLOCKED", "status": "data_blocked",
                "facts": [], "judgments": [], "hypotheses": [], "actions": [],
                "risks": [], "missing_data": [], "evidence_ledger": [],
                "analysis_depth": {
                    **native_analysis_identity("depth_declaration", team_version),
                    "baseline_ack": {"baseline_sha256": packet['baseline']['sha256'], "accepted": False, "deviations": []},
                    "depth_ladder": {"reached_level": "L0", "min_required_level": "L2", "level_evidence": {"L1": "", "L2": ""}},
                    "decomposition": [], "minimum_analysis_set": [],
                    "self_check": {key: False for key in SELF_CHECK_KEYS},
                },
            },
            "entry_examples_are_not_evidence": {
                "fact": {"id": "F1", "claim": "<专家实际核查的事实>", "evidence_ids": ["E1"]},
                "evidence": {"id": "E1", "source": "<实际文件和字段>", "period": "<本次期间>", "metric": "<核查项目>", "value": "<实际观察值>", "status": "unverified"},
                "decomposition": {"dimension": "<实际拆解维度>", "segments": [{"name": "<分段一>", "value": "<实际观察值>"}, {"name": "<分段二>", "value": "<实际观察值>"}], "evidence_ids": ["E1"]},
                "minimum_analysis_item": {"question": "<本岗位核查问题>", "status": "unanswerable", "answer": "", "blocker": "<实际缺口>"},
            },
            "assigned_chapters": assigned,
            "required_result": {
                "handoff_contract": "omni-ecom.expert-handoff@2.0",
                "minimum_depth": "L2",
                "attempt_id_must_equal": attempt,
                "return_status": "completed",
                "return_receipt_required_fields": [
                    "run_id",
                    "agent_id",
                    "attempt_id",
                    "return_status",
                    "returned_at",
                    "contribution_summary",
                    "response",
                    "handoff_sha256",
                ],
                "handoff_sha256_definition": "Lowercase 64-character SHA256 of paths.raw_handoff; the field name must be exactly handoff_sha256, not raw_handoff_sha256.",
                "message_recipient": "team-lead",
                "send_message_count": 1,
            },
            "execution_rules": [
                "Read this card and the listed source files; do not ask the lead to restate them.",
                "Use raw_handoff_template as an empty format only. Independently fill facts, evidence, scope/depth checks and contribution_summary; the template and entry examples are not analysis, evidence or a passing result.",
                "Write the raw handoff yourself, then execute finish_command. It validates and writes the return once. Do not hand-write, patch, or overwrite the return file.",
                "If no chapter is assigned or data is missing, return an evidence-bounded gap analysis; never invent facts or numbers.",
                "Do not call WorkBuddy TaskList/TaskUpdate and do not message peer agents.",
                "After one native host message to team-lead, end the task immediately.",
            ],
        }
        payload['read_packet'] = role_packet(packet,role)
        payload['assigned_chapters']=payload['read_packet']['chapter_plan']['content']['chapters']
        mode='mechanism' if client_scope=='runtime-acceptance-no-client-data' else 'business'
        payload['analysis_question_contract']=contract(role,mode)
        payload['task_type']=task_type
        payload['paths']['expert_analysis']=str(raw_dir/(role+'-'+attempt+'.analysis.json'))
        payload['expert_analysis_template']={key:payload['raw_handoff_template'][key]
            for key in ('gate_status','status','contribution_summary','facts','judgments','hypotheses','actions','risks','missing_data','evidence_ledger')}
        payload['expert_analysis_template']['analysis_depth']={key:payload['raw_handoff_template']['analysis_depth'][key]
            for key in ('baseline_ack','depth_ladder','decomposition','minimum_analysis_set','self_check')}
        payload['expert_analysis_template']['analysis_depth']['minimum_analysis_set']=questions(role,mode)
        payload['execution_rules'].extend([
            'read_packet contains exact current input snapshots, not expert conclusions. Read this card once; use its baseline, inventory and chapter plan. Open actual source tables as needed to independently validate your assigned findings.',
            'Follow analysis_work_plan for responsibility, source routing and non-repetitive writing. Complete all owned chapters and the role minimum analysis set. Necessary independent cross-checks remain mandatory; do not treat planned_not_executed content as verified findings.',
            'Do not browse directories, schemas, bootstrap files or program source just to rediscover identity or output format. Necessary business evidence investigation remains allowed.',
            'The finish_command verifies the input snapshots, validates your independently authored raw handoff and analysis depth, then writes the immutable return. On failure fix only your unfrozen raw handoff; do not change the card or return.',
            'When finish_command returns member_return_ready, send your single message to the lead and end immediately. Do not execute validation_commands or return_command afterwards: they are compatibility-only alternatives, not additional steps. Never rerun write_agent_return.py after finish_command has committed the return.',
        ])
        payload['finish_command'] = f'python -B "{plugin_dir / "scripts" / "finish_agent_handoff.py"}" --task-card "{card_path}"'
        if host == "workbuddy":
            payload["paths"]["team_bootstrap"] = payload["paths"].pop("host_identity")
            payload["required_result"]["send_message_recipient"] = payload["required_result"].pop("message_recipient")
        payload["return_command"] = f'python -B "{plugin_dir / "scripts" / "write_agent_return.py"}" --task-card "{card_path}"'
        payload["validation_commands"] = [
            f'python -B "{payload["paths"]["validate_handoff"]}" "{raw_path}"',
            f'python -B "{payload["paths"]["analysis_depth_guard"]}" --handoff {role}="{raw_path}" --baseline "{baseline_path}" --min-level L2 --output "{raw_dir / (role + "-" + attempt + "-depth.json")}"',
        ]
        if client_scope == "runtime-acceptance-no-client-data":
            payload["execution_rules"].extend([
                "Only for this no-client mechanism test: provide 3-6 concise verified facts, a matching evidence ledger, one or two decomposition dimensions, four answered role checks, and the seven actual self-checks. No need to repeat source tables or full chapter specifications. Business reports retain all substantive findings and coverage requirements.",
                "Use the template and finish_command directly; do not read program source or --help to discover field names. Limit reads to this card and sources needed for your assigned checks. The current baseline, inventory and chapter plan are already in read_packet. Write JSON in explicit UTF-8.",
                "This is a mechanism acceptance, not a business analysis: facts may only state directly verifiable file, hash, field, count, and gate observations.",
                "For this no-client test, do not repeat GMV, visitors, buyers, conversion, cost or other economic numbers in facts, even when they are fixed probes. The source-bound test metrics and charts are generated by the fixed lead program. Keep your facts to independently verified file identities/hashes and mechanism state; do not mix economic field names or chapter titles with numeric structural counts in the same fact. Describe missing economic evidence in missing_data without filling it with zero. Source numeric observations may remain in your evidence ledger for independent review, not as unbound report prose.",
                "finish_command now checks these mechanism facts before committing your return. If it reports narrative_number_binding_mismatch, correct only your unfrozen raw handoff to the stated mechanism scope and rerun the same finish_command; never skip the check or write the return manually.",
                "Set judgments, hypotheses, and actions to empty arrays. Do not use causal or advisory language such as 原因, 导致, 归因, 因此, 建议, 优化, 提升, or 应当.",
                "The fixed CSV values are transparent test probes only; never describe them as real client performance or infer business meaning from them.",
                "For this mechanism acceptance, set gate_status to PASS and status to ready_for_review because the required mechanism evidence is present. List absent client business data only in missing_data; it must not change the mechanism gate to BLOCKED.",
            ])
        # The fixed envelope is assembled locally from the task card. The expert
        # authors all substantive answers and checks; none are pre-approved.
        payload['execution_rules']=[
            '先读本卡的共同口径、本岗章节和完整紧凑索引；逐份完成所属资料。必要交叉核查可读取 paths 中的原清单、章节及原表，不静默丢弃资料。',
            '资料、身份和模板已经在本卡：不为重新找格式扫描目录、读脚本/测试源码或 --help；实际原表核查和反证不受此限制。仅当固定命令报错且卡片不足以定位时，读取与错误直接相关的代码。',
            '亲自填写 expert_analysis_template，写入 paths.expert_analysis（UTF-8）；只填写模板的业务字段，不手写身份、版本、legacy_compatibility 或任务 ID。',
            '六个 question_id 必须齐全；逐题填 answered/unanswerable/not_applicable 和真实证据 ID。缺数据写明原因、影响、补数；仅有依据的 BLOCKED 降级可结束核查，不能据此输出利润或预算结论。',
            '固定身份不是专家发现。首次 a1 就须完成正式分析；证据登记一次，其余位置引用 evidence_ids；六题简述结论与限制并引用发现/证据编号，不把同一段原文重复到事实、回答、风险、贡献和聊天。实质发现不设数量上限。',
            '仅执行 finish_command，它装配本人分析、核对资料、格式和深度并写唯一回执。错误只改本人未封存的 analysis 文件；不要改任务卡/回执，不另跑 validation_commands/return_command。',
            '收到 member_return_ready 后：WorkBuddy 原样使用返回的 native_message_parameters 执行一次 SendMessage；Codex 向本平台真实父代理发送返回的 short_message。不要另写长摘要、复制全文或再验证回执；发送一次后结束。禁止给同级专家发消息，成员不调用 TaskList/TaskUpdate。',
        ]
        if mode=='mechanism':
            payload['execution_rules'].extend([
                '本次只核查无客户机制：事实仅登记亲自验证的文件身份、字段、指纹和执行状态；六题使用本卡的机制问题，不写客户经营结论。',
                '结构条数、列数、行数可保留在 evidence_ledger；不要在同一条 facts 中混写这些数字和 GMV/买家/成本等经营字段名，以免把结构计数误作经营数字。',
                '无客户机制验收通常保留三至六项独立核查事实即可；用证据编号回答六题，不逐字段抄写身份或源表，不扩写测试框架说明。实际新增风险仍须完整记录。',
                '测试经营数字由固定来源程序生成图表；不要在 facts 重复 GMV、访客、买家、转化、成本等数字。judgments/hypotheses/actions 留空；不存在的客户业务资料只列 missing_data。',
                '机制所需证据齐全才填 PASS/ready_for_review；planned_not_executed 不能说成已执行。finish_command 对 narrative_number_binding_mismatch 仍阻断；不跳过检查，不自行写正式回执。',
            ])
        # Keep compatibility fields for older finish/return callers, but avoid
        # presenting the same chapters twice to every analyst.
        payload.pop('assigned_chapters', None)
        pending_cards.append((card_path.name, payload))
        cards.append({
            "agent_id": role,
            "attempt_id": attempt,
            "card_path": str(card_path),
            "launch_prompt": f"读取并执行任务卡：{card_path}。按岗位说明完成 {attempt}；只向 team-lead 回传一次，然后结束。",
        })
        if host=='workbuddy' and identity.get('team_name'):
            cards[-1]['dispatch_parameters']={'team_name':identity['team_name'],'name':role,
                'subagent_type':role,'prompt':cards[-1]['launch_prompt']}

    manifest_path = card_dir / "launch-manifest.json"
    # Reject source mutation during card creation, before providing any launch prompts.
    if any(sha256(path) != packet[label]['sha256'] for label, path in packet_paths.items()):
        raise ValueError('task_packet_source_changed')
    manifest = {
        "status": "agent_task_cards_ready",
        "run_id": run_id,
        "client_scope": client_scope,
        "team_version": team_version,
        "host": host,
        "attempt_id": attempt,
        "cards": cards,
        "launch_prompt_max_chars": max(len(item["launch_prompt"]) for item in cards),
    }
    # Publish one complete immutable directory; failed preparation leaves no official cards.
    card_dir.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='.pending-cards-', dir=card_dir.parent) as folder:
        stage = Path(folder).resolve()
        if not stage.is_relative_to(run_dir):
            raise ValueError('task_card_stage_outside_run')
        for name, payload in pending_cards:
            write_card(stage/name, payload)
        write_card(stage/'launch-manifest.json', manifest)
        if any(sha256(path) != packet[label]['sha256'] for label, path in packet_paths.items()):
            raise ValueError('task_packet_source_changed')
        stage.rename(card_dir)
    return {**manifest, "manifest_path": str(manifest_path)}


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run-dir", required=True)
    parser.add_argument("--plugin-dir", required=True)
    parser.add_argument("--baseline")
    parser.add_argument("--chapter-plan")
    parser.add_argument("--inventory")
    parser.add_argument("--attempt", default="a1")
    parser.add_argument("--roles", nargs='+', choices=ANALYSIS_AGENTS, help="Only recorded failed a1 roles may receive a2 cards")
    parser.add_argument('--task-type')
    parser.add_argument('--collaboration-mode',choices=('comprehensive','single_point'),default='comprehensive')
    parser.add_argument("--host", choices=("workbuddy", "codex"), default="workbuddy")
    parser.add_argument("--kind", choices=("analysis", "review"), default="analysis")
    parser.add_argument("--manifest", help="Frozen manifest for --kind review")
    parser.add_argument("--output")
    parser.add_argument("--pretty", action="store_true")
    return parser


def main() -> int:
    args = build_parser().parse_args()
    if args.kind == 'review':
        if not args.manifest: raise ValueError('review_manifest_required')
        from review_task_card import prepare
        result = prepare(args.manifest,args.plugin_dir,args.host,args.attempt)
    else:
        result = analysis_cards(args)
    text = json.dumps(result, ensure_ascii=False, indent=2 if args.pretty else None)
    if args.output:
        Path(args.output).resolve().write_text(text + "\n", encoding="utf-8")
    print(text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
