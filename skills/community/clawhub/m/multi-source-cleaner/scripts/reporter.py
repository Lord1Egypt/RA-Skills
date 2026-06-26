"""
F6 · Data quality report generation.
Generates structured reports in Markdown (for Feishu Doc) and dict form.

Usage:
    from reporter import DataQualityReporter, Report

    reporter = DataQualityReporter(before_df, after_df, field_info)
    report = reporter.generate()
    markdown = reporter.to_markdown(report)
"""

import math
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from datetime import datetime
import pandas as pd

from field_identifier import FieldType, FieldInfo, FIELD_TYPE_LABELS
from cleaner import CleaningReport as CleaningReport_
from classifier import ClassificationReport as ClassificationReport_

# ─── Report dataclasses ─────────────────────────────────────────────────────────

@dataclass
class ColumnStats:
    col: str
    field_type: str
    total: int
    missing: int
    missing_pct: float
    unique: int
    sample_values: List[str] = field(default_factory=list)

@dataclass
class DataQualityReport:
    generated_at: str
    source_name: str
    tier: str
    before_shape: tuple[int, int]
    after_shape:  tuple[int, int]
    duplicate_rate_before: float
    duplicate_rate_after:  float
    missing_rate_before:   float
    missing_rate_after:    float
    overall_score: float   # 0-100
    column_stats: List[ColumnStats] = field(default_factory=list)
    cleaning_report: Optional[CleaningReport_] = None
    classification_report: Optional[ClassificationReport_] = None
    recommendations: List[str] = field(default_factory=list)


# ─── Reporter ──────────────────────────────────────────────────────────────────

class DataQualityReporter:
    """
    Generate data quality reports before/after cleaning.

    Parameters
    ----------
    before_df  : original DataFrame
    after_df   : cleaned DataFrame
    field_info : Dict[col -> FieldInfo]
    source_name: str identifier for the data source
    tier       : subscription tier string
    cleaning_report   : Optional[CleaningReport]
    classification_report: Optional[ClassificationReport]
    """

    def __init__(
        self,
        before_df: pd.DataFrame,
        after_df:  pd.DataFrame,
        field_info: Dict[str, FieldInfo],
        *,
        source_name: str = "数据源",
        tier: str = "free",
        cleaning_report: Optional[CleaningReport_] = None,
        classification_report: Optional[ClassificationReport_] = None,
    ):
        self.before_df  = before_df.copy()
        self.after_df   = after_df.copy()
        self.field_info = field_info
        self.source_name = source_name
        self.tier       = tier
        self.cleaning_report   = cleaning_report
        self.classification_report = classification_report

    def generate(self) -> DataQualityReport:
        """Build the full quality report."""
        stats = self._compute_stats()
        dup_before = self._dup_rate(self.before_df)
        dup_after  = self._dup_rate(self.after_df)
        miss_before = self._missing_rate(self.before_df)
        miss_after  = self._missing_rate(self.after_df)
        score = self._overall_score(dup_after, miss_after)
        recs  = self._recommendations(stats, dup_after, miss_after)

        return DataQualityReport(
            generated_at=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            source_name=self.source_name,
            tier=self.tier,
            before_shape=(len(self.before_df), len(self.before_df.columns)),
            after_shape =(len(self.after_df),  len(self.after_df.columns)),
            duplicate_rate_before=dup_before,
            duplicate_rate_after=dup_after,
            missing_rate_before=miss_before,
            missing_rate_after=miss_after,
            overall_score=score,
            column_stats=stats,
            cleaning_report=self.cleaning_report,
            classification_report=self.classification_report,
            recommendations=recs,
        )

    # ─── Per-column statistics ─────────────────────────────────────────────────

    def _compute_stats(self) -> List[ColumnStats]:
        stats = []
        for col in self.before_df.columns:
            fi = self.field_info.get(col)
            ft_label = FIELD_TYPE_LABELS.get(fi.field_type, "未知") if fi else "未知"
            total   = len(self.before_df)
            missing = self.before_df[col].astype(str).isin(
                ["", "nan", "NaN", "None", "null", "NULL", "undefined", "未知"]
            ).sum()
            missing_pct = missing / total if total else 0
            unique = self.before_df[col].nunique()

            samples = (
                self.before_df[col]
                .astype(str)
                .loc[lambda x: ~x.isin(["", "nan", "NaN", "None", "null", "未知"])]
                .drop_duplicates()
                .head(5)
                .tolist()
            )

            stats.append(ColumnStats(
                col=str(col),
                field_type=ft_label,
                total=total,
                missing=missing,
                missing_pct=missing_pct,
                unique=unique,
                sample_values=samples,
            ))
        return stats

    # ─── Rate calculations ───────────────────────────────────────────────────────

    def _dup_rate(self, df: pd.DataFrame) -> float:
        if df.empty:
            return 0.0
        return 1.0 - (df.drop_duplicates().shape[0] / len(df))

    def _missing_rate(self, df: pd.DataFrame) -> float:
        if df.empty:
            return 0.0
        total_cells   = df.shape[0] * df.shape[1]
        missing_cells = df.astype(str).isin(
            ["", "nan", "NaN", "None", "null", "NULL", "undefined", "未知"]
        ).sum().sum()
        return missing_cells / total_cells if total_cells else 0.0

    def _overall_score(self, dup_rate: float, miss_rate: float) -> float:
        """Score 0-100, higher = better quality."""
        dup_penalty  = dup_rate  * 40   # up to -40
        miss_penalty = miss_rate * 40   # up to -40
        return round(max(0.0, 100.0 - (dup_rate * 40) - (miss_rate * 40)), 1)

    # ─── Recommendations ────────────────────────────────────────────────────────

    def _recommendations(
        self,
        stats: List[ColumnStats],
        dup_rate: float,
        miss_rate: float,
    ) -> List[str]:
        recs: List[str] = []

        if dup_rate > 0.1:
            recs.append(
                f"⚠️ 重复率较高（{dup_rate:.1%}），建议检查是否存在系统重复导入。"
            )
        if miss_rate > 0.05:
            recs.append(
                f"⚠️ 缺失率偏高（{miss_rate:.1%}），建议补充缺失数据以提高分析准确性。"
            )

        for s in stats:
            if s.missing_pct > 0.3:
                recs.append(
                    f"⚠️ 列「{s.col}」缺失率达 {s.missing_pct:.0%}，"
                    f"建议确认该字段是否必填或启用智能补全功能。"
                )
            if s.unique == 1 and s.total > 10:
                recs.append(
                    f"ℹ️ 列「{s.col}」所有值相同（{s.unique} 个唯一值），"
                    f"可能为无效特征，建议移除。"
                )

        if not recs:
            recs.append("✅ 数据质量良好，未发现明显问题。")

        return recs

    # ─── Markdown output ────────────────────────────────────────────────────────

    def to_markdown(self, report: DataQualityReport) -> str:
        """Render report as Feishu-compatible Markdown."""
        lines: List[str] = []

        lines.append(f"# 📊 数据质量报告")
        lines.append(f"")
        lines.append(f"**数据源：** {report.source_name}")
        lines.append(f"**版本：** {report.tier}")
        lines.append(f"**生成时间：** {report.generated_at}")
        lines.append("")

        # Score card
        score_emoji = (
            "🟢" if report.overall_score >= 80
            else "🟡" if report.overall_score >= 60
            else "🔴"
        )
        lines.append(f"## {score_emoji} 综合质量评分：{report.overall_score}/100")
        lines.append("")

        # Shape summary
        lines.append("## 📐 数据规模")
        lines.append("")
        lines.append("| 阶段 | 行数 | 列数 |")
        lines.append("|------|------|------|")
        lines.append(
            f"| 清洗前 | {report.before_shape[0]:,} | {report.before_shape[1]:,} |"
        )
        lines.append(
            f"| 清洗后 | {report.after_shape[0]:,} | {report.after_shape[1]:,} |"
        )
        lines.append("")

        # Key rates
        lines.append("## 📈 质量指标")
        lines.append("")
        lines.append("| 指标 | 清洗前 | 清洗后 | 变化 |")
        lines.append("|------|--------|--------|------|")
        dup_delta = report.duplicate_rate_after - report.duplicate_rate_before
        dup_arrow = "↓" if dup_delta < 0 else "↑"
        lines.append(
            f"| 重复率 | {report.duplicate_rate_before:.2%} "
            f"| {report.duplicate_rate_after:.2%} | {dup_arrow} {abs(dup_delta):.2%} |"
        )
        miss_delta = report.missing_rate_after - report.missing_rate_before
        miss_arrow = "↓" if miss_delta < 0 else "↑"
        lines.append(
            f"| 缺失率 | {report.missing_rate_before:.2%} "
            f"| {report.missing_rate_after:.2%} | {miss_arrow} {abs(miss_delta):.2%} |"
        )
        lines.append("")

        # Cleaning details
        if report.cleaning_report:
            cr = report.cleaning_report
            lines.append("## 🧹 清洗详情")
            lines.append("")
            lines.append(f"- 原始行数：{cr.original_rows}")
            lines.append(f"- 清洗后行数：{cr.cleaned_rows}")
            lines.append(f"- 去重：移除 {cr.duplicates_removed} 条")
            lines.append(f"- 补全：填补 {cr.missing_filled} 个缺失值")
            lines.append(f"- 格式化：处理 {cr.formatted_cells} 个单元格")
            lines.append("")
            if cr.missing_by_column:
                lines.append("**各列缺失情况：**")
                lines.append("")
                for col, n in cr.missing_by_column.items():
                    lines.append(f"- {col}：{n} 个缺失值")
                lines.append("")
            if cr.duplicate_groups:
                lines.append(f"检测到 {len(cr.duplicate_groups)} 组重复记录，已自动去重。")
                lines.append("")

        # Classification tags
        if report.classification_report:
            cl = report.classification_report
            lines.append("## 🏷️ 标签分布")
            lines.append("")
            lines.append(f"总行数：{cl.total_rows}  |  已打标签：{cl.tagged_rows}")
            lines.append("")
            for t in cl.tags:
                pct = t.rows_matched / cl.total_rows if cl.total_rows else 0
                lines.append(f"- **{t.tag}**：{t.rows_matched} 条（{pct:.0%}）")
            lines.append("")

        # Per-column stats
        lines.append("## 📋 字段质量详情")
        lines.append("")
        lines.append(
            "| 字段名 | 类型 | 样本量 | 缺失 | 缺失率 | 唯一值 | 示例值 |"
        )
        lines.append(
            "|--------|------|--------|------|--------|--------|--------|"
        )
        for s in report.column_stats:
            sample_str = " / ".join(s.sample_values[:2])
            if len(sample_str) > 30:
                sample_str = sample_str[:27] + "..."
            lines.append(
                f"| {s.col} | {s.field_type} | {s.total} | {s.missing} "
                f"| {s.missing_pct:.0%} | {s.unique} | {sample_str} |"
            )
        lines.append("")

        # Recommendations
        if report.recommendations:
            lines.append("## 💡 优化建议")
            lines.append("")
            for rec in report.recommendations:
                lines.append(f"{rec}")
            lines.append("")

        return "\n".join(lines)

    # ─── Compact dict (for JSON / API response) ─────────────────────────────────

    def to_dict(self, report: DataQualityReport) -> Dict[str, Any]:
        return {
            "generated_at":      report.generated_at,
            "source_name":        report.source_name,
            "tier":               report.tier,
            "before_shape":        report.before_shape,
            "after_shape":         report.after_shape,
            "duplicate_rate_before": report.duplicate_rate_before,
            "duplicate_rate_after":  report.duplicate_rate_after,
            "missing_rate_before":   report.missing_rate_before,
            "missing_rate_after":   report.missing_rate_after,
            "overall_score":         report.overall_score,
            "column_stats": [
                {
                    "col":         s.col,
                    "field_type":  s.field_type,
                    "total":       s.total,
                    "missing":     s.missing,
                    "missing_pct": round(s.missing_pct, 4),
                    "unique":      s.unique,
                    "sample_values": s.sample_values,
                }
                for s in report.column_stats
            ],
            "recommendations": report.recommendations,
        }
