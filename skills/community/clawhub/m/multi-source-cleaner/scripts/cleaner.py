"""
F3 · Core data cleaning engine.
Handles:
  - Smart deduplication (exact + fuzzy)
  - Missing value imputation (mean/mode/inference/leave_blank)
  - Format unification (phone/date/amount/address)

Usage:
    from cleaner import DataCleaner

    cleaner = DataCleaner(field_info)
    df_clean = cleaner.clean(df)
"""

import re
import math
from typing import Dict, Optional, List, Callable, Any
from dataclasses import dataclass, field
from datetime import datetime
import pandas as pd

from field_identifier import FieldType, FieldInfo

# ─── Address standardisation helpers ─────────────────────────────────────────

_CN_PROVINCES = [
    "北京市","天津市","上海市","重庆市",
    "河北省","山西省","辽宁省","吉林省","黑龙江省",
    "江苏省","浙江省","安徽省","福建省","江西省","山东省",
    "河南省","湖北省","湖南省","广东省","海南省",
    "四川省","贵州省","云南省","陕西省","甘肃省","青海省","台湾省",
    "内蒙古自治区","广西壮族自治区","西藏自治区","宁夏回族自治区","新疆维吾尔自治区",
    "香港特别行政区","澳门特别行政区",
]
_CN_PROVINCE_ABBR = {
    "北京":"北京市","上海":"上海市","天津":"天津市","重庆":"重庆市",
    "河北":"河北省","山西":"山西省","辽宁":"辽宁省","吉林":"吉林省",
    "黑龙江":"黑龙江省","江苏":"江苏省","浙江":"浙江省","安徽":"安徽省",
    "福建":"福建省","江西":"江西省","山东":"山东省","河南":"河南省",
    "湖北":"湖北省","湖南":"湖南省","广东":"广东省","海南":"海南省",
    "四川":"四川省","贵州":"贵州省","云南":"云南省","陕西":"陕西省",
    "甘肃":"甘肃省","青海":"青海省","台湾":"台湾省",
    "内蒙古":"内蒙古自治区","广西":"广西壮族自治区","西藏":"西藏自治区",
    "宁夏":"宁夏回族自治区","新疆":"新疆维吾尔自治区",
    "香港":"香港特别行政区","澳门":"澳门特别行政区",
}

# ─── Dataclass results ─────────────────────────────────────────────────────────

@dataclass
class CleaningReport:
    original_rows: int
    cleaned_rows: int
    duplicates_removed: int
    missing_filled: int
    formatted_cells: int
    missing_by_column: Dict[str, int] = field(default_factory=dict)
    duplicate_groups: List[List[int]] = field(default_factory=list)

    def summary(self) -> str:
        return (
            f"原始行数：{self.original_rows}  |  清洗后行数：{self.cleaned_rows}\n"
            f"去重：移除 {self.duplicates_removed} 条重复记录\n"
            f"补全：填补 {self.missing_filled} 个缺失值\n"
            f"格式化：处理 {self.formatted_cells} 个单元格"
        )

# ─── Core Cleaner ─────────────────────────────────────────────────────────────

class DataCleaner:
    """
    Main cleaning orchestrator.

    Parameters
    ----------
    field_info : Dict[col -> FieldInfo] from field_identifier
    """

    def __init__(
        self,
        field_info: Dict[str, FieldInfo],
        *,
        dedup_strategy: str = "auto",
        fill_strategy: str = "auto",
        format_phone: bool = True,
        format_date: bool = True,
        format_amount: bool = True,
        format_address: bool = True,
    ):
        self.field_info = field_info
        self.dedup_strategy = dedup_strategy  # "exact" | "fuzzy" | "auto"
        self.fill_strategy  = fill_strategy   # "auto" | "mean" | "mode" | "leave_blank"
        self.format_phone   = format_phone
        self.format_date    = format_date
        self.format_amount  = format_amount
        self.format_address = format_address

        # Per-column type lookup
        self._type_map: Dict[str, FieldType] = {
            col: fi.field_type for col, fi in field_info.items()
        }

    def clean(self, df: pd.DataFrame) -> tuple[pd.DataFrame, CleaningReport]:
        """
        Full cleaning pipeline on a single DataFrame.
        Returns (cleaned_df, report).
        """
        df = df.copy()

        original_rows = len(df)
        total_missing_filled = 0
        total_formatted = 0

        # ── Step 1: Normalise column names ──────────────────────────────────────
        df.columns = [str(c).strip() for c in df.columns]

        # ── Step 2: Missing value imputation ─────────────────────────────────────
        df, missing_filled, missing_by_col = self._impute(df)
        total_missing_filled += missing_filled

        # ── Step 3: Format unification ──────────────────────────────────────────
        df, formatted = self._format_all(df)
        total_formatted += formatted

        # ── Step 4: Deduplication ───────────────────────────────────────────────
        df, dup_removed, dup_groups = self._deduplicate(df)
        total_dup_removed = original_rows - len(df)

        report = CleaningReport(
            original_rows=original_rows,
            cleaned_rows=len(df),
            duplicates_removed=total_dup_removed,
            missing_filled=total_missing_filled,
            formatted_cells=total_formatted,
            missing_by_column=missing_by_col,
            duplicate_groups=dup_groups,
        )
        return df, report

    # ── Imputation ─────────────────────────────────────────────────────────────

    def _impute(
        self,
        df: pd.DataFrame,
    ) -> tuple[pd.DataFrame, int, Dict[str, int]]:
        """Fill missing values according to field type and fill_strategy."""
        filled = 0
        missing_by_col: Dict[str, int] = {}
        df = df.copy()

        for col in df.columns:
            ftype = self._type_map.get(col, FieldType.UNKNOWN)
            blanks = df[col].astype(str).isin(["", "nan", "NaN", "None", "null", "NULL", "undefined"])
            n_blank = blanks.sum()
            if n_blank == 0:
                continue

            missing_by_col[col] = int(n_blank)
            strategy = self.fill_strategy

            if strategy == "leave_blank":
                continue  # keep NaN

            filled_col = self._fill_column(df[col], ftype, strategy)
            df[col] = filled_col
            filled += n_blank

        return df, filled, missing_by_col

    def _fill_column(
        self,
        series: pd.Series,
        ftype: FieldType,
        strategy: str,
    ) -> pd.Series:
        """Apply the appropriate fill logic to a single column."""
        blanks = series.astype(str).isin(["", "nan", "NaN", "None", "null", "NULL"])

        if strategy == "mean":
            if ftype in (FieldType.AMOUNT, FieldType.NUMBER):
                nums = pd.to_numeric(series, errors="coerce")
                mean_val = nums.mean()
                if not math.isnan(mean_val):
                    filled = series.copy()
                    filled[blanks] = f"{mean_val:.2f}"
                    return filled

        elif strategy == "mode":
            # Most common non-blank value
            non_blanks = series[~blanks]
            if not non_blanks.empty:
                mode_val = non_blanks.mode()
                if not mode_val.empty:
                    filled = series.copy()
                    filled[blanks] = mode_val.iloc[0]
                    return filled

        elif strategy in ("auto", "inference"):
            filled = self._auto_fill(series, ftype)
            return filled

        # Default: leave blank
        return series

    def _auto_fill(self, series: pd.Series, ftype: FieldType) -> pd.Series:
        """
        Auto-fill missing values based on field semantics.
        Returns a new series (does not modify in place).
        """
        blanks = series.astype(str).isin(["", "nan", "NaN", "None", "null", "NULL"])
        if blanks.sum() == 0:
            return series

        filled = series.copy()

        if ftype == FieldType.GENDER:
            # Fill with most common
            non_blank = series[~blanks]
            if not non_blank.empty:
                mode = non_blank.mode()
                if not mode.empty:
                    filled[blanks] = mode.iloc[0]

        elif ftype in (FieldType.AMOUNT, FieldType.NUMBER):
            nums = pd.to_numeric(series, errors="coerce")
            mean_val = nums.mean()
            if not math.isnan(mean_val):
                filled[blanks] = f"{mean_val:.2f}"

        elif ftype == FieldType.DATE:
            # Try to parse most common format, fill with placeholder
            filled[blanks] = "未知"

        elif ftype == FieldType.PHONE:
            filled[blanks] = "未知"

        elif ftype == FieldType.EMAIL:
            filled[blanks] = "未知"

        # Text / address / others → "未知"
        elif ftype in (FieldType.TEXT, FieldType.ADDRESS, FieldType.UNKNOWN,
                       FieldType.NAME, FieldType.SKU, FieldType.ORDER_NO):
            filled[blanks] = "未知"

        return filled

    # ── Format unification ───────────────────────────────────────────────────────

    def _format_all(self, df: pd.DataFrame) -> tuple[pd.DataFrame, int]:
        formatted = 0
        df = df.copy()

        for col in df.columns:
            ftype = self._type_map.get(col, FieldType.UNKNOWN)
            before = df[col].astype(str)

            if ftype == FieldType.PHONE and self.format_phone:
                df[col] = df[col].apply(self._format_phone)
            elif ftype == FieldType.DATE and self.format_date:
                df[col] = df[col].apply(self._format_date)
            elif ftype == FieldType.AMOUNT and self.format_amount:
                df[col] = df[col].apply(self._format_amount_)
            elif ftype == FieldType.ADDRESS and self.format_address:
                df[col] = df[col].apply(self._standardise_address)

            after = df[col].astype(str)
            formatted += (before != after).sum()

        return df, formatted

    def _format_phone(self, val: Any) -> str:
        """Normalise phone to 1xx-xxxx-xxxx."""
        s = str(val).strip()
        if s in ("", "nan", "NaN", "None", "未知"):
            return s
        # Strip all non-digit
        digits = re.sub(r"\D", "", s)
        # Take last 11 digits if > 11
        if len(digits) > 11:
            digits = digits[-11:]
        if len(digits) == 11 and digits[0] == "1":
            return f"{digits[0:3]}-{digits[3:7]}-{digits[7:11]}"
        return s  # return original if not recognisable

    def _format_date(self, val: Any) -> str:
        """Normalise date to YYYY-MM-DD."""
        s = str(val).strip()
        if s in ("", "nan", "NaN", "None", "未知"):
            return s

        # Already ISO?
        if re.match(r"\d{4}-\d{2}-\d{2}", s):
            return s

        # Chinese format: YYYY年MM月DD日
        m = re.match(r"(\d{4})年(\d{1,2})月(\d{1,2})日?", s)
        if m:
            return f"{m.group(1)}-{int(m.group(2)):02d}-{int(m.group(3)):02d}"

        # Slash/ hyphen: YYYY/MM/DD or YYYY-MM-DD or YYYYMD
        for pat in [
            r"(\d{4})[-/年](\d{1,2})[-/月](\d{1,2})",
            r"(\d{4})(\d{2})(\d{2})",
        ]:
            m = re.match(pat, s)
            if m:
                return f"{m.group(1)}-{int(m.group(2)):02d}-{int(m.group(3)):02d}"

        # YYYYMMDD integer
        if re.match(r"^\d{8}$", s):
            return f"{s[:4]}-{s[4:6]}-{s[6:8]}"

        # Unix timestamp (seconds)
        if re.match(r"^\d{10}$", s):
            try:
                from datetime import datetime as dt
                return dt.fromtimestamp(int(s)).strftime("%Y-%m-%d")
            except Exception:
                pass

        # Milliseconds
        if re.match(r"^\d{13}$", s):
            try:
                from datetime import datetime as dt
                return dt.fromtimestamp(int(s) / 1000).strftime("%Y-%m-%d")
            except Exception:
                pass

        return s

    def _format_amount_(self, val: Any) -> str:
        """Normalise amount to two decimal places."""
        s = str(val).strip()
        if s in ("", "nan", "NaN", "None", "未知"):
            return s
        # Strip currency symbols and commas
        cleaned = re.sub(r"[¥$€£,\s]", "", s)
        try:
            num = float(cleaned)
            return f"{num:.2f}"
        except ValueError:
            return s

    def _standardise_address(self, val: Any) -> str:
        """Standardise Chinese address to 省市区街道格式."""
        s = str(val).strip()
        if s in ("", "nan", "NaN", "None", "未知"):
            return s

        # Expand province abbreviation
        for abbr, full in _CN_PROVINCE_ABBR.items():
            if s.startswith(abbr):
                s = full + s[len(abbr):]
                break

        # Normalise separators to " "
        s = re.sub(r"[,，;；\t]+", " ", s)
        s = re.sub(r"\s+", " ", s).strip()

        return s

    # ─── Deduplication ─────────────────────────────────────────────────────────

    def _deduplicate(
        self,
        df: pd.DataFrame,
    ) -> tuple[pd.DataFrame, int, List[List[int]]]:
        """
        Deduplicate rows.
        Strategy:
          exact  → drop_duplicates on all columns
          fuzzy  → fuzzy match on key identity columns (phone/name/email/order_no)
          auto   → fuzzy if key columns present, else exact
        """
        strategy = self.dedup_strategy
        dup_groups: List[List[int]] = []

        if df.empty:
            return df, 0, dup_groups

        key_cols = self._find_key_columns()
        original_len = len(df)

        if strategy == "exact":
            before = len(df)
            df = df.drop_duplicates()
            removed = before - len(df)
            return df, removed, dup_groups

        if strategy in ("fuzzy", "auto") and key_cols:
            df, removed, dup_groups = self._fuzzy_dedup(df, key_cols)
            return df, removed, dup_groups

        # Fallback: exact
        before = len(df)
        df = df.drop_duplicates()
        return df, before - len(df), dup_groups

    def _find_key_columns(self) -> List[str]:
        """Find identity-like columns suitable for fuzzy dedup."""
        key_types = {
            FieldType.PHONE, FieldType.EMAIL,
            FieldType.NAME, FieldType.ORDER_NO, FieldType.SKU, FieldType.ID_CARD,
        }
        return [
            col for col, ft in self._type_map.items()
            if ft in key_types
        ]

    def _fuzzy_dedup(
        self,
        df: pd.DataFrame,
        key_cols: List[str],
    ) -> tuple[pd.DataFrame, int, List[List[int]]]:
        """
        Fuzzy deduplication using FuzzyWuzzy on key columns.
        Keeps the first occurrence, removes fuzzy duplicates.
        """
        try:
            from fuzzywuzzy import fuzz
        except ImportError:
            # Fallback to exact if fuzzywuzzy not installed
            before = len(df)
            df = df.drop_duplicates(subset=key_cols, keep="first")
            return df, before - len(df), []

        # Build composite key strings
        key_strs = df[key_cols].astype(str).agg(" | ".join, axis=1)

        keep_idx: List[int] = []
        dup_groups: List[List[int]] = []
        removed = 0

        for i, key in enumerate(key_strs):
            is_dup = False
            for j in keep_idx:
                score = fuzz.ratio(key, key_strs.iloc[j])
                if score >= 88:  # threshold
                    is_dup = True
                    break

            if is_dup:
                removed += 1
            else:
                keep_idx.append(i)

        dup_indices = set(range(len(df))) - set(keep_idx)
        dup_groups = [list(dup_indices)] if dup_indices else []

        return df.iloc[keep_idx].reset_index(drop=True), removed, dup_groups


# ─── Convenience function ─────────────────────────────────────────────────────

def clean_dataframe(
    df: pd.DataFrame,
    field_info: Dict[str, FieldInfo],
    *,
    dedup_strategy: str = "auto",
    fill_strategy: str = "auto",
) -> tuple[pd.DataFrame, CleaningReport]:
    """
    One-liner clean.
    """
    cleaner = DataCleaner(
        field_info,
        dedup_strategy=dedup_strategy,
        fill_strategy=fill_strategy,
    )
    return cleaner.clean(df)
