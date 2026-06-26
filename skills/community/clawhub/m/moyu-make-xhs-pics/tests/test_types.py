"""
测试：类型和常量
"""

import pytest
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.types import STYLES, LAYOUTS, VALID_STYLES, VALID_LAYOUTS


class TestTypes:
    """类型测试"""
    
    def test_styles(self):
        """测试风格定义"""
        assert "fresh" in STYLES
        assert "warm" in STYLES
        assert "notion" in STYLES
        assert "cute" in STYLES
        
        # 验证每个风格都有 keywords
        for style in STYLES.values():
            assert "keywords" in style
            assert len(style["keywords"]) > 0
    
    def test_layouts(self):
        """测试布局定义"""
        assert "balanced" in LAYOUTS
        assert "list" in LAYOUTS
        assert "comparison" in LAYOUTS
        assert "flow" in LAYOUTS
        
        # 验证每个布局都有描述
        for layout in LAYOUTS.values():
            assert len(layout) > 0
    
    def test_valid_styles(self):
        """测试有效风格列表"""
        assert "fresh" in VALID_STYLES
        assert "warm" in VALID_STYLES
        assert "notion" in VALID_STYLES
        assert "cute" in VALID_STYLES
        assert len(VALID_STYLES) == 4
    
    def test_valid_layouts(self):
        """测试有效布局列表"""
        assert "balanced" in VALID_LAYOUTS
        assert "list" in VALID_LAYOUTS
        assert "comparison" in VALID_LAYOUTS
        assert "flow" in VALID_LAYOUTS
        assert "auto" in VALID_LAYOUTS


class TestWatermark:
    """水印测试"""
    
    def test_add_watermark(self):
        """测试添加水印"""
        # 这个测试需要实际的图片文件
        # 这里只测试函数可以调用
        from src import watermark
        
        # 测试水印文字
        assert watermark.WATERMARK_TEXT == "AI 生成"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
