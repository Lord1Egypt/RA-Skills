# -*- coding: utf-8 -*-
"""
网络抓取模块 v2
"""

import os
import requests
import re
from datetime import datetime, timedelta
from bs4 import BeautifulSoup
import urllib3
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)
warnings.filterwarnings("ignore", category=UserWarning)
warnings.filterwarnings("ignore", category=urllib3.exceptions.InsecureRequestWarning)
try:
    from .config import WEBSITES, HEADERS, HOLIDAYS_2026, USE_LLM_SUMMARY, LLM_MAX_LENGTH
except ImportError:
    from config import WEBSITES, HEADERS, HOLIDAYS_2026, USE_LLM_SUMMARY, LLM_MAX_LENGTH


def is_boilerplate(para):
    """
    判断段落是否为废话/非正文内容
    """
    # 图片说明（各种格式）
    if re.search(r'(摄$|新华社[\u4e00-\u9fa5]*摄|人民视觉|视觉中国|影像中国|图片来源|图/|记者\s+\w+\s+摄|受访对象供图|无人机照片)', para):
        return True
    # 编辑/记者/作者署名（各种位置）
    if re.search(r'(（编辑|责编|来源|作者|文/|撰稿|科技日报\s+|本报记者\s+|记者\s+\w+)', para):
        return True
    # 广告/推广
    if re.search(r'(广告|推广|免责声明|版权声明|扫码下载)', para):
        return True
    # 社交互动
    if re.search(r'(分享到|我要评论|扫一扫|关注我们|点赞)', para):
        return True
    # 页面尾部时间戳（如"发布于2026-05-15 20:29:02"）
    if re.match(r'^发布于\d{4}-\d{2}-\d{2}', para):
        return True
    # 导航/链接列表
    if re.search(r'(关于我们|联系我们|网站地图|登录|注册)', para):
        return True
    # 页脚备案号/许可证/版权信息
    if re.search(r'(ICP证|京ICP|京公网安备|网络文化经营|网络出版服务|视听节目许可证|增值电信业务经营许可证|互联网新闻信息服务|版权所有.*copyright|copyright.*reserved)', para, re.IGNORECASE):
        return True
    # 纯数字或太短
    if re.match(r'^[\d\s\.\,、]+$', para) or len(para) < 20:
        return True
    # 分隔符行
    if re.match(r'^[-=—_*\s]+$', para):
        return True
    # 小标题格式（短且无句号）
    if len(para) < 30 and '。' not in para and '，' not in para:
        # 可能是小标题或导航
        if re.search(r'(^[「『【〖]|\s+[」』】〗]$)', para):
            return True
    return False


def extract_brief_summary(content, title='', max_chars=300):
    """
    从网页内容中提取新闻摘要（智能选段版）
    
    策略：
    1. 过滤废话段落（图片说明、编辑署名、广告等）
    2. 对每个段落按信息密度评分（数字、日期、专有名词等）
    3. 导语段落（靠前位置）给予加权
    4. 按分数从高到低选择，但优先保证连贯性
    """
    if not content:
        return ''
    
    # 按段落分割
    paragraphs = [p.strip() for p in content.split('\n') if p.strip()]
    
    # 过滤短段落和废话
    paragraphs = [p for p in paragraphs if len(p) > 15 and not is_boilerplate(p)]
    
    if not paragraphs:
        return content[:max_chars]
    
    # 计算每个段落的信息密度分数
    scored_paras = []
    for i, para in enumerate(paragraphs):
        score = 0
        
        # ===== 位置加分 =====
        # 导语优先：首段通常含核心事实（倒金字塔结构）
        if i == 0:
            score += 10
        elif i <= 2:
            score += 5
        elif i <= 5:
            score += 2
        
        # ===== 高信息密度加分 =====
        # 数字（金额、数量、百分比）—— 数字=事实
        num_count = len(re.findall(r'[\d\.]+', para))
        score += num_count * 2.5  # 从 1.5 提高到 2.5
        
        # 高信息密度信号词：首次/突破/具体名称
        density_signals = [
            '首次', '突破', '超过', '达到', '创', '同比增长',
            '获批', '投产', '签约', '落地', '开工', '竣工',
        ]
        for word in density_signals:
            if word in para:
                score += 3
        
        # 股票代码/具体型号等
        if re.search(r'（[A-Z]{2,}：\d+）', para):
            score += 5
        
        # ===== 关键信号词（政策/行动/结果） =====
        signal_words = ['印发', '发布', '宣布', '决定', '完成', '启动', '达成',
                       '增长', '下降', '同比', '环比', '占', '实现', '提出']
        for word in signal_words:
            if word in para:
                score += 2
        
        # 专有名词（机构、地点）密度
        entity_count = len(re.findall(r'[\u4e00-\u9fa5]{2,6}(?:部|委|局|省|市|县|区|公司|集团|中心|研究院)', para))
        score += entity_count * 1
        
        # ===== 段落完整性 =====
        if para.endswith('。'):
            score += 3
        
        # ===== 降权规则 =====
        # 依赖上下文的段落（不能独立成段）
        if re.match(r'^(此外|另外|同时|另一方面|不仅如此|值得注意的是|值得一提的是)', para):
            score -= 3
        
        # 背景解释/风险分析（非新事实）
        background_patterns = [
            r'属于.*的.*', r'是.*的.*', r'可能.*', r'进而.*',
            r'对.*构成.*风险', r'被利用后', r'一旦.*将.*',
            r'近年来.*', r'长期以来.*', r'一直以来.*',
            r'据悉.*', r'据了解.*', r'有.*表示.*',
            r'标志着.*', r'意味着.*', r'意味着.*',
        ]
        bg_count = sum(1 for pat in background_patterns if re.search(pat, para))
        if bg_count >= 2:
            score -= bg_count * 2  # 多段背景描述大幅降权
        
        # 小标题降权（短且无标点结尾）
        if len(para) < 40 and not re.search(r'[。！？；]', para):
            score -= 2
        
        # 长度适中（30-250 字最佳）
        para_len = len(para)
        if 30 <= para_len <= 250:
            score += 2
        elif para_len > 350:
            score -= 2  # 太长可能是背景材料
            if '。' not in para[:300]:
                score -= 5
        elif para_len < 30:
            score -= 1
        
        # 纯问句降权
        if para.endswith('？') or para.endswith('?'):
            score -= 3
        
        # 纯引用降权（引号开头且无其他内容）
        if re.match(r'^["\u201c]', para) and len(para) < 80:
            score -= 2
        
        scored_paras.append((score, i, para))
    
    # 按分数降序排序
    scored_paras.sort(key=lambda x: x[0], reverse=True)
    
    # 选择段落组成摘要（优先选高分段，但尽量保持位置连贯）
    summary_parts = []
    total_len = 0
    selected_indices = set()
    
    def _find_sentence_end(text):
        """Find the best sentence-ending position in text."""
        text_len = len(text)
        # For shorter texts, use lower threshold
        min_pos = min(20, text_len // 3)
        
        for sep in ['。', '！', '？', '；']:
            pos = text.rfind(sep)
            if pos > min_pos:
                return pos + 1
        # Fallback: comma (but only if it leaves meaningful content)
        pos = text.rfind('，')
        if pos > min_pos and pos < text_len - 5:
            return pos + 1
        return -1
    
    for score, idx, para in scored_paras:
        if score <= -2:
            continue  # 跳过负分段落
        
        if total_len + len(para) > max_chars:
            remaining = max_chars - total_len
            if remaining <= 20:
                break  # 剩余太少，放弃此段
            
            truncated = para[:remaining]
            cut_pos = _find_sentence_end(truncated)
            
            if cut_pos > 0:
                summary_parts.append((idx, truncated[:cut_pos]))
                selected_indices.add(idx)
            # else: 放弃此段（无法找到完整句子结尾）
            break
        
        # 检查段落结尾是否完整（以句号等结束）
        cut_pos = _find_sentence_end(para)
        if cut_pos > 0 and cut_pos < len(para):
            # 段落尾部不完整，截断到完整句子
            # 但如果截掉的部分超过段落长度的 40%，说明信息损失太多，整段放弃
            if cut_pos >= len(para) * 0.6:
                summary_parts.append((idx, para[:cut_pos]))
                selected_indices.add(idx)
                total_len += cut_pos
            # else: 放弃此段，避免信息严重不完整
            break
        else:
            # 结尾完整或本身就是完整句子
            summary_parts.append((idx, para))
            selected_indices.add(idx)
            total_len += len(para)
    
    # 按原始位置排序，保证阅读连贯
    summary_parts.sort(key=lambda x: x[0])
    
    # 合并
    result = ' '.join([p for _, p in summary_parts]).strip()
    
    # 清理多余空格
    result = re.sub(r'\s+', ' ', result)
    
    return result


# 已知 SSL 证书有问题的网站，直接跳过验证

def decode_response(response, url=''):
    """
    智能解码响应内容，优先处理 GBK/GB2312 编码
    人民日报海外版等页面返回 GBK 但 Content-Type 可能未正确声明
    """
    # 1. Content-Type 声明
    content_type = response.headers.get('content-type', '').lower()
    if 'gb2312' in content_type or 'gbk' in content_type:
        response.encoding = 'gbk'
        return response.text
    
    # 2. HTML meta charset 声明
    raw = response.content[:500]
    meta = re.search(rb'charset=["\']?([\w-]+)', raw)
    if meta:
        cs = meta.group(1).decode('ascii', errors='ignore').lower()
        if 'gb2312' in cs or 'gbk' in cs:
            response.encoding = 'gbk'
            return response.text
    
    # 3. 已知 GBK 来源（Content-Type 可能不可靠）
    # 注意：人民日报主站(rmrb)实际是 UTF-8 编码，只有海外版(rmrbhwb)是 GBK
    if 'paper.people.com.cn/rmrbhwb' in url:
        try:
            return response.content.decode('gbk', errors='replace')
        except Exception:
            pass
    
    # 4. 兜底：apparent_encoding
    response.encoding = response.apparent_encoding
    return response.text


def fetch_page(url, timeout=10):
    """
    抓取网页内容
    
    Args:
        url: 网址
        timeout: 超时时间
    
    Returns:
        str: HTML 内容
    """
    try:
        # 特殊处理：36 氪需要较长超时，cinn.cn/cnii.com.cn 需要更长超时
        is_36kr = '36kr.com' in url
        is_cinn = 'cinn.cn' in url
        is_cnii = 'cnii.com.cn' in url
        if is_cinn:
            actual_timeout = 30
        elif is_cnii:
            actual_timeout = 30
        elif is_36kr:
            actual_timeout = 15
        else:
            actual_timeout = timeout
        
        # 特殊处理：gov.cn 需要特定的浏览器头以绕过防护
        is_gov = 'www.gov.cn' in url
        current_headers = HEADERS.copy()
        if is_gov:
            current_headers['User-Agent'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'
            current_headers['Accept'] = 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
            current_headers['Accept-Encoding'] = 'gzip, deflate'
            # gov.cn 可能存在 SSL 策略，尝试不验证
            verify_ssl = False 
        else:
            verify_ssl = True
        
        response = requests.get(url, headers=current_headers, timeout=actual_timeout, verify=verify_ssl)
        response.raise_for_status()
        return decode_response(response, url)
    except requests.exceptions.SSLError:
        # SSL 错误时尝试不验证证书
        try:
            response = requests.get(url, headers=HEADERS, timeout=timeout, verify=False)
            response.raise_for_status()
            return decode_response(response, url)
        except Exception as e2:
            _flog(f"  抓取失败（SSL fallback）：{url} - {e2}")
            return None
    except Exception as e:
        _flog(f"  抓取失败：{url} - {e}")
        return None


def parse_36kr(soup, max_links=15):
    """
    36 氪独立解析器
    使用 CSS 选择器提取新闻文章
    """
    news_list = []
    items = soup.select('li.post-item, a[href*="/p/"]')[:20]
    for item in items:
        title = item.get_text(strip=True)
        link = item.get('href')
        if not title or len(title) < 8:
            continue
        if not link or not link.startswith('http'):
            link = 'https://36kr.com' + link if link else ''
        if not link or any(x in link for x in ['/seek-report', '/img.', 'letschuhai', '36krcdn']):
            continue
        news_list.append({'title': title, 'url': link})
        if len(news_list) >= max_links:
            break
    return news_list


def parse_cinn(soup, max_links=20):
    """
    中国工业新闻网独立解析器
    使用 CSS 选择器 a.list-news-box 提取新闻文章
    """
    news_list = []
    items = soup.select('a.list-news-box')
    for item in items:
        title = item.get_text(strip=True)
        link = item.get('href')
        if not title or len(title) < 8:
            continue
        if not link:
            continue
        # 处理相对链接
        if link.startswith('//'):
            link = 'https:' + link
        elif link.startswith('/'):
            link = 'https://www.cinn.cn' + link
        if not link or any(x in link.lower() for x in ['/about/', '/contact', '/login', '/register']):
            continue
        news_list.append({'title': title, 'url': link})
        if len(news_list) >= max_links:
            break
    return news_list


def parse_cnii(soup, base_url, max_links=20):
    """
    中国工信网独立解析器
    首页前部是导航链接（/rmydb/, /cnjy/ 等目录），新闻文章链接格式：/sz/202604/t20260416_730349.html
    只提取包含 /年月/t+数字.html 模式的新闻文章链接
    """
    import re
    from urllib.parse import urljoin

    news_list = []
    # 新闻链接模式：/栏目/6位年月/tYYYYMMDD_编号.html
    article_pattern = re.compile(r'/\w+/\d{6}/t\d+_\d+\.html')

    for a in soup.find_all('a', href=True):
        href = a['href']
        title = a.get_text(strip=True)

        if not title or len(title) < 10:
            continue

        # 转换为绝对 URL
        if href.startswith('//'):
            abs_url = 'https:' + href
        elif not href.startswith('http'):
            abs_url = urljoin(base_url, href)
        else:
            abs_url = href

        # 只保留匹配新闻文章模式的链接
        if not article_pattern.search(abs_url):
            continue

        if any(x in abs_url.lower() for x in ['/about/', '/contact', '/login', '/register']):
            continue

        news_list.append({'title': title, 'url': abs_url})
        if len(news_list) >= max_links:
            break

    return news_list


def parse_cnii(soup, base_url, max_links=20):
    """
    中国工信网独立解析器
    首页前部是导航链接，新闻文章链接格式：/sz/202604/t20260416_730349.html
    只提取包含日期路径的新闻文章链接
    """
    import re
    from urllib.parse import urljoin

    news_list = []
    # 新闻链接模式：/栏目/年月/tYYYYMMDD_编号.html
    article_pattern = re.compile(r'/\w+/\d{6}/t\d+_\d+\.html$')

    for a in soup.find_all('a', href=True):
        href = a['href']
        title = a.get_text(strip=True)

        if not title or len(title) < 10:
            continue

        # 转换为绝对 URL
        if href.startswith('//'):
            abs_url = 'https:' + href
        elif href.startswith('/'):
            abs_url = urljoin(base_url, href)
        else:
            abs_url = href

        # 只保留匹配新闻文章模式的链接
        if not article_pattern.search(abs_url):
            continue

        if any(x in abs_url.lower() for x in ['/about/', '/contact', '/login', '/register']):
            continue

        news_list.append({'title': title, 'url': abs_url})
        if len(news_list) >= max_links:
            break

    return news_list


def parse_cnii(soup, base_url, max_links=20):
    """
    中国工信网独立解析器
    首页前部是导航链接，新闻文章链接格式：/sz/202604/t20260416_730349.html
    只提取包含日期路径的新闻文章链接
    """
    import re
    from urllib.parse import urljoin

    news_list = []
    # 新闻链接模式：/栏目/年月/tYYYYMMDD_编号.html
    article_pattern = re.compile(r'/\w+/\d{6}/t\d+_\d+\.html$')

    for a in soup.find_all('a', href=True):
        href = a['href']
        title = a.get_text(strip=True)

        if not title or len(title) < 10:
            continue

        # 转换为绝对 URL（统一使用 urljoin 处理所有非 http 开头的链接）
        if href.startswith('//'):
            abs_url = 'https:' + href
        elif not href.startswith('http'):
            abs_url = urljoin(base_url, href)
        else:
            abs_url = href

        # 只保留匹配新闻文章模式的链接
        if not article_pattern.search(abs_url):
            continue

        if any(x in abs_url.lower() for x in ['/about/', '/contact', '/login', '/register']):
            continue

        news_list.append({'title': title, 'url': abs_url})
        if len(news_list) >= max_links:
            break

    return news_list


def parse_cnr(soup, max_links=20):
    """
    央广网独立解析器
    页面结构：<a> 标签内 <strong>标题</strong> <em>摘要</em> <span>时间</span>
    只取 <strong> 作为标题，避免标题+正文混在一起
    """
    import re
    from urllib.parse import urljoin
    
    news_list = []
    seen_urls = set()
    
    # 新闻链接模式：包含 tYYYYMMDD_数字.shtml
    article_pattern = re.compile(r't\d+_\d+\.shtml')
    
    for item in soup.select('.articleList .item'):
        a_tag = item.find('a', href=True)
        if not a_tag:
            continue
        
        href = a_tag['href']
        if not article_pattern.search(href):
            continue
        
        if href in seen_urls:
            continue
        seen_urls.add(href)
        
        # 转换为绝对 URL
        if href.startswith('//'):
            abs_url = 'https:' + href
        elif not href.startswith('http'):
            abs_url = urljoin('http://news.cnr.cn/', href)
        else:
            abs_url = href
        
        # 只取 <strong> 标签作为标题
        strong = a_tag.find('strong')
        if not strong:
            continue
        title = strong.get_text(strip=True)
        
        if not title or len(title) < 5:
            continue
        
        if any(x in abs_url.lower() for x in ['/about/', '/contact', '/login']):
            continue
        
        news_list.append({'title': title, 'url': abs_url})
        if len(news_list) >= max_links:
            break
    
    return news_list


def parse_rmrbhwb(html, base_url, max_links=30):
    """
    人民日报海外版独立解析器
    结构：入口页 -> 版面列表 -> 文章列表
    """
    from urllib.parse import urljoin
    soup = BeautifulSoup(html, 'html.parser')
    news_list = []
    seen_urls = set()
    
    # 1. 提取当天版面链接 (如 202605/25/node_01.html)
    # 页面结构: <ul id="list"><li><a href="202605/25/node_01.html">...</a></li></ul>
    node_links = []
    list_container = soup.find('ul', id='list')
    if list_container:
        for a in list_container.find_all('a', href=True):
            if 'node_' in a['href'] and '.html' in a['href']:
                full_node_url = urljoin(base_url, a['href'])
                node_links.append(full_node_url)
    
    # 2. 遍历版面，提取文章
    for node_url in node_links:
        if len(news_list) >= max_links:
            break
            
        node_html = fetch_page(node_url)
        if not node_html:
            continue
            
        node_soup = BeautifulSoup(node_html, 'html.parser')
        
        # 文章链接通常在 <ul class="news-list"> 中
        # <li><a href="../../../content/...">标题</a></li>
        news_list_container = node_soup.find('ul', class_='news-list')
        if not news_list_container:
            # Fallback: 查找所有 content 链接
            links = node_soup.find_all('a', href=True)
        else:
            links = news_list_container.find_all('a', href=True)
            
        for a in links:
            if len(news_list) >= max_links:
                break
            title = a.get_text(strip=True)
            href = a['href']
            
            if not title or len(title) < 10:
                continue
                
            # 解析绝对 URL
            article_url = urljoin(node_url, href)
            
            if article_url in seen_urls:
                continue
            seen_urls.add(article_url)
            
            # 过滤非文章链接
            if 'content/' not in article_url:
                continue
                
            news_list.append({'title': title, 'url': article_url})
            
    return news_list


def extract_links(html, base_url, max_links=30, site_name=''):
    """
    提取链接（支持站点独立解析器）
    """
    if not html:
        return []
    
    soup = BeautifulSoup(html, 'html.parser')
    
    # 36 氪独立解析器
    if '36kr' in base_url.lower():
        return parse_36kr(soup, max_links)
    
    # 中国工业新闻网独立解析器
    if 'cinn.cn' in base_url.lower():
        return parse_cinn(soup, max_links)

    # 中国工信网独立解析器（首页导航链接多，需过滤）
    if 'cnii.com.cn' in base_url.lower():
        return parse_cnii(soup, base_url, max_links)
    
    # 央广网独立解析器（标题和正文在同一 <a> 标签内，需分开提取）
    if 'cnr.cn' in base_url.lower():
        return parse_cnr(soup, max_links)
    
    # 人民日报海外版 + 人民日报主站 独立解析器（入口页 -> 版面 -> 文章）
    # 两者页面结构完全一致（ul#list 版面导航 -> ul.news-list 文章列表）
    if 'paper.people.com.cn/rmrbhwb/pc/layout/index.html' in base_url.lower() or \
       'paper.people.com.cn/rmrb/pc/layout/index.html' in base_url.lower():
        return parse_rmrbhwb(html, base_url, max_links)
    
    links = []
    seen_urls = set()
    
    from urllib.parse import urlparse, urljoin
    
    for a in soup.find_all('a', href=True):
        url = a['href']
        title = a.get_text(strip=True)
        
        if not title or len(title) < 5:
            continue
        
        # 过滤“更多”、“more”等无效链接
        if title.lower().startswith(('更多', 'more', '>>', '<<')):
            continue
        
        # 转换为绝对 URL（统一使用 urljoin 处理所有相对路径）
        if url.startswith('//'):
            url = 'https:' + url
        elif not url.startswith('http'):
            # 处理 /path, ./path, ../path 等相对路径
            url = urljoin(base_url, url)
            if not url.startswith('http'):
                continue
        
        if url in seen_urls:
            continue
        seen_urls.add(url)
        
        if any(p in url.lower() for p in ['/about/', '/contact', '/jobs', '.pdf', '.doc']):
            continue
        
        # 过滤导航/专题/首页链接
        parsed_url = urlparse(url)
        path = parsed_url.path.lower()
        if any(p in path for p in ['/zt/', '/index.', '/material/', '/img4/', '/tj/', '/rwk/', '/jjgzhy/', '/kzsl', '/sz/index']):
            continue
        
        links.append({'title': title, 'url': url})
        if len(links) >= max_links:
            break
    
    return links


def fetch_article_content(url, timeout=8):
    """
    抓取文章内容
    
    Args:
        url: 文章 URL
        timeout: 超时时间
    
    Returns:
        tuple: (内容，发布时间)
    """
    html = fetch_page(url, timeout=timeout)
    if not html:
        return None, None
    
    try:
        soup = BeautifulSoup(html, 'html.parser')
    except (ValueError, Exception) as e:
        # 处理 malformed HTML（如非法字符引用）
        print(f"  页面解析失败：{url} - {e}")
        return None, None
    
    # 提取正文（尝试常见选择器）
    contentSelectors = [
        '.article-content', '.article-body', '#content', '.main-content',
        '.detail_content',     # 中国工信网（必须在前，避免 .content 误匹配导航）
        '.content',            # 通用（放后面，避免误匹配导航容器）
        '.rm_txt_con',         # 人民网文章正文
        '.showContent',        # 新华网部分页面
        '.TRS_Editor',          # 新华社系统默认编辑器
        '.article-detail',     # 通用变体
        '.detail-content',     # 通用变体
        '.review',             # 中国工信网备用
    ]
    content = None
    
    for selector in contentSelectors:
        elem = soup.select_one(selector)
        if elem:
            content = elem.get_text(separator='\n', strip=True)
            break
    
    if not content:
        #  fallback: 提取所有段落（同时过滤废话）
        paragraphs = soup.find_all('p')
        content = '\n'.join([
            p.get_text(strip=True)
            for p in paragraphs
            if len(p.get_text(strip=True)) > 20 and not is_boilerplate(p.get_text(strip=True))
        ])
    
    # 最终 fallback：提取 meta description 或 og:description
    if not content or len(content) < 50:
        meta_desc = soup.find('meta', attrs={'name': 'description'})
        if not meta_desc:
            meta_desc = soup.find('meta', attrs={'property': 'og:description'})
        if meta_desc and meta_desc.get('content'):
            content = meta_desc['content'].strip()
    
    # 提取发布时间
    pub_time = None
    time_patterns = [
        r'(\d{4})[年/-](\d{1,2})[月/-](\d{1,2})[日\s]',
        r'(\d{4})-(\d{2})-(\d{2})',
    ]
    
    for pattern in time_patterns:
        match = re.search(pattern, html)
        if match:
            pub_time = f"{match.group(1)}-{match.group(2).zfill(2)}-{match.group(3).zfill(2)}"
            break
    
    return content, pub_time


def is_within_days(date_str, max_days=3):
    """
    检查日期是否在有效天数内
    """
    if not date_str:
        return False
    
    try:
        pub_date = datetime.strptime(date_str, '%Y-%m-%d')
        today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        days_diff = (today - pub_date).days
        
        # 检查节假日
        is_holiday = False
        for holiday in HOLIDAYS_2026:
            holiday_date = datetime.strptime(holiday, "%Y-%m-%d")
            if abs((today - holiday_date).days) <= 1:
                is_holiday = True
                break
        
        if is_holiday:
            max_days = 7
        elif today.weekday() >= 5:  # 周末
            max_days = 5
        
        return 0 <= days_diff <= max_days
    except:
        return False


def is_relevant(title, content):
    """
    检查相关性
    """
    try:
        from .config import CORE_KEYWORDS, AUXILIARY_KEYWORDS
    except ImportError:
        from config import CORE_KEYWORDS, AUXILIARY_KEYWORDS
    
    text = (title + ' ' + (content or '')).lower()
    
    # 核心关键词
    if any(kw in text for kw in CORE_KEYWORDS):
        return True
    
    # 辅助关键词≥2
    aux_count = sum(1 for kw in AUXILIARY_KEYWORDS if kw in text)
    if aux_count >= 2:
        return True
    
    return False


# 日志文件路径（避免 stdout 撑爆）
_FETCH_LOG = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), '.news-fetch.log')

def _flog(msg):
    """写入日志文件，避免大量 print 撑爆 exec 沙箱 stdout"""
    try:
        with open(_FETCH_LOG, 'a', encoding='utf-8') as f:
            f.write(f"{datetime.now().strftime('%H:%M:%S')} {msg}\n")
    except Exception:
        pass


def fetch_all_news():
    """
    抓取所有网站的新闻
    
    Returns:
        int: 新增数量
    """
    try:
        from .database import save_to_database
    except ImportError:
        from database import save_to_database
    try:
        try:
            from .filters import is_excluded_topic, is_valid_news
        except ImportError:
            from filters import is_excluded_topic, is_valid_news
    except ImportError:
        from filters import is_excluded_topic, is_valid_news
    
    all_news = []
    seen_titles = set()  # 标题去重
    sites_ok = 0
    sites_fail = 0
    
    # 清空日志文件
    try:
        with open(_FETCH_LOG, 'w', encoding='utf-8') as f:
            f.write(f"=== 新闻抓取日志 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} ===\n")
    except Exception:
        pass
    
    _flog(f"开始抓取 {len(WEBSITES)} 个网站")
    
    for site in WEBSITES:
        _flog(f"  抓取：{site['name']}")
        
        # 每个源独立限流（每站 15 条，让所有站都有机会参与）
        if '36kr' in site['url']:
            max_links = 10  # 36氪 SPA 站，少抓
        elif site['name'].startswith('中国产经网'):
            max_links = 10  # 产经网内容较少
        else:
            max_links = 15
        
        html = fetch_page(site['url'])
        if not html:
            sites_fail += 1
            _flog(f"    {site['name']}: 抓取失败")
            continue
        
        # 超大文件保护：超过 500KB 的页面截断，防止内存溢出
        if len(html) > 500 * 1024:
            _flog(f"    {site['name']}: 页面过大 ({len(html)//1024}KB)，截断处理")
            html = html[:500 * 1024]
        
        links = extract_links(html, site['url'], max_links=max_links)
        _flog(f"    {site['name']}: 找到 {len(links)} 个链接")
        
        if len(links) > 0:
            sites_ok += 1
        
        for link in links:
            # 标题去重保护
            title_key = link['title'].strip()[:30]
            if title_key in seen_titles:
                continue
            seen_titles.add(title_key)
            
            # 快速过滤
            if is_excluded_topic(link['title'], ''):
                continue
            
            # 抓取内容
            content, pub_date = fetch_article_content(link['url'])
            if not content or len(content) < 100:
                continue
            
            # 日期验证
            if not is_within_days(pub_date, max_days=3):
                continue
            
            # 相关性验证
            if not is_relevant(link['title'], content):
                continue
            
            # 完整过滤
            valid, reason = is_valid_news(link['title'], content, link['url'])
            if not valid:
                continue
            
            # 格式化来源
            source_name = format_source_name(site['name'])
            
            # 提取新闻摘要（智能选段，最多 300 字）
            summary = extract_brief_summary(content, title=link['title'], max_chars=300)
            
            # LLM 总结（方案 A：抓取后立即总结）
            try:
                from .config import USE_LLM_SUMMARY, LLM_MAX_LENGTH
            except ImportError:
                from config import USE_LLM_SUMMARY, LLM_MAX_LENGTH
            if USE_LLM_SUMMARY and len(content) > 200:
                try:
                    from .llm_summarize import llm_summarize_article
                    llm_summary = llm_summarize_article(link['title'], content, LLM_MAX_LENGTH)
                    if llm_summary:
                        summary = llm_summary
                        _flog(f"    [LLM] {link['title'][:30]}... -> 已总结")
                except Exception as e:
                    _flog(f"    [LLM] 总结失败: {e}")
            
            all_news.append({
                'title': link['title'],
                'source': source_name,
                'publish_date': pub_date,
                'summary': summary,
                'url': link['url'],
                'content': content  # 保存原文，供 LLM 总结使用
            })
            
            if len(all_news) >= 200:  # 提高上限，让更多站点参与
                break
        
        if len(all_news) >= 200:
            break
    
    # 保存到数据库
    if all_news:
        new_count = save_to_database(all_news)
        _flog(f"抓取完成：新增 {new_count} 条新闻")
        # 只在 stdout 输出摘要，避免刷屏
        print(f"  [OK] 成功 {sites_ok}/{len(WEBSITES)} 个站，新增 {new_count} 条")
        return new_count
    
    print(f"  [WARN] 成功 {sites_ok}/{len(WEBSITES)} 个站，但未找到符合条件的新闻")
    return 0


def format_source_name(site_name):
    """
    格式化来源名称
    """
    try:
        from .config import SOURCE_MAP
    except ImportError:
        from config import SOURCE_MAP
    
    # 应用映射
    for key, value in SOURCE_MAP.items():
        if site_name.startswith(key):
            return value
    
    # 清理后缀
    suffixes = ['滚动新闻', '头条一览', '快讯', '首页', '头条', '一览', '新闻', ' - ', '：']
    for suffix in suffixes:
        if site_name.endswith(suffix):
            site_name = site_name[:-len(suffix)]
    
    return site_name.strip()
