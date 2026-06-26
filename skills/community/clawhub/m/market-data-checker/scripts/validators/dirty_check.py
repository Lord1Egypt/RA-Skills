# -*- coding: utf-8 -*-
"""
DirtyChecker - 脏数据拦截
检测市场数据中的常见脏数据模式：
  - 占位符文本（N/A、--、null、待更新、暂无数据）
  - HTML 标签残留
  - 异常字符（控制字符、过多换行）
  - 超长字段（超过合理长度上限）
"""
import sys, os, re
sys.path.insert(0, os.path.dirname(__file__))

from validators.result import CheckResult


# ── 脏数据模式 ───────────────────────────────────────
DIRTY_PATTERNS = {
    "占位符": [
        r"^N/A$", r"^--$", r"^null$", r"^NULL$",
        r"^待更新$", r"^暂无数据$", r"^暂无$",
        r"^数据缺失$", r"^未知$", r"^待确认$",
        r"^{{.*}}$",   # {{ }} 占位符
        r"^\s*$",      # 纯空白
    ],
    "HTML残留": [
        r"<[^>]+>",                     # HTML 标签
        r"&[a-z]+;",                     # HTML 实体 &nbsp; &amp; 等
        r"\\u[0-9a-f]{4}",               # Unicode 转义序列
    ],
    "控制字符": [
        r"[\x00-\x08\x0b\x0c\x0e-\x1f]",  # 控制字符（换行/回车除外）
    ],
}

# 字段长度上限（字节，UTF-8）
MAX_FIELD_LENGTH = {
    "price": 30,
    "change": 30,
    "volume": 30,
    "标题": 500,
    "内容": 3000,
    "事件": 3000,
    "公司": 200,
    "来源": 200,
    "时间": 100,
    "链接": 500,
}


def _is_dirty_text(text: str) -> tuple:
    """
    检查一段文本是否为脏数据。
    返回 (is_dirty: bool, reason: str, matched_pattern: str)
    """
    if not isinstance(text, str):
        return False, "", ""

    # 空白检查
    if not text.strip():
        return True, "纯空白内容", "空白"

    # 逐模式检查
    for category, patterns in DIRTY_PATTERNS.items():
        for pattern in patterns:
            if re.search(pattern, text):
                return True, f"检测到脏数据模式 [{category}]：匹配 {pattern}", pattern

    return False, "", ""


class DirtyChecker:
    """
    规则 6：脏数据拦截

    检查市场表现、政策动态、企业动态、环球市场速览中的文本字段。
    """

    MARKET_FIELDS = ["price", "change", "volume", "unit"]
    POLICY_FIELDS = ["标题", "内容", "来源", "链接", "时间"]
    ENTERPRISE_FIELDS = ["公司", "事件", "来源", "时间"]
    SUMMARY_FIELDS = ["概述", "更新时间"]

    def check(self, data: dict) -> CheckResult:
        result = CheckResult()

        # 市场表现
        market = data.get("市场表现", {})
        self._check_market_dirty(market, result)

        # 政策动态
        policy = data.get("政策动态", {})
        self._check_policy_dirty(policy, result)

        # 企业动态
        enterprise = data.get("企业动态", {})
        self._check_enterprise_dirty(enterprise, result)

        # 环球市场速览
        summary = data.get("环球市场速览", {})
        if isinstance(summary, dict):
            for field in self.SUMMARY_FIELDS:
                v = summary.get(field)
                if v:
                    is_dirty, reason, matched = _is_dirty_text(str(v))
                    if is_dirty:
                        result.fail(
                            rule="脏数据拦截",
                            category="环球市场速览",
                            key=field,
                            value=str(v)[:80],
                            message=f"{field}: {reason}，匹配 {matched}"
                        )

            # 检查段落列表
            paragraphs = summary.get("段落列表", [])
            if isinstance(paragraphs, list):
                for i, para in enumerate(paragraphs):
                    if para:
                        is_dirty, reason, matched = _is_dirty_text(str(para))
                        if is_dirty:
                            result.fail(
                                rule="脏数据拦截",
                                category="环球市场速览",
                                key=f"段落列表[{i}]",
                                value=str(para)[:80],
                                message=f"段落 {i}: {reason}，匹配 {matched}"
                            )

        return result

    def _check_market_dirty(self, market: dict, result: CheckResult):
        for region, items in market.items():
            if not isinstance(items, dict):
                continue
            for name, fields in items.items():
                if not isinstance(fields, dict):
                    continue
                for field, max_len in MAX_FIELD_LENGTH.items():
                    v = fields.get(field)
                    if v is None:
                        continue
                    s = str(v)

                    # 检查脏数据模式
                    is_dirty, reason, matched = _is_dirty_text(s)
                    if is_dirty:
                        result.fail(
                            rule="脏数据拦截",
                            category=region,
                            key=f"{name}.{field}",
                            value=s[:80],
                            message=f"{name}.{field}: {reason}"
                        )

                    # 检查长度
                    if len(s) > max_len:
                        result.fail(
                            rule="脏数据拦截",
                            category=region,
                            key=f"{name}.{field}",
                            value=f"长度={len(s)}, 上限={max_len}",
                            message=f"{name}.{field} 长度超限（{len(s)} > {max_len}）"
                        )

    def _check_policy_dirty(self, policy: dict, result: CheckResult):
        for region, items in policy.items():
            if not isinstance(items, list):
                continue
            for i, item in enumerate(items):
                if not isinstance(item, dict):
                    continue
                for field, max_len in MAX_FIELD_LENGTH.items():
                    v = item.get(field)
                    if v is None:
                        continue
                    s = str(v)

                    is_dirty, reason, matched = _is_dirty_text(s)
                    if is_dirty:
                        result.fail(
                            rule="脏数据拦截",
                            category=f"政策动态.{region}",
                            key=f"[{i}].{field}",
                            value=s[:80],
                            message=f"{field}: {reason}"
                        )

                    if len(s) > max_len:
                        result.fail(
                            rule="脏数据拦截",
                            category=f"政策动态.{region}",
                            key=f"[{i}].{field}",
                            value=f"长度={len(s)}, 上限={max_len}",
                            message=f"{field} 长度超限（{len(s)} > {max_len}）"
                        )

    def _check_enterprise_dirty(self, enterprise: dict, result: CheckResult):
        for region, items in enterprise.items():
            if not isinstance(items, list):
                continue
            for i, item in enumerate(items):
                if not isinstance(item, dict):
                    continue
                for field, max_len in MAX_FIELD_LENGTH.items():
                    v = item.get(field)
                    if v is None:
                        continue
                    s = str(v)

                    is_dirty, reason, matched = _is_dirty_text(s)
                    if is_dirty:
                        result.fail(
                            rule="脏数据拦截",
                            category=f"企业动态.{region}",
                            key=f"[{i}].{field}",
                            value=s[:80],
                            message=f"{field}: {reason}"
                        )

                    if len(s) > max_len:
                        result.fail(
                            rule="脏数据拦截",
                            category=f"企业动态.{region}",
                            key=f"[{i}].{field}",
                            value=f"长度={len(s)}, 上限={max_len}",
                            message=f"{field} 长度超限（{len(s)} > {max_len}）"
                        )