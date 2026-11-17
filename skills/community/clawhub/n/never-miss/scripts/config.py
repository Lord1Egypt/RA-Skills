# -*- coding: utf-8 -*-
"""配置加载、默认值合并与校验（需求 §3）。密码只存 Keychain，配置中出现 password 键即拒绝。"""
import os
from datetime import datetime
from zoneinfo import ZoneInfo

import yamlmini

DEFAULTS = {
    'timezone': 'Asia/Shanghai',
    'schedule': {'time': '09:00'},
    'calendar': {'name': 'AI 提醒', 'location': 'local', 'per_account': False},
    'reminder': {'lead_minutes': 60, 'all_day_at': '09:00'},
    'mail': {'parse_ics_attachments': True, 'max_body_chars': 8000, 'strip_signatures': True},
    'paths': {'data': '~/.workbuddy/never-miss'},
    'accounts': [],
}

ACCOUNT_KEYS = {
    'label': None, 'host': None, 'port': 993, 'ssl': True, 'username': None,
    'folder': 'INBOX', 'max_per_run': 20, 'backfill_days': 0,
    'sender_allowlist': [], 'sender_blocklist': [], 'enabled': True,
}


class ConfigError(Exception):
    def __init__(self, message, hint=None):
        super().__init__(message)
        self.hint = hint


def data_root():
    """数据根目录：环境变量优先，否则默认 ~/.workbuddy/never-miss。"""
    env = os.environ.get('NEVER_MISS_DATA')
    if env:
        return os.path.expanduser(env)
    return os.path.expanduser('~/.workbuddy/never-miss')


def config_path(root=None):
    root = root or data_root()
    return os.path.join(root, 'config.yaml')


def _deep_merge(base, override):
    out = dict(base)
    for k, v in (override or {}).items():
        if k in base and isinstance(base[k], dict) and isinstance(v, dict):
            out[k] = _deep_merge(base[k], v)
        else:
            out[k] = v
    return out


def load(root=None):
    """加载并校验配置。不存在时返回纯默认值（供 init/doctor 提示）。"""
    root = root or data_root()
    path = config_path(root)
    raw = {}
    if os.path.exists(path):
        try:
            with open(path, 'r', encoding='utf-8') as f:
                raw = yamlmini.load(f.read())
        except yamlmini.YamlMiniError as e:
            raise ConfigError('config.yaml 语法不支持：%s' % e,
                              hint='请保持模板给定的缩进与结构，或运行 init 重新生成')
        if not isinstance(raw, dict):
            raise ConfigError('config.yaml 顶层应为键值映射')
        if raw.get('password') or any('password' in (str(k).lower()) for k in raw):
            raise ConfigError('配置中不允许出现 password 键',
                              hint='密码请经 "secret set <邮箱>" 存入 macOS Keychain')
        for acct in raw.get('accounts') or []:
            if not isinstance(acct, dict):
                raise ConfigError('accounts 列表项应为键值映射')
            if any('password' in str(k).lower() for k in acct):
                raise ConfigError('账户配置中不允许出现 password 键',
                                  hint='密码请经 "secret set <邮箱>" 存入 macOS Keychain')
    cfg = _deep_merge(DEFAULTS, raw)
    validate(cfg, root)
    return cfg


def validate(cfg, root=None):
    try:
        ZoneInfo(cfg['timezone'])
    except Exception:
        raise ConfigError('timezone 无效：%r' % cfg['timezone'])
    for t in (cfg['schedule']['time'], cfg['reminder']['all_day_at']):
        try:
            datetime.strptime(t, '%H:%M')
        except ValueError:
            raise ConfigError('时间格式应为 HH:MM：%r' % t)
    cal = cfg['calendar']
    if not cal.get('name'):
        raise ConfigError('calendar.name 不能为空')
    if cal.get('location') not in ('local', 'icloud'):
        raise ConfigError('calendar.location 只能是 local 或 icloud')
    for k in ('lead_minutes',):
        if not isinstance(cfg['reminder'].get(k), int) or cfg['reminder'][k] < 0:
            raise ConfigError('reminder.%s 应为非负整数' % k)
    m = cfg['mail']
    if not isinstance(m.get('max_body_chars'), int) or m['max_body_chars'] <= 0:
        raise ConfigError('mail.max_body_chars 应为正整数')
    # paths.data 仅作记录，须与实际数据目录一致（环境变量覆盖时跳过：env 即权威）
    if root is not None and not os.environ.get('NEVER_MISS_DATA'):
        declared = os.path.expanduser(str(cfg['paths'].get('data') or ''))
        if declared and os.path.normpath(declared) != os.path.normpath(root):
            raise ConfigError('paths.data(%s) 与实际数据目录(%s) 不一致' % (declared, root),
                              hint='config.yaml 必须位于数据目录内，请保持 paths.data 与之一致')
    # 账户校验
    seen = set()
    for i, acct in enumerate(cfg.get('accounts') or []):
        if not acct.get('host'):
            raise ConfigError('第 %d 个账户缺少 host' % (i + 1))
        if not acct.get('username'):
            raise ConfigError('第 %d 个账户缺少 username' % (i + 1))
        email = acct['username'].strip().lower()
        if email in seen:
            raise ConfigError('账户重复：%s' % email)
        seen.add(email)
        acct['username'] = acct['username'].strip()
        if not acct.get('label'):
            acct['label'] = acct['username']
        if not isinstance(acct.get('port'), int) or not (1 <= acct['port'] <= 65535):
            acct['port'] = 993
        if not isinstance(acct.get('max_per_run'), int) or acct['max_per_run'] <= 0:
            acct['max_per_run'] = 20
        if not isinstance(acct.get('backfill_days'), int) or acct['backfill_days'] < 0:
            acct['backfill_days'] = 0
        for key in ('sender_allowlist', 'sender_blocklist'):
            if not isinstance(acct.get(key), list):
                acct[key] = []
    return cfg


def account_by_email(cfg, email):
    email = (email or '').strip().lower()
    for acct in cfg.get('accounts') or []:
        if acct['username'].strip().lower() == email:
            return acct
    return None


def enabled_accounts(cfg):
    return [a for a in (cfg.get('accounts') or []) if a.get('enabled', True)]
