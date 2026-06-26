#!/usr/bin/env python3
"""
工具函数：随机延迟、弹窗处理等
"""

import time
import random


def human_delay(min_sec: float = 0.5, max_sec: float = 1.5):
    """模拟人类操作的随机延迟"""
    time.sleep(random.uniform(min_sec, max_sec))


def close_popups(page):
    """关闭页面上的弹窗"""
    try:
        popup = page.locator(".hna-pop-wrap-div, [class*='popup'], [class*='modal']").first
        if popup.is_visible(timeout=800):
            for btn_text in ["确定", "我知道了", "关闭", "×"]:
                try:
                    btn = popup.locator(f"text={btn_text}").first
                    if btn.is_visible():
                        btn.click()
                        human_delay(0.3, 0.8)
                        return True
                except:
                    pass
            page.mouse.click(10, 10)
            human_delay(0.3, 0.8)
            return True
    except:
        pass
    return False
