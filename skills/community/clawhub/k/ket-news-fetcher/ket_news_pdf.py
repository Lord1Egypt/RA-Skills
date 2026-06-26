#!/usr/bin/env python3
"""
Daily English News PDF - 完整文章 + 全文翻译 + 全部生词
"""

import os
import re
import asyncio
import xml.etree.ElementTree as ET
from datetime import datetime
from fpdf import FPDF

try:
    from requests_html import AsyncHTMLSession
    from bs4 import BeautifulSoup
except ImportError:
    pass

# BBC News RSS
BBC_RSS = "https://feeds.bbci.co.uk/news/rss.xml"

# 中文字体路径
FONT_PATH = "/usr/share/fonts/google-noto-cjk/NotoSansCJK-DemiLight.ttc"

# 缓存翻译结果
TRANS_CACHE = {}


def get_translation(word):
    """获取单词翻译 - 使用Google翻译API"""
    global TRANS_CACHE
    
    if word.lower() in TRANS_CACHE:
        return TRANS_CACHE[word.lower()]
    
    import urllib.request
    import json
    import time
    from urllib.parse import quote
    
    url = f"https://translate.googleapis.com/translate_a/single?client=gtx&sl=en&tl=zh-CN&dt=t&q={quote(word)}"
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=5) as response:
            result = response.read().decode('utf-8')
            data = json.loads(result)
            if data and data[0] and data[0][0]:
                translation = data[0][0][0]
                TRANS_CACHE[word.lower()] = translation
                time.sleep(0.1)
                return translation
    except:
        pass
    return ""


def translate_text(text):
    """翻译整段文章"""
    if not text or len(text) < 3:
        return ""
    
    import urllib.request
    import json
    import time
    from urllib.parse import quote
    
    result = ""
    # 分段翻译，每段200字符
    chunk_size = 200
    for i in range(0, min(len(text), 800), chunk_size):
        chunk = text[i:i+chunk_size]
        encoded = quote(chunk)
        url = f"https://translate.googleapis.com/translate_a/single?client=gtx&sl=en&tl=zh-CN&dt=t&q={encoded}"
        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req, timeout=10) as response:
                data = json.loads(response.read().decode('utf-8'))
                if data and data[0]:
                    for item in data[0]:
                        if item[0]:
                            result += item[0]
            time.sleep(0.2)
        except Exception as e:
            print(f"Translate chunk error: {e}")
            continue
    
    return result


def get_rss_articles(rss_url, count=4):
    try:
        import urllib.request
        req = urllib.request.Request(rss_url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=15) as response:
            content = response.read().decode('utf-8')
        
        root = ET.fromstring(content)
        articles = []
        
        for item in root.findall('.//item')[:count]:
            title = item.find('title')
            link = item.find('link')
            if title is not None and link is not None:
                articles.append({
                    "title": title.text or "No title",
                    "url": link.text or ""
                })
        
        return articles
    except Exception as e:
        print(f"RSS Error: {e}")
        return []


async def fetch_article(url, session):
    try:
        r = await session.get(url, timeout=20)
        await r.html.arender(timeout=20)
        return r.html.html
    except:
        return ""


def extract_text(html):
    """提取文章内容"""
    if not html:
        return []
    
    soup = BeautifulSoup(html, 'html.parser')
    for t in soup(['script', 'style', 'nav', 'header', 'footer', 'aside']):
        t.decompose()
    
    paras = []
    for p in soup.find_all('p'):
        text = p.get_text(strip=True)
        if len(text) > 40:
            paras.append(text)
    
    return paras


def clean_text(text):
    """清理特殊字符"""
    text = text.replace('–', '-').replace('—', '-')
    text = text.replace('‘', "'").replace('’', "'")
    text = text.replace('“', '"').replace('”', '"')
    text = text.replace('…', '...')  # ellipsis
    text = text.replace(' ', ' ')  # non-breaking space
    # Remove any remaining non-ASCII except Chinese
    result = ''
    for c in text:
        if ord(c) < 128 or ord(c) > 0x4e00:
            result += c
        else:
            result += c  # keep Chinese
    return result

def get_all_words(text):
    """获取文章中所有单词"""
    words = re.findall(r'\b[a-zA-Z]+\b', text.lower())
    # 统计并去重
    word_count = {}
    for w in words:
        if len(w) > 2:
            word_count[w] = word_count.get(w, 0) + 1
    
    # 按出现频率排序
    sorted_words = sorted(word_count.items(), key=lambda x: x[1], reverse=True)
    return [w for w, c in sorted_words[:80]]  # 返回前50个最常见的词


def create_pdf(articles, output_path):
    pdf = FPDF()
    pdf.add_page()
    pdf.add_font('Chinese', '', FONT_PATH)
    
    # 标题
    pdf.set_font('Helvetica', 'B', 20)
    pdf.cell(0, 12, 'Daily English News', ln=True, align='C')
    pdf.set_font('Helvetica', '', 11)
    pdf.cell(0, 6, 'Miaosi English Team', ln=True, align='C')
    pdf.set_font('Helvetica', '', 12)
    pdf.cell(0, 8, datetime.now().strftime('%Y-%m-%d'), ln=True, align='C')
    pdf.ln(8)
    
    for i, art in enumerate(articles):
        paras = art.get('paras', [])
        all_words = art.get("all_words", [])[:80]
        
        # 文章标题
        pdf.set_font('Helvetica', 'B', 14)
        pdf.set_text_color(0, 102, 204)
        pdf.cell(0, 8, f"Article {i+1}", ln=True)
        
        pdf.set_font('Helvetica', 'B', 11)
        pdf.set_text_color(0, 0, 0)
        pdf.multi_cell(0, 6, art.get('title', 'N/A'))
        pdf.ln(3)
        
        # 英文原文
        pdf.set_font('Helvetica', '', 10)
        pdf.set_text_color(50, 50, 50)
        
        full_text = '\n\n'.join(paras)
        for para in paras:
            text = clean_text(para.strip())
            if text:
                pdf.multi_cell(0, 5.5, text)
                pdf.ln(1)
        
        pdf.ln(5)
        pdf.ln(6)
        
        # 全部词汇表
        if all_words:
            pdf.set_font('Chinese', '', 11)
            pdf.set_text_color(0, 100, 0)
            pdf.cell(0, 7, f' Vocabulary ({len(all_words)} words)', ln=True)
            
            pdf.set_font('Chinese', '', 9)
            pdf.set_text_color(40, 40, 40)
            
            # 每行显示2个单词
            for j in range(0, len(all_words), 2):
                w1 = all_words[j]
                cn1 = get_translation(w1)
                line = f"{w1} - {cn1}" if cn1 else w1
                
                if j + 1 < len(all_words):
                    w2 = all_words[j + 1]
                    cn2 = get_translation(w2)
                    line += f"  |  {w2} - {cn2}" if cn2 else f"  |  {w2}"
                
                pdf.cell(0, 5, line, ln=True)
        
        # 分隔线
        pdf.ln(8)
        pdf.set_draw_color(200, 200, 200)
        pdf.line(10, pdf.get_y(), 200, pdf.get_y())
        pdf.ln(10)
    
    pdf.output(output_path)
    return True


async def main():
    pdf_output = '/tmp/daily_english_news.pdf'
    
    print("="*50)
    print("Daily English News PDF Generator")
    print("="*50)
    
    session = AsyncHTMLSession()
    
    print("\nFetching BBC News RSS...")
    articles = get_rss_articles(BBC_RSS, count=4)
    print(f"Found {len(articles)} articles")
    
    all_articles = []
    
    for i, art in enumerate(articles):
        print(f"\n[{i+1}] {art['title'][:50]}...")
        html = await fetch_article(art['url'], session)
        paras = extract_text(html)
        
        if paras:
            text = ' '.join(paras)
            all_words = get_all_words(text)
            art['paras'] = paras
            art['all_words'] = all_words
            
            # 翻译文章
            
            all_articles.append(art)
            print(f"    OK: {len(all_words)} words")
    
    if not all_articles:
        print("No articles!")
        return
    
    print(f"\nGenerating PDF...")
    print(f"Translation cache: {len(TRANS_CACHE)} words")
    
    if create_pdf(all_articles, pdf_output):
        print(f"PDF: {pdf_output}")
        dest = "/root/.openclaw/workspace-explodegao/english-audio/daily_english_news.pdf"
        import shutil
        shutil.copy(pdf_output, dest)
        print(f"Copied to: {dest}")


if __name__ == "__main__":
    asyncio.run(main())
