"""业务规则校验：资产=负债+权益 / 小计=Σ明细。

best-effort：不修改原始数值，发现不一致写到 warnings 字段。
仅对 statement_type == "balance_sheet" 应用资产/负债/权益恒等式。

输入：已经过 numeric_normalizer + finance_terms_aligner 标注后的 cells
（每个 data 行至少有 row_label / group / value，多列时按列分别校验）
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Optional

from finance_terms_aligner import (
    classify_row_label, is_grand_total_row, is_subtotal_row,
)


@dataclass
class Warning:
    code: str            # "asset_eq_liab_plus_equity_mismatch" / "subtotal_mismatch"
    severity: str        # "error" | "warning"
    column_idx: int      # 哪一列发现的
    detail: str
    expected: Optional[float] = None
    actual: Optional[float] = None
    rel_diff: Optional[float] = None


@dataclass
class ValidationReport:
    warnings: List[Warning] = field(default_factory=list)
    stats: Dict[str, int] = field(default_factory=dict)

    def add(self, w: Warning) -> None:
        self.warnings.append(w)
        self.stats[w.code] = self.stats.get(w.code, 0) + 1

    def is_clean(self) -> bool:
        return all(w.severity != "error" for w in self.warnings)


# ---------------------------------------------------------------------------
# 内部：把 cells 转成"按行的 label + 按列的数值"视图
# ---------------------------------------------------------------------------

def _by_row_col(cells) -> Dict[int, Dict[int, dict]]:
    """{row: {col: cell_dict}}, cell_dict 至少含 text/value。"""
    out: Dict[int, Dict[int, dict]] = {}
    for c in cells:
        out.setdefault(c["row"], {})[c["col"]] = c
    return out


# ---------------------------------------------------------------------------
# 校验：资产 = 负债 + 权益（每列独立）
# ---------------------------------------------------------------------------

_TOLERANCE_REL = 1e-3   # 千分之一相对误差（财报舍入到百万元/亿元很常见）
_TOLERANCE_ABS = 1.0    # 绝对误差兜底（单位归一为元，1 元内可忽略）


def _close_enough(actual: float, expected: float) -> bool:
    if expected == 0:
        return abs(actual) <= _TOLERANCE_ABS
    return abs(actual - expected) / abs(expected) <= _TOLERANCE_REL


def validate_balance_sheet(rows: List[dict],
                            data_cols: List[int]) -> ValidationReport:
    """资产负债表恒等式校验。

    Args:
        rows: 已展平的数据行，每行 dict 至少含：
              - row_label: str
              - group: "asset"/"liability"/"equity"/None
              - cells: {col_idx: value or None}
        data_cols: 要校验的数值列索引列表
    """
    rep = ValidationReport()

    # 收集每列的总计行（assets/liabilities/equity）
    totals: Dict[str, Dict[int, float]] = {"asset": {}, "liability": {}, "equity": {}}
    for r in rows:
        grp = is_subtotal_row(r.get("row_label", ""))
        if not grp:
            continue
        for col in data_cols:
            v = r["cells"].get(col)
            if v is None:
                continue
            # 同一 group 多个总计行（应不会发生）以最后一个为准
            totals[grp][col] = v

    # 资产 = 负债 + 权益（按列校验）
    for col in data_cols:
        a = totals["asset"].get(col)
        l = totals["liability"].get(col)
        e = totals["equity"].get(col)
        if a is None or l is None or e is None:
            continue
        if not _close_enough(l + e, a):
            rep.add(Warning(
                code="asset_eq_liab_plus_equity_mismatch",
                severity="error",
                column_idx=col,
                expected=a,
                actual=l + e,
                rel_diff=(l + e - a) / a if a else None,
                detail=f"col={col} asset={a:.2f} liab+equity={l + e:.2f} diff={l + e - a:.2f}",
            ))

    rep.stats["asset_totals_found"] = len(totals["asset"])
    rep.stats["liab_totals_found"] = len(totals["liability"])
    rep.stats["equity_totals_found"] = len(totals["equity"])
    return rep


# ---------------------------------------------------------------------------
# 校验：小计 = Σ 同 group 明细（best-effort，仅当能确定 group 范围时）
# ---------------------------------------------------------------------------

def validate_subtotals(rows: List[dict],
                        data_cols: List[int]) -> ValidationReport:
    """对每个 group（asset/liab/equity）：last_subtotal 应 ≈ Σ(明细 rows 该 group 的 value).

    分段规则：
      - **仅** group header（"资产："/"负债："/"股东权益："）切段
      - subtotal 行**不切段**（金融报表常有"归属于本行X合计/X合计"这种 nested subtotal，
        最后一个 subtotal 才是该 group 的 grand total）
      - 段尾的最后一个 subtotal 行作为 expected total，其余 subtotal 跳过不累计
      - 表尾自动收尾
    """
    rep = ValidationReport()

    segments: List[dict] = []
    current_group: Optional[str] = None
    current_data_rows: List[dict] = []
    current_subtotals: List[dict] = []

    def _close_segment():
        if current_group is None:
            return
        segments.append({
            "group": current_group,
            "rows": list(current_data_rows),
            "subtotals": list(current_subtotals),
        })

    for r in rows:
        label = r.get("row_label", "") or ""
        hdr_group = classify_row_label(label)
        if hdr_group:
            _close_segment()
            current_group = hdr_group
            current_data_rows = []
            current_subtotals = []
            continue
        if current_group is None:
            continue
        # 全表总计（"负债和股东权益总计"）：既非 subtotal 也非明细，跳过
        if is_grand_total_row(label):
            continue
        # subtotal 行：记录但不切段、不计入明细累加
        if is_subtotal_row(label):
            current_subtotals.append(r)
            continue
        current_data_rows.append(r)
    _close_segment()

    for seg in segments:
        if not seg["subtotals"]:
            continue
        last_sub = seg["subtotals"][-1]
        for col in data_cols:
            expected = last_sub["cells"].get(col)
            if expected is None:
                continue
            actual = sum(
                rr["cells"].get(col)
                for rr in seg["rows"]
                if rr["cells"].get(col) is not None
            )
            if not _close_enough(actual, expected):
                rep.add(Warning(
                    code="subtotal_mismatch",
                    severity="warning",
                    column_idx=col,
                    expected=expected,
                    actual=actual,
                    rel_diff=(actual - expected) / expected if expected else None,
                    detail=(f"group={seg['group']} col={col} "
                            f"subtotal={expected:.2f} sum={actual:.2f} "
                            f"diff={actual - expected:.2f} "
                            f"(data_rows={len(seg['rows'])}, "
                            f"intermediate_subtotals={len(seg['subtotals']) - 1})"),
                ))

    rep.stats["segments_checked"] = len(segments)
    return rep


def validate(rows: List[dict], data_cols: List[int],
              statement_type: Optional[str]) -> ValidationReport:
    """统一入口：按 statement_type 选择适用校验项。"""
    merged = ValidationReport()
    if statement_type == "balance_sheet":
        r1 = validate_balance_sheet(rows, data_cols)
        r2 = validate_subtotals(rows, data_cols)
        for w in r1.warnings + r2.warnings:
            merged.add(w)
        for k, v in {**r1.stats, **r2.stats}.items():
            merged.stats[k] = v
    return merged
