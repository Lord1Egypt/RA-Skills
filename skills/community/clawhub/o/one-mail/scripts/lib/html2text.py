#!/usr/bin/env python3
"""
one-mail HTML 邮件正文提取工具
将 HTML 邮件转换为干净的可读文本
"""

import sys
import re
from html.parser import HTMLParser
from html import unescape


class EmailTextExtractor(HTMLParser):
    """从 HTML 邮件中提取干净的可读文本"""

    # 不输出内容的标签
    SKIP_TAGS = {'style', 'script', 'head', 'meta', 'link', 'title'}

    # 块级标签（前后加换行）
    BLOCK_TAGS = {
        'p', 'div', 'br', 'hr', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6',
        'li', 'tr', 'td', 'th', 'blockquote', 'pre', 'section',
        'article', 'header', 'footer', 'nav', 'table'
    }

    # 标题标签（加粗标记）
    HEADING_TAGS = {'h1', 'h2', 'h3', 'h4', 'h5', 'h6'}

    def __init__(self):
        super().__init__()
        self.result = []
        self.skip_depth = 0
        self.tag_stack = []
        self.in_link = False
        self.link_href = ''
        self.link_text = ''
        self.in_list = False
        self.list_type = None  # 'ul' or 'ol'
        self.list_counter = 0

    def handle_starttag(self, tag, attrs):
        tag = tag.lower()
        self.tag_stack.append(tag)
        attrs_dict = dict(attrs)

        # 跳过隐藏元素
        style = attrs_dict.get('style', '')
        if 'display:none' in style.replace(' ', '') or 'visibility:hidden' in style.replace(' ', ''):
            self.skip_depth += 1
            return

        if tag in self.SKIP_TAGS:
            self.skip_depth += 1
            return

        if self.skip_depth > 0:
            return

        # 块级标签加换行
        if tag in self.BLOCK_TAGS:
            self.result.append('\n')

        # 标题加标记
        if tag in self.HEADING_TAGS:
            self.result.append('\n## ')

        # 链接
        if tag == 'a':
            self.in_link = True
            self.link_href = attrs_dict.get('href', '')
            self.link_text = ''

        # 列表
        if tag == 'ul':
            self.in_list = True
            self.list_type = 'ul'
            self.result.append('\n')
        elif tag == 'ol':
            self.in_list = True
            self.list_type = 'ol'
            self.list_counter = 0
            self.result.append('\n')
        elif tag == 'li':
            if self.list_type == 'ol':
                self.list_counter += 1
                self.result.append(f'\n{self.list_counter}. ')
            else:
                self.result.append('\n• ')

        # 换行
        if tag == 'br':
            self.result.append('\n')

        # 分隔线
        if tag == 'hr':
            self.result.append('\n---\n')

        # 图片 alt 文本
        if tag == 'img':
            alt = attrs_dict.get('alt', '')
            if alt and alt.strip():
                self.result.append(f'[图片: {alt.strip()}]')

    def handle_endtag(self, tag):
        tag = tag.lower()

        if self.tag_stack and self.tag_stack[-1] == tag:
            self.tag_stack.pop()

        if tag in self.SKIP_TAGS:
            self.skip_depth = max(0, self.skip_depth - 1)
            return

        # 隐藏元素结束
        if self.skip_depth > 0:
            style_hidden = False  # 简化处理
            self.skip_depth = max(0, self.skip_depth - 1)
            return

        # 块级标签加换行
        if tag in self.BLOCK_TAGS:
            self.result.append('\n')

        # 标题结束
        if tag in self.HEADING_TAGS:
            self.result.append('\n')

        # 链接结束
        if tag == 'a' and self.in_link:
            self.in_link = False
            text = self.link_text.strip()
            href = self.link_href.strip()
            # 跳过无意义的链接
            if href and not href.startswith('#') and not href.startswith('mailto:'):
                if text and text != href:
                    # 文本和链接不同，都显示
                    pass  # 文本已经在 handle_data 中添加
                elif not text:
                    self.result.append(href)
            self.link_href = ''
            self.link_text = ''

        # 列表结束
        if tag in ('ul', 'ol'):
            self.in_list = False
            self.list_type = None
            self.result.append('\n')

    def handle_data(self, data):
        if self.skip_depth > 0:
            return

        text = data

        if self.in_link:
            self.link_text += text

        self.result.append(text)

    def handle_entityref(self, name):
        try:
            char = unescape(f'&{name};')
            self.result.append(char)
        except:
            pass

    def handle_charref(self, name):
        try:
            char = unescape(f'&#{name};')
            self.result.append(char)
        except:
            pass

    def get_text(self):
        raw = ''.join(self.result)
        return self._clean_text(raw)

    def _clean_text(self, text):
        """清理提取的文本"""
        # 移除零宽字符和不可见字符
        text = re.sub(r'[\u200b\u200c\u200d\u200e\u200f\ufeff\u034f]', '', text)
        text = re.sub(r'[\u2800-\u28ff]', '', text)  # 盲文字符（常用于占位）
        text = re.sub(r'͏', '', text)  # 组合用字符

        # 合并多个空格为一个
        text = re.sub(r'[^\S\n]+', ' ', text)

        # 合并多个空行为最多两个
        text = re.sub(r'\n\s*\n\s*\n+', '\n\n', text)

        # 去除每行首尾空格
        lines = [line.strip() for line in text.split('\n')]

        # 过滤纯空白行（保留空行作为段落分隔）
        cleaned = []
        prev_empty = False
        for line in lines:
            if not line:
                if not prev_empty:
                    cleaned.append('')
                    prev_empty = True
            else:
                cleaned.append(line)
                prev_empty = False

        text = '\n'.join(cleaned).strip()
        return text


def extract_text(html_content):
    """从 HTML 内容提取干净文本"""
    extractor = EmailTextExtractor()
    extractor.feed(html_content)
    return extractor.get_text()


def main():
    if len(sys.argv) > 1:
        # 从文件读取
        with open(sys.argv[1], 'r', encoding='utf-8') as f:
            html = f.read()
    else:
        # 从 stdin 读取
        html = sys.stdin.read()

    text = extract_text(html)
    print(text)


if __name__ == '__main__':
    main()
