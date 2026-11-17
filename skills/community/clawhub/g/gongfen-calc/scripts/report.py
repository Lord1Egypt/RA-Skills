"""report —— Markdown 报告、失败回显三件套、红线声明。

固定句必须按模板输出，不允许自由措辞（校准会需要逐句对质）。
去交互化原则：分支 B/C/D 只加固定提示句，**不停流程、不弹询问**，报告照常出全。
"""
from __future__ import annotations

import params as P

RED_LINE = ("本报告输出的是**任务分**，不是个人绩效评级；**未对任何个人给出应得分数或绩效等级建议**，"
            "不产出任何淘汰/扣罚名单。")

FIXED_NO_MODEL = ("本报告由脚本端到端生成：解析 → 识别 → 质检 → 打分 → 出报告，**全流程无模型判断、"
                  "无人工确认环节**。低置信列按规则自动裁定并列入「未映射/仲裁」清单，不中断流程；"
                  "只有阻断性失败（读不到表头、无任务名列）才会停下。")

# 层位说明固定句（主理人裁定：层是数据质量层，不是价值层）
LAYER_NOTE = ("层位（L1/L2）差异主要来自字段填写完整度，**不代表任务价值差异**；"
              "L1 与 L2 均计入总分。")


def _fmt(v, nd=P.ROUND_DIGITS):
    if v is None:
        return "—"
    if isinstance(v, float):
        return f"{v:.{nd}f}"
    return str(v)


def _pct(v, nd=0):
    if v is None:
        return "—"
    return f"{v * 100:.{nd}f}%"


# ============================================================ 首屏风险提示
def build_insurance(payload) -> list:
    """风险提示句（进 JSON 的 insurance_note，同时用于报告首屏）。"""
    notes = [RED_LINE, FIXED_NO_MODEL]
    ba = payload.get("batch_assessment") or {}
    branch = ba.get("branch", "")
    enabled = ba.get("enabled_dims", [])
    norm = ba.get("weight_normalized", {})
    tot = payload.get("totals") or {}

    if "difficulty" in enabled:
        qual = payload.get("difficulty_qualitative")
        if qual:
            notes.append(f"难度为**估算值**（关键词规则推断，占归一权重 "
                         f"{norm.get('difficulty', 0) * 100:.0f}%），非客观测量；"
                         f"命中依据逐条列在任务明细，**建议人工复核**。")
        else:
            notes.append(f"难度来自表内等级列（客观输入，占归一权重 "
                         f"{norm.get('difficulty', 0) * 100:.0f}%），可靠度取决于该列填写规范。")
    if "reuse" in enabled:
        notes.append(f"复用价值来自交付物类型关键词（三档 5/3/1，占归一权重 "
                     f"{norm.get('reuse', 0) * 100:.0f}%），亦为估算值。")

    if branch == "C_DESCRIPTIVE":
        notes.append(f"启用维度权重合计 {ba.get('weight_total', 0):.0f}%，低于 "
                     f"{P.COVERAGE_RANK:.0f}% 门槛。本批数据**不足以形成可比工分**，"
                     f"本报告仅作描述统计。**已按规则自动降级，不输出工分**。")
    elif branch == "D_DEGENERATE":
        deg = (payload.get("selfcheck") or {}).get("degeneracy") or {}
        n_dim = len(ba.get("weight_normalized") or {})
        if n_dim <= 2:
            notes.append(f"有效维度仅 {n_dim} 个，单维 {P.WEIGHT_CAP:.0%} 上限**数学上不可满足**；"
                         f"已强制降级，**不输出工分单价**，只输出层内名次。")
        else:
            notes.append(f"有效自由度 {ba.get('n_eff', 0):.2f} 个；难度排名与工时排名一致性 "
                         f"{_fmt(deg.get('rank_consistency_AB'))}。本批工分**只能用于排序参考，"
                         f"不能作为分配依据**；已强制降级，**不输出工分单价**。")
    elif branch == "B_DEGRADED":
        notes.append(f"可排名，**不建议直接分配**。启用维度权重合计 {ba.get('weight_total', 0):.0f}%。"
                     f"补充数据可提升可用性（见「建议补充列」）。")

    if "quality" not in enabled and norm.get("hours", 0) > P.WEIGHT_CONCENTRATION:
        notes.append(f"本批**无质量结果维度**且工时归一权重 {norm.get('hours', 0) * 100:.0f}%，"
                     f"存在虚报工时激励（无对冲维度）。建议补充验收记录后再用于分配。")

    hp = (payload.get("selfcheck") or {}).get("hours_protection") or {}
    if hp.get("mode") == "no_discount_small_sample":
        notes.append("样本量不足，未启用偏离度打折，极端工时未做衰减处理。")
    if hp.get("conflicts"):
        notes.append(f"{len(hp['conflicts'])} 条任务工时与日期推算的可用工时严重不符，"
                     f"已单列标记，**未自动改分**，请人工复核。")
    if not payload.get("date_anchor_available"):
        notes.append("无起止日期，工时无法交叉验证，虚报风险不可控。")

    n_l3 = tot.get("n_l3", 0)
    if n_l3:
        notes.append(f"{n_l3} 条任务完整度 <{P.LAYER_L2:.0f}%，落在 L3（数据不足），"
                     f"**未计入主口径总分**；含 L3 的参考总分为 "
                     f"{_fmt(tot.get('total_score_with_l3'))}，不建议纳入分配。")
    if payload.get("arbitration_log"):
        notes.append(f"{len(payload['arbitration_log'])} 列存在识别歧义，已按规则自动仲裁，"
                     f"明细见「字段识别明细」，未中断流程。")
    return notes


# ============================================================ 主报告
def render(payload) -> str:
    lines = []
    ba = payload.get("batch_assessment") or {}
    q = payload.get("quality") or {}
    tot = payload.get("totals") or {}
    sc = payload.get("selfcheck") or {}
    branch = ba.get("branch", "A_NORMAL")

    # ---------------- 首屏
    lines.append(f"# 工分计算报告（批次 {payload['meta'].get('batch_id', '-')}）\n")
    for note in payload.get("insurance_note", [RED_LINE]):
        lines.append(f"> {note}\n")

    branch_label = {
        "A_NORMAL": "正常（可排名，可作分配**参考**）",
        "B_DEGRADED": "降级（可排名，**不建议直接分配**）",
        "D_DEGENERATE": "体系退化（**仅排序参考**）",
        "C_DESCRIPTIVE": "低置信（**仅描述统计**）",
        "E_FAILED": "分析失败",
    }.get(branch, branch)
    lines.append(f"**批次结论：{branch_label}**　｜　"
                 f"启用维度 {len(ba.get('enabled_dims', []))} 个　｜　"
                 f"权重合计 {_fmt(ba.get('weight_total'))}%　｜　"
                 f"有效自由度 {_fmt(ba.get('n_eff'))}\n")
    # 只有 L1/L2 同时存在时这句话才有信息量；全是同一层时不加噪声
    if tot.get("n_l1") and tot.get("n_l2"):
        lines.append(f"> {LAYER_NOTE}\n")

    # ---------------- 一、数据概况
    lines.append("## 一、数据概况与清洗说明\n")
    lines.append("| 项目 | 数值 | 说明 |")
    lines.append("|---|---|---|")
    lines.append(f"| 文件 | {payload['meta'].get('file')} | "
                 f"{payload['meta'].get('file_format')} / sheet={payload['meta'].get('sheet')} |")
    lines.append(f"| 原始行数 | {q.get('n_raw_rows')} | 表头定位：第 "
                 f"{payload['header'].get('row_index', 0) + 1} 行"
                 f"（置信度 {_fmt(payload['header'].get('confidence'))}） |")
    lines.append(f"| 有效任务数 | {q.get('n_data_rows')} | 合并同组行已聚合 |")
    lines.append(f"| 剔除行数 | {q.get('n_excluded')} | 合计/小计/备注/空行/重复表头 |")
    lines.append(f"| 金额有效覆盖 | {_pct(q.get('money_valid_rate'), 1)} | 按「非空且非 0」计 |")
    lines.append(f"| 系数冻结 | 1人天={P.HOURS_PER_MANDAY}h，自然日×{P.WORKDAY_FACTOR}，"
                 f"超P90保留{P.HOURS_DEVIATION_FACTOR} | 写入 baseline，跨批次不一致即禁做环比 |")
    ur = (payload.get("unit_resolution") or {}).get("hours") or {}
    if ur:
        lines.append(f"| 工时单位判定 | ×{_fmt(ur.get('factor'))} | 来源：{ur.get('source')}"
                     f"（置信 {_fmt(ur.get('confidence'))}）；{ur.get('note')} |")
    lines.append("")

    # ---------------- 二、字段识别
    lines.append("## 二、字段识别明细\n")
    lines.append("| 列 | 原列名 | 映射到 | 置信度 | 方法 | 需确认 |")
    lines.append("|---|---|---|---|---|---|")
    for c in payload.get("columns", []):
        lines.append(f"| {c['col_idx']} | {c['raw_name'] or '(空)'} | "
                     f"{P.DIM_LABELS.get(c['mapped_to'], c['mapped_to'])} | "
                     f"{_fmt(c['confidence'])} | {c['method']} | "
                     f"{'是' if c.get('requires_confirm') else '否'} |")
    lines.append("")
    if payload.get("unmapped_columns"):
        lines.append("**未映射列**（未参与计算，未中断流程）：" +
                     "、".join(f"{u['raw_name'] or '(空列)'}" for u in payload["unmapped_columns"]) + "\n")
    n_l3 = tot.get("n_l3", 0)
    if n_l3:
        lines.append(f"> **口径提示**：{n_l3} 条任务完整度 <{P.LAYER_L2:.0f}%，落在 L3（数据不足），"
                     f"未计入主口径总分；含 L3 的参考总分为 "
                     f"{_fmt(tot.get('total_score_with_l3'))}（见第九节）。\n")
    if payload.get("arbitration_log"):
        lines.append("**仲裁记录**（脚本自动裁定，未询问）：\n")
        lines.append("| 列 | 候选 | 采纳 | 规则 |")
        lines.append("|---|---|---|---|")
        for a in payload["arbitration_log"]:
            lines.append(f"| {a.get('raw_name')} | {'/'.join(a.get('candidates') or ['—'])} | "
                         f"{a.get('picked') or '不采纳'} | {a.get('rule')} |")
        lines.append("")

    # ---------------- 三、维度分布
    lines.append("## 三、分维度分布\n")
    lines.append("| 维度 | 启用 | 有效覆盖 | 1档 | 2档 | 3档 | 4档 | 5档 | 均值 | 熵 | 提示 |")
    lines.append("|---|---|---|---|---|---|---|---|---|---|---|")
    skew = sc.get("skew") or {}
    for dim, label in P.DIM_LABELS.items():
        if dim in P.NEVER_SCORED:
            continue
        cov = (ba.get("coverage_by_dim") or {}).get(dim, 0)
        s = skew.get(dim)
        if not s:
            lines.append(f"| {label} | 否 | {_pct(cov)} | — | — | — | — | — | — | — |"
                         f"{'不参与小计（红线）' if dim in P.NEVER_SCORED else '未启用/无数据'} |")
            continue
        tips = []
        if s.get("small_sample"):
            tips.append(f"n={s['n']} 样本小，不判偏斜")
        if s.get("flag_loose"):
            tips.append("评分宽松")
        if s.get("flag_harsh"):
            tips.append("评分偏严")
        if s.get("flag_flat"):
            tips.append("分布集中")
        lines.append(f"| {label} | 是 | {_pct(cov)} | "
                     + " | ".join(_fmt(x, 2) for x in s["dist"])
                     + f" | {_fmt(s['mean'])} | {_fmt(s['entropy'])} | {'、'.join(tips) or '—'} |")
    lines.append("")

    # ---------------- 四、任务明细
    ranked = [t for t in payload.get("tasks", []) if t.get("rank_within_layer")]
    ranked.sort(key=lambda x: (x["layer"], x["rank_within_layer"]))
    lines.append("## 四、任务明细（名次仅在完整度同层内可比，L1/L2/L3 之间不可直接比较）\n")
    lines.append("| 层 | 层内名次 | 任务 | 工时(h) | 难度 | 紧迫 | 复用 | 完整度 | 小计S "
                 "| K偏离 | 工分 | 标记 |")
    lines.append("|---|---|---|---|---|---|---|---|---|---|---|---|")
    for t in ranked:
        lines.append(f"| {t['layer']} | {t['rank_within_layer']} | {t['task_name']} | "
                     f"{_fmt(t.get('hours_raw'))} | {_fmt(t.get('difficulty_level'))} | "
                     f"{_fmt(t.get('urgency_level'))} | {_fmt(t.get('reuse_level'))} | "
                     f"{_pct(t['completeness'])} | {_fmt(t['subtotal'])} | "
                     f"{_fmt(t.get('k_deviation'))} | {_fmt(t.get('points'))} | "
                     f"{'、'.join(t.get('flags') or []) or '—'} |")
    lines.append("")
    if not tot.get("points_emitted", True):
        lines.append("> 工分列为「—」：本批已降级（" + str(tot.get("points_suppressed_reason") or "") +
                     "），**不输出工分单价**，只输出层内名次与小计 S。\n")

    # ---------------- 五、工时偏离度打折明细
    disc = payload.get("discounted_tasks") or []
    lines.append("## 五、工时偏离度打折明细（只降工分，不改小计 S、不改分档）\n")
    if disc:
        lines.append("| 任务 | 原始工时 | 本批P90 | h_eff | K偏离 | 小计S | 打折前工分 | 打折后工分 |")
        lines.append("|---|---|---|---|---|---|---|---|")
        for d in disc:
            lines.append(f"| {d['task_name']} | {_fmt(d.get('original_hours'))} | "
                         f"{_fmt(d.get('p90_hours'))} | {_fmt(d.get('effective_hours'))} | "
                         f"{_fmt(d.get('k_deviation'))} | {_fmt(d.get('subtotal'))} | "
                         f"{_fmt(d.get('points_before_discount'))} | "
                         f"{_fmt(d.get('points_after_discount'))} |")
        lines.append("")
        lines.append("**逐条证据**：\n")
        for d in disc:
            lines.append(f"- `{d['task_id']}` {d['task_name']}：{d['evidence']}")
        lines.append("")
        lines.append(f"> 口径：分档用**原始工时**，`K_偏离 = h_eff / h` 只乘在工分上 "
                     f"（`P = S × {P.POINT_MULTIPLIER:.0f} × K_偏离 × K_体量 × K_角色 × K_子任务`）。"
                     f"不存在「削 B 权重 + 回补」这种写法。\n")
    else:
        lines.append("本批无任务触发偏离度打折（或样本量不足未启用）。\n")

    # ---------------- 六、无有效维度冻结
    frozen = payload.get("frozen_tasks") or []
    lines.append("## 六、无有效维度任务（冻结，不计分、不排名、不填 0）\n")
    if frozen:
        lines.append("| 任务 | 完整度 | 有效维度 | 说明 |")
        lines.append("|---|---|---|---|")
        for t in frozen:
            lines.append(f"| {t['task_name']} | {_pct(t['completeness'])} | "
                         f"{'/'.join(t.get('valid_dims') or []) or '无'} | {t.get('note', '—')} |")
        lines.append("")
    else:
        lines.append("本批无任务落到该情形。\n")

    # ---------------- 七、自检
    lines.append("## 七、自检结果\n")
    corr = sc.get("correlation") or {}
    if corr.get("executed"):
        lines.append(f"- A/B 相关性：Spearman ρ={_fmt(corr.get('spearman'))}，"
                     f"Pearson={_fmt(corr.get('pearson'))}，n={corr.get('n')}"
                     f"{'　⚠️ 两维度高度重合' if corr.get('flag') else ''}")
    else:
        lines.append(f"- A/B 相关性：{corr.get('note')}")
    deg = sc.get("degeneracy") or {}
    lines.append(f"- 有效自由度 n_eff={_fmt(deg.get('n_eff'))}；"
                 f"A/B 排名一致性={_fmt(deg.get('rank_consistency_AB'))}"
                 + (f"　⚠️ {deg['verdict']}" if deg.get("verdict") else ""))
    ae = sc.get("a_estimate") or {}
    if ae.get("n"):
        lines.append(f"- A 估算占比：{ae.get('estimated')}/{ae.get('n')}"
                     f"（{_pct(ae.get('ratio'))}）"
                     + ("　⚠️ 超过 50%，建议人工抽检" if ae.get("flag") else ""))
    sd = sc.get("split_detect") or {}
    if sd.get("flags"):
        for f in sd["flags"]:
            lines.append(f"- 疑似拆分提示（批内检测，仅提示不判定）：{f['msg']}")
    else:
        lines.append("- 批内拆分检测：未命中")
    bl = sc.get("baseline_compare") or {}
    lines.append(f"- 环比：{bl.get('note', '—')}")
    hp = sc.get("hours_protection") or {}
    if hp.get("discount"):
        lines.append(f"- 工时偏离度打折：P90={hp['discount']['p90']}h，"
                     f"超 P90 部分保留 {hp['discount']['factor']:.0%}")
    lines.append("")

    # ---------------- 八、异常与剔除
    lines.append("## 八、异常与剔除清单\n")
    qs_warn = q.get("warnings") or []
    if qs_warn:
        lines.append("| 代码 | 级别 | 说明 |")
        lines.append("|---|---|---|")
        for w in qs_warn:
            lines.append(f"| {w['code']} | {w['level']} | {w['msg']} |")
        lines.append("")
    ex = q.get("excluded_rows") or []
    if ex:
        lines.append("**已剔除行**：\n")
        lines.append("| 行号 | 原因 | 原始内容（前5格） |")
        lines.append("|---|---|---|")
        for e in ex[:40]:
            raw = " ｜ ".join(str(x) for x in (e.get("raw") or [])[:5])
            lines.append(f"| {e.get('row_id')} | {e.get('reason')} | {raw} |")
        lines.append("")
    conflicts = hp.get("conflicts") or []
    if conflicts:
        lines.append("**工时与日期矛盾（未自动改分，请人工复核）**：\n")
        lines.append("| 任务 | 声称工时 | 可用工时 | 倍数 |")
        lines.append("|---|---|---|---|")
        for c in conflicts:
            lines.append(f"| {c['task_name']} | {_fmt(c['claimed_hours'])} | "
                         f"{_fmt(c['available_hours'])} | {_fmt(c['ratio'])}× |")
        lines.append("")

    # ---------------- 九、汇总
    lines.append("## 九、汇总\n")
    lines.append(f"- 参与排名任务数：{tot.get('n_scored', 0)}"
                 f"（L1 {tot.get('n_l1', 0)} / L2 {tot.get('n_l2', 0)} / L3 {tot.get('n_l3', 0)}）")
    lines.append(f"- 无有效维度冻结：{tot.get('n_out', 0)} 条"
                 f"　｜　容器父任务（不计分）：{tot.get('n_container', 0)} 条"
                 f"　｜　打折任务：{tot.get('n_discounted', 0)} 条")
    pts = _fmt(tot.get('total_points_L1_L2')) if tot.get("points_emitted", True) else "—（不输出工分）"
    lines.append(f"- **总分（主口径 = L1 + L2）：{_fmt(tot.get('total_score_L1_L2'))}"
                 f"　｜　工分合计：{pts}**")
    ae2 = payload.get("a_estimate") or {}
    if ae2.get("n") and payload.get("difficulty_qualitative"):
        norm = ba.get("weight_normalized", {})
        lines.append(f"  - 其中 A 困难程度 **{_pct(ae2.get('ratio'))} 为关键词推断的估算值**"
                     f"（占归一权重 {norm.get('difficulty', 0) * 100:.0f}%，建议人工复核）；"
                     f"其余维度为表内客观输入。")
    if tot.get("n_l3"):
        lines.append(f"- 参考：含 L3 的参考总分为 {_fmt(tot.get('total_score_with_l3'))}"
                     f"（工分 {_fmt(tot.get('total_points_with_l3'))}）"
                     f"—— L3 数据不足，**不建议纳入分配**")
    lines.append(f"- 分层规则：{tot.get('layer_rule', '—')}")
    lines.append(f"- 完整度口径：{tot.get('completeness_note', '—')}")
    mo = payload.get("manual_override") or {}
    if mo:
        lines.append("")
        lines.append(f"**人工覆写（本流程唯一的人工介入点）**："
                     f"{'本次已使用 ' + '、'.join(mo.get('applied') or []) if mo.get('used') else '本次未使用'}。"
                     f"默认不询问、不中断；需要时按下面命令重跑。")
        lines.append("")
        # 逐行原样缩进 4 空格（代码块），不加 ``` 围栏 —— 避免与有序/无序列表嵌套打架
        for ln in str(mo.get("howto", "")).strip().splitlines():
            lines.append("    " + ln)
    lines.append("")
    lines.append("---")
    lines.append("红线声明：" + RED_LINE)
    return "\n".join(lines)


# ============================================================ 失败回显
def render_failure(payload_or_error) -> str:
    """失败回显三件套：①已识别列名清单 ②缺失必要字段 ③建议补充列。"""
    if isinstance(payload_or_error, dict):
        code = payload_or_error.get("code", "E_UNKNOWN")
        msg = payload_or_error.get("msg", "")
        echo = payload_or_error.get("echo") or {}
    else:
        code = getattr(payload_or_error, "code", "E_UNKNOWN")
        msg = getattr(payload_or_error, "msg", str(payload_or_error))
        echo = getattr(payload_or_error, "echo", {}) or {}

    lines = [f"# 分析失败：[{code}] {msg}\n", f"> {RED_LINE}\n", "## ① 已识别到的列名清单\n"]

    rec = echo.get("recognized_columns")
    if rec:
        lines.append("| 列名 | 识别为 | 置信度 | 方法 |")
        lines.append("|---|---|---|---|")
        for c in rec:
            lines.append(f"| {c.get('raw_name') or '(空)'} | "
                         f"{P.DIM_LABELS.get(c.get('mapped_to'), c.get('mapped_to'))} | "
                         f"{_fmt(c.get('confidence'))} | {c.get('method')} |")
    else:
        all_cols = echo.get("all_column_names") or []
        if all_cols:
            lines.append("未识别出任何字段。读取到的原始列名为：\n")
            for name in all_cols:
                lines.append(f"- `{name or '(空列名)'}`")
        else:
            lines.append("未读到任何列名（可能表头不在前 15 行，或表格为空）。")

    if echo.get("head_rows"):
        lines.append("\n**前 15 行原始内容（供定位表头）**：\n")
        lines.append("| 行 | 内容（前 20 格） |")
        lines.append("|---|---|")
        for i, row in enumerate(echo["head_rows"], 1):
            lines.append(f"| {i} | {' ｜ '.join(str(x) for x in (row or []))} |")

    if echo.get("preview"):
        lines.append("\n**各 Sheet 的列与样例值（供手动映射）**：\n")
        for sh in echo["preview"]:
            lines.append(f"\nSheet `{sh['name']}`（{sh['n_rows']} 行）\n")
            lines.append("| 列号 | 样例值 |")
            lines.append("|---|---|")
            for c in sh.get("columns") or []:
                lines.append(f"| 第{c['col_idx']}列 | {' / '.join(c.get('sample_values') or ['(全空)'])} |")

    if echo.get("candidates"):
        lines.append("\n**候选清单表（分差不足，需指定）**：\n")
        lines.append("| Sheet | 分数 | 别名命中 | 行数 |")
        lines.append("|---|---|---|---|")
        for c in echo["candidates"]:
            lines.append(f"| {c['name']} | {c['score']} | {c.get('alias_hits')} | {c.get('n_rows')} |")

    lines.append("\n## ② 缺失的必要字段\n")
    miss = echo.get("missing_required") or ["任务名称列", "至少 1 个可量化维度（工时/金额/难度等级）"]
    for m in miss:
        lines.append(f"- {m}")

    lines.append("\n## ③ 建议补充的列\n")
    for s in echo.get("suggested_columns") or ["任务名称", "工时", "难度等级"]:
        lines.append(f"- {s}")

    if echo.get("hint"):
        lines.append(f"\n**提示**：{echo['hint']}")
    lines.append("\n**人工覆写**：如果已知某列是什么，可用 `--override 列号=字段名` 强制指定后重跑"
                 "（列号见上方样例值表的「第N列」）：\n")
    lines.append("```\npython run.py 你的文件.xlsx --override 3=hours --override 5=money\n```")
    return "\n".join(lines)
