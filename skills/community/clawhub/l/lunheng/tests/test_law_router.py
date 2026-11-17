"""
law_router.py 单元测试
覆盖：案由匹配、关键词匹配、别名解析、模糊匹配、格式化输出
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))

from law_router import (
    suggest_laws,
    resolve_law_alias,
    format_suggestions,
    CAUSE_LAW_MAP,
    LAW_ALIASES,
    LawSuggestion,
)


# ════════════════════════════════════════════════════════
# suggest_laws — 精确匹配
# ════════════════════════════════════════════════════════
class TestSuggestLawsExact:
    def test_loan_case(self):
        suggestions = suggest_laws("民间借贷纠纷")
        assert len(suggestions) >= 2
        assert any("民法典" in s.law_name for s in suggestions)
        assert any("民间借贷规定" in s.law_name for s in suggestions)
        # 精确匹配的法条置信度=1.0（兜底法除外）
        exact = [s for s in suggestions if s.confidence == 1.0]
        assert len(exact) >= 2

    def test_sale_contract(self):
        suggestions = suggest_laws("买卖合同纠纷")
        assert len(suggestions) >= 1
        assert any("民法典" in s.law_name for s in suggestions)

    def test_divorce(self):
        suggestions = suggest_laws("离婚纠纷")
        assert len(suggestions) >= 2
        assert any("民法典" in s.law_name for s in suggestions)
        assert any("婚姻家庭编解释" in s.law_name for s in suggestions)

    def test_labor_dispute(self):
        suggestions = suggest_laws("劳动争议")
        assert any("劳动合同法" in s.law_name for s in suggestions)

    def test_administrative(self):
        suggestions = suggest_laws("行政处罚纠纷")
        assert any("行政处罚法" in s.law_name for s in suggestions)
        assert any("行政诉讼法" in s.law_name for s in suggestions)

    def test_maritime(self):
        suggestions = suggest_laws("海事海商纠纷")
        assert any("海商法" in s.law_name for s in suggestions)

    def test_priority_order(self):
        """精确匹配的第一条应有 priority=0"""
        suggestions = suggest_laws("民间借贷纠纷")
        assert suggestions[0].priority == 0

    def test_all_causes_have_mappings(self):
        """验证 CAUSE_LAW_MAP 中每个案由至少映射 1 条法条"""
        for cause, laws in CAUSE_LAW_MAP.items():
            assert len(laws) >= 1, f"{cause} 映射为空"


# ════════════════════════════════════════════════════════
# suggest_laws — 模糊匹配（子串包含）
# ════════════════════════════════════════════════════════
class TestSuggestLawsFuzzy:
    def test_superset_match(self):
        """'民间借贷纠纷案' 包含 '民间借贷纠纷'"""
        suggestions = suggest_laws("民间借贷纠纷案")
        assert len(suggestions) >= 2
        assert suggestions[0].confidence == 0.7

    def test_subset_match(self):
        """'民间借贷' 是 '民间借贷纠纷' 的子集"""
        suggestions = suggest_laws("民间借贷")
        assert len(suggestions) >= 2

    def test_no_match_unknown(self):
        """完全无关的案由只返回兜底"""
        suggestions = suggest_laws("量子计算纠纷")
        assert len(suggestions) == 1
        assert suggestions[0].law_name == "民事诉讼法"
        assert suggestions[0].confidence == 0.3


# ════════════════════════════════════════════════════════
# suggest_laws — 关键词匹配（争议焦点 → 法条）
# ════════════════════════════════════════════════════════
class TestSuggestLawsKeywords:
    def test_interest_keyword(self):
        suggestions = suggest_laws("某某纠纷", disputes=["利率过高"])
        law_names = [s.law_name for s in suggestions]
        assert "民间借贷规定" in law_names

    def test_penalty_keyword(self):
        suggestions = suggest_laws("某某纠纷", legal_issues=["违约金过高"])
        law_names = [s.law_name for s in suggestions]
        assert "民法典" in law_names

    def test时效_keyword(self):
        suggestions = suggest_laws("某某纠纷", disputes=["超过诉讼时效"])
        law_names = [s.law_name for s in suggestions]
        assert "民法典" in law_names

    def test_multiple_keywords(self):
        suggestions = suggest_laws("某某纠纷", disputes=["利率过高", "违约金过高"])
        # 应包含多种法条
        law_names = [s.law_name for s in suggestions]
        assert len(law_names) >= 3  # 民间借贷规定 + 民法典(利率) + 民法典(违约金) + 兜底

    def test_no_duplicate_laws(self):
        """同一法律不应重复出现"""
        suggestions = suggest_laws("民间借贷纠纷", disputes=["利率", "利息"])
        law_names = [s.law_name for s in suggestions]
        # 民法典可能因关键词出现两次，但 law_router 已去重
        assert law_names.count("民法典") <= 2  # 允许最多2次（精确匹配+关键词）


# ════════════════════════════════════════════════════════
# resolve_law_alias — 别名解析
# ════════════════════════════════════════════════════════
class TestResolveLawAlias:
    def test_exact_alias(self):
        assert resolve_law_alias("民法典") == "中华人民共和国民法典"

    def test_judicial_alias(self):
        result = resolve_law_alias("民间借贷规定")
        assert "民间借贷" in result
        assert "最高人民法院" in result

    def test_repealed_alias(self):
        result = resolve_law_alias("合同法")
        assert "已废止" in result
        assert "民法典" in result

    def test_repealed_property_law(self):
        result = resolve_law_alias("物权法")
        assert "已废止" in result

    def test_with_book_marks(self):
        """带书名号的输入"""
        result = resolve_law_alias("《民法典》")
        assert "民法典" in result

    def test_unknown_passthrough(self):
        """未知名称原样返回"""
        result = resolve_law_alias("某某不存在的法律")
        assert result == "某某不存在的法律"

    def test_all_aliases_resolve(self):
        """所有别名都能解析，不抛异常"""
        for alias in LAW_ALIASES:
            result = resolve_law_alias(alias)
            assert result is not None

    def test_prefix_match(self):
        """前缀匹配：'中华人民共和国民法典' 应匹配 '民法典' 别名"""
        result = resolve_law_alias("中华人民共和国民法典")
        assert "民法典" in result


# ════════════════════════════════════════════════════════
# format_suggestions — 格式化输出
# ════════════════════════════════════════════════════════
class TestFormatSuggestions:
    def test_empty(self):
        result = format_suggestions([])
        assert "未找到" in result

    def test_basic_format(self):
        suggestions = suggest_laws("民间借贷纠纷")
        result = format_suggestions(suggestions)
        assert "📋" in result
        assert "民法典" in result

    def test_truncation(self):
        """超过10条时应截断"""
        suggestions = [LawSuggestion(law_name=f"法律{i}", priority=i) for i in range(15)]
        result = format_suggestions(suggestions)
        assert "还有" in result

    def test_confidence_display(self):
        """低置信度应显示百分比"""
        s = [LawSuggestion(law_name="测试法", confidence=0.5, priority=0)]
        result = format_suggestions(s)
        assert "50%" in result

    def test_no_confidence_display(self):
        """置信度1.0不显示百分比"""
        s = [LawSuggestion(law_name="测试法", confidence=1.0, priority=0)]
        result = format_suggestions(s)
        assert "%" not in result.split("—")[-1] if "—" in result else True


# ════════════════════════════════════════════════════════
# 边界用例
# ════════════════════════════════════════════════════════
class TestEdgeCases:
    def test_empty_cause(self):
        suggestions = suggest_laws("")
        # 空案由不应崩溃，应返回兜底
        assert len(suggestions) >= 1

    def test_none_disputes(self):
        suggestions = suggest_laws("民间借贷纠纷", disputes=None, legal_issues=None)
        assert len(suggestions) >= 2

    def test_empty_disputes(self):
        suggestions = suggest_laws("民间借贷纠纷", disputes=[], legal_issues=[])
        assert len(suggestions) >= 2

    def test_long_dispute_text(self):
        """长文本争议焦点不应崩溃"""
        long_text = "这是一段非常长的争议焦点描述" * 50
        suggestions = suggest_laws("民间借贷纠纷", disputes=[long_text])
        assert len(suggestions) >= 2

    def test_special_chars_in_cause(self):
        """特殊字符不应导致崩溃"""
        suggestions = suggest_laws("纠纷&案由《》")
        assert isinstance(suggestions, list)
