"""
测试：提示词引擎
"""

import pytest
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.prompt_engine import PromptEngine, STYLE_PRESETS, LAYOUT_PRESETS


class TestPromptEngine:
    """提示词引擎测试"""
    
    def test_generate_cover_prompt(self):
        """测试封面图提示词"""
        article = {
            "title": "AI时代读代码的正确姿势",
            "sections": [
                {"title": "第一章", "content": "内容一"},
                {"title": "第二章", "content": "内容二"}
            ],
            "summary": "测试"
        }
        
        prompt = PromptEngine.generate_cover_prompt(article, "notion")
        
        # 验证包含标题
        assert "AI时代读代码的正确姿势" in prompt
        # 验证包含风格关键词
        assert "notion" in prompt.lower() or "极简" in prompt or "手绘" in prompt
        # 验证包含章节要点
        assert "第一章" in prompt or "第二章" in prompt
    
    def test_generate_illustration_prompt(self):
        """测试插图提示词"""
        article = {
            "title": "安装XX软件",
            "sections": [
                {"title": "步骤1", "content": "下载"},
                {"title": "步骤2", "content": "安装"}
            ],
            "summary": "测试"
        }
        
        prompt = PromptEngine.generate_illustration_prompt(article, "notion", "flow")
        
        # 验证包含章节内容
        assert "步骤1" in prompt or "Point 1" in prompt
        # 验证包含布局关键词
        assert "flow" in prompt.lower() or "Flow" in prompt or "流程" in prompt
    
    def test_generate_decoration_prompt(self):
        """测试配图提示词"""
        section = {
            "title": "环境准备",
            "content": "需要安装Python环境"
        }
        
        prompt = PromptEngine.generate_decoration_prompt(section, "cute")
        
        # 验证包含章节内容
        assert "环境准备" in prompt or "Python" in prompt
        # 验证包含风格
        assert "cute" in prompt.lower() or "可爱" in prompt or "卡通" in prompt
    
    def test_all_styles(self):
        """测试所有风格"""
        article = {
            "title": "测试",
            "sections": [
                {"title": "第一章", "content": "内容"}
            ],
            "summary": "测试"
        }
        
        for style in STYLE_PRESETS.keys():
            prompt = PromptEngine.generate_cover_prompt(article, style)
            assert len(prompt) > 0
            assert style in STYLE_PRESETS
    
    def test_all_layouts(self):
        """测试所有布局"""
        article = {
            "title": "测试",
            "sections": [
                {"title": "第一步", "content": "下载"},
                {"title": "第二步", "content": "安装"}
            ],
            "summary": "测试"
        }
        
        for layout in LAYOUT_PRESETS.keys():
            prompt = PromptEngine.generate_illustration_prompt(article, "notion", layout)
            assert len(prompt) > 0
    
    def test_select_random_sections(self):
        """测试随机选择章节"""
        sections = [
            {"title": "第一章", "content": "内容1"},
            {"title": "第二章", "content": "内容2"},
            {"title": "第三章", "content": "内容3"}
        ]
        
        # 测试选择数量大于章节数
        selected = PromptEngine.select_random_sections(sections, 5)
        assert len(selected) == 5
        
        # 测试选择数量小于章节数
        selected = PromptEngine.select_random_sections(sections, 2)
        assert len(selected) == 2


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
