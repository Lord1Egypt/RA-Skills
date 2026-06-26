"""
F5 · Multi-source data merge and join.
Supports:
  - Exact join on key columns
  - Fuzzy join (fuzzywuzzy) when exact match fails
  - Auto-key detection

Usage:
    from merger import DataMerger, MergeResult

    merger = DataMerger(sources)   # sources = [(name, df), ...]
    result = merger.merge(
        how="left",
        on=[("手机号", "电话")],    # [(left_col, right_col)]
        fuzzy_on=[("姓名", "客户名")],
        fuzzy_threshold=85,
    )
    df_merged = result.df
"""

import re
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass, field
import pandas as pd

# ─── Exceptions ─────────────────────────────────────────────────────────────────

class MergeError(Exception):
    pass

# ─── Results ───────────────────────────────────────────────────────────────────

@dataclass
class MergeResult:
    df: pd.DataFrame
    left_name: str
    right_name: str
    matched_rows: int
    unmatched_left: int
    unmatched_right: int
    fuzzy_matched: int
    join_type: str

    def summary(self) -> str:
        return (
            f"合并「{self.left_name}」+「{self.right_name}」\n"
            f"匹配行：{self.matched_rows}  |  左表未匹配：{self.unmatched_left}"
            f"  |  右表未匹配：{self.unmatched_right}\n"
            f"模糊匹配：{self.fuzzy_matched} 行"
        )

# ─── Merger ────────────────────────────────────────────────────────────────────

class DataMerger:
    """
    Merge multiple DataFrames with exact and fuzzy join support.

    Parameters
    ----------
    sources : List[Tuple[name, df]]
    """

    def __init__(self, sources: List[Tuple[str, pd.DataFrame]]):
        if len(sources) < 2:
            raise MergeError("至少需要 2 个数据源才能合并。")
        self.sources = sources

    def merge(
        self,
        how: str = "inner",
        on: Optional[List[Tuple[str, str]]] = None,
        fuzzy_on: Optional[List[Tuple[str, str]]] = None,
        fuzzy_threshold: int = 85,
        suffix_left: str = "_x",
        suffix_right: str = "_y",
    ) -> MergeResult:
        """
        Perform a join between the first two sources.

        Parameters
        ----------
        how            : "inner" | "left" | "right" | "outer" | "cross"
        on             : list of (left_col, right_col) for exact join
        fuzzy_on       : list of (left_col, right_col) for fuzzy join
                         (applied after exact join fails)
        fuzzy_threshold: 0-100, fuzzy match score threshold
        suffix_left/right: suffix for overlapping columns
        """
        if how not in ("inner", "left", "right", "outer", "cross"):
            raise MergeError(f"不支持的 join 类型：{how}。可选：inner/left/right/outer/cross")

        left_name, left_df  = self.sources[0]
        right_name, right_df = self.sources[1]

        # Normalise: strip + lowercase column names
        left_df  = left_df.copy()
        right_df = right_df.copy()
        left_df.columns  = [str(c).strip() for c in left_df.columns]
        right_df.columns = [str(c).strip() for c in right_df.columns]

        # ── Auto-detect key columns if not provided ────────────────────────────
        if not on and not fuzzy_on:
            on = self._auto_detect_keys(left_df, right_df)

        if not on and not fuzzy_on:
            raise MergeError(
                "未指定合并键，请通过 on= 参数指定要关联的列名，"
                "或使用 fuzzy_on= 进行模糊关联。"
            )

        # ── Exact join ─────────────────────────────────────────────────────────
        df_exact, exact_matched = self._exact_merge(
            left_df, right_df, on or [], how, suffix_left, suffix_right
        )

        # ── Fuzzy join on remaining rows ───────────────────────────────────────
        fuzzy_matched = 0
        if fuzzy_on:
            df_exact, fuzzy_matched = self._fuzzy_merge(
                df_exact, left_df, right_df,
                fuzzy_on, exact_matched, how,
                fuzzy_threshold, suffix_left, suffix_right
            )

        # ── Compute stats ───────────────────────────────────────────────────────
        matched = exact_matched + fuzzy_matched
        if how in ("left", "inner"):
            unmatched_left = len(left_df) - matched
        else:
            unmatched_left = 0

        if how in ("right", "inner", "outer"):
            unmatched_right = len(right_df) - matched
        else:
            unmatched_right = 0

        return MergeResult(
            df=df_exact,
            left_name=left_name,
            right_name=right_name,
            matched_rows=matched,
            unmatched_left=unmatched_left,
            unmatched_right=unmatched_right,
            fuzzy_matched=fuzzy_matched,
            join_type=how,
        )

    # ─── Auto key detection ─────────────────────────────────────────────────────

    KEY_PATTERNS = {
        "phone":  ["手机", "电话", "mobile", "phone", "tel"],
        "email":  ["邮箱", "email", "mail"],
        "name":   ["姓名", "name", "客户名", "用户名", "username"],
        "order":  ["订单", "order", "order_no", "订单号"],
        "sku":    ["sku", "商品编号", "产品编号"],
        "id":     ["id", "编号", "用户id"],
    }

    def _auto_detect_keys(
        self,
        left: pd.DataFrame,
        right: pd.DataFrame,
    ) -> List[Tuple[str, str]]:
        """Find matching column pairs between left and right DataFrames."""
        matches: List[Tuple[str, str]] = []
        for pattern_name, keywords in self.KEY_PATTERNS.items():
            for kw in keywords:
                kw_lower = kw.lower()
                left_cols  = [c for c in left.columns  if kw_lower in c.lower()]
                right_cols = [c for c in right.columns if kw_lower in c.lower()]
                if left_cols and right_cols:
                    matches.append((left_cols[0], right_cols[0]))
        return matches

    # ─── Exact merge ────────────────────────────────────────────────────────────

    def _exact_merge(
        self,
        left: pd.DataFrame,
        right: pd.DataFrame,
        on: List[Tuple[str, str]],
        how: str,
        sfx_l: str,
        sfx_r: str,
    ) -> Tuple[pd.DataFrame, int]:
        """Perform pandas merge on specified columns."""
        if not on:
            return left, 0

        left_keys  = [pair[0] for pair in on]
        right_keys = [pair[1] for pair in on]

        # Rename right keys to match left for pandas merge
        right_renamed = right.rename(columns=dict(zip(right_keys, left_keys)))

        # Only keep right columns not in left (to avoid ambiguity)
        overlap = set(left.columns) & set(right_renamed.columns) - set(left_keys)
        right_dedup = right_renamed.drop(columns=list(overlap), errors="ignore")

        merged = left.merge(
            right_dedup,
            left_on=left_keys,
            right_on=left_keys,
            how=how,
            suffixes=(sfx_l, sfx_r),
        )

        # Count matched rows (rows that got a match)
        matched = len(merged)
        return merged, matched

    # ─── Fuzzy merge ────────────────────────────────────────────────────────────

    def _fuzzy_merge(
        self,
        merged_df: pd.DataFrame,
        left_orig: pd.DataFrame,
        right_orig: pd.DataFrame,
        fuzzy_on: List[Tuple[str, str]],
        already_matched: int,
        how: str,
        threshold: int,
        sfx_l: str,
        sfx_r: str,
    ) -> Tuple[pd.DataFrame, int]:
        """
        For left rows with no match, try fuzzy match against right.
        Append fuzzy-matched rows to merged_df.
        """
        try:
            from fuzzywuzzy import fuzz
        except ImportError:
            return merged_df, 0

        if not fuzzy_on:
            return merged_df, 0

        left_col, right_col = fuzzy_on[0]

        # Rows already matched have non-null right-side data
        # We identify unmatched by checking if right-side join columns are null
        right_cols_in_merged = [c for c in merged_df.columns if sfx_r in c]
        if not right_cols_in_merged:
            # No right columns present yet; treat all as unmatched
            unmatched_mask = pd.Series(True, index=merged_df.index)
        else:
            # If all right suffix cols are null → unmatched
            unmatched_mask = merged_df[right_cols_in_merged[0]].isna()

        unmatched_left = merged_df.loc[unmatched_mask, left_col].copy()
        right_vals    = right_orig[right_col].astype(str).tolist()
        right_orig_index = right_orig.index.tolist()

        fuzzy_rows = []
        fuzzy_count = 0

        for idx, left_val in unmatched_left.items():
            best_score  = 0
            best_row    = None
            best_ridx   = None
            for ri, rv in enumerate(right_vals):
                score = fuzz.ratio(str(left_val), str(rv))
                if score > best_score and score >= threshold:
                    best_score = score
                    best_row   = right_orig.iloc[ri]
                    best_ridx  = right_orig_index[ri]

            if best_row is not None:
                fuzzy_count += 1
                row_data = merged_df.loc[idx].copy()
                # Add right columns that aren't already present
                for col in right_orig.columns:
                    new_col = f"{col}{sfx_r}"
                    if new_col not in row_data.index:
                        row_data[new_col] = best_row[col]
                fuzzy_rows.append(row_data)

        if fuzzy_rows:
            fuzzy_df = pd.DataFrame(fuzzy_rows, index=[r.name for r in fuzzy_rows])
            # Ensure same column order
            fuzzy_df = fuzzy_df.reindex(columns=merged_df.columns)
            merged_df = pd.concat([merged_df, fuzzy_df], ignore_index=True)

        return merged_df, fuzzy_count

    # ─── Convenience: merge all sources iteratively ──────────────────────────────

    def merge_all(
        self,
        on: Optional[List[Tuple[str, str]]] = None,
        fuzzy_on: Optional[List[Tuple[str, str]]] = None,
        fuzzy_threshold: int = 85,
    ) -> Tuple[pd.DataFrame, List[MergeResult]]:
        """
        Merge all sources in order (left-fold).
        Returns the final DataFrame and list of per-step results.
        """
        if len(self.sources) == 2:
            result = self.merge(
                how="outer",
                on=on,
                fuzzy_on=fuzzy_on,
                fuzzy_threshold=fuzzy_threshold,
            )
            return result.df, [result]

        # First merge
        temp_sources = self.sources[:2]
        merger = DataMerger(temp_sources)
        first  = merger.merge(how="outer", on=on, fuzzy_on=fuzzy_on,
                               fuzzy_threshold=fuzzy_threshold)
        results = [first]
        current = ("merged_0", first.df)

        for i in range(2, len(self.sources)):
            _, next_src = self.sources[i]
            temp_sources = [current, (self.sources[i][0], next_src)]
            merger = DataMerger(temp_sources)
            step = merger.merge(how="outer", on=on, fuzzy_on=fuzzy_on,
                                 fuzzy_threshold=fuzzy_threshold)
            results.append(step)
            current = (f"merged_{i}", step.df)

        return current[1], results
