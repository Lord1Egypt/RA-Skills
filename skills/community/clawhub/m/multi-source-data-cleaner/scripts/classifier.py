"""
F4 · Data classification and tagging.
AI-powered auto-tagging + user-defined classification rules.

Usage:
    from classifier import DataClassifier, load_rules, DEFAULT_RULES

    clf = DataClassifier(field_info, rules=rules)
    df_tagged, tag_col = clf.classify(df)
"""

import os
import json
import re
import math
from typing import Dict, List, Optional, Callable, Any
from dataclasses import dataclass, field
import pandas as pd

from field_identifier import FieldType, FieldInfo

# ─── Built-in classification rules ─────────────────────────────────────────────

DEFAULT_RULES: List[Dict[str, Any]] = [
    # ── Customer value tiers ────────────────────────────────────────────────────
    {
        "name": "高价值客户",
        "description": "累计消费 ≥ 5000 元",
        "conditions": [
            {
                "column": ".*金额|.*消费|.*总额|.*销售额",
                "type": "amount",
                "operator": "gte",
                "value": 5000,
            }
        ],
    },
    {
        "name": "中等价值客户",
        "description": "累计消费 1000–5000 元",
        "conditions": [
            {
                "column": ".*金额|.*消费|.*总额|.*销售额",
                "type": "amount",
                "operator": "between",
                "value": [1000, 5000],
            }
        ],
    },
    {
        "name": "低价值客户",
        "description": "累计消费 < 1000 元",
        "conditions": [
            {
                "column": ".*金额|.*消费|.*总额|.*销售额",
                "type": "amount",
                "operator": "lt",
                "value": 1000,
            }
        ],
    },
    {
        "name": "沉睡用户",
        "description": "超过 90 天未消费",
        "conditions": [
            {
                "column": ".*日期|.*时间|.*最后.*购买",
                "type": "days_ago",
                "operator": "gt",
                "value": 90,
            }
        ],
    },
    {
        "name": "新客户",
        "description": "注册/首次购买在 30 天内",
        "conditions": [
            {
                "column": ".*注册|.*首次|.*创建.*时间",
                "type": "days_ago",
                "operator": "lte",
                "value": 30,
            }
        ],
    },
    {
        "name": "高风险订单",
        "description": "金额异常高（> 平均值 3σ）或收货地址模糊",
        "conditions": [
            {
                "column": ".*金额|.*总额|.*实付",
                "type": "amount_outlier",
                "operator": "gt_3sigma",
            }
        ],
    },
    {
        "name": "企业客户",
        "description": "邮箱为企业域名（非 gmail/qq/163 等公共邮箱）",
        "conditions": [
            {
                "column": ".*邮箱|.*邮件",
                "type": "email_domain",
                "operator": "not_public",
            }
        ],
    },
    {
        "name": "VIP客户",
        "description": "累计消费 ≥ 20000 元",
        "conditions": [
            {
                "column": ".*金额|.*消费|.*总额",
                "type": "amount",
                "operator": "gte",
                "value": 20000,
            }
        ],
    },
]

# Public email domains to exclude for "企业客户" rule
PUBLIC_EMAIL_DOMAINS = {
    "gmail.com", "qq.com", "163.com", "126.com", "sina.com",
    "sohu.com", "hotmail.com", "outlook.com", "yahoo.com",
    "foxmail.com", "google.com", "live.com", "msn.com",
}

# ─── Rule evaluation engine ────────────────────────────────────────────────────

@dataclass
class TagResult:
    tag: str
    description: str
    rows_matched: int

@dataclass
class ClassificationReport:
    total_rows: int
    tagged_rows: int
    tags: List[TagResult]

    def summary(self) -> str:
        lines = [
            f"总行数：{self.total_rows}  |  已打标签：{self.tagged_rows}"
            f"（{self.tagged_rows/self.total_rows:.0%}）"
            if self.total_rows else "总行数：0",
            "标签分布：",
        ]
        for t in self.tags:
            lines.append(f"  - {t.tag}：{t.rows_matched} 条")
        return "\n".join(lines)


class DataClassifier:
    """
    Apply classification rules to a DataFrame to produce tags.

    Parameters
    ----------
    field_info : Dict[col -> FieldInfo] from field_identifier
    rules      : list of rule dicts (see DEFAULT_RULES format)
    tag_col    : name for the output tag column
    """

    def __init__(
        self,
        field_info: Dict[str, FieldInfo],
        rules: Optional[List[Dict[str, Any]]] = None,
        tag_col: str = "标签",
        *,
        use_ai: bool = False,
        ai_api_key: Optional[str] = None,
    ):
        self.field_info = field_info
        self.rules = rules or DEFAULT_RULES
        self.tag_col = tag_col
        self.use_ai = use_ai
        self.ai_api_key = ai_api_key

    def classify(
        self,
        df: pd.DataFrame,
    ) -> tuple[pd.DataFrame, str, ClassificationReport]:
        """
        Apply rules and return tagged DataFrame.
        Adds a column named self.tag_col.
        """
        df = df.copy()
        df[self.tag_col] = ""  # initialise

        tag_counts: Dict[str, int] = {}
        matched_any = 0

        for rule in self.rules:
            mask = self._evaluate_rule(df, rule)
            n_matched = mask.sum()
            if n_matched > 0:
                # Append tag (may already have one)
                new_tags = df.loc[mask, self.tag_col].apply(
                    lambda x: f"{x}; {rule['name']}" if x else rule["name"]
                )
                df[self.tag_col] = new_tags.combine_first(df[self.tag_col])
                tag_counts[rule["name"]] = int(n_matched)
                matched_any += n_matched

        # Remove leading semicolon on first tag
        df[self.tag_col] = df[self.tag_col].str.lstrip("; ")

        report = ClassificationReport(
            total_rows=len(df),
            tagged_rows=int((df[self.tag_col] != "").sum()),
            tags=[
                TagResult(tag=name, description="", rows_matched=count)
                for name, count in tag_counts.items()
            ],
        )

        return df, self.tag_col, report

    # ─── Rule evaluation ───────────────────────────────────────────────────────

    def _evaluate_rule(self, df: pd.DataFrame, rule: Dict) -> pd.Series:
        """Return a boolean mask for rows matching the rule."""
        import numpy as np

        conditions = rule.get("conditions", [])
        if not conditions:
            return pd.Series(False, index=df.index)

        masks: List[pd.Series] = []
        for cond in conditions:
            col_pat  = cond["column"]
            cond_type = cond["type"]
            operator = cond["operator"]
            value    = cond.get("value")

            # Find matching columns
            matching_cols = [
                c for c in df.columns
                if re.match(col_pat, str(c), re.IGNORECASE)
            ]

            col_mask = pd.Series(False, index=df.index)
            for col in matching_cols:
                col_mask |= self._eval_condition(df[col], cond_type, operator, value)

            masks.append(col_mask)

        # All conditions must match (AND)
        if not masks:
            return pd.Series(False, index=df.index)
        result = masks[0]
        for m in masks[1:]:
            result = result & m
        return result

    def _eval_condition(
        self,
        series: pd.Series,
        cond_type: str,
        operator: str,
        value: Any,
    ) -> pd.Series:
        """Evaluate a single condition on a series."""
        import numpy as np

        if cond_type == "amount":
            # Parse numeric from string like "¥1,234.56"
            nums = series.astype(str).str.replace(
                r"[¥$€£,\s]", "", regex=True
            ).str.replace(r"元", "", regex=False)
            nums = pd.to_numeric(nums, errors="coerce").fillna(0)

            if operator == "gte":
                return nums >= float(value)
            elif operator == "gt":
                return nums > float(value)
            elif operator == "lt":
                return nums < float(value)
            elif operator == "lte":
                return nums <= float(value)
            elif operator == "between":
                lo, hi = float(value[0]), float(value[1])
                return (nums >= lo) & (nums <= hi)

        elif cond_type == "days_ago":
            # Parse date and compute days since
            dates = series.astype(str).str.strip()
            now_ts = pd.Timestamp.now().timestamp()

            def to_days_ago(v: str):
                for fmt in ("%Y-%m-%d", "%Y/%m/%d", "%Y年%m月%d日",
                            "%Y%m%d", "%m/%d/%Y"):
                    try:
                        dt = pd.to_datetime(v, format=fmt)
                        return (now_ts - dt.timestamp()) / 86400
                    except Exception:
                        continue
                return -1  # can't parse

            days = dates.apply(to_days_ago)
            if operator == "gt":
                return days > float(value)
            elif operator == "lte":
                return (days >= 0) & (days <= float(value))

        elif cond_type == "amount_outlier":
            if operator == "gt_3sigma":
                nums = pd.to_numeric(
                    series.astype(str).str.replace(r"[¥$€£,\s]", "", regex=True),
                    errors="coerce"
                )
                mean = nums.mean()
                std  = nums.std()
                if std == 0 or math.isnan(std):
                    return pd.Series(False, index=series.index)
                return nums > (mean + 3 * std)

        elif cond_type == "email_domain":
            if operator == "not_public":
                domain_col = series.astype(str).str.split("@").str[-1].str.lower()
                return ~domain_col.isin(PUBLIC_EMAIL_DOMAINS)

        return pd.Series(False, index=series.index)

    # ─── AI-powered auto-tagging ───────────────────────────────────────────────

    def classify_with_ai(
        self,
        df: pd.DataFrame,
    ) -> tuple[pd.DataFrame, str, ClassificationReport]:
        """
        Use AI to generate tags when built-in rules are insufficient.
        Requires DATA_CLEANER_API_KEY env var.
        """
        if not self.use_ai:
            return self.classify(df)

        api_key = self.ai_api_key or os.environ.get("DATA_CLEANER_API_KEY", "")
        if not api_key:
            # Fallback to rules
            return self.classify(df)

        # Build sample for AI
        samples = df.head(20).to_csv(index=False, encoding="utf-8")

        prompt = (
            "你是一个数据分析师。根据以下数据样本，为每行生成合适的业务标签。\n"
            "标签例如：高价值客户、低价值客户、沉睡用户、新客户、VIP客户、"
            "企业客户、高风险订单、待激活用户、忠诚客户等。\n"
            "每行输出一个标签（最多2个，用分号分隔）。\n"
            "只输出CSV格式，第一列是原数据索引，第二列是标签。\n"
            f"\n样本数据：\n{samples}"
        )

        try:
            import urllib.request
            url = "https://api.minimax.chat/v1/text/chatcompletion_pro"
            payload = json.dumps({
                "model": "MiniMax-Text-01",
                "messages": [{"role": "user", "content": prompt}],
                "max_tokens": 500,
                "temperature": 0.3,
            }).encode("utf-8")

            req = urllib.request.Request(
                url,
                data=payload,
                headers={
                    "Authorization": f"Bearer {api_key}",
                    "Content-Type": "application/json",
                },
                method="POST",
            )
            with urllib.request.urlopen(req, timeout=20) as resp:
                raw = json.loads(resp.read().decode("utf-8"))
            content = raw["choices"][0]["message"]["content"]

            # Parse AI output into tags
            df_tagged, tag_col, report = self.classify(df)
            # Overlay AI tags from content
            df_tagged, report = self._apply_ai_tags(df_tagged, content, report)
            return df_tagged, tag_col, report

        except Exception:
            return self.classify(df)

    def _apply_ai_tags(
        self,
        df: pd.DataFrame,
        ai_output: str,
        report: ClassificationReport,
    ) -> tuple[pd.DataFrame, ClassificationReport]:
        """Parse AI output CSV and merge tags."""
        import io as _io
        import numpy as np

        try:
            ai_df = pd.read_csv(
                _io.StringIO(ai_output),
                header=None,
                names=["index", "tag"],
                dtype={"index": str},
            )
            idx_map = dict(zip(ai_df["index"].astype(str), ai_df["tag"].astype(str)))

            for idx_str, tag in idx_map.items():
                if idx_str.isdigit():
                    idx = int(idx_str)
                    if idx < len(df):
                        cur = df.at[idx, self.tag_col] or ""
                        df.at[idx, self.tag_col] = f"{cur}; {tag}".lstrip("; ")
        except Exception:
            pass  # If AI output is unparseable, keep rule-based tags

        report.tagged_rows = int((df[self.tag_col] != "").sum())
        return df, report


# ─── User rule management ─────────────────────────────────────────────────────

def load_rules(path: str) -> List[Dict[str, Any]]:
    """Load custom classification rules from a JSON file."""
    with open(path, encoding="utf-8") as f:
        return json.load(f)

def save_rules(rules: List[Dict[str, Any]], path: str) -> None:
    """Save custom classification rules to a JSON file."""
    with open(path, "w", encoding="utf-8") as f:
        json.dump(rules, f, ensure_ascii=False, indent=2)
