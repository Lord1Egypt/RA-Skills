"""
law_checker.py 单元测试
覆盖：法条提取、本地验证、中文数字转换、模糊匹配
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))

from law_checker import (
    extract_law_refs,
    _cn_to_arabic,
    _fuzzy_match_law,
    _local_validate,
    check_law_references,
    LawRef,
    LOCAL_LAWS,
    LOCAL_JUDICIAL,
    REPEALED,
)
from fixtures import SIMPLE_LOAN_CASE, SAMPLE_VERDICT


# ════════════════════════════════════════════════════════
# 中文数字转换
# ════════════════════════════════════════════════════════
class TestCnToArabic:
    def test_simple_numbers(self):
        assert _cn_to_arabic("一") == "1"
        assert _cn_to_arabic("十") == "10"
        assert _cn_to_arabic("百") == "100"

    def test_compound_numbers(self):
        assert _cn_to_arabic("十五") == "15"
        assert _cn_to_arabic("二十") == "20"
        assert _cn_to_arabic("六十六") == "66"
        assert _cn_to_arabic("一百") == "100"
        assert _cn_to_arabic("一千") == "1000"

    def test_complex_numbers(self):
        assert _cn_to_arabic("一千二百六十") == "1260"
        assert _cn_to_arabic("二万") == "20000"

    def test_passthrough_arabic(self):
        assert _cn_to_arabic("667") == "667"
        assert _cn_to_arabic("12") == "12"

    def test_empty_and_none(self):
        assert _cn_to_arabic("") == ""
        assert _cn_to_arabic(None) is None


# ════════════════════════════════════════════════════════
# 法条引用提取
# ════════════════════════════════════════════════════════
class TestExtractLawRefs:
    def test_basic_extract(self):
        text = "根据《中华人民共和国民法典》第六百六十七条之规定"
        refs = extract_law_refs(text)
        assert len(refs) >= 1
        ref = refs[0]
        assert "民法典" in ref.law_name
        assert ref.article_num == "667"

    def test_arabic_article(self):
        text = "依照《民事诉讼法》第264条"
        refs = extract_law_refs(text)
        assert len(refs) >= 1
        assert refs[0].article_num == "264"

    def test_multiple_refs(self):
        text = "根据《民法典》第六百六十七条、《民事诉讼法》第二百六十四条"
        refs = extract_law_refs(text)
        assert len(refs) >= 2

    def test_no_refs(self):
        text = "本案事实清楚，证据充分"
        refs = extract_law_refs(text)
        assert len(refs) == 0

    def test_skip_court_names(self):
        text = "本院认为应当适用法律"
        refs = extract_law_refs(text)
        # "本院" 开头的不应被匹配
        assert all("本院" not in r.law_name for r in refs)

    def test_amendment_pattern(self):
        text = "《民间借贷规定》（2020年第二次修正）第二十五条"
        refs = extract_law_refs(text)
        assert len(refs) >= 1
        assert "民间借贷规定" in refs[0].law_name
        assert refs[0].article_num == "25"

    def test_sample_verdict(self):
        refs = extract_law_refs(SAMPLE_VERDICT)
        assert len(refs) >= 2
        law_names = [r.law_name for r in refs]
        assert any("民法典" in n for n in law_names)


# ════════════════════════════════════════════════════════
# 本地验证
# ════════════════════════════════════════════════════════
class TestLocalValidate:
    def test_valid_law(self):
        ref = LawRef(raw_text="《民法典》第667条", law_name="民法典", article_num="667")
        result = _local_validate(ref)
        assert result is True
        assert ref.is_valid is True
        assert ref.source == "local"
        assert "民法典" in ref.law_name

    def test_full_name_match(self):
        ref = LawRef(raw_text="test", law_name="中华人民共和国民法典", article_num="100")
        result = _local_validate(ref)
        assert result is True
        assert ref.is_valid is True

    def test_article_out_of_range(self):
        ref = LawRef(raw_text="test", law_name="民法典", article_num="9999")
        result = _local_validate(ref)
        assert result is True
        assert ref.is_valid is False
        assert any("越界" in w for w in ref.warnings)

    def test_repealed_law(self):
        ref = LawRef(raw_text="test", law_name="合同法", article_num="10")
        result = _local_validate(ref)
        assert result is True
        assert ref.is_valid is False
        assert any("废止" in w for w in ref.warnings)

    def test_unknown_law(self):
        ref = LawRef(raw_text="test", law_name="某某不存在的法律", article_num="1")
        result = _local_validate(ref)
        assert result is False

    def test_judicial_interpretation(self):
        ref = LawRef(raw_text="test", law_name="民间借贷规定", article_num="25")
        result = _local_validate(ref)
        assert result is True
        assert ref.is_valid is True


# ════════════════════════════════════════════════════════
# 模糊匹配
# ════════════════════════════════════════════════════════
class TestFuzzyMatch:
    def test_exact_match(self):
        candidates = ["民法典", "刑法", "民事诉讼法"]
        match, score = _fuzzy_match_law("民法典", candidates)
        assert match == "民法典"
        assert score == 100

    def test_partial_match(self):
        candidates = ["中华人民共和国民法典", "中华人民共和国刑法"]
        match, score = _fuzzy_match_law("民法典", candidates, threshold=70)
        assert match is not None

    def test_no_match(self):
        candidates = ["民法典", "刑法"]
        match, score = _fuzzy_match_law("完全不相关的名称", candidates, threshold=90)
        assert match is None

    def test_no_false_match_similar_names(self):
        # 确保"合同法"不会误匹配到"劳动合同法"
        ref = LawRef(raw_text="test", law_name="合同法", article_num="10")
        result = _local_validate(ref)
        # 合同法已废止，应被识别为废止法律，不应误匹配到劳动合同法
        assert result is True
        assert ref.is_valid is False
        assert any("废止" in w for w in ref.warnings)
        # 不应匹配到劳动合同法
        assert "劳动合同法" not in ref.law_name


# ════════════════════════════════════════════════════════
# 完整检查流程（不含 API 调用的部分）
# ════════════════════════════════════════════════════════
class TestCheckLawReferences:
    def test_no_refs(self):
        result = check_law_references("本案事实清楚")
        assert result.total_refs == 0
        assert result.score == 50
        assert len(result.warnings) > 0

    def test_with_valid_refs(self):
        text = "根据《中华人民共和国民法典》第六百六十七条之规定，借款合同成立。"
        result = check_law_references(text)
        assert result.total_refs >= 1
        assert result.valid_refs >= 1

    def test_with_repealed_ref(self):
        text = "根据《合同法》第一百零七条之规定"
        result = check_law_references(text)
        assert result.total_refs >= 1
        # 废止法律应被标记
        assert any("废止" in w for w in result.warnings)

    def test_score_range(self):
        result = check_law_references(SAMPLE_VERDICT)
        assert 0 <= result.score <= 100
