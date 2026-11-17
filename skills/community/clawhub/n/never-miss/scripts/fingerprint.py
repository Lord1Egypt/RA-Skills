# -*- coding: utf-8 -*-
"""内容指纹 → 事件 UID（跨账户去重的核心，需求 §6.2）。"""
import hashlib
import re
import unicodedata


def normalize(s):
    """规范化：NFC / 去首尾空白 / 折叠连续空白 / casefold。"""
    if not s:
        return ''
    s = unicodedata.normalize('NFC', str(s))
    s = re.sub(r'\s+', ' ', s).strip()
    return s.casefold()


def canonical_start(start_iso):
    """规范化时间字符串（datetime → 标准 isoformat；日期串保持原样）。"""
    from datetime import datetime
    s = str(start_iso).strip()
    if re.fullmatch(r'\d{4}-\d{2}-\d{2}', s):
        return s  # 全天事件的纯日期
    try:
        return datetime.fromisoformat(s).isoformat()
    except ValueError:
        return s


def uid_of(title, start_iso, location=''):
    """UID = nm-<sha1[:12]>@never-miss.local，与账户无关（需求 §6.2）。"""
    payload = '|'.join([
        normalize(title),
        canonical_start(start_iso),
        normalize(location),
    ])
    fp = hashlib.sha1(payload.encode('utf-8')).hexdigest()[:12]
    return 'nm-%s@never-miss.local' % fp
