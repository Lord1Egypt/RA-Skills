"""
测试：文章解析
"""

import pytest
import tempfile
from pathlib import Path

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.article_parser import ArticleParser
from src.types import Article


class TestArticleParser:
    """文章解析测试"""
    
    def test_parse_simple_article(self):
        """测试解析简单文章"""
        content = """# 测试标题

这是第一段内容。

## 第一章

这是第一章的内容。

## 第二章

这是第二章的内容。
"""
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False) as f:
            f.write(content)
            f.flush()
            
            article = ArticleParser.parse(f.name)
            
            # 验证标题
            assert article["title"] == "测试标题"
            
            # 验证章节数
            assert len(article["sections"]) >= 1
            
            Path(f.name).unlink()
    
    def test_parse_no_title(self):
        """测试解析无标题文章"""
        content = """这是第一段内容。

## 第一章

这是第一章的内容。
"""
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False) as f:
            f.write(content)
            f.flush()
            
            article = ArticleParser.parse(f.name)
            
            # 应该有默认标题
            assert article["title"] != ""
            
            Path(f.name).unlink()
    
    def test_extract_all_content(self):
        """测试提取全部内容"""
        article = {
            "title": "测试标题",
            "sections": [
                {"title": "第一章", "content": "内容一"},
                {"title": "第二章", "content": "内容二"}
            ],
            "summary": "测试"
        }
        
        content = ArticleParser.extract_all_content(article)
        
        assert "测试标题" in content
        assert "第一章" in content
        assert "内容一" in content
    
    def test_get_plain_text(self):
        """测试去除 Markdown 语法"""
        md = """# 标题

这是**加粗**文本，这是[链接](http://example.com)。

```python
print("hello")
```
"""
        
        text = ArticleParser.get_plain_text(md)
        
        assert "#" not in text
        assert "**" not in text
        assert "[" not in text
        assert "```" not in text


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
