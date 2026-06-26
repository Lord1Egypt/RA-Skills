#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "requests",
# ]
# ///
# -*- coding: utf-8 -*-

import re
import json
from config_manager import ConfigManager
from errors import JsonArgumentParser, SkillError


class PhoneManager:
    """手机号管理"""

    def __init__(self, session_key: str):
        self.config = ConfigManager()
        self.session_key = self.config.resolve_session_key(session_key)

    def get_phone(self) -> str:
        """获取手机号"""
        phone_config = self.config.get_phone_by_session_key(self.session_key)
        if not phone_config:
            raise SkillError("请提供 11 位手机号（例如 13800138000）")
        return phone_config

    def save_phone(self, phone_config: str) -> str:
        """保存手机号"""
        # 清洗
        clean_phone_config = re.sub(r'\D', '', phone_config)

        # 校验
        if len(clean_phone_config) != 11 or not clean_phone_config.startswith('1'):
            raise SkillError("手机号格式不正确，请输入 11 位中国大陆手机号后重试")

        success = self.config.set_phone_by_session_key(clean_phone_config, self.session_key)
        if success:
            return self.get_phone()
        else:
            raise SkillError("手机号保存未完成，请稍后重试")


if __name__ == "__main__":
    try:
        parser = JsonArgumentParser()
        parser.add_argument('--action', choices=['get', 'save'], required=True)
        parser.add_argument('--phone', help='Phone number for save')
        parser.add_argument('--session-key', required=True, help='Session key from current conversation context, e.g. agent:main:main')
        args = parser.parse_args()

        manager = PhoneManager(session_key=args.session_key)

        if args.action == 'get':
            phone = manager.get_phone()
            print(f"{phone}")
        elif args.action == 'save':
            if not args.phone:
                raise SkillError("请先提供手机号，再执行保存")

            phone = manager.save_phone(args.phone)
            print(f"{phone}")
        else:
            raise SkillError("当前操作不受支持，请使用 get 或 save")
    except SkillError as e:
        print(json.dumps(e.to_dict(), ensure_ascii=False))
        raise SystemExit(1)
    except Exception as e:
        wrapped = SkillError("手机号处理失败，请稍后重试", {"error": str(e)})
        print(json.dumps(wrapped.to_dict(), ensure_ascii=False))
        raise SystemExit(1)
