# -*- coding: utf-8 -*-
"""
CompletenessChecker - 语句完整性 + 截断检测校验
检查维度：
  1. 文本是否以完整句子结尾（句号/问号/感叹号）
  2. 内容是否在句子中途截断（英文截断/括号未闭/极短文本）
  3. 政策/企业动态必填字段是否齐全
  4. 段落列表长度上限（13句）
"""
import sys, os, re
sys.path.insert(0, os.path.dirname(__file__))

from validators.result import CheckResult


# ── 句子完整性检测 ─────────────────────────────────
SENTENCE_END_CHARS = "。？！?!."
SENTENCE_END_PATTERN = re.compile(r'[。？！?!.]\s*$')


def _is_complete_sentence(text: str) -> bool:
    """判断文本是否以完整句子结尾"""
    if not isinstance(text, str) or not text.strip():
        return False
    return bool(SENTENCE_END_PATTERN.search(text.strip()))


# ── 截断检测（与 content_cleaner.py 保持一致）──────────
TRUNCATE_MARKERS = ['...', '…']


def _is_truncated_content(text: str, min_length: int = 20) -> bool:
    """
    判断事件正文/内容字段是否在句子中途截断。

    截断标准：
    1. 文本极短（< min_length 字符） → 截断残留
    2. 括号未闭合（来源信息截断进入正文） → 截断
    3. 以省略符结尾（... / …） → 截断
    4. 以 ASCII 字母/数字结尾 + 无句末标点 → 英文章节截断

    注意：中文句子（非 ASCII 结尾）不以截断论，通过 ensure_sentence_end 补句号。
    """
    if not text or not isinstance(text, str):
        return True
    s = text.strip()
    if not s:
        return True
    if len(s) < min_length:
        return True
    if s.count('(') > s.count(')') or s.count('（') > s.count('）'):
        return True
    if any(s.rstrip().endswith(m) for m in TRUNCATE_MARKERS):
        return True
    last_char = s[-1] if s else ''
    # 仅 ASCII 字母/数字代表英文章节截断
    if last_char.encode('utf-8', errors='ignore').isascii() and last_char.isalnum():
        if not any(s.rstrip().endswith(p) for p in SENTENCE_END_CHARS):
            return True
    return False


class CompletenessChecker:
    """
    规则 7：语句完整性校验

    检查维度：
      1. 环球市场速览 概述/段落列表 是否以句号结尾（完整句子）
      2. 政策动态 每条记录的 标题/内容 是否完整
      3. 企业动态 每条记录的 公司/事件 是否完整
      4. 段落列表长度是否合理（最多 13 句）
    """

    POLICY_REQUIRED_FIELDS = ["标题", "内容"]
    ENTERPRISE_REQUIRED_FIELDS = ["公司", "事件"]

    def check(self, data: dict) -> CheckResult:
        result = CheckResult()

        # 规则 7-1：环球市场速览 概述完整性
        summary = data.get("环球市场速览", {})
        if isinstance(summary, dict):
            overview = summary.get("概述", "")
            if overview and not _is_complete_sentence(str(overview)):
                result.fail(
                    rule="语句完整性",
                    category="环球市场速览",
                    key="概述",
                    value=str(overview)[:60],
                    message="概述未以完整句号结尾"
                )

            # 规则 7-2：段落列表完整性
            paragraphs = summary.get("段落列表", [])
            if isinstance(paragraphs, list):
                if len(paragraphs) > 13:
                    result.fail(
                        rule="语句完整性",
                        category="环球市场速览",
                        key=f"段落列表[长度={len(paragraphs)}]",
                        value=len(paragraphs),
                        message=f"段落列表超过 13 句上限（当前 {len(paragraphs)} 句）"
                    )
                for i, para in enumerate(paragraphs):
                    if para and not _is_complete_sentence(str(para)):
                        result.fail(
                            rule="语句完整性",
                            category="环球市场速览",
                            key=f"段落列表[{i}]",
                            value=str(para)[:60],
                            message=f"第 {i+1} 句未以完整句号结尾"
                        )

        # 规则 7-3：政策动态必填字段 + 语句完整性 + 截断检测
        policy = data.get("政策动态", {})
        for region, items in policy.items():
            if not isinstance(items, list):
                continue
            for i, item in enumerate(items):
                if not isinstance(item, dict):
                    continue
                for field in self.POLICY_REQUIRED_FIELDS:
                    v = item.get(field)
                    if not v:
                        result.fail(
                            rule="语句完整性",
                            category=f"政策动态.{region}",
                            key=f"[{i}].{field}",
                            value=None,
                            message=f"政策动态 [{i}] 缺少必填字段 {field}"
                        )
                    elif not _is_complete_sentence(str(v)):
                        result.fail(
                            rule="语句完整性",
                            category=f"政策动态.{region}",
                            key=f"[{i}].{field}",
                            value=str(v)[:60],
                            message=f"{field} 未以完整句号结尾"
                        )

                # 截断检测：政策内容截断 → 严重问题
                content = item.get('内容', '')
                if content and _is_truncated_content(content):
                    result.fail(
                        rule="截断检测",
                        category=f"政策动态.{region}",
                        key=f"[{i}].内容",
                        value=str(content)[:60],
                        message="政策内容在句子中途截断，数据不可用"
                    )

        # 规则 7-4：企业动态必填字段 + 语句完整性 + 截断检测
        enterprise = data.get("企业动态", {})
        for region, items in enterprise.items():
            if not isinstance(items, list):
                continue
            for i, item in enumerate(items):
                if not isinstance(item, dict):
                    continue
                for field in self.ENTERPRISE_REQUIRED_FIELDS:
                    v = item.get(field)
                    if not v:
                        result.fail(
                            rule="语句完整性",
                            category=f"企业动态.{region}",
                            key=f"[{i}].{field}",
                            value=None,
                            message=f"企业动态 [{i}] 缺少必填字段 {field}"
                        )
                    elif not _is_complete_sentence(str(v)):
                        result.fail(
                            rule="语句完整性",
                            category=f"企业动态.{region}",
                            key=f"[{i}].{field}",
                            value=str(v)[:60],
                            message=f"{field} 未以完整句号结尾"
                        )

                # 截断检测：企业事件正文截断 → 严重问题
                event = item.get('事件', '')
                if event and _is_truncated_content(event):
                    result.fail(
                        rule="截断检测",
                        category=f"企业动态.{region}",
                        key=f"[{i}].事件",
                        value=str(event)[:60],
                        message="事件正文在句子中途截断，数据不可用"
                    )

        return result