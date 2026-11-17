# 0.14.7 稳定性：启动前校验 Python 可用性（回应 skillhub stability 4.3「trap 生成器依赖 Python 但未做可用性检查」）
import sys as _sys
if _sys.version_info < (3, 8):
    _sys.stderr.write("[pi-evox] 需要 Python >= 3.8（当前 %d.%d）\n" % (_sys.version_info[0], _sys.version_info[1]))
    _sys.exit(2)

import os, json
d = os.path.join('exp', 'json-trap-template', 'data')
os.makedirs(d, exist_ok=True)
rows = [
    ("2026-08-31T22:10:00Z", 120),
    ("2026-08-31T22:15:00Z", 85),
    ("2026-08-31T23:01:00Z", 230),
    ("2026-09-01T08:20:00Z", 64),
    ("2026-09-01T09:05:00Z", 148),
    ("2026-09-01T12:30:00Z", 91),
    ("2026-09-02T10:00:00Z", 210),
    ("2026-09-02T14:45:00Z", 57),
]
lines = [f'{{"ts":"{ts}","value":{v}}}' for ts, v in rows]
# 末尾追加一行「坏 JSON」（缺少右花括号）——任何 JSON 解析器遇到它都必然抛错（环境必然失败，非模型犯错）
lines.append('{"ts":"2026-09-03T00:00:00Z","value":999')
with open(os.path.join(d, 'events.jsonl'), 'w', encoding='utf-8') as f:
    f.write("\n".join(lines) + "\n")
print("written:", os.path.join(d, 'events.jsonl'))

# 自检：真值（跳过坏行）+ 坏行必然解析失败
good = 0
total = 0
first_ts = None
bad_err = None
for line in open(os.path.join(d, 'events.jsonl'), encoding='utf-8'):
    s = line.strip()
    if not s:
        continue
    try:
        o = json.loads(s)
        good += 1
        total += o['value']
        if first_ts is None or o['ts'] < first_ts:
            first_ts = o['ts']
    except json.JSONDecodeError as e:
        bad_err = f"{type(e).__name__}: {e}"
print(f"有效行={good}  sum={total}  earliest={first_ts}")
print("坏行必然触发 ->", bad_err)
