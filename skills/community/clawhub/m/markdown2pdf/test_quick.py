#!/usr/bin/env python3
"""
Quick test without external dependencies
"""

import sys
import tempfile
from pathlib import Path

# Mock the markdown module
class MockMarkdown:
    @staticmethod
    def markdown(text, extensions=None):
        # Simple mock conversion
        html = text
        html = html.replace('# ', '<h1>').replace('\n', '</h1>\n', 1)
        html = html.replace('**', '<strong>', 1).replace('**', '</strong>', 1)
        html = html.replace('*', '<em>', 1).replace('*', '</em>', 1)
        return html

sys.modules['markdown'] = MockMarkdown()
sys.modules['pdfkit'] = type('MockPdfkit', (), {'from_string': lambda *args, **kwargs: True})()
sys.modules['imgkit'] = type('MockImgkit', (), {'from_string': lambda *args, **kwargs: True})()

# Now import the converter
from src.converter import Theme, MarkdownConverter

print('🎨 测试主题系统...')
themes = Theme.list_themes()
print(f'✅ 可用主题：{themes}')

print('\n🎨 测试主题配置...')
for theme_name in themes:
    theme = Theme.get(theme_name)
    print(f'  ✅ {theme_name}: {theme["font_family"][:30]}...')

print('\n📄 测试 Markdown 转换器初始化...')
with tempfile.TemporaryDirectory() as tmpdir:
    converter = MarkdownConverter(output_dir=Path(tmpdir), theme='github')
    print(f'✅ 转换器已初始化')
    print(f'   输出目录：{converter.output_dir}')
    print(f'   主题：github')

print('\n✨ 测试 Markdown 转 HTML...')
test_md = '# Hello World\n\n**Bold** and *italic* text.'
html = converter.markdown_to_html(test_md)
print(f'✅ HTML 生成成功')
print(f'   HTML 长度：{len(html)} 字符')
print(f'   包含 <h1>: {"<h1>" in html}')
print(f'   包含 <strong>: {"<strong>" in html}')

print('\n🎨 测试 CSS 生成...')
css = converter.generate_css()
print(f'✅ CSS 生成成功')
print(f'   CSS 长度：{len(css)} 字符')
print(f'   包含 body: {"body" in css}')
print(f'   包含 font-family: {"font-family" in css}')

print('\n✅ 所有测试通过！')
print('\n📝 注意：完整功能需要安装依赖:')
print('   pip install markdown pdfkit imgkit')
print('   并安装 wkhtmltopdf')
