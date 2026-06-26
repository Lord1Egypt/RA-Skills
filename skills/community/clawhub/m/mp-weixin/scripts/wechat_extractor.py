#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
WeChat Article Extractor - Python 版本
提取微信公众号文章的标题、作者、内容、发布时间等元数据

用法:
    python3 wechat_article_extractor.py <微信文章 URL>
    
示例:
    python3 wechat_article_extractor.py "https://mp.weixin.qq.com/s/xN1H5s66ruXY9s8aOd4Rcg"
"""

import sys
import json
import re
from datetime import datetime
from urllib.parse import urlparse, parse_qs

import requests
from bs4 import BeautifulSoup


class WeChatArticleExtractor:
    """微信公众号文章提取器"""
    
    HEADERS = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 MicroMessenger/7.0.20.1781(0x6700143B) NetType/WIFI MiniProgramEnv/Windows WindowsWechat/WMPF WindowsWechat(0x63090B11) XWEB/11233',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'sec-ch-ua': '"Not A(Brand";v="8", "Chromium";v="120", "WeChat";v="11.0"',
        'sec-ch-ua-mobile': '?1',
        'sec-ch-ua-platform': '"Android"',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'none',
        'Sec-Fetch-User': '?1',
        'Upgrade-Insecure-Requests': '1',
    }
    
    def __init__(self, timeout=30):
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update(self.HEADERS)
    
    def extract(self, url):
        """
        提取微信文章信息
        
        Args:
            url: 微信文章 URL
            
        Returns:
            dict: 提取结果
        """
        try:
            # 获取文章内容
            response = self.session.get(url, timeout=self.timeout, allow_redirects=True)
            response.encoding = 'utf-8'
            
            if response.status_code != 200:
                return {
                    'done': False,
                    'code': 1002,
                    'msg': f'请求失败，状态码：{response.status_code}'
                }
            
            html = response.text
            
            # 检查是否有验证码
            if '环境异常' in html or '验证码' in html:
                return {
                    'done': False,
                    'code': 2006,
                    'msg': '需要验证码验证，请稍后重试或使用已登录的会话'
                }
            
            # 解析 HTML
            soup = BeautifulSoup(html, 'lxml')
            
            # 提取文章元数据
            result = self._parse_article(soup, url)
            
            if not result:
                return {
                    'done': False,
                    'code': 1001,
                    'msg': '无法获取文章信息'
                }
            
            return {
                'done': True,
                'code': 0,
                'data': result
            }
            
        except requests.exceptions.Timeout:
            return {
                'done': False,
                'code': 1002,
                'msg': '请求超时'
            }
        except requests.exceptions.RequestException as e:
            return {
                'done': False,
                'code': 1002,
                'msg': f'请求失败：{str(e)}'
            }
        except Exception as e:
            return {
                'done': False,
                'code': 2008,
                'msg': f'系统出错：{str(e)}'
            }
    
    def _parse_article(self, soup, url):
        """解析文章内容"""
        result = {}
        
        # 提取文章标题
        title_tag = soup.find('h1', id='activity-name') or soup.find('h1', class_='rich_media_title')
        if title_tag:
            result['msg_title'] = title_tag.get_text(strip=True)
        else:
            # 尝试从 meta 标签获取
            meta_title = soup.find('meta', attrs={'property': 'og:title'})
            if meta_title and meta_title.get('content'):
                result['msg_title'] = meta_title['content'].strip()
            else:
                return None
        
        # 提取文章摘要
        meta_desc = soup.find('meta', attrs={'property': 'og:description'})
        if meta_desc and meta_desc.get('content'):
            result['msg_desc'] = meta_desc['content'].strip()
        else:
            result['msg_desc'] = ''
        
        # 提取封面图
        meta_image = soup.find('meta', attrs={'property': 'og:image'})
        if meta_image and meta_image.get('content'):
            result['msg_cover'] = meta_image['content'].strip()
        else:
            result['msg_cover'] = ''
        
        # 提取发布时间
        publish_time = None
        
        # 尝试从 em 标签获取
        em_tag = soup.find('em', class_='rich_media_meta_text')
        if em_tag:
            time_text = em_tag.get_text(strip=True)
            publish_time = self._parse_time(time_text)
        
        # 尝试从 meta 标签获取
        if not publish_time:
            meta_time = soup.find('meta', attrs={'property': 'article:published_time'})
            if meta_time and meta_time.get('content'):
                publish_time = self._parse_time(meta_time['content'])
        
        # 尝试从 script 中获取
        if not publish_time:
            script_tags = soup.find_all('script')
            for script in script_tags:
                if script.string and 'ct' in script.string:
                    match = re.search(r'"ct"\s*:\s*(\d+)', script.string)
                    if match:
                        timestamp = int(match.group(1))
                        publish_time = datetime.fromtimestamp(timestamp).strftime('%Y/%m/%d %H:%M:%S')
                        break
        
        result['msg_publish_time_str'] = publish_time or '未知'
        
        # 提取作者
        author_tag = soup.find('span', class_='rich_media_meta_nickname')
        if author_tag:
            result['msg_author'] = author_tag.get_text(strip=True)
        else:
            meta_author = soup.find('meta', attrs={'property': 'article:author'})
            if meta_author and meta_author.get('content'):
                result['msg_author'] = meta_author['content'].strip()
            else:
                result['msg_author'] = ''
        
        # 提取公众号信息
        account_name = soup.find('div', id='meta_content')
        if account_name:
            strong_tag = account_name.find('strong')
            if strong_tag:
                result['account_name'] = strong_tag.get_text(strip=True)
        else:
            # 尝试从其他位置获取
            js_content = soup.find('script', id='js_content')
            if js_content and js_content.string:
                match = re.search(r'account_nickname\s*=\s*["\']([^"\']+)["\']', js_content.string)
                if match:
                    result['account_name'] = match.group(1)
        
        if 'account_name' not in result:
            result['account_name'] = '未知公众号'
        
        result['account_alias'] = ''  # 微信号
        result['account_id'] = ''  # 原始 ID
        result['account_description'] = ''  # 功能介绍
        result['account_avatar'] = ''  # 头像
        
        # 提取文章内容
        content_div = soup.find('div', id='js_content') or soup.find('div', class_='rich_media_content')
        if content_div:
            # 保留 HTML 格式
            result['msg_content'] = str(content_div)
            result['msg_type'] = 'post'
        else:
            result['msg_content'] = ''
            result['msg_type'] = 'text'
        
        # 提取文章链接
        result['msg_link'] = url
        
        # 提取 URL 参数
        params = parse_qs(urlparse(url).query)
        result['msg_mid'] = params.get('mid', [''])[0]
        result['msg_idx'] = params.get('idx', [''])[0]
        result['msg_sn'] = params.get('sn', [''])[0]
        result['msg_biz'] = params.get('__biz', [''])[0]
        
        # 版权信息
        copyright_tag = soup.find('div', class_='rich_media_meta_rich_media_copyright')
        result['msg_has_copyright'] = copyright_tag is not None
        
        return result
    
    def _parse_time(self, time_str):
        """解析时间字符串"""
        if not time_str:
            return None
        
        # 尝试多种格式
        formats = [
            '%Y-%m-%d %H:%M',
            '%Y/%m/%d %H:%M:%S',
            '%Y年%m月%d日',
            '%Y-%m-%d',
            '%Y/%m/%d',
        ]
        
        for fmt in formats:
            try:
                dt = datetime.strptime(time_str.strip(), fmt)
                return dt.strftime('%Y/%m/%d %H:%M:%S')
            except ValueError:
                continue
        
        # 如果是时间戳
        try:
            timestamp = int(time_str)
            return datetime.fromtimestamp(timestamp).strftime('%Y/%m/%d %H:%M:%S')
        except (ValueError, OSError):
            pass
        
        return time_str


def main():
    """主函数"""
    if len(sys.argv) < 2:
        print('❌ 请提供微信文章 URL')
        print('用法：python3 wechat_article_extractor.py <微信文章 URL>')
        print('示例：python3 wechat_article_extractor.py "https://mp.weixin.qq.com/s/xN1H5s66ruXY9s8aOd4Rcg"')
        sys.exit(1)
    
    url = sys.argv[1]
    
    print(f'正在提取文章：{url}')
    print('---')
    
    extractor = WeChatArticleExtractor(timeout=30)
    result = extractor.extract(url)
    
    if result['done'] and result['code'] == 0:
        data = result['data']
        print('✅ 提取成功！')
        print('')
        print(f'📰 文章标题：{data.get("msg_title", "未知")}')
        print(f'👤 作者：{data.get("msg_author", "未署名")}')
        print(f'📢 公众号：{data.get("account_name", "未知")}')
        print(f'⏰ 发布时间：{data.get("msg_publish_time_str", "未知")}')
        print(f'📝 文章摘要：{data.get("msg_desc", "")[:100]}...')
        print(f'🖼️ 封面图：{data.get("msg_cover", "")}')
        print(f'📄 文章类型：{data.get("msg_type", "unknown")}')
        print(f'🔗 文章链接：{data.get("msg_link", url)}')
        print('')
        print('📊 公众号信息:')
        print(f'  - 名称：{data.get("account_name", "未知")}')
        print(f'  - 微信号：{data.get("account_alias", "未设置")}')
        print(f'  - 原始 ID: {data.get("account_id", "未设置")}')
        print(f'  - 功能介绍：{data.get("account_description", "未设置")}')
        print('')
        print(f'📝 文章内容长度：{len(data.get("msg_content", ""))} 字符')
        
        # 保存为 JSON 文件
        output_file = '/tmp/wechat_article.json'
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
        print(f'')
        print(f'💾 详细数据已保存到：{output_file}')
    else:
        print(f'❌ 提取失败：{result.get("msg", result.get("code", "未知错误"))}')
        sys.exit(1)


if __name__ == '__main__':
    main()
