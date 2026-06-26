# -*- coding: utf-8 -*-
"""
科技新闻合并推送脚本 v4.2
整合 LightReading + TechCrunch，优先 Iain Morris 文章
v4.1: 自动检测旧文件并删除重做，避免重复推送
v4.2: 检测 RSS 内容重复时，清除历史记录重新抓取，避免推送相同内容
"""

import cloudscraper
import xml.etree.ElementTree as ET
import json
import http.client
import urllib.parse
import os
import re
from datetime import datetime

WEBHOOK_URL = "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=66260502-9806-45ec-b23e-8db5223a9b27"
LR_RSS_URL = "https://www.lightreading.com/rss.xml"
TC_RSS_URL = "https://techcrunch.com/feed/"
PUSHED_FILE = os.path.join(os.path.dirname(__file__), 'pushed_history.json')

def fetch_lr_rss():
    """获取 LightReading RSS"""
    scraper = cloudscraper.create_scraper()
    try:
        resp = scraper.get(LR_RSS_URL, timeout=60)
        if resp.status_code == 200:
            return resp.text
    except Exception as e:
        print("LightReading RSS 获取失败：{}".format(str(e)[:50]))
    return None

def fetch_tc_rss():
    """获取 TechCrunch RSS"""
    scraper = cloudscraper.create_scraper()
    try:
        resp = scraper.get(TC_RSS_URL, timeout=60)
        if resp.status_code == 200:
            return resp.text
    except Exception as e:
        print("TechCrunch RSS 获取失败：{}".format(str(e)[:50]))
    return None

def parse_rss(xml_content, source=''):
    """解析 RSS feed"""
    articles = []
    try:
        root = ET.fromstring(xml_content.encode('utf-8'))
        
        # 定义命名空间
        namespaces = {
            'dc': 'http://purl.org/dc/elements/1.1/',
            'content': 'http://purl.org/rss/1.0/modules/content/',
            'atom': 'http://www.w3.org/2005/Atom'
        }
        
        for item in root.findall('.//item', namespaces):
            title_elem = item.find('title', namespaces)
            link_elem = item.find('link', namespaces)
            pub_date_elem = item.find('pubDate', namespaces)
            desc_elem = item.find('description', namespaces)
            
            # 尝试多种方式获取作者
            author = ''
            author_elem = item.find('dc:creator', namespaces)
            if author_elem is not None and author_elem.text:
                author = author_elem.text
            else:
                # 尝试 author 子元素
                author_elem2 = item.find('author', namespaces)
                if author_elem2 is not None and author_elem2.text:
                    author = author_elem2.text
            
            if title_elem is not None and link_elem is not None:
                title = title_elem.text or ''
                link = link_elem.text or ''
                pub_date = pub_date_elem.text if pub_date_elem is not None else ''
                desc = desc_elem.text if desc_elem is not None else ''
                
                # 过滤广告
                if any(kw in title.lower() for kw in ['sponsor', 'advertisement', 'newsletter']):
                    continue
                
                # 验证作者信息
                validated_author = validate_author(author, source)
                
                articles.append({
                    'title': title.strip(),
                    'url': link.strip(),
                    'date': pub_date[:10] if pub_date else '',
                    'author': validated_author,
                    'desc': desc[:300] if desc else '',
                    'source': source
                })
    except Exception as e:
        print("RSS 解析失败：{}".format(str(e)))
    
    return articles

def validate_author(author, source):
    """验证作者信息，无效时返回编辑部名称"""
    # 无效作者关键词（抓取错误时会出现这些词）
    invalid_keywords = ['next', 'combining', 'read', 'more', 'click', 'subscribe', 'login', 'sign', 'join']
    
    # 没有作者
    if not author or not author.strip():
        return '{}编辑部'.format(source)
    
    author = author.strip()
    
    # 包含无效关键词
    if any(kw in author.lower() for kw in invalid_keywords):
        return '{}编辑部'.format(source)
    
    # 作者名太长（可能是抓错了）
    if len(author) > 50:
        return '{}编辑部'.format(source)
    
    # 包含邮箱
    if '@' in author:
        return '{}编辑部'.format(source)
    
    return author

def is_iain_morris(article):
    """判断是否为 Iain Morris 的文章"""
    if not article.get('author'):
        return False
    return 'iain morris' in article['author'].lower() or 'iain' in article['author'].lower()

def load_pushed_history():
    """加载已推送文章记录"""
    if os.path.exists(PUSHED_FILE):
        try:
            with open(PUSHED_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)
                cutoff = datetime.now().timestamp() - 7 * 24 * 3600
                data = {k: v for k, v in data.items() if v > cutoff}
                return data
        except:
            pass
    return {}

def save_pushed_history(history):
    """保存已推送文章记录"""
    try:
        with open(PUSHED_FILE, 'w', encoding='utf-8') as f:
            json.dump(history, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print("保存推送历史失败：{}".format(e))

def get_article_key(article):
    """生成文章唯一标识"""
    key_str = (article.get('title', '') + '|' + article.get('url', '')).lower().strip()
    return re.sub(r'[^a-z0-9]', '', key_str)[:50]

def create_message(featured, others):
    """创建合并推送消息"""
    
    if not featured:
        return "抱歉，今日未能获取到文章，请稍后重试。"
    
    # AI 翻译的文章数据（实际使用时由 AI 填充）
    message = "科技新闻每日摘要\n\n"
    
    # 重点推荐（Iain Morris 文章）
    message += "【重点推荐】\n"
    message += "{}\n".format(featured['title_cn'])
    message += "作者：{}\n".format(featured.get('author', 'Unknown'))
    message += "发布时间：{}\n".format(featured.get('date', ''))
    message += "来源：{}\n\n".format(featured.get('source', 'LightReading'))
    message += "要点摘要：\n"
    for i, point in enumerate(featured.get('points', []), 1):
        message += "  {}. {}\n".format(i, point)
    message += "\n原文链接：{}\n".format(featured.get('url', ''))
    message += "\n" + "="*50 + "\n\n"
    
    # 其他精选（3 篇，混合 LightReading 和 TechCrunch）
    message += "【其他精选】\n\n"
    for i, art in enumerate(others, 1):
        message += "精选{}：{}\n".format(i, art['title_cn'])
        message += "作者：{}\n".format(art.get('author', 'Unknown'))
        message += "发布时间：{}\n".format(art.get('date', ''))
        message += "来源：{}\n\n".format(art.get('source', ''))
        message += "要点摘要：\n"
        for j, point in enumerate(art.get('points', []), 1):
            message += "  {}. {}\n".format(j, point)
        message += "\n原文链接：{}\n\n".format(art.get('url', ''))
        message += "-"*50 + "\n\n"
    
    message += "来源：LightReading.com + TechCrunch.com"
    
    return message

def send_to_wechat(content):
    """发送到企业微信"""
    data = {"msgtype": "text", "text": {"content": content}}
    body = json.dumps(data, ensure_ascii=False).encode('utf-8')
    
    parsed = urllib.parse.urlparse(WEBHOOK_URL)
    conn = http.client.HTTPSConnection(parsed.netloc, timeout=60)
    try:
        conn.request('POST', parsed.path + '?' + parsed.query, body, {'Content-Type': 'application/json; charset=utf-8'})
        response = conn.getresponse()
        response_body = response.read().decode('utf-8')
        
        if response.status != 200:
            raise Exception('HTTP {}: {}'.format(response.status, response_body))
        
        return json.loads(response_body)
    finally:
        conn.close()

def main():
    print("=" * 60)
    print("科技新闻合并推送（v4.0）")
    print("=" * 60)
    
    # 【新增】检查中文文件日期，如果不是今天就删除重做
    output_file_cn = os.path.join(os.path.dirname(__file__), 'combined_cn.txt')
    if os.path.exists(output_file_cn):
        file_mtime = datetime.fromtimestamp(os.path.getmtime(output_file_cn))
        today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        if file_mtime.date() < today.date():
            print("\n[INFO] 检测到中文文件是旧文件（{}），删除后重新抓取".format(file_mtime.strftime('%Y-%m-%d')))
            os.remove(output_file_cn)
            # 同时删除英文文件，确保重新抓取
            for f in ['combined_en.txt', 'today_en.txt', 'techcrunch_en.txt']:
                fpath = os.path.join(os.path.dirname(__file__), f)
                if os.path.exists(fpath):
                    os.remove(fpath)
                    print("[INFO] 删除旧文件：{}".format(f))
    
    # 获取 LightReading RSS
    print("\n正在获取 LightReading RSS...")
    lr_xml = fetch_lr_rss()
    if lr_xml:
        print("LightReading RSS 获取成功（{} 字符）".format(len(lr_xml)))
        lr_articles = parse_rss(lr_xml, 'LightReading')
        print("找到 {} 篇文章".format(len(lr_articles)))
    else:
        lr_articles = []
    
    # 获取 TechCrunch RSS
    print("\n正在获取 TechCrunch RSS...")
    tc_xml = fetch_tc_rss()
    if tc_xml:
        print("TechCrunch RSS 获取成功（{} 字符）".format(len(tc_xml)))
        tc_articles = parse_rss(tc_xml, 'TechCrunch')
        print("找到 {} 篇文章".format(len(tc_articles)))
    else:
        tc_articles = []
    
    # 合并所有文章
    all_articles = lr_articles + tc_articles
    
    # 过滤已推送
    pushed_history = load_pushed_history()
    filtered = []
    for a in all_articles:
        key = get_article_key(a)
        if key not in pushed_history:
            filtered.append(a)
    
    print("\n去重后剩余 {} 篇".format(len(filtered)))
    
    # 【v4.2 新增】如果没有新文章，清除历史记录重新抓取
    if not filtered:
        print("\n[WARNING] 没有新文章（RSS 内容可能重复）")
        print("[INFO] 清除推送历史记录，重新抓取...")
        pushed_history = {}
        save_pushed_history(pushed_history)
        
        # 重新获取 RSS
        print("\n重新获取 LightReading RSS...")
        lr_xml = fetch_lr_rss()
        if lr_xml:
            lr_articles = parse_rss(lr_xml, 'LightReading')
            print("LightReading: {} 篇".format(len(lr_articles)))
        
        print("重新获取 TechCrunch RSS...")
        tc_xml = fetch_tc_rss()
        if tc_xml:
            tc_articles = parse_rss(tc_xml, 'TechCrunch')
            print("TechCrunch: {} 篇".format(len(tc_articles)))
        
        all_articles = lr_articles + tc_articles
        filtered = all_articles[:10]  # 取前 10 篇
        
        if not filtered:
            print("\n[ERROR] 重新抓取后仍没有文章，跳过本次推送")
            return None
        
        print("[OK] 重新抓取后找到 {} 篇新文章".format(len(filtered)))
    
    # 检查是否有现成的中文文件（如果是今天的，且内容匹配，直接推送）
    output_file_cn = os.path.join(os.path.dirname(__file__), 'combined_cn.txt')
    
    # 选择文章：优先 Iain Morris 作为重点推荐，确保两个网站都有代表
    iain_articles = [a for a in filtered if is_iain_morris(a)]
    lr_articles = [a for a in filtered if a['source'] == 'LightReading' and not is_iain_morris(a)]
    tc_articles = [a for a in filtered if a['source'] == 'TechCrunch']
    
    # 重点推荐：优先 Iain Morris，没有则选 LightReading 最新
    if iain_articles:
        featured = iain_articles[0]
        print("重点推荐：Iain Morris 文章 ({})".format(featured['source']))
    elif lr_articles:
        featured = lr_articles[0]
        print("重点推荐：LightReading 文章（今日无 Iain Morris 新文章）")
    else:
        featured = filtered[0]
        print("重点推荐：{}（今日无 LightReading 文章）".format(featured['source']))
    
    # 其他精选：确保至少 1 篇 TechCrunch + 2 篇其他
    others = []
    
    # 至少选 1 篇 TechCrunch
    if tc_articles:
        others.append(tc_articles[0])
        print("其他精选 1: TechCrunch - {}".format(tc_articles[0]['title'][:40]))
    
    # 再选 2 篇（优先 LightReading，排除已选）
    remaining_lr = [a for a in lr_articles if a['url'] != featured['url']]
    remaining_tc = [a for a in tc_articles if a['url'] != (others[0]['url'] if others else '')]
    
    # 选第 2 篇（LightReading）
    if remaining_lr:
        others.append(remaining_lr[0])
        print("其他精选 2: LightReading - {}".format(remaining_lr[0]['title'][:40]))
    
    # 选第 3 篇（混合，优先未代表的网站）
    if len(others) < 3:
        if len(others) == 1:  # 只有 TechCrunch，再选 2 篇 LightReading
            others.extend(remaining_lr[:2])
        else:  # 有 LightReading，再选 1 篇 TechCrunch
            if remaining_tc:
                others.append(remaining_tc[0])
            elif remaining_lr:
                others.append(remaining_lr[0])
    
    print("其他精选：{} 篇（TechCrunch: {}, LightReading: {}）".format(
        len(others),
        sum(1 for a in others if a['source'] == 'TechCrunch'),
        sum(1 for a in others if a['source'] == 'LightReading')
    ))
    
    # 抓取网页全文 + RSS 描述（供 AI 翻译）
    print("\n正在抓取网页全文和 RSS 描述...")
    
    def fetch_full_content(url, rss_desc='', current_author=''):
        """抓取网页全文 - 多种方式尝试 + RSS 描述补充 + 提取作者"""
        author = current_author
        
        try:
            scraper = cloudscraper.create_scraper()
            resp = scraper.get(url, timeout=60)
            if resp.status_code == 200:
                html = resp.text
                
                # 提取作者（如果 RSS 没有提供）
                if not author:
                    # 方式 1: 从作者链接提取（最可靠）
                    author_link = re.search(r'href="[^"]*/author/([^"]+)"', html, re.IGNORECASE)
                    if author_link:
                        author_slug = author_link.group(1).replace('-', ' ').title()
                        author = author_slug
                        print("  从作者链接提取：{}".format(author))
                    
                    # 方式 2: 尝试多种正则表达式
                    if not author or len(author) < 3:
                        author_patterns = [
                            r'"author":\s*\[\s*\{[^}]*"name":\s*"([^"]+)"',  # JSON-LD
                            r'<meta[^>]*name=["\']author["\'][^>]*content=["\']([^"\']+)["\']',  # Meta
                            r'class="[^"]*author[^"]*"[^>]*>([^<]+)</',  # Author class
                            r'name="author"[^>]*content="([^"]+)"'  # name=author
                        ]
                        for pattern in author_patterns:
                            match = re.search(pattern, html, re.IGNORECASE)
                            if match:
                                author_candidate = match.group(1).strip()
                                # 过滤掉邮箱等无效内容
                                if '@' not in author_candidate and len(author_candidate) < 50:
                                    author = author_candidate
                                    print("  从正则提取：{}".format(author))
                                    break
                    
                    # 方式 3: By 开头（最后尝试，容易误匹配）
                    if not author or len(author) < 3:
                        by_match = re.search(r'By\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)+)', html, re.IGNORECASE)
                        if by_match:
                            author_candidate = by_match.group(1).strip()
                            # 验证不是无效关键词
                            invalid_keywords = ['next', 'combining', 'read', 'more', 'click', 'subscribe', 'login', 'sign', 'join', 'than', 'to', 'an', 'the', 'cost']
                            if not any(kw in author_candidate.lower() for kw in invalid_keywords):
                                author = author_candidate
                                print("  从 By 提取：{}".format(author))
                    
                    # 验证作者信息，无效则使用编辑部名称
                    author = validate_author(author, source)
                    if author != current_author and '{}编辑部'.format(source) not in author:
                        print("  验证后作者：{}".format(author))
                
                # 方式 1: 提取所有段落
                paragraphs = re.findall(r'<p[^>]*>([^<]+)</p>', html, re.IGNORECASE)
                content_p = ' '.join([p.strip() for p in paragraphs if len(p.strip()) > 20])
                
                # 方式 2: 提取 article 标签
                article = re.search(r'<article[^>]*>(.*?)</article>', html, re.DOTALL | re.IGNORECASE)
                content_article = ''
                if article:
                    article_p = re.findall(r'<p[^>]*>([^<]+)</p>', article.group(1), re.IGNORECASE)
                    content_article = ' '.join([p.strip() for p in article_p if len(p.strip()) > 20])
                
                # 合并网页内容
                web_content = content_p + ' ' + content_article
                web_content = re.sub(r'\s+', ' ', web_content).strip()
                
                # 【关键】过滤网站通用内容（在去重之前）
                # 只过滤明确的通用短语，保留可能有实质内容的句子
                generic_phrases = [
                    'Together, we power an unparalleled network of 220+ online properties',
                    'We help you gain critical insights and make more informed decisions across your business priorities',
                    'Want more Light Reading stories in your Google search results?',
                    'Subscribe for the industry\'s biggest tech news',
                    'TechCrunch Mobility is your destination for transportation news and insight',
                    'Startups are the core of TechCrunch, so get our best coverage delivered weekly',
                    'Provides movers and shakers with the info they need to start their day',
                    '© 2026 TechCrunch Media LLC',
                    '© 2026 Informa TechTarget',
                    'Contributing Editor, Light Reading',
                    'Senior Editor, Light Reading',
                    'International Editor, Light Reading',
                    'Assistant Editor, Europe, Light Reading',
                    'Senior Editor, APAC, Light Reading',
                ]
                for phrase in generic_phrases:
                    web_content = web_content.replace(phrase, '')
                
                # 过滤"Eight telco trends"等推广链接（整句过滤）
                promo_sentences = [
                    'Eight telco trends we\'re tracking in 2026',
                    'Looking ahead: M&A watch for 2026',
                    'It\'s time to think about 6G – yes, really',
                    'Looking ahead: AI agents creep into broadband networks',
                    'Nvidia\'s chips need to be cheaper and less power-hungry to be deployed across mobile network sites, says Samsung\'s Woojune Kim',
                ]
                for sent in promo_sentences:
                    web_content = web_content.replace(sent, '')
                
                # 如果网页内容不足，使用 RSS 描述补充
                if len(web_content) < 500 and rss_desc:
                    print("  网页内容不足，使用 RSS 描述补充")
                    web_content = web_content + ' ' + rss_desc
                
                # 去重
                sentences = web_content.split('. ')
                unique_sentences = []
                seen = set()
                for sent in sentences:
                    sent_clean = sent.strip()
                    # 过滤短句和重复句
                    if len(sent_clean) > 20 and sent_clean not in seen:
                        # 过滤包含通用关键词的句子
                        generic_keywords = ['subscribe', 'delivered weekly', 'techcrunch mobility', 'startups are the core', 'provides movers and shakers', 'want more light reading']
                        if not any(kw in sent_clean.lower() for kw in generic_keywords):
                            seen.add(sent_clean)
                            unique_sentences.append(sent_clean)
                web_content = '. '.join(unique_sentences)
                web_content = re.sub(r'\s+', ' ', web_content).strip()
                
                print("  抓取到 {} 字符（过滤后）".format(len(web_content)))
                return web_content[:5000], author
        except Exception as e:
            print("  抓取失败：{}".format(str(e)[:50]))
        return rss_desc if rss_desc else "", author
    
    # 要求 2: 确保每篇文章都有足够内容（至少能总结 3 个要点）
    print("\n验证文章内容是否充足...")
    
    def has_enough_content(content):
        """检查内容是否足够总结 3 个要点（必须 >200 字符）"""
        return len(content) > 200
    
    # 验证重点推荐（传入 RSS 描述作为补充）
    featured_full, featured_author = fetch_full_content(featured['url'], featured.get('desc', ''), featured.get('author', ''))
    if featured_author:
        featured['author'] = featured_author
    if not featured_full or len(featured_full) <= 200:
        print("  重点推荐内容不足（{} 字符），尝试更换文章...".format(len(featured_full) if featured_full else 0))
        # 尝试从其他文章中选择，优先选择 RSS 描述丰富的
        candidates = sorted(lr_articles + tc_articles, key=lambda a: len(a.get('desc', '')), reverse=True)
        for a in candidates:
            if a['url'] != featured['url']:
                full, author = fetch_full_content(a['url'], a.get('desc', ''), a.get('author', ''))
                if full and len(full) > 200:
                    featured = a
                    featured_full = full
                    if author:
                        featured['author'] = author
                    print("  已更换为：{} (作者：{}, 内容：{} 字符)".format(featured['title'][:50], author, len(full)))
                    break
    
    if not featured_full:
        featured_full = featured.get('desc', '')
    print("  重点推荐全文：{} 字符，作者：{}".format(len(featured_full), featured.get('author', 'Unknown')))
    
    # 验证其他精选（传入 RSS 描述作为补充）
    others_full = []
    valid_others = []
    for a in others:
        full, author = fetch_full_content(a['url'], a.get('desc', ''), a.get('author', ''))
        if author:
            a['author'] = author
        if full and len(full) > 200:
            others_full.append(full)
            valid_others.append(a)
            print("  精选全文：{} 字符，作者：{} [OK]".format(len(full), a.get('author', 'Unknown')))
        else:
            print("  精选内容不足 200 字符（实际：{} 字符），跳过".format(len(full) if full else 0))
    
    # 如果有效文章不足 3 篇，从剩余文章中选择
    if len(valid_others) < 3:
        print("\n有效文章不足 3 篇，尝试补充...")
        remaining = [a for a in filtered if a not in [featured] + valid_others]
        for a in remaining:
            if len(valid_others) >= 3:
                break
            full, author = fetch_full_content(a['url'], a.get('desc', ''), a.get('author', ''))
            if author:
                a['author'] = author
            if full and len(full) > 200:
                others_full.append(full)
                valid_others.append(a)
                print("  补充文章：{} 字符，作者：{} [OK]".format(len(full), a.get('author', 'Unknown')))
    
    others = valid_others
    
    # 【严格要求】检查是否有足够的内容
    if not featured_full or len(featured_full) <= 200:
        print("\n[ERROR] 重点推荐内容不足 200 字符（实际：{} 字符），无法推送".format(len(featured_full) if featured_full else 0))
        print("[INFO] 所有可抓取的文章内容都不足，建议稍后重试")
        print("\n跳过本次推送...")
        return None
    
    if len(valid_others) < 3:
        print("\n[WARNING] 有效文章不足 3 篇（实际：{} 篇），尝试降低要求...".format(len(valid_others)))
        # 如果文章不足 3 篇，但有 2 篇也可以推送
        if len(valid_others) < 2:
            print("[ERROR] 有效文章少于 2 篇，无法推送")
            print("[INFO] 建议稍后重试，等待更多文章更新")
            print("\n跳过本次推送...")
            return None
    
    # 【关键】先检查是否已有 AI 翻译的中文文件（在保存英文和删除之前！）
    output_file_cn = os.path.join(os.path.dirname(__file__), 'combined_cn.txt')
    
    if os.path.exists(output_file_cn):
        # 读取已有的中文翻译
        print("\n[INFO] 发现已有的中文翻译文件：{}".format(output_file_cn))
        with open(output_file_cn, 'r', encoding='utf-8') as f:
            message = f.read()
        
        # 检查是否包含占位符，如果有，不要推送
        if '[AI 翻译]' in message or '[待翻译]' in message or '(根据完整英文内容翻译要点' in message:
            print("\n[WARNING] 中文翻译包含占位符，跳过推送")
            print("[INFO] 请 AI 先翻译 combined_en.txt，更新 combined_cn.txt 后再推送")
            print("\n跳过本次推送...")
            return None
        else:
            print("[INFO] 中文翻译已完成，准备推送")
            # 直接推送，不保存英文文件，不删除中文文件
            print("\n正在发送到企业微信...")
            result = send_to_wechat(message)
            print("推送结果：{}".format(result))
            
            if result.get('errcode') == 0:
                print("OK 推送成功")
                # 保存推送记录
                for a in [featured] + others:
                    key = get_article_key(a)
                    pushed_history[key] = datetime.now().timestamp()
                save_pushed_history(pushed_history)
                print("已保存推送记录")
            else:
                print("推送失败：{}".format(result))
            
            return result
    
    # 【v5.9】没有中文文件时，保存英文文件，等待 AI 翻译（不推送）
    print("\n[INFO] 无中文翻译文件，保存英文文件等待 AI 翻译...")
    
    # 保存英文文件（供 AI 翻译）
    output_file_en = os.path.join(os.path.dirname(__file__), 'combined_en.txt')
    with open(output_file_en, 'w', encoding='utf-8') as f:
        f.write("=== 重点推荐 ===\n")
        f.write("标题：{}\n".format(featured['title']))
        f.write("作者：{}\n".format(featured.get('author', 'Unknown')))
        f.write("来源：{}\n".format(featured['source']))
        f.write("URL: {}\n\n".format(featured['url']))
        f.write("全文内容：\n{}\n\n".format(featured_full))
        
        f.write("=== 其他精选 ===\n\n")
        for i, a in enumerate(others, 1):
            f.write("{}. 标题：{}\n".format(i, a['title']))
            f.write("   作者：{}\n".format(a.get('author', 'Unknown')))
            f.write("   来源：{}\n".format(a['source']))
            f.write("   URL: {}\n\n".format(a['url']))
            f.write("   全文内容：\n{}\n\n".format(others_full[i-1]))
    
    print("\n英文内容已保存到：{}".format(output_file_en))
    
    # 2. 单独保存 LightReading 和 TechCrunch（方便 AI 分别翻译）
    lr_articles = [featured] + [a for a in others if a['source'] == 'LightReading']
    tc_articles = [a for a in others if a['source'] == 'TechCrunch']
    
    # LightReading 单独文件
    lr_en_file = os.path.join(os.path.dirname(__file__), 'today_en.txt')
    with open(lr_en_file, 'w', encoding='utf-8') as f:
        f.write("=== LightReading 文章 ===\n\n")
        for i, a in enumerate(lr_articles, 1):
            f.write("{}. 标题：{}\n".format(i, a['title']))
            f.write("   作者：{}\n".format(a.get('author', 'Unknown')))
            f.write("   URL: {}\n\n".format(a['url']))
            f.write("   描述：{}\n\n".format(a.get('desc', '')))
    print("LightReading 英文已保存到：{}".format(lr_en_file))
    
    # TechCrunch 单独文件
    tc_en_file = os.path.join(os.path.dirname(__file__), 'techcrunch_en.txt')
    with open(tc_en_file, 'w', encoding='utf-8') as f:
        f.write("=== TechCrunch 文章 ===\n\n")
        for i, a in enumerate(tc_articles, 1):
            f.write("{}. 标题：{}\n".format(i, a['title']))
            f.write("   作者：{}\n".format(a.get('author', 'Unknown')))
            f.write("   URL: {}\n\n".format(a['url']))
            f.write("   描述：{}\n\n".format(a.get('desc', '')))
    print("TechCrunch 英文已保存到：{}".format(tc_en_file))
    
    # 【v5.9】保存英文文件后退出，等待 AI 翻译
    print("\n[INFO] 英文文件已保存")
    print("[INFO] 等待 AI 翻译 combined_en.txt 生成 combined_cn.txt")
    print("[INFO] 翻译完成后再次运行此脚本会自动推送")
    print("\n退出（等待 AI 翻译）...")
    return None

if __name__ == '__main__':
    main()
