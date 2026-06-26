#!/usr/bin/env python3
"""
企业微信官方文档抓取脚本
基于 Playwright，系统抓取并整理成 Markdown 知识库
"""
import argparse
import json
import time
import re
from pathlib import Path
from datetime import datetime
from playwright.sync_api import sync_playwright

BASE_URL = "https://developer.work.weixin.qq.com"
OUTPUT_DIR = Path.home() / "workspace" / "knowledge-base" / "企业微信文档"

# 文档分类映射
CATEGORIES = {
    # 快速入门
    "90556": ("01-快速入门", "快速入门"),
    "90487": ("01-快速入门", "简易教程"),
    "90665": ("01-快速入门", "基本概念"),
    
    # 服务端API - 通讯录
    "90193": ("02-服务端API/通讯录管理", "成员管理概述"),
    "90195": ("02-服务端API/通讯录管理", "创建成员"),
    "90196": ("02-服务端API/通讯录管理", "读取成员"),
    "90197": ("02-服务端API/通讯录管理", "更新成员"),
    "90198": ("02-服务端API/通讯录管理", "删除成员"),
    "90205": ("02-服务端API/通讯录管理", "创建部门"),
    "90208": ("02-服务端API/通讯录管理", "获取部门列表"),
    
    # 服务端API - 身份验证
    "91039": ("02-服务端API/身份验证", "获取access_token"),
    "90930": ("02-服务端API/身份验证", "回调配置"),
    "91022": ("02-服务端API/身份验证", "构造网页授权链接"),
    "91023": ("02-服务端API/身份验证", "获取访问用户身份"),
    
    # 服务端API - 消息推送
    "90235": ("02-服务端API/消息推送", "发送应用消息"),
    "90238": ("02-服务端API/消息推送", "消息格式"),
    "90244": ("02-服务端API/消息推送", "群聊会话管理"),
    
    # 服务端API - 应用管理
    "90226": ("02-服务端API/应用管理", "应用管理概述"),
    "90227": ("02-服务端API/应用管理", "获取应用"),
    "90228": ("02-服务端API/应用管理", "设置应用"),
    
    # 服务端API - 素材管理
    "91054": ("02-服务端API/素材管理", "临时素材"),
    
    # 服务端API - 客户联系
    "92109": ("02-服务端API/客户联系", "客户联系概述"),
    "92113": ("02-服务端API/客户联系", "获取客户列表"),
    "92114": ("02-服务端API/客户联系", "获取客户详情"),
    "92117": ("02-服务端API/客户联系", "管理企业标签"),
    
    # 服务端API - 企业支付
    "90273": ("02-服务端API/企业支付", "企业红包"),
    "90278": ("02-服务端API/企业支付", "向员工付款"),
    
    # 服务端API - 会话内容存档
    "91360": ("02-服务端API/会话存档", "会话内容存档"),
    "99941": ("02-服务端API/会话存档", "会话内容存档概述"),
    
    # 客户端API - 小程序
    "91506": ("03-客户端API/小程序", "wx.qy.login"),
    "91519": ("03-客户端API/小程序", "wx.qy.openEnterpriseChat"),
    "90513": ("03-客户端API/小程序", "小程序JS-SDK概述"),
    
    # 客户端API - JS-SDK
    "90506": ("03-客户端API/JS-SDK", "JS-SDK签名算法"),
    "90508": ("03-客户端API/JS-SDK", "所有菜单项列表"),
    
    # 工具与资源
    "90305": ("04-工具资源", "样式库WeUI"),
    "90312": ("04-工具资源", "访问频率限制"),
    "90313": ("04-工具资源", "全局错误码"),
    
    # 附录
    "90968": ("99-附录", "附录"),
    "93221": ("99-附录", "更新日志"),
    "90623": ("99-附录", "联系我们"),
}

# 额外要抓取的文档ID（按类别）
EXTRA_DOCS = [
    # 客户端API - 小程序
    ("90513", "03-客户端API/小程序", "小程序JS-SDK概述"),
    ("90506", "03-客户端API/JS-SDK", "JS-SDK签名算法"),
    ("90508", "03-客户端API/JS-SDK", "所有菜单项列表"),
    ("90509", "03-客户端API/JS-SDK", "常见错误及解决方法"),
    
    # 更多服务端API
    ("90283", "02-服务端API/电子发票", "电子发票概述"),
    ("90284", "02-服务端API/电子发票", "查询电子发票"),
    
    # 会话存档
    ("99968", "02-服务端API/会话存档", "获取会话记录"),
    ("99992", "02-服务端API/会话存档", "会话存档回调事件"),
    
    # 客户联系
    ("92120", "02-服务端API/客户联系", "获取客户群列表"),
    ("92122", "02-服务端API/客户联系", "获取客户群详情"),
    ("92135", "02-服务端API/客户联系", "创建企业群发"),
    
    # 企业支付
    ("93665", "02-服务端API/企业支付", "对外收款概述"),
    
    # 附录
    ("90311", "99-附录", "与企业号接口差异"),
    ("90314", "99-附录", "企业规模与行业信息"),
    ("90315", "99-附录", "常见问题FAQ"),
]


def scrape_doc(path_id, timeout=30):
    """抓取单个文档"""
    url = f"{BASE_URL}/document/path/{path_id}"
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        
        page.set_extra_http_headers({
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
        })
        
        try:
            page.goto(url, wait_until='networkidle', timeout=timeout * 1000)
            time.sleep(3)  # 等待JS渲染
            
            # 获取标题
            title = page.title().replace(' - 文档 - 企业微信开发者中心', '').strip()
            
            # 获取正文内容
            content = page.locator('body').inner_text()
            
            # 获取URL（可能有跳转）
            final_url = page.url
            
            browser.close()
            
            return {
                'path_id': path_id,
                'url': final_url,
                'title': title,
                'content': content
            }
        except Exception as e:
            browser.close()
            return {
                'path_id': path_id,
                'error': str(e)
            }


def save_doc(doc_info, category_dir, title):
    """保存文档为Markdown"""
    if 'error' in doc_info:
        print(f"  ❌ {title}: {doc_info['error']}")
        return False
    
    # 构建文件路径
    safe_title = re.sub(r'[<>:"/\\|?*]', '_', title)
    file_path = category_dir / f"{safe_title}.md"
    
    # 构建Markdown内容
    md_content = f"""---
title: {title}
path_id: {doc_info['path_id']}
url: {doc_info['url']}
scrape_time: {datetime.now().isoformat()}
category: {category_dir.name}
---

# {title}

> 原文地址: {doc_info['url']}

## 内容

{doc_info['content']}

---

*最后抓取时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*
"""
    
    # 写入文件
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(md_content)
    
    print(f"  ✅ {title}")
    return True


def main():
    parser = argparse.ArgumentParser(description='企业微信官方文档抓取工具')
    parser.add_argument('--path-id', '-p', help='指定文档ID')
    parser.add_argument('--list', '-l', action='store_true', help='列出所有文档')
    parser.add_argument('--all', '-a', action='store_true', help='抓取所有文档')
    parser.add_argument('--category', '-c', help='指定分类目录')
    parser.add_argument('--title', '-t', help='文档标题')
    
    args = parser.parse_args()
    
    # 确保目录存在
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    for subdir in ["02-服务端API/通讯录管理", "02-服务端API/身份验证", 
                   "02-服务端API/消息推送", "02-服务端API/应用管理",
                   "02-服务端API/素材管理", "02-服务端API/客户联系",
                   "02-服务端API/企业支付", "02-服务端API/会话存档",
                   "02-服务端API/电子发票", "03-客户端API/小程序",
                   "03-客户端API/JS-SDK", "04-工具资源"]:
        (OUTPUT_DIR / subdir).mkdir(parents=True, exist_ok=True)
    
    # 列出所有文档
    if args.list:
        print(f"共 {len(CATEGORIES) + len(EXTRA_DOCS)} 个已配置文档:\n")
        for path_id, (cat, title) in list(CATEGORIES.items())[:20]:
            print(f"  {path_id}: {title} ({cat})")
        if len(CATEGORIES) > 20:
            print(f"  ... 还有 {len(CATEGORIES) - 20} 个")
        return
    
    # 抓取指定文档
    if args.path_id:
        if args.category and args.title:
            category_dir = OUTPUT_DIR / args.category
            category_dir.mkdir(parents=True, exist_ok=True)
        else:
            if args.path_id in CATEGORIES:
                category_dir = OUTPUT_DIR / CATEGORIES[args.path_id][0]
            else:
                category_dir = OUTPUT_DIR / "99-附录"
        
        print(f"抓取文档 {args.path_id}...")
        doc_info = scrape_doc(args.path_id)
        title = args.title or (CATEGORIES.get(args.path_id, ['', ''])[1] if args.path_id in CATEGORIES else '未命名')
        save_doc(doc_info, category_dir, title)
        return
    
    # 抓取所有文档
    if args.all:
        print(f"开始抓取企微文档，共 {len(CATEGORIES) + len(EXTRA_DOCS)} 个...\n")
        
        # 合并所有文档
        all_docs = {}
        for path_id, (cat, title) in CATEGORIES.items():
            all_docs[path_id] = (cat, title)
        for path_id, cat, title in EXTRA_DOCS:
            all_docs[path_id] = (cat, title)
        
        success = 0
        failed = 0
        
        for i, (path_id, (cat, title)) in enumerate(all_docs.items()):
            print(f"[{i+1}/{len(all_docs)}] 抓取 {title}...")
            
            category_dir = OUTPUT_DIR / cat
            category_dir.mkdir(parents=True, exist_ok=True)
            
            doc_info = scrape_doc(path_id)
            if save_doc(doc_info, category_dir, title):
                success += 1
            else:
                failed += 1
            
            time.sleep(1)  # 避免请求过快
        
        print(f"\n完成！成功: {success}, 失败: {failed}")
        return
    
    # 生成索引
    print("生成知识库索引...")
    generate_index()
    print("完成！")


def generate_index():
    """生成知识库索引"""
    index_content = """# 企业微信官方文档知识库

> 基于官方文档自动构建，包含服务端API、客户端API、工具资源等

## 目录结构

"""
    
    # 遍历目录
    for section_dir in sorted(OUTPUT_DIR.iterdir()):
        if section_dir.is_dir():
            index_content += f"\n### {section_dir.name}\n\n"
            
            for sub_dir in sorted(section_dir.iterdir()):
                if sub_dir.is_dir():
                    index_content += f"- **{sub_dir.name}**\n"
                    for md_file in sorted(sub_dir.glob("*.md")):
                        title = md_file.stem
                        index_content += f"  - [{title}]({md_file.relative_to(OUTPUT_DIR)})\n"
                else:
                    if sub_dir.suffix == '.md':
                        title = sub_dir.stem
                        index_content += f"- [{title}]({sub_dir.relative_to(OUTPUT_DIR)})\n"
    
    # 写入索引
    with open(OUTPUT_DIR / "README.md", 'w', encoding='utf-8') as f:
        f.write(index_content)


if __name__ == '__main__':
    main()
