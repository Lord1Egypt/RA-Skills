#!/usr/bin/env python3
"""pinkr_crm.py
Python CLI to login to Pinkr CRM and call its API with Bearer token authentication.
Tokens are kept in memory for the duration of a single run.
All API calls use POST with JSON payloads.
"""

import argparse
import json
import os
import sys
import time
import datetime
from typing import Any, Dict, Optional

import requests
from formatters.member import MemberFormatter
from formatters.default import DefaultFormatter
try:
    from formatters.system_reminder import SystemReminderFormatter
except Exception:
    SystemReminderFormatter = None  # type: ignore


class SimpleFormatter:
    """Lightweight formatter wrapper to unify interface: format(raw)"""
    def __init__(self, func=None):
        self._func = func

    def format(self, raw):
        if self._func:
            return self._func(raw)
        return raw


class PinkrCrmClient:
    def __init__(self) -> None:
        # Load configuration from config.json if present, otherwise environment variables
        cfg = self.load_config()
        self.base_url = cfg.get('base_url', os.environ.get('PINKR_BASE_URL', 'https://crm.pinkr.com'))
        self.admin_name = cfg.get('admin_name') or os.environ.get('PINKR_ADMIN_NAME')
        self.password = cfg.get('password') or os.environ.get('PINKR_PASSWORD')

        self.session = requests.Session()
        # In-memory token cache (single run)
        self.token: Optional[str] = None
        self.token_expires_at: Optional[datetime.datetime] = None

        self.validate_config()
        # 进入格式化器注册阶段
        self._formatters: Dict[str, object] = {}
        self._register_default_formatters()
        # 初始化系统提醒格式化器（如果可用）
        self._system_reminder_formatter = SystemReminderFormatter() if SystemReminderFormatter else None
        # 载入字段映射配置并应用到格式化器
        self._load_and_apply_field_mappings()

    def _register_default_formatters(self) -> None:
        """注册默认的格式化器（当前阶段先针对会员接口实现）"""
        self._formatters['Crm/Customer/GetCustomers'] = MemberFormatter()
        self._formatters['Crm/Customer/GetCustomer'] = MemberFormatter()
        # Order related formatters (示例)
    

    def load_config(self) -> Dict[str, Any]:
        cfg: Dict[str, Any] = {}
        if os.path.exists('config.json'):
            try:
                with open('config.json', 'r', encoding='utf-8') as f:
                    cfg = json.load(f)
            except Exception:
                cfg = {}
        return cfg

    def _load_and_apply_field_mappings(self) -> None:
        """Load field mappings from config/field_mappings.json and apply to MemberFormatter instances"""
        mappings_path = os.path.join('config', 'field_mappings.json')
        if not os.path.exists(mappings_path):
            return
        try:
            with open(mappings_path, 'r', encoding='utf-8') as f:
                mappings = json.load(f)
        except Exception:
            return
        if not isinstance(mappings, dict):
            return
        for endpoint, mapping in mappings.items():
            if endpoint in self._formatters:
                fmt = self._formatters[endpoint]
                try:
                    # 检查是否为 MemberFormatter 实例
                    from formatters.member import MemberFormatter as MF
                    if isinstance(fmt, MF):
                        fmt.field_mappings.update(mapping)
                except Exception:
                    pass

    def validate_config(self) -> None:
        if not self.admin_name:
            raise ValueError('缺少 Admin 名称，请设置 PINKR_ADMIN_NAME 或在 config.json 中 admin_name')
        if not self.password:
            raise ValueError('缺少 Admin 密码，请设置 PINKR_PASSWORD 或在 config.json 中 password')

    def _login_once(self) -> str:
        url = self.base_url.rstrip('/') + '/Crm/Business/getToken'
        payload = {
            'admin_name': self.admin_name,
            'password': self.password,
        }
        # 简单的重试机制（不依赖外部依赖）
        for attempt in range(3):
            resp = self.session.post(url, json=payload, timeout=30)
            try:
                resp.raise_for_status()
            except Exception:
                if attempt < 2:
                    time.sleep(1 * (2 ** attempt))
                    continue
                raise
            data = resp.json()
            token = None
            if isinstance(data, dict):
                if 'token' in data:
                    token = data['token']
                elif 'data' in data and isinstance(data['data'], dict) and 'token' in data['data']:
                    token = data['data']['token']
                elif 'data' in data and isinstance(data['data'], dict) and 'access_token' in data['data']:
                    token = data['data']['access_token']
                # data could be a list of objects with token
                elif 'data' in data and isinstance(data['data'], list) and len(data['data']) > 0 and isinstance(data['data'][0], dict) and 'token' in data['data'][0]:
                    token = data['data'][0]['token']
                # alternate structure with code 200 and data as list
                elif 'code' in data and data.get('code') == 200 and isinstance(data.get('data'), list) and len(data['data']) > 0 and isinstance(data['data'][0], dict) and 'token' in data['data'][0]:
                    token = data['data'][0]['token']
            if not token:
                # Debug 观察原始响应结构
                try:
                    print("DEBUG_LOGIN_RESPONSE:", json.dumps(data) if isinstance(data, dict) else data, flush=True, file=sys.stderr)
                except Exception:
                    pass
                raise RuntimeError('登录响应中未发现 token')
            self.token = token
            self.token_expires_at = datetime.datetime.utcnow() + datetime.timedelta(hours=23)
            return token
        raise RuntimeError('Pinkr CRM 登录失败')

    def login(self) -> str:
        return self._login_once()

    def is_token_valid(self) -> bool:
        if self.token is None or self.token_expires_at is None:
            return False
        return datetime.datetime.utcnow() < self.token_expires_at

    def get_token(self) -> str:
        if self.is_token_valid():
            return self.token  # type: ignore[return-value]
        return self.login()

    def call_api(self, endpoint: str, data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        token = self.get_token()
        url = endpoint if endpoint.lower().startswith('http') else self.base_url.rstrip('/') + '/' + endpoint.lstrip('/')
        headers = {
            'Authorization': 'Bearer ' + token,
            'Content-Type': 'application/json',
            'Accept': 'application/json',
        }
        payload = data or {}

        # 所有接口均为 POST + JSON 请求体
        resp = self.session.post(url, json=payload, headers=headers, timeout=30)
        if resp.status_code == 401:
            # token 失效，重新登录并重试
            self.token = None
            token = self.login()
            headers['Authorization'] = 'Bearer ' + token
            resp = self.session.post(url, json=payload, headers=headers, timeout=30)
        resp.raise_for_status()
        try:
            raw = resp.json()
        except ValueError:
            raw = {"code": resp.status_code, "data": None, "message": resp.text}
        # 先应用系统提醒格式化器（若有），以处理 <system-reminder> 场景
        if getattr(self, '_system_reminder_formatter', None):
            transformed = self._system_reminder_formatter.format(raw)  # type: ignore
            if transformed != raw:
                return transformed
        # 使用格式化器进行输出（若已注册），否则返回原始数据
        formatter = getattr(self, '_formatters', None)
        if formatter and endpoint in formatter:
            return formatter[endpoint].format(raw)  # type: ignore[index]
        # 未注册格式化器的接口，直接返回原始数据
        return raw

    def clear_token_cache(self) -> None:
        self.token = None
        self.token_expires_at = None

    def test_connection(self) -> Dict[str, Any]:
        try:
            self.login()
            return {"success": True, "message": "连接成功"}
        except Exception as e:
            return {"success": False, "message": str(e)}

    # 格式化逻辑已迁移到 formatters 目录中，pinkr_crm.py 只负责加载、注册和调用格式化器


def parse_json_or_none(s: Optional[str]) -> Optional[Dict[str, Any]]:
    if not s:
        return None
    try:
        return json.loads(s)
    except Exception:
        return None


def main() -> int:
    parser = argparse.ArgumentParser(description='Pinkr CRM API CLI')
    subparsers = parser.add_subparsers(dest='command', required=True)

    login_p = subparsers.add_parser('login', help='Login to Pinkr CRM and cache token in memory')
    login_p.add_argument('--admin-name', help='Admin username (override config)')
    login_p.add_argument('--password', help='Admin password (override config)')

    api_p = subparsers.add_parser('api', help='Call Pinkr CRM API (POST with JSON)')
    api_p.add_argument('--endpoint', required=True, help='API endpoint path or full URL')
    api_p.add_argument('--data', help='JSON data string for request body')

    clear_p = subparsers.add_parser('clear-cache', help='Clear in-memory token cache')

    test_p = subparsers.add_parser('test-connection', help='Test login and connection')

    show_p = subparsers.add_parser('show-config', help='Show current configuration')

    args = parser.parse_args()
    try:
        client = PinkrCrmClient()
    except Exception as e:
        print(json.dumps({"error": str(e)}, ensure_ascii=False, indent=2))
        return 1

    if args.command == 'login':
        if args.admin_name:
            client.admin_name = args.admin_name
        if args.password:
            client.password = args.password
        token = client.login()
        print(json.dumps({"token": token}, ensure_ascii=False, indent=2))
        return 0

    if args.command == 'api':
        data = parse_json_or_none(args.data) if args.data else {}
        result = client.call_api(args.endpoint, data)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0

    if args.command == 'clear-cache':
        client.clear_token_cache()
        print(json.dumps({"status": "cache-cleared"}, ensure_ascii=False, indent=2))
        return 0

    if args.command == 'test-connection':
        res = client.test_connection()
        print(json.dumps(res, ensure_ascii=False, indent=2))
        return 0

    if args.command == 'show-config':
        print(json.dumps({
            'base_url': client.base_url,
            'admin_name': client.admin_name,
            'has_token': client.token is not None,
        }, ensure_ascii=False, indent=2))
        return 0

    return 0


if __name__ == '__main__':
    sys.exit(main())
