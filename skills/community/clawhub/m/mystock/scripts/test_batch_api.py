#!/usr/bin/env python3
import requests
import time

# 生成 50、100 个测试代码
base_codes = ['sh600519', 'sz000858', 'sz300750', 'sh601318', 'sz000001',
              'sh600036', 'sz002594', 'sh600276', 'sz000333', 'sh688599']

tests = [
    ('50个', base_codes * 5),
    ('100个', base_codes * 10),
]

print('继续测试更多数量...')
print('=' * 50)

for name, codes in tests:
    t0 = time.time()
    try:
        r = requests.get(f'https://qt.gtimg.cn/q={",".join(codes)}', timeout=15)
        elapsed = (time.time() - t0) * 1000
        count = r.text.count('=')
        print(f'{name:6}: 耗时 {elapsed:6.0f}ms, 返回 {count} 条')
    except Exception as e:
        print(f'{name:6}: 失败 - {e}')
