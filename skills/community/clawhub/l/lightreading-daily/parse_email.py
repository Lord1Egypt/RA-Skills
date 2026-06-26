# -*- coding: utf-8 -*-
"""
从 Light Reading 邮件中提取文章内容
"""

import os
import re
from html.parser import HTMLParser

class EmailContentExtractor(HTMLParser):
    """提取邮件中的正文内容"""
    
    def __init__(self):
        super().__init__()
        self.in_article = False
        self.in_paragraph = False
        self.in_title = False
        self.content = []
        self.current_text = ''
        self.skip_tags = {'script', 'style', 'nav', 'header', 'footer', 'aside'}
        self.in_skip = False
    
    def handle_starttag(self, tag, attrs):
        attrs_dict = dict(attrs)
        
        if tag in self.skip_tags:
            self.in_skip = True
            return
        
        if self.in_skip:
            return
        
        # 检查是否是文章相关内容
        class_attr = attrs_dict.get('class', '').lower()
        id_attr = attrs_dict.get('id', '').lower()
        
        # 常见的文章容器 class
        if any(x in class_attr for x in ['article', 'content', 'body', 'post', 'entry']):
            self.in_article = True
        
        if tag in ['p', 'div'] and self.in_article:
            self.in_paragraph = True
            self.current_text = ''
        
        if tag in ['h1', 'h2', 'h3', 'title']:
            self.in_title = True
            self.current_text = ''
    
    def handle_endtag(self, tag):
        if tag in self.skip_tags:
            self.in_skip = False
            return
        
        if self.in_skip:
            return
        
        if self.in_paragraph and tag in ['p', 'div']:
            text = self.current_text.strip()
            if len(text) > 30:
                self.content.append(text)
            self.in_paragraph = False
            self.current_text = ''
        
        if tag in ['h1', 'h2', 'h3', 'title']:
            self.in_title = False
    
    def handle_data(self, data):
        if self.in_skip:
            return
        if self.in_paragraph or self.in_title:
            self.current_text += data
    
    def get_content(self):
        return self.content


def extract_article_from_email(html_content):
    """从邮件 HTML 中提取文章正文"""
    
    # 移除注释
    html_content = re.sub(r'<!--.*?-->', '', html_content, flags=re.DOTALL)
    
    # 提取所有 <h3> 标题和对应的段落
    articles = []
    
    # 匹配文章项：标题 + 摘要
    pattern = r'<h3[^>]*>.*?<a[^>]*class="linked-header"[^>]*>([^<]+)</a>.*?</h3>.*?<table[^>]*class="spacer[^>]*>.*?</table>([^<]+)'
    matches = re.findall(pattern, html_content, re.DOTALL | re.IGNORECASE)
    
    for title, summary in matches:
        title = re.sub(r'\s+', ' ', title).strip()
        summary = re.sub(r'\s+', ' ', summary).strip()
        summary = re.sub(r'&[a-zA-Z]+;', '', summary)  # 移除 HTML 实体
        if len(summary) > 30:
            articles.append("{} - {}".format(title, summary))
    
    # 如果正则没匹配到，用 HTML 解析器回退
    if not articles:
        extractor = EmailContentExtractor()
        try:
            extractor.feed(html_content)
        except:
            pass
        content = extractor.get_content()
        cleaned = []
        for para in content:
            para = re.sub(r'\s+', ' ', para).strip()
            if len(para) > 50:
                if any(x in para.lower() for x in ['unsubscribe', 'copyright', '©', 'all rights reserved']):
                    continue
                cleaned.append(para)
        return cleaned
    
    return articles


def find_latest_email(emails_dir):
    """找到最新的 Light Reading 邮件"""
    if not os.path.exists(emails_dir):
        return None
    
    files = sorted(os.listdir(emails_dir), reverse=True)
    for f in files:
        if f.endswith('.html') or f.endswith('.eml'):
            return os.path.join(emails_dir, f)
    return None


def get_article_from_email():
    """获取最新邮件中的文章内容"""
    emails_dir = os.path.join(os.path.dirname(__file__), 'emails')
    latest_file = find_latest_email(emails_dir)
    
    if not latest_file:
        print("未找到邮件文件")
        return None
    
    print("读取邮件：{}".format(latest_file))
    
    with open(latest_file, 'r', encoding='utf-8', errors='ignore') as f:
        html = f.read()
    
    paragraphs = extract_article_from_email(html)
    
    if paragraphs:
        print("提取到 {} 段内容".format(len(paragraphs)))
        return ' '.join(paragraphs)
    else:
        print("未能提取到有效内容")
        return None


if __name__ == '__main__':
    content = get_article_from_email()
    if content:
        print("\n=== 文章内容预览 ===")
        print(content[:1000])
