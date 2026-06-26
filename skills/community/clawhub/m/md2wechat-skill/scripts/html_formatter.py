"""
HTML 内联样式适配器 — 微信公众号兼容

将原始 HTML 转换为仅包含内联 CSS 的微信图文编辑器兼容格式。
微信不支持 <style> 标签、class/id 属性，所有样式必须写在元素的 style 属性中。
"""

import re
from bs4 import BeautifulSoup, NavigableString, Tag


class HTMLFormatter:
    """负责将 HTML 转换为微信公众号兼容的格式，主要处理 CSS 内联化"""

    # 列表项的内联样式（用 section/p 模拟列表）
    LIST_ITEM_STYLE = 'font-size: 16px; line-height: 1.75; margin-bottom: 0.5em; color: #3f3f3f; padding-left: 2em; text-indent: -1.5em;'
    LIST_WRAPPER_STYLE = 'margin-bottom: 1em;'

    # 微信允许的基本安全样式
    STYLES = {
        'h1': 'font-size: 22px; font-weight: bold; margin-bottom: 1em; margin-top: 1.5em; border-bottom: 2px solid #eee; padding-bottom: 5px; color: #333;',
        'h2': 'font-size: 20px; font-weight: bold; margin-bottom: 0.8em; margin-top: 1.2em; color: #444;',
        'h3': 'font-size: 18px; font-weight: bold; margin-bottom: 0.6em; margin-top: 1em; color: #555;',
        'p': 'font-size: 16px; line-height: 1.75; margin-bottom: 1em; color: #3f3f3f;',
        'strong': 'font-weight: bold; color: #1a1a1a;',
        'em': 'font-style: italic; color: #666;',
        'blockquote': 'border-left: 4px solid #cbcbcb; padding: 10px 15px; margin: 15px 0; background-color: #f8f8f8; color: #666;',
        'a': 'color: #576b95; text-decoration: none;',
        'pre': 'background-color: #282c34; padding: 15px; border-radius: 6px; overflow-x: auto; max-width: 100%; margin: 1.5em 0; white-space: pre; color: #abb2bf; font-family: Consolas, Monaco, "Courier New", monospace; font-size: 14px; line-height: 1.5;',
        'code': 'font-family: Consolas, Monaco, "Courier New", monospace; font-size: 14px; background-color: #f3f4f4; padding: 2px 5px; border-radius: 3px; color: #d14;'
    }

    # 当 code 标签在 pre 标签内部时，使用此特定样式
    PRE_CODE_STYLE = 'font-family: Consolas, Monaco, "Courier New", monospace; font-size: 14px; background-color: transparent; padding: 0; color: inherit;'

    @classmethod
    def _convert_lists_for_wechat(cls, soup):
        """
        将 <ul>/<ol> 及其 <li> 子节点替换为 <section>/<p>，
        使用文本字符 • 或数字序号作为列表标记。
        微信公众号编辑器对原生 <ul>/<ol>/<li> 渲染行为不可控，
        此方法是所有主流微信排版工具的通用方案。
        """
        while True:
            list_tag = soup.find(['ul', 'ol'])
            if not list_tag:
                break

            is_ordered = list_tag.name == 'ol'
            wrapper = soup.new_tag('section')
            wrapper['style'] = cls.LIST_WRAPPER_STYLE

            counter = 0
            for child in list(list_tag.children):
                if isinstance(child, Tag) and child.name == 'li':
                    counter += 1
                    marker = f'{counter}. ' if is_ordered else '• '

                    p = soup.new_tag('p')
                    p['style'] = cls.LIST_ITEM_STYLE

                    p.append(marker)

                    for sub in list(child.children):
                        if isinstance(sub, Tag) and sub.name == 'span' and not sub.get('style'):
                            for inner in list(sub.children):
                                p.append(inner.extract())
                        else:
                            p.append(sub.extract())

                    wrapper.append(p)

            list_tag.replace_with(wrapper)

    @classmethod
    def format_for_wechat(cls, html_content: str) -> str:
        """
        将原始 HTML 转换为只有真实内容和内联 CSS 的微信风格富文本
        """
        if not html_content:
            return ""

        soup = BeautifulSoup(html_content, 'html.parser')

        body = soup.find('body')
        root = body if body else soup

        # 移除内部 style 或 script 标签
        for tag in root.find_all(['style', 'script']):
            tag.decompose()

        # 将 ul/ol/li 转换为 section/p 以绕过微信渲染缺陷
        cls._convert_lists_for_wechat(root)

        # 遍历所有节点应用内联样式
        for tag_name, style in cls.STYLES.items():
            for tag in root.find_all(tag_name):
                existing_style = tag.get('style', '')
                if existing_style and not existing_style.endswith(';'):
                    existing_style += ';'

                if tag_name == 'code' and tag.parent and tag.parent.name == 'pre':
                    tag['style'] = existing_style + ' ' + cls.PRE_CODE_STYLE
                else:
                    tag['style'] = existing_style + ' ' + style

        return ''.join(str(child) for child in root.contents if not isinstance(child, NavigableString) or child.strip())
