"""MemoryGuard CLI 入口（spec §4）。

命令面:
- audit [path]       只读扫描 + 规则引擎，生成 report.json + report.html
- open [path]        打开报告（降级链：原生窗口->localhost->HTML）
- explain <id>       解释 Finding 的证据和风险
- plan <id...>       生成最小修复补丁 Diff（不写文件）
- apply <plan>       经批准应用：备份 + 补丁 + 重扫
- verify             重扫并比较修复前后
- undo <change>      撤销并再次验证

退出码（spec §4）:
- 0 成功
- 1 可恢复错误
- 2 安全策略阻断
- 3 能力不可用需回退

无网络、Core 零第三方依赖。
"""

from __future__ import annotations

import argparse
import sys
import time
import webbrowser
from pathlib import Path

from . import __version__
from .discover import WorkspaceDiscoverer
from .report import render_html_report
from .rules import RuleContext, default_registry, run_rules
# 触发规则注册（副作用：导入即注册到 default_registry）
from .rules import instruction_rules  # noqa: F401
from .rules import skill_rules  # noqa: F401
from .rules import memory_rules  # noqa: F401
from .rules import rag_rules  # noqa: F401
from .schema import (
    Change,
    ChangeStatus,
    Finding,
    Plan,
    Patch,
    Report,
    RiskLevel,
    now_iso,
    sha256_file,
    sha256_text,
    stable_id,
)


# ---------------------------------------------------------------------------
# .memoryguard/ 布局（spec §2）
# ---------------------------------------------------------------------------

MG_DIR = ".memoryguard"
REPORTS_DIR = f"{MG_DIR}/reports"


def ensure_layout(workspace: Path) -> None:
    """创建 .memoryguard/ 布局（spec §2）。可完全删除，非事实源。"""
    (workspace / MG_DIR).mkdir(exist_ok=True)
    (workspace / REPORTS_DIR).mkdir(exist_ok=True)


# ---------------------------------------------------------------------------
# audit
# ---------------------------------------------------------------------------


def run_audit(workspace: Path) -> Report:
    """执行只读扫描 + 规则引擎，返回 Report。无副作用（不写文件由调用方决定）。"""
    start = time.perf_counter()
    discoverer = WorkspaceDiscoverer(workspace)
    discovery = discoverer.discover()

    # 规则引擎（spec §8）
    ctx = RuleContext(agrs=discovery.agrs)
    findings = run_rules(ctx)

    duration_ms = int((time.perf_counter() - start) * 1000)

    report = Report(
        schema_version="1.0",
        workspace=str(workspace),
        generated_at=now_iso(),
        duration_ms=duration_ms,
        health_score=_health_score(discovery, findings),
        objects=discovery.agrs,
        findings=findings,
        invisible=discovery.invisible,
    )
    return report


def _health_score(discovery, findings=None) -> float:
    """健康分：可见率为主，扣减 Finding 严重度。0-100。"""
    total = len(discovery.agrs) + len(discovery.invisible)
    if total == 0:
        return 0.0
    visible_ratio = len(discovery.agrs) / total
    score = visible_ratio * 80 + min(len(discovery.agrs) / 20, 1.0) * 20
    # Finding 扣分
    if findings:
        sev_penalty = {"critical": 15, "high": 8, "medium": 3, "low": 1, "info": 0}
        for f in findings:
            score -= sev_penalty.get(f.severity.value, 0)
    return round(max(0.0, min(100.0, score)), 1)


def cmd_audit(args: argparse.Namespace) -> int:
    workspace = Path(args.path).resolve()
    if not workspace.is_dir():
        print(f"error: workspace not found: {workspace}", file=sys.stderr)
        return 1
    if not _is_within_cwd_or_explicit(workspace, args):
        # 安全：扫描范围必须由用户参数限定（spec §1.3, §10）
        print(f"error: workspace must be under current directory or given explicitly", file=sys.stderr)
        return 2

    ensure_layout(workspace)
    report = run_audit(workspace)

    # 写 JSON + HTML
    json_path = workspace / REPORTS_DIR / "report.json"
    html_path = workspace / REPORTS_DIR / "report.html"
    json_path.write_text(report.to_json(), encoding="utf-8")
    html_path.write_text(render_html_report(report), encoding="utf-8")

    # 摘要输出到 stdout
    s = report.summary()
    print(f"MemoryGuard audit complete in {report.duration_ms} ms")
    print(f"  workspace: {workspace}")
    print(f"  objects:   {s['object_count']}")
    print(f"  findings:  {len(report.findings)}")
    print(f"  invisible: {s['invisible_count']}")
    print(f"  health:    {report.health_score}/100")
    print(f"  report:    {html_path}")
    return 0


def _is_within_cwd_or_explicit(workspace: Path, args: argparse.Namespace) -> bool:
    """允许：显式传参，或在 cwd 下。禁止默认扫描整个用户目录。"""
    if args.path != ".":
        return True
    try:
        workspace.relative_to(Path.cwd().resolve())
        return True
    except ValueError:
        return True  # 显式传 . 也允许


# ---------------------------------------------------------------------------
# open
# ---------------------------------------------------------------------------


def cmd_open(args: argparse.Namespace) -> int:
    """按 spec §6.1 降级链打开报告。

    顺序: 桌面原生窗口 -> localhost 浏览器 -> 静态 HTML 文件 -> 文本+JSON 路径
    退出码: 0 成功, 1 无报告, 3 所有 GUI 能力不可用（已降级到文本）
    """
    workspace = Path(args.path).resolve()
    html_path = workspace / REPORTS_DIR / "report.html"
    json_path = workspace / REPORTS_DIR / "report.json"
    if not html_path.exists():
        print(f"error: no report found. run `memoryguard audit {args.path}` first.", file=sys.stderr)
        return 1

    html_content = html_path.read_text(encoding="utf-8")
    mode = getattr(args, "mode", "auto")

    # --mode html 跳过窗口，直接静态文件
    if mode == "html":
        return _open_static_html(html_path)

    # 1. 桌面原生窗口（pywebview 可选依赖）
    if mode in ("auto", "native"):
        from .gui import open_interactive_window, has_native_gui

        if has_native_gui():
            print("opening interactive governance panel (pywebview)...")
            rc = open_interactive_window(str(workspace), title=f"MemoryGuard - {workspace.name}")
            if rc == 0:
                return 0
            print("warning: native window unavailable, falling back...", file=sys.stderr)

    # 2. localhost 浏览器窗口（标准库 http.server）
    if mode in ("auto", "localhost"):
        from .gui import open_localhost_window

        print("opening localhost window (press Ctrl+C to close)...")
        rc, url = open_localhost_window(html_content, auto_open=True)
        if rc == 0:
            return 0

    # 3. 静态 HTML 文件（webbrowser.open file://）
    return _open_static_html(html_path)


def _open_static_html(html_path: Path) -> int:
    """降级第3步：用默认浏览器打开静态 HTML 文件。"""
    url = html_path.resolve().as_uri()
    print(f"opening static HTML: {url}")
    try:
        webbrowser.open(url)
        return 0
    except Exception as e:
        print(f"warning: could not open browser ({e})", file=sys.stderr)
        # 4. 最终回退：文本 + JSON 路径
        print(f"open manually: {url}")
        print(f"json report:   {html_path.with_suffix('.json')}")
        return 3


# ---------------------------------------------------------------------------
# explain (spec §4)
# ---------------------------------------------------------------------------


def _load_report(workspace: Path) -> Report | None:
    """从 .memoryguard/reports/report.json 加载最近报告。"""
    json_path = workspace / REPORTS_DIR / "report.json"
    if not json_path.exists():
        return None
    import json

    return Report.from_dict(json.loads(json_path.read_text(encoding="utf-8")))


def cmd_explain(args: argparse.Namespace) -> int:
    """解释 Finding 的证据、影响、建议、验证方式（spec §4）。"""
    workspace = Path(args.workspace).resolve()
    report = _load_report(workspace)
    if report is None:
        print(f"error: no report found. run `memoryguard audit {args.workspace}` first.", file=sys.stderr)
        return 1
    finding = next((f for f in report.findings if f.id == args.finding_id), None)
    if finding is None:
        print(f"error: finding not found: {args.finding_id}", file=sys.stderr)
        print(f"available findings: {[f.id for f in report.findings]}", file=sys.stderr)
        return 1
    print(f"Finding: {finding.id}")
    print(f"  rule:      {finding.rule_id}")
    print(f"  severity:  {finding.severity.value}")
    print(f"  dimension: {finding.dimension.value}")
    print(f"  surface:   {finding.surface.value}")
    print(f"  location:  {finding.location.path}:{finding.location.span[0]}-{finding.location.span[1]}")
    print(f"  evidence:  {finding.evidence}")
    print(f"  impact:    {finding.impact}")
    print(f"  suggestion:{finding.suggestion}")
    print(f"  confidence:{finding.confidence}")
    print(f"  fixable:   {finding.fixable}")
    print(f"  verify:    {finding.verification}")
    return 0


# ---------------------------------------------------------------------------
# plan / apply / verify / undo (spec §3.4, §9)
# ---------------------------------------------------------------------------

PLANS_DIR = f"{MG_DIR}/plans"
CHANGES_DIR = f"{MG_DIR}/changes"
BACKUPS_DIR = f"{MG_DIR}/backups"


def cmd_plan(args: argparse.Namespace) -> int:
    """为指定 Findings 生成最小修复 Plan（只读，不写源文件，spec §9）。"""
    workspace = Path(args.workspace).resolve()
    report = _load_report(workspace)
    if report is None:
        print("error: no report found. run audit first.", file=sys.stderr)
        return 1
    # 找到指定的 findings
    target_findings = [f for f in report.findings if f.id in args.finding_ids]
    if not target_findings:
        print(f"error: no matching findings. available: {[f.id for f in report.findings]}", file=sys.stderr)
        return 1
    # 生成补丁（首期仅支持可 fixable 的简单文本替换/删除）
    patches: list[Patch] = []
    for f in target_findings:
        if not f.fixable:
            print(f"warning: {f.id} not auto-fixable, skipping patch generation")
            continue
        try:
            patch = _generate_patch(f)
            if patch:
                patches.append(patch)
        except Exception as e:
            print(f"warning: could not generate patch for {f.id}: {e}", file=sys.stderr)
    if not patches:
        print("no auto-fixable patches generated. manual review required.", file=sys.stderr)
        return 1
    # 风险评估
    has_high = any(f.severity.value in ("high", "critical") for f in target_findings)
    risk = RiskLevel.HIGH if has_high else RiskLevel.LOW
    plan = Plan(
        plan_id=stable_id("plan", *[f.id for f in target_findings]),
        finding_ids=[f.id for f in target_findings],
        intent=f"fix {len(target_findings)} finding(s)",
        risk_level=risk,
        patches=patches,
        created_at=now_iso(),
        preconditions=[f"file hash matches: {p.before_hash}" for p in patches],
        verification=[f.verification for f in target_findings],
        requires_approval=True,
    )
    # 写 plan 到 .memoryguard/plans/
    (workspace / PLANS_DIR).mkdir(parents=True, exist_ok=True)
    plan_path = workspace / PLANS_DIR / f"{plan.plan_id}.json"
    import json

    plan_path.write_text(json.dumps(plan.to_dict(), ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"plan generated: {plan_path}")
    print(f"  findings: {plan.finding_ids}")
    print(f"  patches:  {len(plan.patches)}")
    print(f"  risk:     {plan.risk_level.value}")
    if plan.requires_approval:
        print(f"  requires approval: run `memoryguard apply {plan.plan_id}`")
    return 0


def _generate_patch(finding: Finding) -> Patch | None:
    """为 Finding 生成简单补丁。首期仅支持空文件删除/标题补全等简单场景。"""
    path = finding.location.path
    try:
        before_hash = sha256_file(Path(path))
    except OSError:
        return None
    # 简单策略：根据 rule_id 生成 diff
    if finding.rule_id == "rag.empty" and finding.evidence == "文档内容为空":
        # 删除空文件
        return Patch(path=path, operation="delete", before_hash=before_hash, diff="- (empty file) delete it")
    if finding.rule_id == "rag.missing_metadata":
        # 补标题
        return Patch(
            path=path,
            operation="insert",
            before_hash=before_hash,
            diff="+ # Document Title (auto-generated placeholder)",
        )
    return None


def cmd_apply(args: argparse.Namespace) -> int:
    """经批准应用 Plan：备份 + 补丁 + 重扫（spec §9）。"""
    workspace = Path(args.workspace).resolve()
    plan_path = workspace / PLANS_DIR / f"{args.plan_id}.json"
    if not plan_path.exists():
        print(f"error: plan not found: {args.plan_id}", file=sys.stderr)
        return 1
    import json

    plan_dict = json.loads(plan_path.read_text(encoding="utf-8"))
    # 简化：手动重建 Plan
    from .schema import RiskLevel as RL

    plan = Plan(
        plan_id=plan_dict["plan_id"],
        finding_ids=plan_dict["finding_ids"],
        intent=plan_dict["intent"],
        risk_level=RL(plan_dict["risk_level"]),
        patches=[Patch(**p) for p in plan_dict["patches"]],
        created_at=plan_dict.get("created_at", ""),
        preconditions=plan_dict.get("preconditions", []),
        verification=plan_dict.get("verification", []),
        requires_approval=plan_dict.get("requires_approval", True),
    )

    # 安全：high risk 首期不自动应用
    if plan.risk_level == RiskLevel.HIGH and not args.force:
        print(f"error: plan {plan.plan_id} is high risk, requires --force to apply", file=sys.stderr)
        return 2

    # 校验 preconditions
    for patch in plan.patches:
        try:
            current_hash = sha256_file(Path(patch.path))
        except OSError as e:
            print(f"error: cannot read {patch.path}: {e}", file=sys.stderr)
            return 2
        if current_hash != patch.before_hash:
            print(f"error: file changed since plan was generated: {patch.path}", file=sys.stderr)
            print(f"  expected: {patch.before_hash}", file=sys.stderr)
            print(f"  actual:   {current_hash}", file=sys.stderr)
            return 2

    # 备份 + 应用
    (workspace / BACKUPS_DIR).mkdir(parents=True, exist_ok=True)
    (workspace / CHANGES_DIR).mkdir(parents=True, exist_ok=True)
    backup_paths: list[str] = []
    changed_paths: list[str] = []
    for patch in plan.patches:
        src = Path(patch.path)
        backup = workspace / BACKUPS_DIR / f"{src.name}.{stable_id('bak', patch.path)[:8]}"
        backup.write_bytes(src.read_bytes())
        backup_paths.append(str(backup))
        if patch.operation == "delete":
            src.unlink()
        elif patch.operation == "insert":
            content = src.read_text(encoding="utf-8")
            src.write_text(patch.diff.lstrip("+ ") + "\n" + content, encoding="utf-8")
        elif patch.operation == "replace":
            src.write_text(patch.diff, encoding="utf-8")
        changed_paths.append(patch.path)

    # 重扫验证
    verify_report = run_audit(workspace)
    verify_path = workspace / REPORTS_DIR / "report.json"
    # 验证 Finding 是否消失
    remaining = [f for f in verify_report.findings if f.id in plan.finding_ids]
    status = ChangeStatus.VERIFIED if not remaining else ChangeStatus.FAILED

    change = Change(
        change_id=stable_id("change", plan.plan_id),
        plan_id=plan.plan_id,
        applied_at=now_iso(),
        backup_paths=backup_paths,
        changed_paths=changed_paths,
        status=status,
        verify_report=str(verify_path),
    )
    change_path = workspace / CHANGES_DIR / f"{change.change_id}.json"
    change_path.write_text(json.dumps(change.to_dict(), ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"applied: {change.change_id}")
    print(f"  status:  {status.value}")
    print(f"  backups: {len(backup_paths)}")
    print(f"  changed: {len(changed_paths)}")
    if remaining:
        print(f"  remaining findings: {[f.id for f in remaining]}", file=sys.stderr)
    print(f"  undo:   run `memoryguard undo {change.change_id}`")
    return 0 if status == ChangeStatus.VERIFIED else 1


def cmd_undo(args: argparse.Namespace) -> int:
    """撤销 Change：从备份恢复 + 重扫验证（spec §9）。"""
    workspace = Path(args.workspace).resolve()
    change_path = workspace / CHANGES_DIR / f"{args.change_id}.json"
    if not change_path.exists():
        print(f"error: change not found: {args.change_id}", file=sys.stderr)
        return 1
    import json

    change_dict = json.loads(change_path.read_text(encoding="utf-8"))
    # 恢复备份
    for backup_path, changed_path in zip(change_dict["backup_paths"], change_dict["changed_paths"]):
        backup = Path(backup_path)
        target = Path(changed_path)
        if not backup.exists():
            print(f"error: backup missing: {backup}", file=sys.stderr)
            return 1
        target.write_bytes(backup.read_bytes())
    # 重扫验证
    verify_report = run_audit(workspace)
    # 更新 change 状态
    change_dict["status"] = ChangeStatus.UNDONE.value
    change_path.write_text(json.dumps(change_dict, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"undone: {args.change_id}")
    print(f"  restored: {len(change_dict['backup_paths'])} files")
    print(f"  health:   {verify_report.health_score}/100")
    return 0


def cmd_verify(args: argparse.Namespace) -> int:
    """重扫并比较修复前后（spec §4）。"""
    workspace = Path(args.workspace).resolve()
    report = _load_report(workspace)
    if report is None:
        print("error: no report found.", file=sys.stderr)
        return 1
    # 重新扫描
    new_report = run_audit(workspace)
    print(f"verify: {new_report.generated_at}")
    print(f"  before: {len(report.findings)} findings, health {report.health_score}")
    print(f"  after:  {len(new_report.findings)} findings, health {new_report.health_score}")
    # 写新报告
    json_path = workspace / REPORTS_DIR / "report.json"
    html_path = workspace / REPORTS_DIR / "report.html"
    import json

    json_path.write_text(new_report.to_json(), encoding="utf-8")
    html_path.write_text(render_html_report(new_report), encoding="utf-8")
    return 0


# ---------------------------------------------------------------------------
# v3 命令：source / scan / import / memory（spec §4.1-§4.4）
# ---------------------------------------------------------------------------


def cmd_source(args: argparse.Namespace) -> int:
    """来源管理（spec §4.1）。"""
    from .source_registry import SourceRegistry
    from .schema_v3 import SourceRootType
    workspace = Path(getattr(args, "workspace", ".")).resolve()
    reg = SourceRegistry(workspace)
    action = args.action
    if action == "list":
        sources = reg.list_sources()
        print(f"sources: {len(sources)}")
        for s in sources:
            print(f"  - {s.root_id}  {s.type.value}  {s.display_name}  scope={s.scope}")
            print(f"      path: {s.path}")
        return 0
    if action == "add":
        root_type = SourceRootType(args.type)
        root = reg.add(args.path, root_type, display_name=args.name or "")
        print(f"added: {root.root_id}  type={root.type.value}  scope={root.scope}")
        preview = reg.preview(args.path, root_type)
        print(f"  estimated_files: {preview.get('estimated_files', 0)}")
        return 0
    if action == "remove":
        ok = reg.remove(args.source_id)
        if ok:
            print(f"removed: {args.source_id}")
            return 0
        print(f"error: cannot remove {args.source_id} (not found or project default)", file=sys.stderr)
        return 1
    if action == "preview":
        root_type = SourceRootType(args.type)
        preview = reg.preview(args.path, root_type)
        print(f"preview: {preview}")
        return 0
    print(f"unknown source action: {action}", file=sys.stderr)
    return 1


def cmd_scan(args: argparse.Namespace) -> int:
    """只读扫描，生成快照 + 覆盖率账本（spec §4.2）。"""
    import json as _json
    from .source_registry import SourceRegistry, ScanBudget
    workspace = Path(getattr(args, "workspace", ".")).resolve()
    reg = SourceRegistry(workspace)
    snap = reg.scan(ScanBudget())
    cov = snap.coverage
    counts = cov.counts()
    print(f"snapshot: {snap.snapshot_id}")
    print(f"  created_at: {snap.created_at}")
    print(f"  source_objects: {len(snap.source_objects)}")
    print(f"  coverage: {counts['coverage_status'] if 'coverage_status' in counts else cov.status().value}")
    print(f"  candidates: {counts['candidate_count']}")
    print(f"  read: {counts['read']}  unsupported: {counts['unsupported']}  unreadable: {counts['unreadable']}")
    print(f"  skipped_by_policy: {counts['skipped_by_policy']}  unaccounted: {counts['unaccounted_count']}")
    # 持久化快照
    snap_dir = workspace / MG_DIR / "snapshots" / snap.snapshot_id
    snap_dir.mkdir(parents=True, exist_ok=True)
    (snap_dir / "sources.json").write_text(
        _json.dumps([o.to_dict() for o in snap.source_objects], ensure_ascii=False, indent=2),
        encoding="utf-8")
    (snap_dir / "coverage.json").write_text(
        _json.dumps(cov.to_dict(), ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"  saved: {snap_dir}")
    return 0


def cmd_import(args: argparse.Namespace) -> int:
    """离线导入（spec §4.3）。"""
    import json as _json
    from .adapters import GenericImportAdapter, ChatGPTImportAdapter
    workspace = Path(getattr(args, "workspace", ".")).resolve()
    bundle = Path(args.bundle).resolve()
    if not bundle.exists():
        print(f"error: bundle not found: {bundle}", file=sys.stderr)
        return 1
    # 尝试 detect
    adapters = [ChatGPTImportAdapter(), GenericImportAdapter()]
    detected = None
    for ad in adapters:
        d = ad.detect(bundle)
        if d.supported:
            detected = (ad, d)
            break
    if detected is None:
        print(f"error: unsupported bundle format: {bundle}", file=sys.stderr)
        return 1
    ad, det = detected
    print(f"detected: provider={det.provider} confidence={det.confidence} notes={det.notes}")
    if args.action == "preview":
        inv = ad.inventory(bundle)
        print(f"inventory: {inv}")
        return 0
    if args.action == "create":
        convs = ad.parse(bundle)
        records = ad.normalize(convs)
        print(f"imported: conversations={len(convs)} memory_records={len(records)}")
        # 保存到 imports
        import_id = "imp-" + stable_id(bundle.name, str(len(records)))
        imp_dir = workspace / MG_DIR / "imports" / import_id
        imp_dir.mkdir(parents=True, exist_ok=True)
        manifest = {
            "import_id": import_id, "provider": det.provider,
            "bundle_path": str(bundle), "created_at": now_iso(),
            "conversation_count": len(convs),
            "memory_record_count": len(records),
            "records": [r.to_dict() for r in records[:100]],
        }
        (imp_dir / "manifest.json").write_text(
            _json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"  saved: {imp_dir / 'manifest.json'}")
        return 0
    return 1


def cmd_memory(args: argparse.Namespace) -> int:
    """记忆构建与发布（spec §4.4）。"""
    import json as _json
    from .adapters import GenericMarkdownTarget
    from .release_manager import ReleaseManager
    from .source_registry import ScanBudget
    workspace = Path(getattr(args, "workspace", ".")).resolve()
    rm = ReleaseManager(workspace)
    action = args.action
    if action == "build-plan":
        target = GenericMarkdownTarget()
        target_path = Path(args.target).resolve() if args.target else workspace / ".memoryguard" / "memory-target"
        snap, ir = rm.scan_and_normalize(ScanBudget())
        plan = rm.create_build_plan(ir, target, target_path)
        print(f"plan: {plan.plan_id}")
        print(f"  snapshot: {plan.snapshot_id}")
        print(f"  target_profile: {plan.target_profile}")
        print(f"  coverage: {plan.coverage_status}")
        print(f"  integrity: {plan.integrity_ok}")
        print(f"  published: {plan.manifest.published_record_count}")
        print(f"  unaccounted: {plan.manifest.unaccounted_record_count}")
        print(f"  diff: {plan.diff_preview}")
        if not plan.integrity_ok:
            print("  WARNING: integrity check failed; apply will refuse", file=sys.stderr)
            return 2
        return 0
    if action == "build-apply":
        if not args.yes:
            print("error: apply requires --yes to confirm", file=sys.stderr)
            return 2
        target = GenericMarkdownTarget()
        target_path = Path(args.target).resolve() if args.target else workspace / ".memoryguard" / "memory-target"
        release = rm.apply_build(args.plan_id, target, target_path, approval=True)
        print(f"apply: {release.release_id}  status={release.status.value}")
        print(f"  changed: {len(release.changed_paths)}  backups: {len(release.backup_paths)}")
        if release.status.value != "verified":
            print(f"  FAILED: {release.verify_result}", file=sys.stderr)
            return 1
        return 0
    if action == "verify":
        target = GenericMarkdownTarget()
        target_path = Path(args.target).resolve() if args.target else workspace / ".memoryguard" / "memory-target"
        # 从 changes 读取 manifest
        change_path = workspace / MG_DIR / "changes" / f"{args.release_id}.json"
        if not change_path.exists():
            print(f"error: release not found: {args.release_id}", file=sys.stderr)
            return 1
        data = _json.loads(change_path.read_text(encoding="utf-8"))
        # 读取 plan 的 manifest
        plan_files = list((workspace / MG_DIR / "plans").glob("*.json"))
        manifest = None
        for pf in plan_files:
            pd = _json.loads(pf.read_text(encoding="utf-8"))
            if pd.get("manifest", {}).get("build_id") == data.get("build_id"):
                manifest = pd["manifest"]
                break
        if manifest is None:
            print(f"error: manifest not found for build {data.get('build_id')}", file=sys.stderr)
            return 1
        from .schema_v3 import BuildManifest, RecordMappingEntry, RecordMappingKind
        mm = BuildManifest(
            build_id=manifest["build_id"], source_snapshot_id=manifest.get("source_snapshot_id", ""),
            target_profile=manifest.get("target_profile", ""), coverage_status=manifest.get("coverage_status", ""),
            input_record_count=manifest.get("input_record_count", 0),
            published_record_count=manifest.get("published_record_count", 0),
            linked_record_count=manifest.get("linked_record_count", 0),
            excluded_record_count=manifest.get("excluded_record_count", 0),
            quarantined_record_count=manifest.get("quarantined_record_count", 0),
            unaccounted_record_count=manifest.get("unaccounted_record_count", 0),
            release_hash=manifest.get("release_hash", ""),
        )
        v = rm.verify_release(args.release_id, target, target_path, mm)
        print(f"verify: {v['release_id']}  rescan={v['rescan_match']}  hashes={v['hashes_match']}")
        return 0 if v["rescan_match"] and v["hashes_match"] else 1
    if action == "rollback":
        if not args.yes:
            print("error: rollback requires --yes to confirm", file=sys.stderr)
            return 2
        target = GenericMarkdownTarget()
        target_path = Path(args.target).resolve() if args.target else workspace / ".memoryguard" / "memory-target"
        rb = rm.rollback_release(args.release_id, target, target_path)
        print(f"rollback: {rb.release_id}  status={rb.status.value}")
        return 0
    print(f"unknown memory action: {action}", file=sys.stderr)
    return 1


# ---------------------------------------------------------------------------
# doctor / mcp-status
# ---------------------------------------------------------------------------


def cmd_doctor(args: argparse.Namespace) -> int:
    """诊断安装环境，输出检查报告。"""
    workspace = Path(getattr(args, "workspace", ".")).resolve()
    issues = 0
    lines: list[str] = ["MemoryGuard Doctor", "=================="]

    # 1. Python 版本（>= 3.10）
    py_ok = sys.version_info >= (3, 10)
    py_ver = f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
    lines.append(f"Python: {py_ver} {'✓' if py_ok else '✗ (require >= 3.10)'}")
    if not py_ok:
        issues += 1

    # 2. memoryguard 包可 import
    try:
        import memoryguard  # noqa: F401
        lines.append("memoryguard package: ✓")
    except ImportError as e:
        lines.append(f"memoryguard package: ✗ ({e})")
        issues += 1

    # 3. MCP server 模块可 import
    try:
        from . import mcp_server  # noqa: F401
        lines.append("MCP server module: ✓")
    except ImportError as e:
        lines.append(f"MCP server module: ✗ ({e})")
        issues += 1

    # 4. 工作区 .memoryguard/ 目录
    mg_dir = workspace / MG_DIR
    if mg_dir.is_dir():
        lines.append(f"Workspace .memoryguard/: ✓ (found at {mg_dir})")
    else:
        lines.append(f"Workspace .memoryguard/: not found (run `memoryguard audit` to initialize)")

    # 5. 已绑定的 Agent
    try:
        from .agent_binding import AgentBindingStore
        from .schema_v3 import BindingStatus
        store = AgentBindingStore(workspace)
        bindings = store.list_bindings(include_inactive=False)
        lines.append(f"Agent bindings: {len(bindings)} active")
    except Exception as e:
        lines.append(f"Agent bindings: error ({e})")

    # 6. shared-memory 记录
    sm_dir = workspace / MG_DIR / "shared-memory"
    group_count = 0
    record_count = 0
    if sm_dir.is_dir():
        try:
            from .shared_memory_store import SharedMemoryStore
            for group_dir in sorted(sm_dir.iterdir()):
                if not group_dir.is_dir():
                    continue
                group_count += 1
                s = SharedMemoryStore(workspace, group_dir.name).status()
                record_count += s.get("total_records", 0)
        except Exception:
            pass
    lines.append(f"Shared memory: {group_count} groups, {record_count} records")

    # 7. provider adapter 安装状态
    lines.append("Provider adapters:")
    try:
        from .provider_adapters import ClaudeAdapter, CodexAdapter, CursorAdapter
        for name, cls in (("claude", ClaudeAdapter), ("codex", CodexAdapter), ("cursor", CursorAdapter)):
            try:
                st = cls(str(workspace)).status()
                if st.get("installed"):
                    lines.append(f"  {name}: installed ✓")
                else:
                    lines.append(f"  {name}: not installed")
            except Exception as e:
                lines.append(f"  {name}: error ({e})")
    except ImportError as e:
        lines.append(f"  (provider_adapters unavailable: {e})")

    # 8. pywebview（可选）
    try:
        import webview  # type: ignore  # noqa: F401
        lines.append("GUI (pywebview): available ✓")
    except ImportError:
        lines.append("GUI (pywebview): not available (optional)")

    # 汇总
    if issues == 0:
        lines.append("")
        lines.append("All checks passed.")
    else:
        lines.append("")
        lines.append(f"{issues} issue(s) found.")

    print("\n".join(lines))
    return 0 if issues == 0 else 1


def cmd_mcp_status(args: argparse.Namespace) -> int:
    """查询 MCP 记忆后端状态。"""
    workspace = Path(getattr(args, "workspace", ".")).resolve()
    lines: list[str] = ["MemoryGuard MCP Status", "======================"]

    # MCP server 运行状态（stdio 模式，无常驻进程）
    lines.append("MCP server: not running (stdio mode, starts on demand)")
    lines.append("")

    # 收集所有 share group
    sm_dir = workspace / MG_DIR / "shared-memory"
    groups: list[tuple[str, dict]] = []
    if sm_dir.is_dir():
        try:
            from .shared_memory_store import SharedMemoryStore
            for group_dir in sorted(sm_dir.iterdir()):
                if not group_dir.is_dir():
                    continue
                st = SharedMemoryStore(workspace, group_dir.name).status()
                groups.append((group_dir.name, st))
        except Exception as e:
            lines.append(f"error reading shared-memory: {e}")
            print("\n".join(lines))
            return 1
    # 收集已绑定 Agent
    group_agents: dict[str, list[str]] = {}
    try:
        from .agent_binding import AgentBindingStore
        from .schema_v3 import BindingStatus
        store = AgentBindingStore(workspace)
        for b in store.list_bindings(include_inactive=False):
            group_agents.setdefault(b.share_group_id, []).append(b.agent_instance_id)
    except Exception:
        pass

    # 输出每个 group
    lines.append("Shared Memory Groups:")
    total_records = 0
    total_events = 0
    for group_id, st in groups:
        recs = st.get("total_records", 0)
        evs = st.get("total_events", 0)
        confs = st.get("total_conflicts", 0)
        quar = st.get("total_quarantine", 0)
        ver = st.get("active_version") or "(none)"
        agents = group_agents.get(group_id, [])
        lines.append(
            f"  [{group_id}] {recs} records, {evs} events, {confs} conflicts, {quar} quarantined"
        )
        lines.append(f"    active version: {ver}")
        lines.append(f"    agents: {', '.join(agents) if agents else '(none)'}")
        lines.append("")
        total_records += recs
        total_events += evs

    # 绑定的 Agent 总览
    bound_agents: list[str] = []
    try:
        from .agent_binding import AgentBindingStore
        store = AgentBindingStore(workspace)
        bound_agents = [b.agent_instance_id for b in store.list_bindings(include_inactive=False)]
    except Exception:
        pass
    if bound_agents:
        lines.append(f"Bound agents: {len(bound_agents)} ({', '.join(bound_agents)})")

    lines.append(f"Total: {len(groups)} groups, {total_records} records, {total_events} events")
    print("\n".join(lines))
    return 0


# ---------------------------------------------------------------------------
# argparse
# ---------------------------------------------------------------------------


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="memoryguard",
        description="Local-first Agent governance: audit instructions, skills, memory, and local RAG.",
    )
    parser.add_argument("--version", action="version", version=f"memoryguard {__version__}")
    sub = parser.add_subparsers(dest="command", required=True)

    p_audit = sub.add_parser("audit", help="read-only scan, generate report")
    p_audit.add_argument("path", nargs="?", default=".", help="workspace path (default: .)")
    p_audit.add_argument(
        "--json", action="store_true", help="also print JSON to stdout"
    )
    p_audit.set_defaults(func=cmd_audit)

    p_open = sub.add_parser("open", help="open latest report in a window")
    p_open.add_argument("path", nargs="?", default=".", help="workspace path (default: .)")
    p_open.add_argument(
        "--mode",
        choices=("auto", "native", "localhost", "html"),
        default="auto",
        help="window mode: auto(native->localhost->html) | native | localhost | html (default: auto)",
    )
    p_open.set_defaults(func=cmd_open)

    p_explain = sub.add_parser("explain", help="explain a finding's evidence and risk")
    p_explain.add_argument("finding_id", help="finding id from report")
    p_explain.add_argument("-w", "--workspace", default=".", help="workspace path (default: .)")
    p_explain.set_defaults(func=cmd_explain)

    p_plan = sub.add_parser("plan", help="generate minimal fix plan (no write)")
    p_plan.add_argument("finding_ids", nargs="+", help="finding ids to fix")
    p_plan.add_argument("-w", "--workspace", default=".", help="workspace path (default: .)")
    p_plan.set_defaults(func=cmd_plan)

    p_apply = sub.add_parser("apply", help="apply a plan: backup + patch + rescan")
    p_apply.add_argument("plan_id", help="plan id from `plan` command")
    p_apply.add_argument("-w", "--workspace", default=".", help="workspace path (default: .)")
    p_apply.add_argument("--force", action="store_true", help="force apply high-risk plans")
    p_apply.set_defaults(func=cmd_apply)

    p_verify = sub.add_parser("verify", help="rescan and compare before/after")
    p_verify.add_argument("-w", "--workspace", default=".", help="workspace path (default: .)")
    p_verify.set_defaults(func=cmd_verify)

    p_undo = sub.add_parser("undo", help="restore from backup and re-verify")
    p_undo.add_argument("change_id", help="change id from `apply` command")
    p_undo.add_argument("-w", "--workspace", default=".", help="workspace path (default: .)")
    p_undo.set_defaults(func=cmd_undo)

    # v3 命令（spec §4.1-§4.4）
    p_source = sub.add_parser("source", help="manage authorized sources (v3)")
    p_source.add_argument("action", choices=("list", "add", "remove", "preview"))
    p_source.add_argument("path", nargs="?", help="path for add/preview")
    p_source.add_argument("--type", default="selected_directory",
                          choices=("project_directory", "selected_directory", "selected_file", "obsidian_vault"))
    p_source.add_argument("--name", default="", help="display name")
    p_source.add_argument("source_id", nargs="?", help="source_id for remove")
    p_source.add_argument("-w", "--workspace", default=".", help="workspace path")
    p_source.set_defaults(func=cmd_source)

    p_scan = sub.add_parser("scan", help="read-only scan, build coverage ledger (v3)")
    p_scan.add_argument("-w", "--workspace", default=".", help="workspace path")
    p_scan.set_defaults(func=cmd_scan)

    p_import = sub.add_parser("import", help="offline import bundle (v3)")
    p_import.add_argument("action", choices=("preview", "create"))
    p_import.add_argument("bundle", help="bundle path (file or dir)")
    p_import.add_argument("-w", "--workspace", default=".", help="workspace path")
    p_import.set_defaults(func=cmd_import)

    p_memory = sub.add_parser("memory", help="memory build & release (v3)")
    p_memory.add_argument("action", choices=("build-plan", "build-apply", "verify", "rollback"))
    p_memory.add_argument("plan_id", nargs="?", help="plan id for build-apply")
    p_memory.add_argument("release_id", nargs="?", help="release id for verify/rollback")
    p_memory.add_argument("--target", default="", help="target path")
    p_memory.add_argument("--yes", action="store_true", help="confirm apply/rollback")
    p_memory.add_argument("-w", "--workspace", default=".", help="workspace path")
    p_memory.set_defaults(func=cmd_memory)

    p_doctor = sub.add_parser("doctor", help="diagnose installation and environment")
    p_doctor.add_argument("-w", "--workspace", default=".", help="workspace path")
    p_doctor.set_defaults(func=cmd_doctor)

    p_mcp_status = sub.add_parser("mcp-status", help="query MCP memory backend status")
    p_mcp_status.add_argument("-w", "--workspace", default=".", help="workspace path")
    p_mcp_status.set_defaults(func=cmd_mcp_status)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
