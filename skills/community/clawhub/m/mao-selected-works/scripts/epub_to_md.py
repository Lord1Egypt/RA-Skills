#!/usr/bin/env python3
"""EPUB to Markdown converter for 毛泽东选集"""

import os
import re
import shutil
from html.parser import HTMLParser
import xml.etree.ElementTree as ET

EPUB_PATH = "/home/zzgzczq/01-AI/02-openclaw-skills/mao-selected-works/data/毛选1-7卷.epub"
OUTPUT_DIR = "/home/zzgzczq/01-AI/02-openclaw-skills/mao-selected-works/output"
EXTRACT_DIR = "/tmp/epub_convert"

NS = {"ncx": "http://www.daisy.org/z3986/2005/ncx/"}


def extract_epub():
    if os.path.exists(EXTRACT_DIR):
        shutil.rmtree(EXTRACT_DIR)
    os.makedirs(EXTRACT_DIR, exist_ok=True)
    os.system(f'unzip -q "{EPUB_PATH}" -d "{EXTRACT_DIR}"')


def chinese_to_arabic(chinese_num):
    """将中文数字转换为阿拉伯数字"""
    chinese_to_digit = {
        '一': 1, '二': 2, '三': 3, '四': 4, '五': 5,
        '六': 6, '七': 7, '八': 8, '九': 9, '十': 10,
        '十一': 11, '十二': 12, '十三': 13, '十四': 14, '十五': 15,
        '十六': 16, '十七': 17, '十八': 18, '十九': 19, '二十': 20
    }
    if chinese_num in chinese_to_digit:
        return chinese_to_digit[chinese_num]
    elif chinese_num.isdigit():
        return int(chinese_num)
    else:
        return 0  # 默认值

def parse_toc():
    toc_path = os.path.join(EXTRACT_DIR, "OEBPS", "toc.ncx")
    tree = ET.parse(toc_path)
    root = tree.getroot()

    articles = []

    def process_navpoint(navpoint, volume='', depth=0):
        label = navpoint.find("ncx:navLabel/ncx:text", NS)
        content = navpoint.find("ncx:content", NS)
        label_text = label.text.strip() if label is not None else ""

        if content is not None:
            src = content.get("src", "")
            if label_text and src.startswith("Text/Section"):
                if depth == 2:  # 文章节点
                    filename = src.replace("Text/", "").replace(".xhtml", "")
                    # 提取卷号数字
                    volume_num = re.search(r'第([一二三四五六七八九十\d]+)卷', volume)
                    if volume_num:
                        chinese_vol = volume_num.group(1)
                        arabic_vol = chinese_to_arabic(chinese_vol)
                        vol_num = f"{arabic_vol:02d}"  # 转换为两位数的阿拉伯数字
                    else:
                        vol_num = "00"
                    
                    articles.append({
                        "volume": vol_num,
                        "title": label_text,
                        "filename": filename,
                        "src": src,
                    })
            elif depth == 0 and '卷' in label_text:  # 卷节点
                volume = label_text

        for child in navpoint.findall("ncx:navPoint", NS):
            process_navpoint(child, volume, depth + 1)

    for navpoint in root.findall(".//ncx:navPoint", NS):
        is_root_level = True
        for other in root.findall(".//ncx:navPoint", NS):
            if other != navpoint:
                for child in other.findall("ncx:navPoint", NS):
                    if child == navpoint:
                        is_root_level = False
                        break
            if not is_root_level:
                break
        if is_root_level:
            process_navpoint(navpoint, '', 0)

    # 按卷分类，分配文章编号
    volume_articles = {}
    for article in articles:
        vol = article['volume']
        if vol not in volume_articles:
            volume_articles[vol] = []
        volume_articles[vol].append(article)
    
    # 为每卷的文章分配编号
    result = []
    for vol, arts in volume_articles.items():
        for idx, article in enumerate(arts, 1):
            article['article_num'] = idx
            result.append(article)
    
    return result


class EPUBContentParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.md_lines = []
        self.current_text = ""
        self.in_body = False
        self.in_heading = False
        self.in_paragraph = False
        self.heading_level = 0
        self.paragraph_class = ""
        self.footnotes = []
        self.in_footnote = False
        self.footnote_text = ""
        self.footnote_id = None
        self.skip_content = False
        self.depth = 0

    def handle_starttag(self, tag, attrs):
        attrs_dict = dict(attrs)
        class_attr = attrs_dict.get("class", "")

        if tag == "body":
            self.in_body = True
        elif tag == "div" and "footnote" in class_attr:
            self.in_footnote = True
            self.footnote_text = ""
        elif tag == "a" and "zy" in class_attr:
            href = attrs_dict.get("href", "")
            id_attr = attrs_dict.get("id", "")
            if self.in_footnote and id_attr:
                self.footnote_id = id_attr
            elif href:
                match = re.search(r"#id(\d+)a", href)
                if match:
                    num = len(self.footnotes) + 1
                    self.footnotes.append((num, ""))
                    self.current_text += f"[^{num}]"
        elif tag in ("h1", "h2", "h3", "h4", "h5", "h6"):
            self.in_heading = True
            self.heading_level = int(tag[1])
            h_match = re.search(r'h(\d)', class_attr)
            if h_match:
                self.heading_level = int(h_match.group(1))
            self.current_text = ""
        elif tag == "p":
            self.in_paragraph = True
            self.paragraph_class = class_attr
            self.current_text = ""
        elif tag == "br":
            self.current_text += "\n"
        elif tag in ("span", "a", "sup", "sub"):
            pass

    def handle_endtag(self, tag):
        if tag == "body":
            self.in_body = False
        elif tag == "div" and self.in_footnote:
            self.in_footnote = False
            if self.footnote_id and self.footnote_text.strip():
                self.footnotes.append((self.footnote_id, self.footnote_text.strip()))
        elif tag in ("h1", "h2", "h3", "h4", "h5", "h6") and self.in_heading:
            self.in_heading = False
            text = self._clean_text(self.current_text)
            if text:
                if self.heading_level == 3:
                    self.md_lines.append(f"# {text}")
                elif self.heading_level == 4:
                    self.md_lines.append(f"## {text}")
                elif self.heading_level == 5:
                    self.md_lines.append(f"### {text}")
                self.md_lines.append("")
            self.current_text = ""
        elif tag == "p" and self.in_paragraph:
            self.in_paragraph = False
            text = self._clean_text(self.current_text)
            if text:
                if "a5" in self.paragraph_class:
                    self.md_lines.append(f"#### {text}")
                    self.md_lines.append("")
                elif "a0" in self.paragraph_class:
                    self.md_lines.append(f"（{text}）")
                    self.md_lines.append("")
                else:
                    self.md_lines.append(f"  {text}")
                    self.md_lines.append("")
            self.current_text = ""

    def handle_data(self, data):
        if self.in_footnote:
            self.footnote_text += data
        elif self.in_heading or self.in_paragraph:
            self.current_text += data

    def _clean_text(self, text):
        text = re.sub(r'\s+', ' ', text)
        text = text.replace('\u3000', '  ')
        return text.strip()

    def get_markdown(self):
        md_content = "\n".join(self.md_lines)

        if self.footnotes:
            md_content += "\n---\n\n"
            footnote_map = {fid: text for fid, text in self.footnotes if isinstance(fid, str)}
            numbered_footnotes = [(num, text) for num, text in self.footnotes if isinstance(num, int)]
            
            for num, text in numbered_footnotes:
                md_content += f"[^{num}]: {text}\n"

        return md_content


def convert_html_to_md(html_path):
    with open(html_path, "r", encoding="utf-8") as f:
        content = f.read()

    parser = EPUBContentParser()
    parser.feed(content)

    md_content = parser.get_markdown()

    title_match = re.search(r'<title>(.*?)</title>', content)
    title_text = title_match.group(1).strip() if title_match else "未知"

    return title_text, md_content


def main():
    print("正在解压EPUB文件...")
    extract_epub()

    print("正在解析目录结构...")
    articles = parse_toc()
    print(f"找到 {len(articles)} 篇文章")

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    converted = []
    for i, article in enumerate(articles):
        html_path = os.path.join(EXTRACT_DIR, "OEBPS", article["src"])
        if not os.path.exists(html_path):
            print(f"  跳过（文件不存在）: {article['title']}")
            continue

        title, md_content = convert_html_to_md(html_path)
        if md_content:
            # 使用 卷-第几篇-文章名.md 的格式
            filename = f"{article['volume']}-{article['article_num']:02d}-{article['title']}.md"
            output_path = os.path.join(OUTPUT_DIR, filename)
            with open(output_path, "w", encoding="utf-8") as f:
                f.write(md_content)
            converted.append(article["title"])
            print(f"  已转换: {article['title']}")

    print(f"\n转换完成！共转换 {len(converted)} 篇文章")
    print(f"输出目录: {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
