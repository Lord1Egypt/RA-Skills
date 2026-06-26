#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Cookie管理器 - 管理头条Cookie登录
支持从配置文件读取Cookie文件路径
"""

import os
import json
from datetime import datetime


class CookieManager:
    """Cookie管理器"""

    def __init__(self, cookie_path=None, config_file=None):
        """
        初始化Cookie管理器

        Args:
            cookie_path: Cookie文件路径（优先级更高）
            config_file: 配置文件路径，包含 cookie_file 字段
        """
        # 优先使用直接传入的路径
        if cookie_path:
            self.cookie_path = cookie_path
        elif config_file and os.path.exists(config_file):
            # 从配置文件读取
            with open(config_file, 'r', encoding='utf-8') as f:
                config = json.load(f)
            self.cookie_path = config.get("cookie_file")
        else:
            self.cookie_path = None
        
        self.cookies = None
        if self.cookie_path:
            self.load_cookies()

    def load_cookies(self):
        """加载Cookie"""
        if self.cookie_path and os.path.exists(self.cookie_path):
            with open(self.cookie_path, 'r', encoding='utf-8') as f:
                self.cookies = json.load(f)
            print(f"[Cookie管理器] Cookie加载成功: {os.path.basename(self.cookie_path)}")
            return True
        else:
            print(f"[Cookie管理器] Cookie文件不存在或未指定: {self.cookie_path}")
            return False

    def get_cookies(self):
        """获取Cookie"""
        if self.cookies is None and self.cookie_path:
            self.load_cookies()
        return self.cookies

    def get_cookie_string(self):
        """获取Cookie字符串"""
        cookies = self.get_cookies()

        if cookies:
            # 检查Cookie格式：如果是数组格式，转换为字典
            if isinstance(cookies, list):
                cookie_dict = {}
                for cookie in cookies:
                    if isinstance(cookie, dict) and 'name' in cookie and 'value' in cookie:
                        cookie_dict[cookie['name']] = cookie['value']
                cookies = cookie_dict

            # 生成Cookie字符串
            if isinstance(cookies, dict):
                cookie_string = "; ".join([f"{k}={v}" for k, v in cookies.items()])
                return cookie_string
        return None

    def is_valid(self):
        """检查Cookie是否有效"""
        if self.cookies is None:
            return False

        # 检查Cookie格式：如果是数组，检查数组长度；如果是字典，检查键数量
        if isinstance(self.cookies, list):
            return len(self.cookies) > 0
        elif isinstance(self.cookies, dict):
            return len(self.cookies) > 0

        return False

    def refresh_cookies(self, new_cookies):
        """
        刷新Cookie

        Args:
            new_cookies: 新的Cookie字典
        """
        self.cookies = new_cookies
        self.save_cookies()

    def save_cookies(self):
        """保存Cookie到文件"""
        if self.cookies and self.cookie_path:
            with open(self.cookie_path, 'w', encoding='utf-8') as f:
                json.dump(self.cookies, f, ensure_ascii=False, indent=2)
            print(f"[Cookie管理器] Cookie保存成功: {os.path.basename(self.cookie_path)}")
            return True
        return False

    def get_headers(self):
        """
        获取包含Cookie的请求头

        Returns:
            dict: 请求头
        """
        cookie_string = self.get_cookie_string()
        if cookie_string:
            return {
                "Cookie": cookie_string,
                "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
            }
        return {}


def main():
    """测试Cookie管理器"""
    manager = CookieManager()

    print(f"Cookie有效: {manager.is_valid()}")
    print(f"Cookie数量: {len(manager.get_cookies()) if manager.get_cookies() else 0}")
    if manager.get_headers():
        print(f"请求头已准备")


if __name__ == "__main__":
    main()
