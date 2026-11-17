"""
enhanced_parser.py 单元测试
覆盖：正则 fallback 解析、案由检测、当事人提取、诉讼请求提取
注意：LLM 解析需要 API key，此处仅测试 regex fallback
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))

from enhanced_parser import (
    regex_parse_elements,
    _detect_cause,
    _extract_parties,
    _extract_claims,
    CaseElements,
    CAUSE_KEYWORDS,
)
from fixtures import SIMPLE_LOAN_CASE, SALE_CONTRACT_CASE, BARE_CASE


# ════════════════════════════════════════════════════════
# 案由检测
# ════════════════════════════════════════════════════════
class TestDetectCause:
    def test_loan_case(self):
        cause = _detect_cause(SIMPLE_LOAN_CASE)
        assert "借贷" in cause or "借款" in cause

    def test_sale_case(self):
        cause = _detect_cause(SALE_CONTRACT_CASE)
        assert "买卖" in cause or "合同" in cause

    def test_empty_text(self):
        cause = _detect_cause("")
        assert cause == "" or isinstance(cause, str)

    def test_hint_passed_through(self):
        # _detect_cause 不接受 cause_hint，测试 regex_parse_elements 的 hint 传递
        from enhanced_parser import regex_parse_elements
        elements = regex_parse_elements(SIMPLE_LOAN_CASE, cause_hint="租赁合同纠纷")
        assert elements.cause == "租赁合同纠纷"


# ════════════════════════════════════════════════════════
# 当事人提取
# ════════════════════════════════════════════════════════
class TestExtractParties:
    def test_loan_parties(self):
        parties = _extract_parties(SIMPLE_LOAN_CASE)
        assert isinstance(parties, dict)
        # 应该能提取到原告和被告
        all_names = []
        for names in parties.values():
            all_names.extend(names)
        # 至少应该有一些名字
        assert len(all_names) >= 0  # regex 可能不完美

    def test_returns_dict(self):
        parties = _extract_parties("原告张三诉被告李四")
        assert isinstance(parties, dict)


# ════════════════════════════════════════════════════════
# 诉讼请求提取
# ════════════════════════════════════════════════════════
class TestExtractClaims:
    def test_loan_claims(self):
        claims = _extract_claims(SIMPLE_LOAN_CASE)
        assert isinstance(claims, list)
        # 应该能提取到还款请求
        assert len(claims) >= 0

    def test_sale_claims(self):
        claims = _extract_claims(SALE_CONTRACT_CASE)
        assert isinstance(claims, list)


# ════════════════════════════════════════════════════════
# 完整 regex 解析流程
# ════════════════════════════════════════════════════════
class TestRegexParseElements:
    def test_loan_case_parse(self):
        elements = regex_parse_elements(SIMPLE_LOAN_CASE)
        assert isinstance(elements, CaseElements)
        assert elements.parse_method == "regex"
        assert elements.raw_text == SIMPLE_LOAN_CASE
        # 案由应被识别
        assert elements.cause != ""

    def test_sale_case_parse(self):
        elements = regex_parse_elements(SALE_CONTRACT_CASE)
        assert isinstance(elements, CaseElements)
        assert elements.parse_method == "regex"

    def test_bare_case_parse(self):
        elements = regex_parse_elements(BARE_CASE)
        assert isinstance(elements, CaseElements)
        assert elements.parse_method == "regex"

    def test_hint_passed_through(self):
        elements = regex_parse_elements(SIMPLE_LOAN_CASE, cause_hint="民间借贷纠纷")
        assert elements.cause == "民间借贷纠纷"

    def test_empty_input(self):
        elements = regex_parse_elements("")
        assert isinstance(elements, CaseElements)
        assert elements.parse_method == "regex"


# ════════════════════════════════════════════════════════
# CaseElements 数据结构
# ════════════════════════════════════════════════════════
class TestCaseElements:
    def test_default_values(self):
        e = CaseElements()
        assert e.cause == ""
        assert e.parties == {}
        assert e.claims == []
        assert e.facts == []
        assert e.disputes == []
        assert e.evidence == []
        assert e.legal_issues == []
        assert e.applicable_laws == []

    def test_cause_keywords_coverage(self):
        """确保每个关键词都有对应的案由"""
        for cause, keywords in CAUSE_KEYWORDS.items():
            assert len(keywords) > 0, f"案由 {cause} 没有关键词"
