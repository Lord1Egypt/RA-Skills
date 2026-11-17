"""excel_out —— 把打分结果写成带格式的 Excel 表（交付主产物）。

只读 payload（run.pipeline 的输出），不接触原始 Excel、不改任何分数。
输出 4 个 sheet：
    ① 工分明细    —— 逐任务：档位 / 小计 / 分层 / 排名 / 工分 / 依据
    ② 批次汇总    —— 总分、总工分、分支结论、维度权重与覆盖度、口径冻结
    ③ 质检与自检  —— warnings、自检提示、被剔除行、冻结/容器任务
    ④ 字段识别    —— 列映射明细 + 未映射列

红线：工分是任务分，不是个人绩效等级；本表不产出任何个人得分/等级/淘汰名单。
"""
from __future__ import annotations

import re
from pathlib import Path

from openpyxl import Workbook
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter

import params as P

# ---------------------------------------------------------------- 样式
FILL_HEAD = PatternFill("solid", fgColor="1F4E79")     # 表头：深蓝底白字
FILL_SECTION = PatternFill("solid", fgColor="D9E1F2")  # 分区标题：浅蓝底
FILL_DIM = PatternFill("solid", fgColor="EDEDED")      # 维度列：浅灰底
FILL_L3 = PatternFill("solid", fgColor="FFF2CC")       # L3/冻结行：浅黄底
FILL_WARN = PatternFill("solid", fgColor="FFC7CE")     # 警示：浅红底
FONT_HEAD = Font(bold=True, color="FFFFFF", size=11)
FONT_SECTION = Font(bold=True, size=11, color="1F4E79")
FONT_BOLD = Font(bold=True)
FONT_NOTE = Font(size=9, color="808080", italic=True)
FONT_WARN = Font(bold=True, color="9C0006")
THIN = Side(style="thin", color="BFBFBF")
BORDER = Border(left=THIN, right=THIN, top=THIN, bottom=THIN)

ILLEGAL = re.compile(r"[\x00-\x08\x0b\x0c\x0e-\x1f]")
MAX_CELL = 2000

# 维度 → 原始值列（None 表示不单列原始值，走「判定依据」列）
ORIGINAL_COLS = {
    "hours": ("工时(h)", lambda v: v.get("parsed")),
    "money": ("金额(元)", lambda v: v.get("parsed")),
    "collab": ("协同人数", lambda v: v.get("parsed")),
    "urgency": ("优先级原值", lambda v: v.get("raw")),
    "risk": ("风险原值", lambda v: v.get("raw")),
    "quality": ("质量原值", lambda v: v.get("raw")),
    "reuse": ("交付物", lambda v: v.get("raw")),
    "difficulty": (None, None),
}

BRANCH_TEXT = {
    "A_NORMAL": "A 正常可分配参考",
    "B_DEGRADED": "B 可排名·不可分配",
    "C_DESCRIPTIVE": "C 仅描述（数据不足，不输出工分）",
    "D_DEGENERATE": "D 退化（维度过少，不输出工分）",
}


def _safe(v):
    """清掉 Excel 非法字符、截断超长文本。"""
    if v is None:
        return None
    if isinstance(v, (int, float)):
        return v
    s = str(v)
    s = ILLEGAL.sub("", s)
    if len(s) > MAX_CELL:
        s = s[:MAX_CELL] + "…"
    return s


def _width_of(v, header_len=0):
    s = "" if v is None else str(v)
    w = sum(2 if ord(ch) > 127 else 1 for ch in s)
    return max(w, header_len)


def _autosize(ws, widths, min_w=6, max_w=52):
    for i, w in enumerate(widths, 1):
        ws.column_dimensions[get_column_letter(i)].width = max(min_w, min(max_w, w + 2))


def _head_row(ws, row, headers):
    for c, h in enumerate(headers, 1):
        cell = ws.cell(row=row, column=c, value=h)
        cell.fill = FILL_HEAD
        cell.font = FONT_HEAD
        cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
        cell.border = BORDER
    ws.row_dimensions[row].height = 30


def _section(ws, row, title, ncols):
    cell = ws.cell(row=row, column=1, value=title)
    cell.font = FONT_SECTION
    cell.fill = FILL_SECTION
    cell.alignment = Alignment(vertical="center")
    for c in range(2, ncols + 1):
        ws.cell(row=row, column=c).fill = FILL_SECTION
    return row + 1


def _kv(ws, row, key, value, bold_value=False, warn=False):
    k = ws.cell(row=row, column=1, value=key)
    k.font = FONT_BOLD
    k.alignment = Alignment(vertical="top")
    v = ws.cell(row=row, column=2, value=_safe(value))
    if bold_value:
        v.font = FONT_BOLD
    if warn:
        v.font = FONT_WARN
        v.fill = FILL_WARN
    v.alignment = Alignment(vertical="top", wrap_text=True)
    return row + 1


# ============================================================ Sheet ① 工分明细
def _sheet_detail(wb, payload):
    ws = wb.create_sheet("工分明细")
    tasks = list(payload.get("tasks") or [])
    assessment = payload.get("batch_assessment") or {}
    enabled = assessment.get("enabled_dims") or []
    norm = assessment.get("weight_normalized") or {}
    totals = payload.get("totals") or {}
    emit = bool(totals.get("points_emitted"))

    # 容器父任务（不在 tasks 里，但必须让用户看见，否则以为漏了任务）
    containers = (payload.get("hierarchy") or {}).get("containers_detail") or []

    dims = [d for d in enabled if d in P.WEIGHTS and P.WEIGHTS[d] > 0] or list(enabled)
    headers = ["原表行号", "任务ID", "任务名称"]
    dim_heads = []
    for d in dims:
        w = norm.get(d, 0.0)
        dim_heads.append(f"{P.DIM_LABELS.get(d, d)} 档位(权重{w:.0%})")
    headers += dim_heads
    orig_heads = [ORIGINAL_COLS.get(d, (None, None))[0] for d in dims]
    headers += [h for h in orig_heads if h]
    headers += ["有效维度数", "完整度(本批)", "完整度(vs满池)", "分层", "层内排名",
                "小计 S", "K偏离", "K合计"]
    headers.append("工分 P" if emit else "工分 P（本批不输出）")
    if not emit:
        headers.append("参考工分（仅供排序对照·不可用于分配）")
    headers += ["判定依据 / 标记"]

    ws.append([])  # 占位，下面从第 2 行开始写，给标题留位置
    title = ws.cell(row=1, column=1, value="工分明细（任务分，非个人绩效等级）")
    title.font = Font(bold=True, size=13)
    note = ws.cell(row=1, column=len(headers) + 1,
                   value=("说明：档位 1–5；小计 S = Σ(档位×权重)/Σ权重；"
                          "工分 P = S × 20 × K系数；分层 L1≥90% / L2 60–90% / L3<60%"))
    note.font = FONT_NOTE
    _head_row(ws, 2, headers)

    rows = [dict(t) for t in tasks]
    for c in containers:
        rows.append({"task_id": c.get("task_id"), "task_name": c.get("task_name"),
                     "container": True, "container_reason": c.get("reason"),
                     "values": {}, "flags": [], "layer": None, "subtotal": None,
                     "points": None, "completeness": None, "valid_dims": [],
                     "rank_within_layer": None, "k_deviation": None, "k_total": None,
                     "row": None})
    rows.sort(key=lambda r: (r.get("block") or 0,
                             r.get("row") if r.get("row") is not None else 99999,
                             r.get("task_id") or ""))

    widths = [_width_of(h, len(h)) for h in headers]
    r = 3
    for rec in rows:
        vals = rec.get("values") or {}
        line = []
        line.append((rec.get("row") + 1) if rec.get("row") is not None else None)
        line.append(rec.get("task_id"))
        line.append(rec.get("task_name"))
        for d in dims:
            line.append((vals.get(d) or {}).get("level"))
        for d in dims:
            name, getter = ORIGINAL_COLS.get(d, (None, None))
            if not name:
                continue
            v = vals.get(d) or {}
            if d == "hours":
                eff = v.get("effective")
                base = v.get("parsed")
                line.append(f"{base:g}（有效 {eff:g}）"
                            if (base is not None and eff is not None
                                and abs(float(eff) - float(base)) > 1e-6) else base)
            else:
                line.append(getter(v) if getter else None)
        line.append(len(rec.get("valid_dims") or []))
        comp = rec.get("completeness")
        line.append(round(comp, 4) if isinstance(comp, (int, float)) else None)
        c100 = rec.get("completeness_vs_100")
        line.append(round(c100, 4) if isinstance(c100, (int, float)) else None)
        if rec.get("container"):
            # 有效维度数/完整度已在上面追加，这里补齐：分层 / 排名 / 小计 / K偏离 / K合计
            line += ["容器父任务", None, None, None, None]
            line.append("不计分（防父子重复计分）")
            if not emit:
                line.append(None)
            line.append(rec.get("container_reason") or "")
        else:
            line.append(rec.get("layer"))
            line.append(rec.get("rank_within_layer"))
            line.append(rec.get("subtotal"))
            line.append(rec.get("k_deviation"))
            line.append(rec.get("k_total"))
            line.append(rec.get("points"))
            if not emit:
                s = rec.get("subtotal")
                kt = rec.get("k_total") or 0.0
                line.append(round(s * P.POINT_MULTIPLIER * kt, P.ROUND_DIGITS)
                            if s is not None else None)
            ev = list(rec.get("difficulty_evidence") or [])
            fl = list(rec.get("flags") or [])
            bits = []
            if ev:
                bits.append("难度：" + "、".join(str(e) for e in ev))
            if rec.get("note"):
                bits.append(str(rec["note"]))
            if fl:
                bits.append("标记：" + "、".join(str(f) for f in fl))
            line.append("；".join(bits))

        if len(line) != len(headers):
            raise ValueError(
                f"明细行列数与表头不一致（{len(line)} vs {len(headers)}）"
                f" @ {rec.get('task_id')} container={rec.get('container')}"
                f" dims={dims} orig={orig_heads} emit={emit}")

        for ci, v in enumerate(line, 1):
            cell = ws.cell(row=r, column=ci, value=_safe(v))
            cell.border = BORDER
            cell.alignment = Alignment(vertical="top", wrap_text=(ci == 3 or ci == len(line)))
            if headers[ci - 1].startswith(("A ", "B ", "C ", "D ", "E ", "G ", "H ", "J ")) \
                    or "档位" in headers[ci - 1]:
                cell.fill = FILL_DIM
                cell.alignment = Alignment(horizontal="center", vertical="top")
            if headers[ci - 1] == "工分 P":
                cell.font = FONT_BOLD
                cell.number_format = "0.00"
            if headers[ci - 1] in ("小计 S", "K偏离", "K合计",
                                   "参考工分（仅供排序对照·不可用于分配）"):
                cell.number_format = "0.00"
            if headers[ci - 1] in ("完整度(本批)", "完整度(vs满池)"):
                cell.number_format = "0.0%"
            if rec.get("container") or rec.get("layer") == "L3" or rec.get("subtotal") is None:
                if headers[ci - 1] not in ("任务名称", "判定依据 / 标记"):
                    cell.fill = FILL_L3
        for ci, v in enumerate(line, 1):
            widths[ci - 1] = max(widths[ci - 1], _width_of(v))
        r += 1

    # 合计行（只合计进入总分的 L1+L2）
    sum_row = r
    ws.cell(row=sum_row, column=1, value="合计").font = FONT_BOLD
    ws.cell(row=sum_row, column=3, value="总分（L1+L2 小计之和）").font = FONT_BOLD
    idx_s = headers.index("小计 S") + 1
    c = ws.cell(row=sum_row, column=idx_s,
                value=round(float(totals.get("total_score") or 0), P.ROUND_DIGITS))
    c.font = FONT_BOLD
    c.number_format = "0.00"
    c.fill = FILL_SECTION
    if emit:
        idx_p = headers.index("工分 P") + 1
        cp = ws.cell(row=sum_row, column=idx_p,
                     value=round(float(totals.get("total_points") or 0), P.ROUND_DIGITS))
        cp.font = FONT_BOLD
        cp.number_format = "0.00"
        cp.fill = FILL_SECTION
    else:
        idx_ref = headers.index("参考工分（仅供排序对照·不可用于分配）") + 1
        cr = ws.cell(row=sum_row, column=idx_ref,
                     value=round(float(totals.get("total_points_with_l3") or 0)
                                 if totals.get("total_points_with_l3") else
                                 sum((x.get("subtotal") or 0) * P.POINT_MULTIPLIER
                                     * (x.get("k_total") or 0) for x in tasks
                                     if x.get("layer") in ("L1", "L2")), P.ROUND_DIGITS))
        cr.font = FONT_WARN
        cr.number_format = "0.00"
        cr.fill = FILL_WARN

    ws.freeze_panes = "D3"
    _autosize(ws, widths)
    ws.auto_filter.ref = f"A2:{get_column_letter(len(headers))}{max(r - 1, 2)}"
    return ws


# ============================================================ Sheet ② 批次汇总
def _sheet_summary(wb, payload):
    ws = wb.create_sheet("批次汇总")
    meta = payload.get("meta") or {}
    totals = payload.get("totals") or {}
    a = payload.get("batch_assessment") or {}
    cf = payload.get("caliber_freeze") or {}
    branch = a.get("branch") or ""

    r = 1
    t = ws.cell(row=r, column=1, value="批次汇总")
    t.font = Font(bold=True, size=13)
    r += 2

    r = _section(ws, r, "一、结论", 6)
    r = _kv(ws, r, "源文件", f"{meta.get('file')}  /  sheet：{meta.get('sheet')}")
    r = _kv(ws, r, "解析日期", meta.get("parsed_at"))
    r = _kv(ws, r, "分支结论", BRANCH_TEXT.get(branch, branch),
            warn=branch in ("C_DESCRIPTIVE", "D_DEGENERATE"))
    r = _kv(ws, r, "覆盖度等级", a.get("coverage_grade"))
    r = _kv(ws, r, "维度覆盖度", f"{(a.get('weight_total') or 0):.0f}%"
            f"（启用 {len(a.get('enabled_dims') or [])} 个维度，"
            f"门槛：可排名 ≥{P.COVERAGE_RANK:.0f}%，可分配 ≥{P.COVERAGE_NORMAL:.0f}%）")
    r = _kv(ws, r, "有效自由度 n_eff", a.get("n_eff"))
    if totals.get("points_suppressed_reason"):
        r = _kv(ws, r, "工分未输出原因", totals["points_suppressed_reason"], warn=True)
    if totals.get("points_forced"):
        r = _kv(ws, r, "强制输出提示",
                "已按 --force-points 强制输出工分：覆盖度/自由度未达分配门槛，"
                "工分仅供相对参考，不建议直接用于价值分配。", warn=True)
    r += 1

    r = _section(ws, r, "二、总量", 6)
    r = _kv(ws, r, "任务总数", totals.get("n_scored"))
    r = _kv(ws, r, "分层分布", f"L1 {totals.get('n_l1')} 条 / L2 {totals.get('n_l2')} 条 / "
                              f"L3 {totals.get('n_l3')} 条；冻结(无有效维度) {totals.get('n_out')} 条；"
                              f"容器父任务 {totals.get('n_container')} 条")
    r = _kv(ws, r, "总分 T（主口径：L1+L2 小计之和）",
            round(float(totals.get("total_score") or 0), 2), bold_value=True)
    r = _kv(ws, r, "总分 T（参考口径：含 L3）",
            round(float(totals.get("total_score_with_l3") or 0), 2))
    if totals.get("points_emitted"):
        r = _kv(ws, r, "总工分（主口径：L1+L2）",
                round(float(totals.get("total_points") or 0), 2), bold_value=True)
        r = _kv(ws, r, "总工分（参考口径：含 L3）",
                round(float(totals.get("total_points_with_l3") or 0), 2))
    else:
        r = _kv(ws, r, "总工分", "本批不输出工分（见「工分未输出原因」）", warn=True)
    r = _kv(ws, r, "被打折任务数", totals.get("n_discounted"))
    r = _kv(ws, r, "完整度分母", totals.get("completeness_note"))
    r += 1

    r = _section(ws, r, "三、维度权重与覆盖度", 6)
    hr = r
    _head_row(ws, hr, ["维度", "是否启用", "基础权重", "归一化权重", "有效覆盖率", "分档方式"])
    r += 1
    banding = (payload.get("selfcheck") or {}).get("banding") or {}
    cov = a.get("coverage_by_dim") or {}
    for d in P.DIM_LABELS:
        if d in P.PERMANENTLY_OFF:
            continue
        on = d in (a.get("enabled_dims") or [])
        mode = (banding.get(d) or {}).get("mode")
        mode_txt = {"relative": "分位数相对档", "absolute": "绝对档",
                    "absolute_degenerate": "绝对档(退化)", "rank_quintile": "等频五分",
                    "cuts": "绝对切点", "direct": "表内直读/规则映射"}.get(mode, mode or "—")
        line = [P.DIM_LABELS[d], "启用" if on else "未启用",
                P.WEIGHTS.get(d, 0.0),
                (a.get("weight_normalized") or {}).get(d) if on else None,
                cov.get(d), mode_txt]
        for ci, v in enumerate(line, 1):
            cell = ws.cell(row=r, column=ci, value=_safe(v))
            cell.border = BORDER
            if ci == 4 or ci == 5:
                cell.number_format = "0.0%"
            if not on:
                cell.font = Font(color="808080")
        r += 1
    r += 1

    r = _section(ws, r, "四、口径冻结", 6)
    r = _kv(ws, r, "1 人天 =", f"{cf.get('hours_per_manday')} 小时")
    r = _kv(ws, r, "工作日系数", cf.get("workday_factor"))
    r = _kv(ws, r, "周/月工时", f"{cf.get('week_hours')}h / {cf.get('month_hours')}h")
    r = _kv(ws, r, "偏离度衰减系数", f"{cf.get('hours_deviation_factor'):.0%}（超 P90 部分）")
    r = _kv(ws, r, "节假日日历", "已接入" if cf.get("holiday_calendar_applied") else "未接入")
    ur = (payload.get("unit_resolution") or {}).get("hours") or {}
    if ur:
        r = _kv(ws, r, "工时单位判定",
                f"{ur.get('factor')}（来源：{ur.get('source')}，置信 {ur.get('confidence')}）")
    r = _kv(ws, r, "工分公式", "P = S × 20 × K偏离 × K体量 × K角色 × K子任务")
    r = _kv(ws, r, "小计公式", "S = Σ(档位 × 权重) / Σ权重（不含任何 K，避免双重打折）")
    r += 1

    r = _section(ws, r, "五、提升建议（补齐下列字段即可提升覆盖度）", 6)
    sug = []
    for w in (payload.get("quality") or {}).get("warnings") or []:
        for s in ((w.get("echo") or {}).get("suggestions") or []):
            if s not in sug:
                sug.append(s)
    if not sug:
        sug = ["当前维度已满足分配门槛，建议按 references/scoring_anchors.md 校准各维度锚点"]
    for s in sug:
        ws.cell(row=r, column=1, value="•")
        c = ws.cell(row=r, column=2, value=_safe(s))
        c.alignment = Alignment(wrap_text=True, vertical="top")
        r += 1

    _autosize(ws, [22, 34, 14, 14, 14, 20])
    return ws


# ============================================================ Sheet ③ 质检与自检
def _sheet_checks(wb, payload):
    ws = wb.create_sheet("质检与自检")
    r = 1
    t = ws.cell(row=r, column=1, value="质检与自检（只提示，不自动改分）")
    t.font = Font(bold=True, size=13)
    r += 2

    r = _section(ws, r, "一、质检提示", 4)
    _head_row(ws, r, ["代码", "级别", "说明"])
    r += 1
    for w in (payload.get("quality") or {}).get("warnings") or []:
        lv = {"info": "提示", "degrade": "降级", "warn": "警告"}.get(w.get("level"), w.get("level"))
        for ci, v in enumerate([w.get("code"), lv, w.get("msg")], 1):
            cell = ws.cell(row=r, column=ci, value=_safe(v))
            cell.border = BORDER
            cell.alignment = Alignment(wrap_text=True, vertical="top")
            if w.get("level") == "degrade":
                cell.fill = FILL_L3
        r += 1
    r += 1

    r = _section(ws, r, "二、批次评级提示", 4)
    for f in (payload.get("batch_assessment") or {}).get("flags") or []:
        ws.cell(row=r, column=1, value=_safe(f.get("code"))).border = BORDER
        c = ws.cell(row=r, column=2, value=_safe(f.get("msg")))
        c.border = BORDER
        c.alignment = Alignment(wrap_text=True, vertical="top")
        r += 1
    r += 1

    r = _section(ws, r, "三、自检结果", 4)
    sc = payload.get("selfcheck") or {}
    ae = sc.get("a_estimate") or {}
    if ae:
        r = _kv(ws, r, "难度估算占比",
                f"{ae.get('ratio', 0):.0%}（{ae.get('estimated')}/{ae.get('n')} 条来自关键词推断）"
                + ("  → 建议人工抽检" if ae.get("flag") else ""))
    hp = sc.get("hours_protection") or {}
    r = _kv(ws, r, "工时偏离度处理", f"模式：{hp.get('mode')}；"
                                   f"冲突 {len(hp.get('conflicts') or [])} 条")
    corr = sc.get("correlation") or {}
    r = _kv(ws, r, "重合性检验", "已执行" if corr.get("executed") else
            f"未执行（{corr.get('note')}）")
    sd = sc.get("split_detect") or {}
    r = _kv(ws, r, "拆分/合并检测", f"模式：{sd.get('mode')}")
    bc = sc.get("baseline_compare") or {}
    r = _kv(ws, r, "环比", bc.get("note") if not bc.get("available") else "已比对")
    am = payload.get("a_method") or {}
    if am:
        r = _kv(ws, r, "难度判定方法",
                f"{am.get('method')}（词表 {am.get('table_size')} 词 / 排除词 "
                f"{am.get('exclude_words')} 个，命中率 {am.get('hit_rate')}）")
    r += 1

    r = _section(ws, r, "四、被打折任务（K偏离 < 1）", 4)
    _head_row(ws, r, ["任务ID", "任务名称", "原始工时", "P90", "有效工时", "K偏离", "折前工分", "折后工分"])
    r += 1
    for d in payload.get("discounted_tasks") or []:
        line = [d.get("task_id"), d.get("task_name"), d.get("original_hours"),
                d.get("p90_hours"), d.get("effective_hours"), d.get("k_deviation"),
                d.get("points_before_discount"), d.get("points_after_discount")]
        for ci, v in enumerate(line, 1):
            cell = ws.cell(row=r, column=ci, value=_safe(v))
            cell.border = BORDER
            if ci >= 3:
                cell.number_format = "0.00"
        r += 1
    if not (payload.get("discounted_tasks") or []):
        ws.cell(row=r, column=1, value="无")
        r += 1
    r += 1

    r = _section(ws, r, "五、被剔除行（合计/小计/备注/空行/重复表头等）", 4)
    _head_row(ws, r, ["行号", "原因", "原始内容"])
    r += 1
    for e in (payload.get("quality") or {}).get("excluded_rows") or []:
        raw = " | ".join(str(x) for x in (e.get("raw") or []))[:200]
        for ci, v in enumerate([e.get("row_id"), e.get("reason"), raw], 1):
            cell = ws.cell(row=r, column=ci, value=_safe(v))
            cell.border = BORDER
            cell.alignment = Alignment(wrap_text=True, vertical="top")
        r += 1
    r += 1

    r = _section(ws, r, "六、冻结任务（无任何有效维度，不填 0、不排名）", 4)
    for f in payload.get("frozen_tasks") or []:
        ws.cell(row=r, column=1, value=_safe(f.get("task_id"))).border = BORDER
        ws.cell(row=r, column=2, value=_safe(f.get("task_name"))).border = BORDER
        ws.cell(row=r, column=3, value=_safe(f.get("note"))).border = BORDER
        r += 1
    if not (payload.get("frozen_tasks") or []):
        ws.cell(row=r, column=1, value="无")
        r += 1
    r += 1

    r = _section(ws, r, "七、红线声明", 4)
    for n in payload.get("insurance_note") or []:
        c = ws.cell(row=r, column=1, value=_safe(re.sub(r"\*\*", "", str(n))))
        c.alignment = Alignment(wrap_text=True, vertical="top")
        ws.merge_cells(start_row=r, start_column=1, end_row=r, end_column=4)
        ws.row_dimensions[r].height = 30
        r += 1

    _autosize(ws, [16, 46, 30, 20, 14, 12, 14, 14])
    return ws


# ============================================================ Sheet ④ 字段识别
def _sheet_fields(wb, payload):
    ws = wb.create_sheet("字段识别")
    r = 1
    t = ws.cell(row=r, column=1, value="字段识别明细（如需人工纠正，用 --override 列号=字段名 重跑）")
    t.font = Font(bold=True, size=13)
    r += 2

    _head_row(ws, r, ["列号", "原始列名", "识别为", "置信度", "识别方式", "样例值"])
    r += 1
    for c in payload.get("columns") or []:
        sample = " | ".join(str(x) for x in (c.get("sample_values") or [])[:3])[:200]
        line = [c.get("col_idx"), c.get("raw_name"), c.get("mapped_to"),
                c.get("confidence"), c.get("method"), sample]
        for ci, v in enumerate(line, 1):
            cell = ws.cell(row=r, column=ci, value=_safe(v))
            cell.border = BORDER
            cell.alignment = Alignment(wrap_text=True, vertical="top")
            if ci == 4 and isinstance(v, (int, float)):
                cell.number_format = "0.00"
        r += 1
    r += 1

    r = _section(ws, r, "未映射列（已跳过空白列）", 6)
    n_blank = 0
    for u in payload.get("unmapped_columns") or []:
        if not str(u.get("raw_name") or "").strip():
            n_blank += 1
            continue
        ws.cell(row=r, column=1, value=_safe(u.get("col_idx"))).border = BORDER
        ws.cell(row=r, column=2, value=_safe(u.get("raw_name"))).border = BORDER
        ws.cell(row=r, column=3, value=_safe(u.get("reason") or "未匹配到已知字段")).border = BORDER
        r += 1
    if n_blank:
        ws.cell(row=r, column=1, value=f"（另有 {n_blank} 个空列已忽略）").font = FONT_NOTE
        r += 1
    r += 1

    r = _section(ws, r, "仲裁日志", 6)
    for a in payload.get("arbitration_log") or []:
        ws.cell(row=r, column=1, value=_safe(a if not isinstance(a, dict) else
                                             a.get("msg") or str(a))).border = BORDER
        ws.merge_cells(start_row=r, start_column=1, end_row=r, end_column=6)
        r += 1

    _autosize(ws, [8, 24, 16, 10, 16, 40])
    return ws


# ============================================================ 入口
def write_xlsx(payload: dict, out_path: Path) -> Path:
    wb = Workbook()
    wb.remove(wb.active)
    _sheet_detail(wb, payload)
    _sheet_summary(wb, payload)
    _sheet_checks(wb, payload)
    _sheet_fields(wb, payload)
    wb.properties.title = "工分计算结果"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    wb.save(str(out_path))
    return out_path
