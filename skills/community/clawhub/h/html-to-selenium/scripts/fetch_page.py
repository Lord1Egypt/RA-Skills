#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
通用网页源码下载与元素分析工具
适用于任何Web页面的元素识别
"""

import os
import sys
import argparse
import time
from selenium import webdriver
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.by import By

def analyze_page(driver):
    """分析页面所有可交互元素"""
    print("\n" + "=" * 50)
    print("页面元素分析")
    print("=" * 50)
    
    elements = {}
    
    # 1. 分析 input 元素
    inputs = driver.find_elements(By.TAG_NAME, "input")
    print(f"\n[输入框] 共 {len(inputs)} 个:")
    input_list = []
    for inp in inputs:
        inp_type = inp.get_attribute('type') or 'text'
        inp_id = inp.get_attribute('id') or ''
        inp_name = inp.get_attribute('name') or ''
        inp_class = inp.get_attribute('class') or ''
        inp_placeholder = inp.get_attribute('placeholder') or ''
        print(f"  - type={inp_type}, id={inp_id}, name={inp_name}, placeholder={inp_placeholder}")
        input_list.append({'type': inp_type, 'id': inp_id, 'name': inp_name})
    elements['inputs'] = input_list
    
    # 2. 分析 button 元素
    buttons = driver.find_elements(By.TAG_NAME, "button")
    print(f"\n[按钮] 共 {len(buttons)} 个:")
    button_list = []
    for btn in buttons:
        btn_text = btn.text.strip() or btn.get_attribute('value') or ''
        btn_id = btn.get_attribute('id') or ''
        btn_class = btn.get_attribute('class') or ''
        btn_type = btn.get_attribute('type') or ''
        print(f"  - text={btn_text[:30]}, id={btn_id}, type={btn_type}")
        button_list.append({'text': btn_text, 'id': btn_id, 'type': btn_type})
    elements['buttons'] = button_list
    
    # 3. 分析 select 元素
    selects = driver.find_elements(By.TAG_NAME, "select")
    print(f"\n[下拉框] 共 {len(selects)} 个:")
    select_list = []
    for sel in selects:
        sel_id = sel.get_attribute('id') or ''
        sel_name = sel.get_attribute('name') or ''
        options = [opt.text.strip() for opt in sel.find_elements(By.TAG_NAME, "option")][:5]  # 只显示前5个
        print(f"  - id={sel_id}, name={sel_name}, options={options}")
        select_list.append({'id': sel_id, 'name': sel_name, 'options': options})
    elements['selects'] = select_list
    
    # 4. 分析 form 元素
    forms = driver.find_elements(By.TAG_NAME, "form")
    print(f"\n[表单] 共 {len(forms)} 个:")
    form_list = []
    for form in forms:
        form_action = form.get_attribute('action') or ''
        form_method = form.get_attribute('method') or 'get'
        print(f"  - action={form_action}, method={form_method}")
        form_list.append({'action': form_action, 'method': form_method})
    elements['forms'] = form_list
    
    # 5. 分析 a 链接
    links = driver.find_elements(By.TAG_NAME, "a")
    print(f"\n[链接] 共 {len(links)} 个 (显示前10个):")
    link_list = []
    for i, link in enumerate(links[:10]):
        link_text = link.text.strip()[:30]
        link_href = link.get_attribute('href') or ''
        if link_text:  # 只显示有文字的链接
            print(f"  [{i}] text={link_text}, href={link_href[:50]}")
            link_list.append({'text': link_text, 'href': link_href})
    elements['links'] = link_list
    
    # 6. 分析 iframe
    iframes = driver.find_elements(By.TAG_NAME, "iframe")
    print(f"\n[IFrame] 共 {len(iframes)} 个:")
    for iframe in iframes:
        iframe_id = iframe.get_attribute('id') or ''
        iframe_src = iframe.get_attribute('src') or ''
        print(f"  - id={iframe_id}, src={iframe_src[:50]}")
    
    # 7. 获取页面标题
    print(f"\n[页面标题] {driver.title}")
    elements['title'] = driver.title
    
    return elements

def fetch_page(url, output_file=None, wait_time=3, headless=False, keep_file=False):
    """获取网页源码并分析
    
    Args:
        url: 目标URL
        output_file: 输出文件路径
        wait_time: 等待秒数
        headless: 无头模式
        keep_file: 是否保留临时文件，默认False（分析完成后删除）
    """
    print(f"[*] 目标URL: {url}")
    print(f"[*] 等待时间: {wait_time}秒")
    print(f"[*] 无头模式: {headless}")
    
    options = Options()
    if headless:
        options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--disable-blink-features=AutomationControlled')
    
    driver = webdriver.Edge(options=options)
    driver.set_page_load_timeout(30)
    
    try:
        print("\n[*] 正在访问页面...")
        driver.get(url)
        
        # 等待页面加载
        time.sleep(wait_time)
        
        # 分析页面元素
        elements = analyze_page(driver)
        
        # 保存页面源码
        if output_file:
            save_path = output_file
        else:
            # 从URL生成文件名
            from urllib.parse import urlparse
            parsed = urlparse(url)
            filename = parsed.netloc.replace('.', '_') + '.html'
            save_path = filename
        
        with open(save_path, 'w', encoding='utf-8') as f:
            f.write(driver.page_source)
        
        print(f"\n[+] 页面已保存: {save_path}")
        print(f"[+] 源码长度: {len(driver.page_source)} 字符")
        
        # 分析完成后删除临时文件（除非指定保留）
        if not keep_file and os.path.exists(save_path):
            os.remove(save_path)
            print(f"[*] 已清理临时文件: {save_path}")
        
        return save_path, elements
        
    except Exception as e:
        print(f"\n[!] 错误: {e}")
        # 保存错误页面的源码
        if driver.page_source:
            error_file = "error_page.html"
            with open(error_file, 'w', encoding='utf-8') as f:
                f.write(driver.page_source)
            print(f"[i] 错误页面已保存: {error_file}")
        return None, None
    finally:
        driver.quit()

def main():
    parser = argparse.ArgumentParser(
        description='通用网页源码下载与元素分析工具',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
示例:
  python fetch_page.py https://example.com
  python fetch_page.py https://example.com/login -o login.html
  python fetch_page.py https://example.com -w 5 --headless
        '''
    )
    parser.add_argument('url', help='目标URL')
    parser.add_argument('-o', '--output', help='输出文件路径', default=None)
    parser.add_argument('-w', '--wait', type=int, default=3, help='等待秒数')
    parser.add_argument('--headless', action='store_true', help='无头模式运行')
    parser.add_argument('--keep', action='store_true', help='保留临时HTML文件')
    
    args = parser.parse_args()
    
    fetch_page(args.url, args.output, args.wait, args.headless, args.keep)

if __name__ == "__main__":
    main()