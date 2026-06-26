#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
JIRA登录调试脚本
用于调试JIRA登录问题
"""

import os
import sys
import time
import logging
from playwright.sync_api import sync_playwright

# 配置日志
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

def debug_jira_login():
    """调试JIRA登录"""
    logger.info("🚀 开始JIRA登录调试")
    
    try:
        playwright = sync_playwright().start()
        browser = playwright.chromium.launch(
            headless=False,  # 使用有头模式以便观察
            args=['--disable-blink-features=AutomationControlled']
        )
        
        # 创建上下文
        context = browser.new_context(
            viewport={'width': 1920, 'height': 1080},
            user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
        )
        
        page = context.new_page()
        logger.info("浏览器初始化完成")
        
        # 访问JIRA
        jira_url = "http://jira.51baiwang.com"
        logger.info(f"正在访问JIRA: {jira_url}")
        
        page.goto(jira_url, wait_until='networkidle')
        time.sleep(3)
        
        # 截图当前页面
        screenshot_path = os.path.join(os.path.dirname(__file__), '..', 'logs', 'jira_login_page.png')
        page.screenshot(path=screenshot_path, full_page=True)
        logger.info(f"页面截图已保存: {screenshot_path}")
        
        # 检查页面内容
        logger.info("检查页面内容...")
        page_content = page.content()
        
        # 检查登录表单
        login_form_selectors = [
            '#login-form',
            '#login',
            'form[action*="login"]',
            'input[name="os_username"]',
            'input[name="username"]',
            '#login-form-username'
        ]
        
        for selector in login_form_selectors:
            count = page.locator(selector).count()
            if count > 0:
                logger.info(f"找到登录表单元素: {selector} (数量: {count})")
        
        # 检查是否已登录
        user_elements = page.locator('#header-details-user-fullname')
        if user_elements.count() > 0:
            logger.info("检测到已登录状态")
            username = user_elements.inner_text()
            logger.info(f"当前登录用户: {username}")
        else:
            logger.info("未检测到登录状态")
            
            # 尝试查找用户名输入框
            username_selectors = [
                '#login-form-username',
                '#username',
                'input[name="os_username"]',
                'input[name="username"]',
                'input[type="text"][id*="user"]',
                'input[type="text"][name*="user"]'
            ]
            
            for selector in username_selectors:
                elements = page.locator(selector)
                count = elements.count()
                if count > 0:
                    logger.info(f"找到用户名输入框: {selector}")
                    # 尝试输入用户名
                    try:
                        elements.first.fill("liuwei1")
                        logger.info(f"已输入用户名到 {selector}")
                    except Exception as e:
                        logger.error(f"输入用户名失败: {str(e)}")
            
            # 尝试查找密码输入框
            password_selectors = [
                '#login-form-password',
                '#password',
                'input[name="os_password"]',
                'input[name="password"]',
                'input[type="password"]'
            ]
            
            for selector in password_selectors:
                elements = page.locator(selector)
                count = elements.count()
                if count > 0:
                    logger.info(f"找到密码输入框: {selector}")
                    # 尝试输入密码
                    try:
                        elements.first.fill("Lw@123456")
                        logger.info(f"已输入密码到 {selector}")
                    except Exception as e:
                        logger.error(f"输入密码失败: {str(e)}")
            
            # 尝试查找登录按钮
            submit_selectors = [
                '#login-form-submit',
                '#login-submit',
                'input[type="submit"][value*="登录"]',
                'input[type="submit"][value*="Login"]',
                'button[type="submit"]',
                '.login-button'
            ]
            
            for selector in submit_selectors:
                elements = page.locator(selector)
                count = elements.count()
                if count > 0:
                    logger.info(f"找到登录按钮: {selector}")
                    # 截图
                    page.screenshot(path=os.path.join(os.path.dirname(__file__), '..', 'logs', 'before_login.png'))
                    
                    # 尝试点击
                    try:
                        elements.first.click()
                        logger.info(f"已点击登录按钮: {selector}")
                        time.sleep(3)
                        
                        # 检查登录是否成功
                        if page.locator('#header-details-user-fullname').count() > 0:
                            logger.info("登录成功！")
                        else:
                            logger.info("登录后状态检查...")
                            page.screenshot(path=os.path.join(os.path.dirname(__file__), '..', 'logs', 'after_login.png'))
                    except Exception as e:
                        logger.error(f"点击登录按钮失败: {str(e)}")
        
        # 等待一段时间观察
        logger.info("等待10秒观察页面...")
        time.sleep(10)
        
        # 最终截图
        final_screenshot = os.path.join(os.path.dirname(__file__), '..', 'logs', 'final_page.png')
        page.screenshot(path=final_screenshot, full_page=True)
        logger.info(f"最终页面截图: {final_screenshot}")
        
        # 输出页面标题和URL
        logger.info(f"页面标题: {page.title()}")
        logger.info(f"当前URL: {page.url}")
        
        # 清理资源
        page.close()
        context.close()
        browser.close()
        playwright.stop()
        
        logger.info("调试完成")
        
    except Exception as e:
        logger.error(f"调试过程中发生错误: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    debug_jira_login()