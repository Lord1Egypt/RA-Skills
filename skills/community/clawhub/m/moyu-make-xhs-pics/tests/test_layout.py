"""
测试：布局选择器
"""

import pytest
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.layout_selector import LayoutSelector


class TestLayoutSelector:
    """布局选择器测试"""
    
    def test_auto_select_comparison(self):
        """测试自动选择对比布局"""
        article = {
            "title": "对比测试",
            "sections": [
                {"title": "比较", "content": "A和B的差异是什么"}
            ],
            "summary": "测试"
        }
        
        layout = LayoutSelector.auto_select(article)
        assert layout == "comparison"
    
    def test_auto_select_flow(self):
        """测试自动选择流程布局"""
        article = {
            "title": "安装教程",
            "sections": [
                {"title": "步骤", "content": "首先下载，然后安装，接着配置，最后运行"}
            ],
            "summary": "测试"
        }
        
        layout = LayoutSelector.auto_select(article)
        assert layout == "flow"
    
    def test_auto_select_list(self):
        """测试自动选择列表布局"""
        article = {
            "title": "要点总结",
            "sections": [
                {"title": "要点", "content": "1. 第一点 2. 第二点 3. 第三点"}
            ],
            "summary": "测试"
        }
        
        layout = LayoutSelector.auto_select(article)
        assert layout == "list"
    
    def test_auto_select_default(self):
        """测试默认布局"""
        article = {
            "title": "普通文章",
            "sections": [
                {"title": "内容", "content": "这是一段普通的内容"}
            ],
            "summary": "测试"
        }
        
        layout = LayoutSelector.auto_select(article)
        assert layout == "balanced"
    
    def test_is_valid_layout(self):
        """测试布局验证"""
        assert LayoutSelector.is_valid_layout("balanced")
        assert LayoutSelector.is_valid_layout("list")
        assert LayoutSelector.is_valid_layout("comparison")
        assert LayoutSelector.is_valid_layout("flow")
        assert LayoutSelector.is_valid_layout("auto")
        assert not LayoutSelector.is_valid_layout("invalid")
    
    def test_resolve_layout(self):
        """测试布局解析"""
        article = {
            "title": "测试",
            "sections": [{"title": "A", "content": "内容"}],
            "summary": "测试"
        }
        
        # auto 应该解析为具体布局
        layout = LayoutSelector.resolve_layout("auto", article)
        assert layout in ["balanced", "list", "comparison", "flow"]
        
        # 其他直接返回
        layout = LayoutSelector.resolve_layout("list", article)
        assert layout == "list"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
