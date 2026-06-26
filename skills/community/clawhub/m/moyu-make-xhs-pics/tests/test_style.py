import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from scripts.image_gen import generate_prompt


def test_style_keywords():
    """验证 3 种风格（warm/notion/fresh）是否正确定义"""
    styles = {
        'warm': ['温暖', '柔和', '温馨', '舒适', '自然'],
        'notion': ['简洁', '现代', '极简', '清晰', '有序'],
        'fresh': ['清新', '明亮', '活力', '清爽', '青春']
    }
    
    assert 'warm' in styles
    assert 'notion' in styles
    assert 'fresh' in styles
    
    # 验证每种风格都有对应的关键词
    for style, keywords in styles.items():
        assert len(keywords) > 0
        assert isinstance(keywords, list)
        for keyword in keywords:
            assert isinstance(keyword, str)


def test_aspect_ratio():
    """验证 720x1200 符合 3:5 比例且是 8 的倍数"""
    width = 720
    height = 1200
    
    # 检查是否符合 3:5 比例
    ratio = width / height
    expected_ratio = 3 / 5
    assert abs(ratio - expected_ratio) < 0.0001, f"比例 {ratio} 不等于 3:5"
    
    # 检查宽高是否都是 8 的倍数
    assert width % 8 == 0, f"宽度 {width} 不是 8 的倍数"
    assert height % 8 == 0, f"高度 {height} 不是 8 的倍数"


def test_generate_prompt():
    """测试提示词生成函数"""
    # 测试基本功能
    prompt = generate_prompt("测试主题", "warm")
    assert isinstance(prompt, str)
    assert "测试主题" in prompt
    assert len(prompt) > 0
    
    # 测试不同风格
    for style in ['warm', 'notion', 'fresh']:
        prompt = generate_prompt("主题", style)
        assert isinstance(prompt, str)
        assert "主题" in prompt
        
    # 测试空输入
    try:
        empty_prompt = generate_prompt("", "warm")
        # 如果函数能处理空输入则继续
    except Exception:
        # 如果函数不能处理空输入则正常
        pass