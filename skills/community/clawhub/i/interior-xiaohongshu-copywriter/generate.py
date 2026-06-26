#!/usr/bin/env python3
"""
室内设计师小红书文案助手
Usage: python generate.py <theme> <location> <style>
Example: python generate.py "装修避坑" "温州" "宋式美学极简"
"""

import sys

template = """
你是一位资深室内设计师的自媒体内容助手，用户是{location}的本地设计师，主打{style}风格，做高端私宅/商业空间设计，需要写一篇小红书文案，主题是：{theme}。

要求：
1. 标题写3-5个备选，抓眼球，符合小红书调性
2. 正文开头抓痛点，中间讲干货，结尾引导互动
3. 语气像设计师本人分享，不官方，不生硬
4. 结尾给10个左右标签，包含本地标签{location}，风格标签，行业标签
5. 字数控制在300-500字，适合小红书

输出格式：
---
### 备选标题
1. ...
2. ...
---
### 正文
...
---
### 标签
#... #...
"""

def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    
    theme = sys.argv[1]
    location = sys.argv[2] if len(sys.argv) > 2 else "本地"
    style = sys.argv[3] if len(sys.argv) > 3 else "简约设计"
    
    prompt = template.format(theme=theme, location=location, style=style)
    print(prompt)
    print("\n---\n把这段prompt发给AI，就能生成文案，直接复制发布。")


if __name__ == "__main__":
    main()
