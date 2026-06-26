#!/usr/bin/env python3
"""分析快手上传页面的 DOM 结构"""

import json
import sys
sys.path.insert(0, '.')

from chrome_launcher import ensure_chrome, has_display
from kbs.cdp import Browser

def analyze_kuaishou_page():
    # 连接浏览器
    browser = Browser(host='127.0.0.1', port=9222)
    browser.connect()
    page = browser.get_or_create_page()
    
    # 导航到快手上传页面
    print("导航到快手上传页面...")
    page.navigate("https://cp.kuaishou.com/article/publish/video")
    page.wait_for_load(timeout=15.0)
    
    # 额外等待，确保动态内容加载
    import time
    print("等待页面渲染...")
    time.sleep(3)
    
    # 检查当前 URL
    current_url = page.evaluate("window.location.href")
    print(f"当前 URL: {current_url}")
    
    # 分析页面元素
    print("\n=== 分析页面元素 ===\n")
    
    result = page.evaluate('''
    () => {
        const results = {
            url: window.location.href,
            textareas: [],
            coverButtons: [],
            fileInputs: [],
            publishButtons: [],
            allButtons: []
        };
        
        // 找所有 textarea
        document.querySelectorAll('textarea').forEach((el, i) => {
            const rect = el.getBoundingClientRect();
            results.textareas.push({
                index: i,
                placeholder: el.placeholder || '',
                className: el.className,
                id: el.id,
                name: el.name,
                text: el.value ? el.value.substring(0, 100) : '',
                visible: rect.width > 0 && rect.height > 0,
                cssSelector: `textarea[${el.id ? 'id="'+el.id+'"' : 'class="'+el.className.split(' ')[0]+'"' }]`
            });
        });
        
        // 找所有按钮
        document.querySelectorAll('button, div[role="button"], span[role="button"]').forEach((el) => {
            const text = (el.innerText || el.textContent || '').trim();
            const rect = el.getBoundingClientRect();
            const info = {
                text: text.substring(0, 50),
                className: el.className,
                tagName: el.tagName,
                id: el.id,
                ariaLabel: el.getAttribute('aria-label'),
                visible: rect.width > 0 && rect.height > 0,
            };
            
            results.allButtons.push(info);
            
            // 特定关键词
            if (text.includes('封面') || text.includes('设置') || text.includes('上传') || text.includes('选择') || text.includes('本地')) {
                results.coverButtons.push(info);
            }
            
            if (text.includes('发布') || text.includes('发表')) {
                results.publishButtons.push(info);
            }
        });
        
        // 找所有 file input
        document.querySelectorAll('input[type="file"]').forEach((el, i) => {
            results.fileInputs.push({
                index: i,
                accept: el.accept,
                className: el.className,
                id: el.id,
                name: el.name,
                cssSelector: `input[type="file"]${el.id ? '[id="'+el.id+'"]' : ''}`
            });
        });
        
        return results;
    }
    ''')
    
    print(json.dumps(result, indent=2, ensure_ascii=False))
    
    browser.close()
    print("\n=== 分析完成 ===")

if __name__ == '__main__':
    analyze_kuaishou_page()
