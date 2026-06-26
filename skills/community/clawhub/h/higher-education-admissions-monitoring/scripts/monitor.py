#!/usr/bin/env python3
"""高校招生通知监控 — v1.0.2"""
import sys
sys.dont_write_bytecode = True

import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import datetime
import re
import json
import os
import sys
import time

# ============= 配置 =============
MAX_RETRIES = 3
RETRY_DELAY = [2, 4, 8]  # 重试间隔（递增）
MAX_NOTICES = 10
REQUEST_TIMEOUT = 20
# ===============================

SKILL_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def load_schools():
    """从配置文件加载学校列表"""
    config_path = os.path.join(SKILL_DIR, 'schools.json')
    with open(config_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def fetch_with_retry(site_name, url, headers):
    """带重试机制的请求，返回(response, error_info)"""
    last_error = None
    for attempt in range(MAX_RETRIES):
        try:
            if attempt > 0:
                delay = RETRY_DELAY[min(attempt - 1, len(RETRY_DELAY) - 1)]
                print(f"    🔄 第{attempt + 1}次重试（等待{delay}秒）...")
                time.sleep(delay)

            response = requests.get(url, headers=headers, timeout=REQUEST_TIMEOUT)
            
            if response.status_code == 200:
                return response, None
            elif response.status_code == 403:
                return None, ("被禁止访问(403)", "⚠️ 网站可能开启了反爬机制，可尝试更换 User-Agent")
            elif response.status_code == 404:
                return None, ("页面不存在(404)", "⚠️ 网址可能已变更，请检查 schools.json 中的链接")
            elif response.status_code == 503:
                return None, ("服务暂时不可用(503)", "⚠️ 网站服务器可能正忙，稍后再试")
            else:
                last_error = (f"HTTP {response.status_code}", f"网站返回了异常状态码")
                
        except requests.exceptions.Timeout:
            last_error = ("请求超时", "⚠️ 网站响应时间过长，可能是网络问题或网站较慢")
        except requests.exceptions.ConnectionError:
            last_error = ("网络连接失败", "⚠️ 无法连接到该网站，请检查网络或网站是否正常运行")
        except requests.exceptions.RequestException as e:
            last_error = ("请求异常", f"⚠️ 具体错误: {str(e)[:60]}")
    
    return None, last_error


def parse_notices_from_soup(soup, url, site_name):
    """从BeautifulSoup对象中解析通知"""
    notices = []
    
    date_patterns = [
        r'\d{4}-\d{1,2}-\d{1,2}',      # 2026-03-17
        r'\d{4}年\d{1,2}月\d{1,2}日',   # 2026年3月17日
        r'\d{1,2}-\d{1,2}',            # 03-17
        r'\d{1,2}月\d{1,2}日',         # 3月17日
        r'\d{4}\.\d{1,2}',             # 2026.04
    ]
    
    keywords = [
        '招生', '复试', '录取', '硕士', '博士', '研究生',
        '简章', '考试', '报名', '调剂', '推免', '免试',
        '分数线', '成绩', '考点', '考场', '体检', '政审'
    ]
    
    garbage_keywords = [
        '版权所有', 'Copyright', '©', '电话：', '邮箱：',
        '传真：', '友情链接', '联系我们', '官方微信', '网站地图',
        '回到顶部', '站点导航', '首页', '概况', '简介',
        '快速导航', '设为首页', '加入收藏', 'RSS', '常见问题',
        '★',
    ]
    
    # 提取有效标题
    seen_titles = set()
    
    for link in soup.find_all('a'):
        text = link.get_text(strip=True)
        
        if not text or len(text) < 15 or len(text) > 120:
            continue
        
        # 检查关键词
        has_keyword = any(keyword in text for keyword in keywords)
        
        # 检查日期
        has_date = any(re.search(pattern, text) for pattern in date_patterns)
        
        # 过滤规则：
        # 有关键词的（如"硕士""复试""招生"），短标题也保留
        # 无关键词的，必须有日期且够长才保留
        if not has_keyword and not has_date:
            continue
        if not has_keyword and has_date and len(text) < 25:
            continue
        
        # 过滤垃圾
        is_garbage = any(garbage in text for garbage in garbage_keywords)
        if is_garbage:
            continue
        
        # 拼接链接
        href = link.get('href', '')
        if href and not href.startswith(('http://', 'https://')):
            href = urljoin(url, href)
        
        clean_text = ' '.join(text.split())
        
        # 先提取日期（从原始文本中提取，因为清理后会丢失日期前缀）
        matched_date = extract_date(clean_text)
        
        # 如果日期不在链接文本中，尝试从父元素附近找日期
        if not matched_date:
            parent = link.find_parent('li') or link.parent
            if parent:
                # 查找父元素内的日期标签
                nearby_dates = parent.find_all(['span', 'div', 'em'], class_=lambda c: c and ('time' in c.lower() or 'date' in c.lower()))
                for nd in nearby_dates:
                    nd_text = nd.get_text(strip=True)
                    nd_date = extract_date(nd_text)
                    if nd_date:
                        matched_date = nd_date
                        break
                # 如果还没找到，尝试找父元素中任何包含日期的文本
                if not matched_date:
                    parent_text = parent.get_text(strip=True)
                    if parent_text != clean_text:
                        pd = extract_date(parent_text)
                        if pd and pd != matched_date:
                            matched_date = pd
        
        # 清理标题（如清华的 "162026.04标题" → "标题"）
        clean_text = clean_tsinghua_title(clean_text)
        
        # 查重
        dedup_key = clean_text[:30]
        if dedup_key in seen_titles:
            continue
        seen_titles.add(dedup_key)
        
        notices.append({
            'title': clean_text,
            'link': href,
            'date': matched_date or datetime.datetime.now().strftime('%Y-%m-%d')
        })
        
        if len(notices) >= MAX_NOTICES:
            break
    
    return notices


def extract_date(text):
    """从文本中提取日期"""
    # 2026-03-17
    m = re.search(r'(\d{4})-(\d{1,2})-(\d{1,2})', text)
    if m:
        return f"{m.group(1)}-{m.group(2).zfill(2)}-{m.group(3).zfill(2)}"
    
    # 2026年3月17日
    m = re.search(r'(\d{4})年(\d{1,2})月(\d{1,2})日', text)
    if m:
        return f"{m.group(1)}-{m.group(2).zfill(2)}-{m.group(3).zfill(2)}"
    
    # 03-17（补当前年份）
    m = re.search(r'(\d{1,2})-(\d{1,2})(?![-\d])', text)
    if m:
        year = datetime.datetime.now().year
        return f"{year}-{m.group(1).zfill(2)}-{m.group(2).zfill(2)}"
    
    # 2026.04（清华格式）
    m = re.search(r'(\d{4})\.(\d{1,2})', text)
    if m:
        return f"{m.group(1)}-{m.group(2).zfill(2)}"
    
    return None


def clean_tsinghua_title(text):
    """清理清华页面的标题（去掉前面的日期数字粘连）"""
    # 匹配 "162026.04" 这种模式并去掉
    m = re.match(r'^(\d{1,2})(\d{4}\.\d{1,2})', text)
    if m:
        # 只保留标题部分
        rest = text[m.end():]
        if rest:
            return rest.strip()
    # 匹配 "2026.04标题" 模式
    m = re.match(r'^(\d{4}\.\d{1,2})', text)
    if m:
        rest = text[m.end():]
        if rest:
            return rest.strip()
    return text


def get_exact_notices_for_site(site_name, url):
    """为特定网站精确获取通知"""
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'Accept-Encoding': 'gzip, deflate',
        'Connection': 'keep-alive',
        'Cache-Control': 'max-age=0',
    }
    
    response, error_info = fetch_with_retry(site_name, url, headers)
    
    if response is None:
        error_type, error_hint = error_info
        return [{
            'title': f'⚠️ {error_type}',
            'link': '',
            'date': '',
            'error_hint': error_hint,
            'error_type': 'connection'
        }]
    
    try:
        response.encoding = 'utf-8'
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # 检测是否是动态加载的页面
        text_length = len(response.text)
        link_count = len(soup.find_all('a'))
        
        if link_count < 5 and text_length < 5000:
            return [{
                'title': '⚠️ 页面内容过少',
                'link': '',
                'date': '',
                'error_hint': '该网站可能使用了动态加载技术（JavaScript渲染），需要浏览器才能看到完整内容',
                'error_type': 'dynamic_page'
            }]
        
        notices = parse_notices_from_soup(soup, url, site_name)
        
        if not notices:
            return [{
                'title': '⚠️ 未找到相关通知',
                'link': '',
                'date': '',
                'error_hint': '网页已正常打开，但未解析到招生相关链接。可能是页面结构已变更',
                'error_type': 'no_data'
            }]
        
        return notices[:MAX_NOTICES]
        
    except Exception as e:
        return [{
            'title': f'⚠️ 解析失败',
            'link': '',
            'date': '',
            'error_hint': f'页面解析出错: {str(e)[:50]}。可能是网站改版了',
            'error_type': 'parse_error'
        }]


def list_available_schools(schools):
    """列出所有可选的学校"""
    print(f"\n📋 共有 {len(schools)} 所可监控学校：\n")
    for i, school in enumerate(schools, 1):
        sites_info = ", ".join([f"{s['site_name']}" for s in school['sites']])
        print(f"  {i}. {school['name']}（{sites_info}）")


def get_all_school_notices(school_names=None, save_to_file=False):
    """获取指定学校的通知"""
    all_schools = load_schools()
    
    if school_names:
        # 模糊匹配
        schools = [s for s in all_schools if any(name in s['name'] for name in school_names)]
        if not schools:
            print(f"\n⚠️ 未找到匹配的学校。")
            list_available_schools(all_schools)
            return []
    else:
        print("\n⚠️ 请指定要监控的学校，例如：")
        print("   python3 monitor.py --schools 深圳大学,武汉理工大学")
        print("   python3 monitor.py --schools 深圳大学,武汉理工大学 --save")
        list_available_schools(all_schools)
        return []
    
    all_results = []
    
    for school in schools:
        school_name = school['name']
        print(f"\n📡 正在查询: {school_name}")
        print("-" * 40)
        
        school_result = {
            'name': school_name,
            'sites': []
        }
        
        for site in school['sites']:
            site_name = site['site_name']
            url = site['url']
            print(f"  ▶ {site_name}: {url}")
            notices = get_exact_notices_for_site(site_name, url)
            school_result['sites'].append({
                'name': site_name,
                'url': url,
                'notices': notices
            })
            
            # 显示结果摘要
            if notices:
                if notices[0].get('error_type'):
                    print(f"  ❌ {notices[0]['title']}")
                    print(f"     {notices[0]['error_hint']}")
                else:
                    print(f"  ✅ 获取到 {len(notices)} 条通知")
            else:
                print(f"  ⚠️ 无结果")
        
        all_results.append(school_result)
    
    if save_to_file:
        filename = save_results_to_file(all_results)
        if filename:
            print(f"\n📁 结果已保存到: {filename}")
    
    return all_results


def save_results_to_file(results):
    """将结果保存为 Markdown 文件"""
    now = datetime.datetime.now()
    output_dir = os.path.join(SKILL_DIR, 'output')
    os.makedirs(output_dir, exist_ok=True)
    
    filename = f"招生监控报告_{now.strftime('%Y%m%d_%H%M%S')}.md"
    filepath = os.path.join(output_dir, filename)
    
    lines = []
    lines.append(f"# 🎓 高校招生通知监控报告")
    lines.append(f"")
    lines.append(f"**生成时间**: {now.strftime('%Y-%m-%d %H:%M:%S')}")
    lines.append(f"**来源**: [高校招生监控 Skill](skillhub.cn)")
    lines.append("")
    lines.append("---")
    lines.append("")
    
    total_schools = 0
    total_sites = 0
    total_notices = 0
    
    for school in results:
        total_schools += 1
        lines.append(f"## 🏫 {school['name']}")
        lines.append("")
        
        for site in school['sites']:
            total_sites += 1
            lines.append(f"### 📢 {site['name']}")
            lines.append(f"来源: {site['url']}")
            lines.append("")
            
            notices = site['notices']
            if notices:
                err_type = notices[0].get('error_type')
                if err_type == 'connection':
                    lines.append(f"| 状态 | 说明 |")
                    lines.append(f"|------|------|")
                    lines.append(f"| ❌ {notices[0]['title']} | {notices[0]['error_hint']} |")
                elif err_type == 'dynamic_page':
                    lines.append(f"| 状态 | 说明 |")
                    lines.append(f"|------|------|")
                    lines.append(f"| ⚠️ 动态页面 | {notices[0]['error_hint']} |")
                elif err_type == 'no_data':
                    lines.append(f"| 状态 | 说明 |")
                    lines.append(f"|------|------|")
                    lines.append(f"| ⚠️ 无数据 | {notices[0]['error_hint']} |")
                elif err_type == 'parse_error':
                    lines.append(f"| 状态 | 说明 |")
                    lines.append(f"|------|------|")
                    lines.append(f"| ⚠️ 解析失败 | {notices[0]['error_hint']} |")
                else:
                    lines.append(f"| # | 标题 | 日期 | 链接 |")
                    lines.append(f"|---|------|------|------|")
                    for i, notice in enumerate(notices, 1):
                        link_text = f"[查看]({notice['link']})" if notice['link'] else "无"
                        lines.append(f"| {i} | {notice['title']} | {notice['date']} | {link_text} |")
                    total_notices += len(notices)
            else:
                lines.append(f"_暂无通知_")
            
            lines.append("")
    
    lines.append("---")
    lines.append("")
    lines.append(f"**📈 统计**: {total_schools} 所学校 · {total_sites} 个网站 · {total_notices} 条通知")
    lines.append("")
    lines.append(f"_由高校招生监控 Skill 自动生成_")
    
    content = "\n".join(lines)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    
    return filepath


def format_results_for_display(results):
    """格式化结果用于显示"""
    output = []
    
    output.append(f"🎓 高校招生通知监控 - 精确获取")
    output.append(f"📅 时间: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    output.append("=" * 70)
    
    total_schools = 0
    total_sites = 0
    total_notices = 0
    
    for school in results:
        total_schools += 1
        output.append(f"\n🏫 {school['name']}")
        
        for site in school['sites']:
            total_sites += 1
            output.append(f"  📢 {site['name']}:")
            
            if site['notices']:
                err_type = site['notices'][0].get('error_type')
                if err_type:
                    output.append(f"    ❌ {site['notices'][0]['title']}")
                    output.append(f"       {site['notices'][0]['error_hint']}")
                else:
                    for i, notice in enumerate(site['notices'], 1):
                        date_str = f"[{notice['date']}]" if notice['date'] else ""
                        output.append(f"    {i}. {date_str} {notice['title']}")
                        if notice.get('link'):
                            output.append(f"        链接: {notice['link']}")
                        total_notices += 1
            else:
                output.append(f"    ⚠️ 未找到通知")
    
    output.append("\n" + "=" * 70)
    output.append(f"📈 统计: {total_schools}个学校, {total_sites}个网站, {total_notices}条通知")
    output.append("=" * 70)
    
    return "\n".join(output)


if __name__ == "__main__":
    # 解析参数
    school_names = None
    save_to_file = False
    
    for arg in sys.argv[1:]:
        if arg.startswith('--schools='):
            school_names = [s.strip() for s in arg.split('=', 1)[1].split(',')]
        elif arg == '--schools' and len(sys.argv) > sys.argv.index(arg) + 1:
            idx = sys.argv.index(arg)
            school_names = [s.strip() for s in sys.argv[idx + 1].split(',')]
        elif arg == '--save':
            save_to_file = True
        elif arg == '--help' or arg == '-h':
            print("""🎓 高校招生监控 v1.0.1

用法:
  python3 monitor.py                                    # 列出可选学校
  python3 monitor.py --schools 深圳大学,武汉理工大学     # 查询指定学校
  python3 monitor.py --schools 深圳大学 --save           # 查询并保存到文件

参数:
  --schools <学校名1,学校名2>   指定要查询的学校（用逗号分隔）
  --save                        将结果保存为 Markdown 文件
  --help / -h                   显示帮助信息
""")
            sys.exit(0)
    
    print("🎯 高校招生通知监控 v1.0.1")
    print("=" * 70)
    
    results = get_all_school_notices(school_names, save_to_file)
    
    if not results:
        sys.exit(0)
    
    formatted_output = format_results_for_display(results)
    
    print(f"\n{formatted_output}")
    print(f"\n✅ 运行完成")
