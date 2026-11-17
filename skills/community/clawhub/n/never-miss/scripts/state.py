# -*- coding: utf-8 -*-
"""state.json：各账户游标与全局状态（需求 §6.1）。原子写。"""
import json
import os
import tempfile
from datetime import datetime


def _state_path(root):
    return os.path.join(root, 'state.json')


def load(root):
    path = _state_path(root)
    if not os.path.exists(path):
        return {'accounts': {}}
    try:
        with open(path, 'r', encoding='utf-8') as f:
            st = json.load(f)
    except (json.JSONDecodeError, OSError) as e:
        raise RuntimeError('state.json 损坏: %s' % e)
    st.setdefault('accounts', {})
    return st


def save(root, st):
    os.makedirs(root, exist_ok=True)
    fd, tmp = tempfile.mkstemp(dir=root, prefix='.state-', suffix='.tmp')
    try:
        with os.fdopen(fd, 'w', encoding='utf-8') as f:
            json.dump(st, f, ensure_ascii=False, indent=2)
        os.replace(tmp, _state_path(root))
    except BaseException:
        if os.path.exists(tmp):
            os.unlink(tmp)
        raise


def account(st, email):
    """取（或初始化）账户状态：last_uid=0 表示尚未初始化游标。"""
    accs = st.setdefault('accounts', {})
    if email not in accs:
        accs[email] = {'last_uid': 0, 'uidvalidity': None, 'last_run': None}
    return accs[email]


def advance(st, email, last_uid, uidvalidity):
    acc = account(st, email)
    acc['last_uid'] = last_uid
    acc['uidvalidity'] = uidvalidity
    acc['last_run'] = datetime.now().astimezone().isoformat(timespec='seconds')
