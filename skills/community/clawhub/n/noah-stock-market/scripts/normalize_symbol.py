#!/usr/bin/env python3
import re
from typing import Optional


HK_PATTERN = re.compile(r'^(?:HK[-.]?)?(\d{5})$')
US_PATTERN = re.compile(r'^(?:US[-.]?)?([A-Z][A-Z0-9.-]{0,9})$')
NAME_HINTS = {
    '腾讯': 'HK-00700',
    '腾讯控股': 'HK-00700',
    'APPLE': 'US-AAPL',
    '苹果': 'US-AAPL',
    'NVIDIA': 'US-NVDA',
    '英伟达': 'US-NVDA',
    'TESLA': 'US-TSLA',
    '特斯拉': 'US-TSLA',
}

AMBIGUOUS_NAME_HINTS = {
    '阿里': {'HK': 'HK-09988', 'US': 'US-BABA'},
    '阿里巴巴': {'HK': 'HK-09988', 'US': 'US-BABA'},
    '百度': {'HK': 'HK-09888', 'US': 'US-BIDU'},
    '京东': {'HK': 'HK-09618', 'US': 'US-JD'},
    '哔哩哔哩': {'HK': 'HK-09626', 'US': 'US-BILI'},
    '蔚来': {'HK': 'HK-09866', 'US': 'US-NIO'},
    '小鹏': {'HK': 'HK-09868', 'US': 'US-XPEV'},
    '理想': {'HK': 'HK-02015', 'US': 'US-LI'},
}


def normalize_symbol(raw: str) -> Optional[str]:
    if not raw:
        return None
    s = raw.strip().upper()

    if raw.strip() in NAME_HINTS:
        return NAME_HINTS[raw.strip()]
    if s in NAME_HINTS:
        return NAME_HINTS[s]

    hk = HK_PATTERN.match(s)
    if hk:
        return f'HK-{hk.group(1)}'

    us = US_PATTERN.match(s)
    if us and not s.isdigit():
        return f'US-{us.group(1)}'

    return None


if __name__ == '__main__':
    samples = ['00700', 'HK-00700', 'aapl', 'US-AAPL', '腾讯控股', '苹果', '英伟达']
    for item in samples:
        print(item, '->', normalize_symbol(item))
