"""GCAE adapter — bridges NOMOS typed models to the SPL Cognitive Audit Engine.

The vendored GCAE engine (:mod:`second_perspective.audit.cognitive.engine`)
expects a plain ``dict`` decision context with keys like ``decision``,
``assumptions`` (list of str), ``outcome``, ``branches``, ``text``.  This
adapter:

1. Translates a NOMOS :class:`DecisionRequest` / :class:`DecisionResult`
   into the GCAE dict context.
2. Runs the deterministic audit pipeline over the operators NOMOS can
   actually feed (:data:`ADAPTER_BASE_OPERATORS` — the rationale for why that is
   *not* all ten lives with the constant, and it is measured, not assumed).
3. Translates the GCAE output dict back into NOMOS
   :class:`CognitiveAuditReport` / :class:`CognitiveRiskFinding` models.
"""

from __future__ import annotations

from typing import Any

from ...models.enums import IssueSeverity
from ...models.schemas import (
    Assumption,
    CognitiveAuditReport,
    CognitiveRiskFinding,
    DecisionRequest,
    DecisionResult,
    ResponsibilityRef,
)
from ..cognitive import (
    BinaryFactCheckPlugin,
    CausalChainSyncPlugin,
    CognitiveAuditEngine,
    FragilityLatchPlugin,
    GrayFeedbackPlugin,
    ImplicitAssumptionPlugin,
    MetaCausalLedgerPlugin,
    NarrativeStripPlugin,
    OriginAnchorPlugin,
    ResponsibilityAccount,
    StateAnchorPlugin,
    TopologyGraphPlugin,
)


_GCAE_SEVERITY_TO_NOMOS = {
    "HALT": IssueSeverity.ERROR,
    "WARN": IssueSeverity.WARNING,
    "PASS": IssueSeverity.INFO,
    "INFO": IssueSeverity.INFO,
}


# ── 本 adapter 注册的算子：基础集 + 条件集 ───────────────────────────────────
#
# 引擎有十算子，但「注册」不等于「喂得起」。实测（真实 make_request 夹具，
# 不是推断）：把十算子原样接进来时——
#
#     ORI → BLOCKED / ORIGIN_VACUUM（每次）
#     GRF → HIGH_RISK / NO_GRAY_LADDER（每次）
#     STATE → level=AUDIT_HALT, pass=False（每次）
#
# 一个永真的阻断不是信号，是淹没真信号的噪音，还会让「审计通过了」这句话
# 彻底失去意义。但反过来把两个算子永久剔除也不对：企业决策里原点（立项申请 /
# 预算请求 / 风险事件 / 董事会决议）与灰度阶梯（试点→分批→全量）都是真实
# 存在的东西，只是原先在模型里无处声明。
#
# 所以走**条件注册：喂得起才审**。
#     request.origin  已声明 → 注册 ORI
#     request.rollout 已声明 → 注册 GRF
# 不声明就不注册，于是：
#   · 「NOMOS 表达不了原点」不再被误判成「这次决策真的没有原点」；
#   · 一次性决策（批准/否决一笔预算）本就没有灰度阶梯，不会吃假阳性；
#   · 录入表单一旦补上这两个字段，对应算子自动参与，无需再改代码。
# 相同的请求 → 相同的算子集，可复现性不受影响。
ADAPTER_BASE_OPERATORS = [
    NarrativeStripPlugin,        # ⊗ 去语义化
    ImplicitAssumptionPlugin,    # ⊕ 约束挖掘
    FragilityLatchPlugin,        # ⊿ 薄弱点加固
    TopologyGraphPlugin,         # ⊞ 无规则拓扑（含链内时序四进程校验）
    BinaryFactCheckPlugin,       #   二元事实校验（未声明 facts 则 SKIPPED）
    CausalChainSyncPlugin,       # ⚙ 因果链同步
    MetaCausalLedgerPlugin,      #   元因果账本（度量，永不阻断）
    StateAnchorPlugin,           # ⊚ 责任锚定 + 最终裁定
]

# 条件算子：算子名 -> (算子类, 判定「这份请求喂不喂得起」)
ADAPTER_CONDITIONAL_OPERATORS: dict[str, tuple[Any, Any]] = {
    "ORI": (OriginAnchorPlugin, lambda req: req.origin is not None),
    "GRF": (GrayFeedbackPlugin, lambda req: req.rollout is not None),
}

# 版本串进 CognitiveAuditReport.scanner_version，因此它属于对外可见的产物。
# 算子集变了就必须跟着升：否则同一份决策会带一个说不清自己由谁产出的版本号。
ADAPTER_SCANNER_VERSION = "GCAE-1.1.0"


def build_gcae_context(
    request: DecisionRequest,
    result: DecisionResult,
) -> dict[str, Any]:
    """Translate NOMOS typed models into a GCAE decision-context dict.

    The GCAE engine expects::

        {
          "decision":  str,             # the decision being made (P)
          "assumptions": list[str],     # declared premises (A1..An)
          "outcome":   str,             # expected outcome (Q), if known
          "branches":  list[dict],      # per-assumption failure responses
          "text":      str,             # narrative text for NS
        }
    """
    assumptions_list = [a.statement for a in request.assumptions]

    # Build branches (failure responses) from assumption falsification_conditions
    branches: list[dict[str, str]] = []
    for a in request.assumptions:
        if a.falsification_condition:
            branches.append({
                "assumption": a.statement,
                "delta_d": a.falsification_condition,
                "assumption_id": a.id,
            })

    # Narrative text: objective + alternative names/descriptions give GCAE
    # enough material for NS (narrative strip) to scan.
    narrative_parts: list[str] = [request.objective]
    if request.time_horizon:
        narrative_parts.append(f"Time horizon: {request.time_horizon}")
    for alt in request.alternatives:
        desc = f"{alt.id}: {alt.name}"
        if alt.description:
            desc += f" — {alt.description}"
        narrative_parts.append(desc)
    text = "\n".join(narrative_parts)

    # Outcome: leading candidate(s) plus status
    if result.leading_candidate_ids:
        outcome = (
            f"Selected leading candidates: {', '.join(result.leading_candidate_ids)} "
            f"(status: {result.status.value})"
        )
    else:
        outcome = f"Decision status: {result.status.value}"

    ctx = {
        "decision": request.objective,
        "assumptions": assumptions_list,
        "outcome": outcome,
        "branches": branches,
        "text": text,
        "_nomos_request": request,
        "_nomos_result": result,
    }

    # ── ⊙ORI 的输入 ──
    # 键名与 OriginAnchorPlugin 的 ORIGIN_KEYS / GOAL_KEYS / RESOURCE_KEYS 对齐。
    # 只在声明了原点时才写入：未声明时 ctx 与扩展前逐字节一致，
    # 存量调用方的行为因此不受影响（兼容不是靠解释，是靠不写入空字段）。
    if request.origin is not None:
        ctx["origin"] = request.origin.trigger
        # objective 就是 ORI 要的「目标稳态」，直接映射，不新造概念。
        ctx["goal"] = request.objective
        if request.origin.resources:
            ctx["resources"] = {
                r.name: {"budget": r.budget, "used": r.used}
                for r in request.origin.resources
            }

    # ── ⇄GRF 的输入 ──
    # 键名与 GrayFeedbackPlugin 的 LEVEL_KEYS / RATIO_KEYS / FEEDBACK_KEYS 对齐。
    if request.rollout is not None:
        if request.rollout.stages:
            ctx["gray_levels"] = [s.ratio for s in request.rollout.stages]
        if request.rollout.current_ratio is not None:
            ctx["commit_ratio"] = request.rollout.current_ratio
        if request.rollout.feedback:
            ctx["feedback"] = dict(request.rollout.feedback)

    return ctx


def run_gcae_audit(
    request: DecisionRequest,
    result: DecisionResult,
    policy: object | None = None,
    operators: list[Any] | None = None,
) -> tuple[CognitiveAuditReport, dict[str, Any]]:
    """Run the GCAE audit and return (NOMOS report, raw report).

    The operators registered are :data:`ADAPTER_BASE_OPERATORS`, not the full ten —
    see the rationale there.  Pass ``operators`` to override (e.g. once NOMOS
    declares an origin, to bring ORI back in).

    Returns:
        (CognitiveAuditReport, raw_gcae_report_dict)
    """
    # Responsibility anchor: use the declared decision owner if available
    owner: ResponsibilityRef = request.decision_owner
    account = ResponsibilityAccount(
        organization=owner.owner if owner else "UNKNOWN",
        role=owner.role if owner.role else "decision_owner",
        stage="post_decision",
    )

    config = {
        "allowed_stages": ["pre_decision", "in_decision", "post_decision", "review"],
        "disclaimer": (
            "This cognitive audit report is generated by the SPL Cognitive Audit "
            "Engine (NS/IAP/LCH/TPG/BFC/CCS/META/STATE). It is a structural "
            "diagnostic only and does not substitute for human judgment."
        ),
        "custom_fields": {
            "scanner": "GCAE-vendored",
            "decision_id": request.decision_id or "PENDING",
        },
    }

    engine = CognitiveAuditEngine(account=account, config=config)
    if operators is None:
        selected = list(ADAPTER_BASE_OPERATORS)
        for plugin_cls, is_fed in ADAPTER_CONDITIONAL_OPERATORS.values():
            if is_fed(request):
                selected.append(plugin_cls)
    else:
        selected = operators
    for plugin_cls in selected:
        engine.register_plugin(plugin_cls())

    ctx = build_gcae_context(request, result)
    raw_report = engine.audit(ctx, save_log=False)

    findings = _translate_findings(raw_report)
    report = CognitiveAuditReport(
        findings=findings,
        total_findings=len(findings),
        scanner_version=ADAPTER_SCANNER_VERSION,
    )
    return report, raw_report


def _translate_findings(raw_report: dict[str, Any]) -> list[CognitiveRiskFinding]:
    """Translate GCAE plugin outputs into NOMOS CognitiveRiskFinding list."""
    findings: list[CognitiveRiskFinding] = []
    analysis = raw_report.get("analysis", {})
    if not isinstance(analysis, dict):
        return findings

    # ── NS: narrative violations ──
    ns = analysis.get("NS", {})
    if isinstance(ns, dict):
        for v in ns.get("violations", []):
            findings.append(
                CognitiveRiskFinding(
                    code=f"NS_{v.get('rule_id', 'rhetoric')}",
                    severity=_GCAE_SEVERITY_TO_NOMOS.get(v.get("severity", "WARN"), IssueSeverity.WARNING),
                    description=v.get("description", "Narrative rhetoric detected"),
                    affected_elements=["objective"],
                    recommendation="Strip rhetorical/emotional language; state only verifiable premises.",
                )
            )

    # ── IAP: implicit assumption flags ──
    iap = analysis.get("IAP", {})
    if isinstance(iap, dict):
        for flag in iap.get("flags", []):
            findings.append(
                CognitiveRiskFinding(
                    code=f"IAP_{flag.get('flag_type', flag.get('flag_id', 'implicit'))}",
                    severity=_GCAE_SEVERITY_TO_NOMOS.get(flag.get("severity", "WARN"), IssueSeverity.WARNING),
                    description=flag.get("description", "Implicit assumption detected"),
                    affected_elements=_iap_affected_elements(flag),
                    recommendation="Declare the premise explicitly with a falsification condition and owner.",
                )
            )

    # ── LCH: fragility findings ──
    lch = analysis.get("LCH", {})
    if isinstance(lch, dict):
        weakest = lch.get("weakest_variable")
        if isinstance(weakest, dict):
            dd = weakest.get("delta_d", 0)
            if dd >= 0.7:
                sev = IssueSeverity.ERROR
            elif dd >= 0.4:
                sev = IssueSeverity.WARNING
            else:
                sev = IssueSeverity.INFO
            findings.append(
                CognitiveRiskFinding(
                    code="LCH_WEAKEST_VARIABLE",
                    severity=sev,
                    description=(
                        f"Weakest assumption: '{weakest.get('assumption','?')[:80]}' "
                        f"(Delta D = {dd}). {weakest.get('failure_scenario','')}"
                    ),
                    affected_elements=[f"assumptions.{weakest.get('index',0)}"],
                    recommendation="Add branch response / falsification path; confirm evidence quality for this assumption.",
                )
            )
        if not lch.get("has_branch_coverage", True):
            findings.append(
                CognitiveRiskFinding(
                    code="LCH_INCOMPLETE_BRANCHES",
                    severity=IssueSeverity.ERROR,
                    description="Not all assumptions have failure-branch responses; system lacks recovery paths.",
                    affected_elements=["assumptions"],
                    recommendation="Define an explicit failure-response (ΔD) for every critical assumption.",
                )
            )

    # ── CCS: causal chain checks ──
    ccs = analysis.get("CCS", {})
    if isinstance(ccs, dict):
        for check in ccs.get("checks", []):
            findings.append(
                CognitiveRiskFinding(
                    code=f"CCS_{check.get('check','chain')}",
                    severity=_GCAE_SEVERITY_TO_NOMOS.get(check.get("severity", "WARN"), IssueSeverity.WARNING),
                    description=check.get("description", "Causal chain issue detected"),
                    affected_elements=_ccs_affected_elements(check),
                    recommendation=_ccs_recommendation(check),
                )
            )

    # ── ORI: origin anchor ──
    # 当前未被 ADAPTER_OPERATORS 注册（NOMOS 契约无 origin 字段）。映射先写好，
    # 否则哪天把它启用，它会跑出一个 BLOCKED 却在报告里一个 finding 都不留 ——
    # 那正是「静默吞掉阻断」这种最危险的失效。
    ori = analysis.get("ORI", {})
    if isinstance(ori, dict) and ori.get("status") not in (None, "PASS"):
        findings.append(
            CognitiveRiskFinding(
                code=f"ORI_{ori.get('reason', 'NOT_ANCHORED')}",
                severity=(
                    IssueSeverity.ERROR
                    if ori.get("status") == "BLOCKED"
                    else IssueSeverity.WARNING
                ),
                description=(
                    f"Origin anchor unresolved ({ori.get('reason', 'not anchored')}). "
                    "Without a declared origin event a causal chain cannot be ordered."
                ),
                affected_elements=["objective", "decision_owner"],
                recommendation=(
                    "Declare the origin event that triggered this decision, its target "
                    "steady state, and the resource budget available to reach it."
                ),
            )
        )

    # ── TPG: topology validation ──
    # 四个并行进程：一致性 / 约束 / 闭合 / 链内时序。时序是 1.1.0 新增。
    tpg = analysis.get("TPG", {})
    if isinstance(tpg, dict):
        validation = tpg.get("validation", {})
        if isinstance(validation, dict):
            for group in ("consistency", "constraint", "closure", "time_order"):
                part = validation.get(group)
                if not isinstance(part, dict):
                    continue
                for issue in part.get("issues", []):
                    findings.append(
                        CognitiveRiskFinding(
                            code=f"TPG_{issue.get('code', group.upper())}",
                            severity=_GCAE_SEVERITY_TO_NOMOS.get(
                                issue.get("severity", "WARN"), IssueSeverity.WARNING
                            ),
                            description=issue.get("message", "Topology validation issue"),
                            affected_elements=[str(issue.get("where") or group)],
                            recommendation=_tpg_recommendation(str(issue.get("code", ""))),
                        )
                    )

    # ── BFC: binary fact check ──
    # 未声明 facts 时 BFC 是 SKIPPED，不产生 finding —— 缺就是缺，不补默认值。
    bfc = analysis.get("BFC", {})
    if isinstance(bfc, dict):
        for v in bfc.get("verdicts", []) or []:
            verdict_value = v.get("verdict") or v.get("binary") or v.get("value")
            if verdict_value in ("FALSE", "UNVERIFIABLE", "VACUOUS", "CONFLICTED"):
                findings.append(
                    CognitiveRiskFinding(
                        code=f"BFC_{verdict_value}",
                        severity=(
                            IssueSeverity.ERROR
                            if verdict_value in ("FALSE", "CONFLICTED")
                            else IssueSeverity.WARNING
                        ),
                        description=(
                            f"Fact check {verdict_value}: "
                            f"{v.get('statement') or v.get('claim') or v.get('id') or 'claim'}"
                        ),
                        affected_elements=["assumptions"],
                        recommendation=(
                            "Attach a falsifiable source to this claim, or remove it "
                            "from the declared premises."
                        ),
                    )
                )

    # ── GRF: gray feedback ──（当前未注册；写法同上，为的是不留静默空窗）
    grf = analysis.get("GRF", {})
    if isinstance(grf, dict) and grf.get("status") not in (None, "PASS", "SKIPPED"):
        findings.append(
            CognitiveRiskFinding(
                code=f"GRF_{grf.get('reason', 'FEEDBACK_GAP')}",
                severity=(
                    IssueSeverity.ERROR
                    if grf.get("status") == "BLOCKED"
                    else IssueSeverity.WARNING
                ),
                description=(
                    f"Gray-feedback gap ({grf.get('reason', 'unknown')}): the decision "
                    "has no declared rollout ladder or reality-feedback path."
                ),
                affected_elements=["alternatives", "outcome"],
                recommendation=(
                    "Declare a rollout ladder and the reality signal that would "
                    "falsify the chosen option; define the rollback trigger."
                ),
            )
        )

    # ── META: meta-causal ledger ──
    # 恒 INFO：META 是度量算子，结构上不允许它阻断。把度量升格为阻断，等于用
    # 「指标不好看」替换「输入不完整」——那不是更强的审计，是更差的审计。
    meta = analysis.get("META", {})
    if isinstance(meta, dict):
        for base, body in sorted((meta.get("meta_bases") or {}).items()):
            if not isinstance(body, dict) or body.get("status") == "PASS":
                continue
            findings.append(
                CognitiveRiskFinding(
                    code=f"META_{body.get('reason', base)}",
                    severity=IssueSeverity.INFO,
                    description=(
                        f"[{base}] {body.get('reason', 'ledger entry flagged')} — "
                        f"{body.get('doctrine', '')}".strip()
                    ),
                    affected_elements=["decision_structure"],
                    recommendation=(
                        "Review the meta-causal ledger entry; it is a measurement, "
                        "not a blocking defect."
                    ),
                )
            )

    # ── STATE: anchor status ──
    state = analysis.get("STATE", {})
    if isinstance(state, dict):
        resp = state.get("responsibility", {})
        if isinstance(resp, dict) and resp.get("is_vague"):
            findings.append(
                CognitiveRiskFinding(
                    code="STATE_VAGUE_ANCHOR",
                    severity=IssueSeverity.ERROR,
                    description=resp.get("warning", "Responsibility anchor is vague"),
                    affected_elements=["decision_owner"],
                    recommendation="Anchor responsibility to a specific, identifiable decision-maker, not a collective.",
                )
            )
        verdict = state.get("verdict", {})
        if isinstance(verdict, dict) and verdict.get("level") == "AUDIT_HALT":
            # STATE already aggregates all HALT items; do not duplicate as a new finding
            # but ensure at least one ERROR-severity finding exists (it will via the
            # plugin-level findings above).
            pass

    return findings


def _iap_affected_elements(flag: dict[str, Any]) -> list[str]:
    flag_type = flag.get("flag_type", "")
    if flag_type == "self_referential":
        return ["objective", "decision_owner"]
    if flag_type == "privilege_bypass":
        return ["constraints", "decision_owner"]
    if flag_type == "missing_assumptions":
        return ["assumptions"]
    if flag_type == "circular_justification":
        return ["objective"]
    return ["assumptions"]


def _tpg_recommendation(code: str) -> str:
    """Map a topology diagnostic code to a structural remediation hint.

    Keyed on the code family (T1xx identity / T2xx parameter / T3xx closure
    and time order), never on the message text — messages are for humans,
    codes are for behaviour.
    """
    if code.startswith("T30"):
        return (
            "Restore chain ordering: every effect must become the next cause — "
            "no forks between the same two nodes, no inverted time order."
        )
    if code.startswith("T20"):
        return "Bring the offending parameter back inside the declared ⦿ constraint."
    if code.startswith("T10"):
        return "Resolve the duplicated or role-conflicting edge between the same two nodes."
    return (
        "Fix the topology issue so the graph is consistent, constraint-satisfying, "
        "closed, and time-ordered."
    )


def _ccs_affected_elements(check: dict[str, Any]) -> list[str]:
    check_name = check.get("check", "")
    result = check.get("result", "")
    if result == "BLACKHOLE":
        return ["assumptions", "alternatives"]
    if result == "SYSTEM_COLLAPSE":
        return ["assumptions"]
    if result in ("BROKEN", "BROKEN_AT_ROOT"):
        return ["objective"]
    if result == "MISSING_A":
        return ["assumptions"]
    if result == "MISSING_Q":
        return ["alternatives"]
    if result == "UNCOVERED":
        return ["assumptions"]
    if check_name == "inverse":
        return ["assumptions"]
    return []


def _ccs_recommendation(check: dict[str, Any]) -> str:
    result = check.get("result", "")
    if result == "BLACKHOLE":
        return "Declare the missing P/A/Q variables explicitly before re-evaluating."
    if result == "SYSTEM_COLLAPSE":
        return "Add explicit failure-branch responses (ΔD) for every critical assumption."
    if result == "COLLAPSE_RISK":
        return "Insufficient branch coverage; add more recovery paths."
    if result == "BROKEN":
        return "Causal chain P→A→Q is incomplete; declare the missing link."
    if result == "MISSING_A":
        return "Add explicit assumptions between decision and outcome."
    if result == "MISSING_Q":
        return "Declare the expected outcome/result of the decision."
    if result == "UNCOVERED":
        return "Describe a counterfactual scenario (¬P) explicitly."
    return "Review the causal chain structure."