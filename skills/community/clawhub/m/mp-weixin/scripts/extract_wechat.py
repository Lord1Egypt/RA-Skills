#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
微信公众号文章提取器 - 快速调用脚本
用法：python3 extract_wechat.py <微信文章 URL>
"""

import sys
import os

# 添加脚本路径
script_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, script_dir)

from wechat_extractor import WeChatArticleExtractor

def main():
    if len(sys.argv) < 2:
        print('❌ 请提供微信文章 URL')
        print('用法：python3 extract_wechat.py <微信文章 URL>')
        print('示例：python3 extract_wechat.py "https://mp.weixin.qq.com/s/xxx"')
        sys.exit(1)
    
    url = sys.argv[1]
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
        print(f'🔗 文章链接：{data.get("msg_link", url)}')
        print('')
        print(f'📝 文章内容长度：{len(data.get("msg_content", ""))} 字符')
    else:
        print(f'❌ 提取失败：{result.get("msg", result.get("code", "未知错误"))}')
        sys.exit(1)

if __name__ == '__main__':
    main()
