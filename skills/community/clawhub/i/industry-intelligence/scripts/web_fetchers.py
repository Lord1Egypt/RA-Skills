import argparse
import sys
import json
import requests
from bs4 import BeautifulSoup

def fetch_dynamic_page(url, wait_time=3000):
    """使用Playwright获取动态渲染后的页面内容"""
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        print("错误: 缺少 playwright 库，请先执行 pip install playwright && playwright install", file=sys.stderr)
        sys.exit(1)

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(url)
        page.wait_for_load_state('networkidle')
        page.wait_for_timeout(wait_time)  # 额外等待动态内容加载
        content = page.content()
        browser.close()
        return content

def fetch_with_encoding(url):
    """处理各种编码的网页并转换为 UTF-8"""
    response = requests.get(url, timeout=15)
    
    # 尝试从响应头获取编码
    encoding = response.encoding
    
    # 如果是ISO-8859-1（默认值），尝试从HTML内容检测
    if encoding and encoding.lower() in ['iso-8859-1', 'latin-1']:
        soup = BeautifulSoup(response.content, 'html.parser')
        meta = soup.find('meta', attrs={'charset': True})
        if meta:
            encoding = meta.get('charset')
        else:
            meta = soup.find('meta', attrs={'http-equiv': 'Content-Type'})
            if meta and meta.get('content') and 'charset=' in meta.get('content'):
                encoding = meta.get('content').split('charset=')[-1].strip()
    
    # 常见中文编码映射
    encoding_map = {
        'gb2312': 'gb18030',  # gb18030兼容gb2312
        'gbk': 'gb18030',
    }
    encoding = encoding_map.get(encoding.lower(), encoding) if encoding else 'utf-8'
    
    # 解码并重新编码为UTF-8
    try:
        content = response.content.decode(encoding)
    except:
        content = response.content.decode('utf-8', errors='ignore')
    
    return content

def fetch_xueqiu_hot():
    """获取雪球热帖"""
    url = "https://xueqiu.com/statuses/hot/listV2.json?since_id=-1&max_id=-1&size=20"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)"
    }
    # Note: cookie is sometimes required for Xueqiu API but let's try without it or use a default session
    response = requests.get(url, headers=headers, timeout=15)
    return response.text

def extract_zhihu_answers(url):
    """提取知乎答案"""
    content = fetch_with_encoding(url)
    soup = BeautifulSoup(content, 'html.parser')
    answers = []
    for item in soup.select('.List-item'):
        title = item.select_one('.ContentItem-title')
        if title:
            answers.append(title.get_text(strip=True))
    return json.dumps(answers, ensure_ascii=False)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Industry Intelligence Web Fetchers")
    subparsers = parser.add_subparsers(dest="command", help="使用何种抓取方式")
    
    # dynamic
    parser_dynamic = subparsers.add_parser("dynamic", help="使用 playwright 获取动态页面")
    parser_dynamic.add_argument("url", help="目标URL")
    parser_dynamic.add_argument("--wait", type=int, default=3000, help="网络空闲后等待时长(ms)")
    
    # encoding
    parser_encoding = subparsers.add_parser("encoding", help="获取需处理编码(如GBK)的静态页面")
    parser_encoding.add_argument("url", help="目标URL")
    
    # xueqiu
    parser_xueqiu = subparsers.add_parser("xueqiu", help="获取雪球最新热帖")
    
    # zhihu
    parser_zhihu = subparsers.add_parser("zhihu", help="提取知乎问题答案")
    parser_zhihu.add_argument("url", help="知乎问题URL")
    
    args = parser.parse_args()
    
    if args.command == "dynamic":
        print(fetch_dynamic_page(args.url, args.wait))
    elif args.command == "encoding":
        print(fetch_with_encoding(args.url))
    elif args.command == "xueqiu":
        print(fetch_xueqiu_hot())
    elif args.command == "zhihu":
        print(extract_zhihu_answers(args.url))
    else:
        parser.print_help()
