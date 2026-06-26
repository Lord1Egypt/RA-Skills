#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
配置加载模块 (milb-email)

从 .env 文件读取配置，所有配置项必填，缺失时直接报错
只加载 EMAIL_* 前缀的配置
"""

from pathlib import Path
from typing import Dict


# 必填配置项列表
REQUIRED_CONFIG_KEYS = [
    'EMAIL_TO',
    'EMAIL_CC',
    'EMAIL_FROM',
    'EMAIL_SMTP_HOST',
    'EMAIL_SMTP_PORT',
    'EMAIL_SMTP_USER',
    'EMAIL_SMTP_PASSWORD',
]


def load_config() -> Dict:
    """
    从 .env 文件加载配置

    Returns:
        Dict: 配置字典，包含所有配置项
    """
    # 按优先级查找：当前工作目录 → ~/.config/milb-email/
    candidates = [
        Path.cwd() / '.env',
        Path.home() / '.config' / 'milb-email' / '.env',
    ]
    env_path = next((p for p in candidates if p.exists()), None)

    config = {}

    if env_path:
        with open(env_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#'):
                    if '=' in line:
                        key, value = line.split('=', 1)
                        config[key.strip()] = value.strip()

    return config


def get_config(key: str) -> str:
    """
    获取配置项，缺失时抛出异常

    Args:
        key: 配置键名

    Returns:
        配置值字符串

    Raises:
        ValueError: 配置项未在 .env 中设置
    """
    config = load_config()
    value = config.get(key)
    if not value:
        raise ValueError(f"配置项 {key} 未在 .env 中设置，请参考 .env.example")
    return value


def get_email_config() -> Dict:
    """
    获取邮件配置，缺失任何必填项则报错

    Returns:
        Dict: 邮件配置字典

    Raises:
        ValueError: 任何必填配置项缺失时
    """
    # 先验证必填项
    for key in REQUIRED_CONFIG_KEYS:
        get_config(key)  # 缺失会抛异常

    return {
        'to': get_config('EMAIL_TO').split(','),
        'cc': get_config('EMAIL_CC').split(','),
        'from': get_config('EMAIL_FROM'),
        'recipient_name': get_config('EMAIL_RECIPIENT_NAME'),
        'sender_name': get_config('EMAIL_SENDER_NAME'),
        'subject_prefix': get_config('EMAIL_SUBJECT_PREFIX'),
        'body_intro': get_config('EMAIL_BODY_INTRO'),
        'smtp_host': get_config('EMAIL_SMTP_HOST'),
        'smtp_port': get_config('EMAIL_SMTP_PORT'),
        'smtp_user': get_config('EMAIL_SMTP_USER'),
        'smtp_password': get_config('EMAIL_SMTP_PASSWORD'),
    }


if __name__ == '__main__':
    # 测试输出
    print("=== milb-email 配置加载测试 ===")
    try:
        email_cfg = get_email_config()
        print(f"收件人: {email_cfg['to']}")
        print(f"抄送人: {email_cfg['cc']}")
        print(f"发件人: {email_cfg['from']}")
        print(f"收件人称呼: {email_cfg['recipient_name']}")
        print(f"发件人签名: {email_cfg['sender_name']}")
        print(f"主题前缀: {email_cfg['subject_prefix']}")
    except ValueError as e:
        print(f"[ERROR] {e}")
