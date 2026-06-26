#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
简单JIRA访问调试
"""

import time
import logging
from playwright.sync_api import sync_playwright

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def simple_debug():
    try:
        playwright = sync_playwright().start()
        browser = playwright.chromium.launch(headless=False)
        page = browser.new_page()
        
        # 访问JIRA
        url = "http://jira.51baiwang.com"
        logger.info(f"访问: {url}")
        
        try:
            page.goto(url, timeout=30000)
            logger.info(f"页面加载完成，状态码: 200")
            logger.info(f"页面标题: {page.title()}")
            logger.info(f"当前URL: {page.url}")
            
            # 等待并截图
            time.sleep(3)
            page.screenshot(path="/tmp/jira_page.png")
            logger.info("截图已保存到 /tmp/jira_page.png")
            
            # 检查页面内容
            content = page.content()
            if "login" in content.lower() or "登录" in content.lower():
                logger.info("页面包含登录相关元素")
            
            # 查找所有输入框
            inputs = page.query_selector_all("input")
            logger.info(f"找到 {len(inputs)} 个输入框")
            
            for i, input_elem in enumerate(inputs[:5]):  # 只显示前5个
                input_type = input_elem.get_attribute("type") or "unknown"
                input_id = input_elem.get_attribute("id") or "no-id"
                input_name = input_elem.get_attribute("name") or "no-name"
                logger.info(f"输入框 {i+1}: type={input_type}, id={input_id}, name={input_name}")
            
        except Exception as e:
            logger.error(f"访问页面失败: {str(e)}")
        
        # 保持页面打开以便观察
        logger.info("保持页面打开10秒...")
        time.sleep(10)
        
        browser.close()
        playwright.stop()
        
    except Exception as e:
        logger.error(f"调试失败: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    simple_debug()