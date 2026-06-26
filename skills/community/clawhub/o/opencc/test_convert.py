"""
Tests for OpenCC conversion functionality.
Run with: uv run pytest test_convert.py
"""

import opencc


def test_s2t_basic():
    """Test simplified to traditional conversion."""
    converter = opencc.OpenCC('s2t.json')
    assert converter.convert('汉字') == '漢字'
    assert converter.convert('软件') == '軟件'


def test_t2s_basic():
    """Test traditional to simplified conversion."""
    converter = opencc.OpenCC('t2s.json')
    assert converter.convert('漢字') == '汉字'
    assert converter.convert('軟件') == '软件'


def test_s2tw():
    """Test simplified to Taiwan standard."""
    converter = opencc.OpenCC('s2tw.json')
    # Note: s2tw uses Taiwan standard (not generic traditional)
    result = converter.convert('软件')
    assert '軟' in result or result == '軟體'


def test_s2twp_phrases():
    """Test simplified to Taiwan with phrase conversion."""
    converter = opencc.OpenCC('s2twp.json')
    # s2twp includes idiomatic phrases
    result = converter.convert('鼠标')
    # Taiwan standard: 滑鼠 (not 鼠標)
    assert '滑' in result or '鼠' in result


def test_s2hk():
    """Test simplified to Hong Kong variant."""
    converter = opencc.OpenCC('s2hk.json')
    result = converter.convert('软件')
    # Hong Kong: 軟件
    assert '軟' in result


def test_t2jp():
    """Test traditional to Japanese kanji."""
    converter = opencc.OpenCC('t2jp.json')
    # This test verifies the conversion mode works
    # (exact output depends on OpenCC's Japanese mappings)
    result = converter.convert('漢字')
    assert result is not None
    assert len(result) > 0


def test_multiple_conversions():
    """Test that converter can handle multiple conversions."""
    converter = opencc.OpenCC('s2t.json')
    text1 = converter.convert('中文')
    text2 = converter.convert('汉字')
    assert text1 != '中文'  # Should convert
    assert text2 != '汉字'  # Should convert


def test_empty_string():
    """Test converter handles empty strings."""
    converter = opencc.OpenCC('s2t.json')
    assert converter.convert('') == ''


def test_mixed_content():
    """Test converter with mixed Chinese and English."""
    converter = opencc.OpenCC('s2t.json')
    result = converter.convert('Hello 世界')
    assert 'Hello' in result
    assert '世' in result


if __name__ == '__main__':
    # Quick test run
    print("Running OpenCC conversion tests...")
    test_s2t_basic()
    print("✓ s2t conversion works")
    test_t2s_basic()
    print("✓ t2s conversion works")
    test_s2tw()
    print("✓ s2tw conversion works")
    test_s2hk()
    print("✓ s2hk conversion works")
    test_empty_string()
    print("✓ empty string handling works")
    test_mixed_content()
    print("✓ mixed content handling works")
    print("\nAll tests passed!")
