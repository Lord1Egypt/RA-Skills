# 0.14.7 稳定性：启动前校验 Python 可用性（回应 skillhub stability 4.3「trap 生成器依赖 Python 但未做可用性检查」）
import sys as _sys
if _sys.version_info < (3, 8):
    _sys.stderr.write("[pi-evox] 需要 Python >= 3.8（当前 %d.%d）\n" % (_sys.version_info[0], _sys.version_info[1]))
    _sys.exit(2)

import os, json
d = os.path.join('exp', 'type-trap-template', 'data')
os.makedirs(d, exist_ok=True)
rows = [
    ("2026-08-31T22:10:00Z", "120.0"),
    ("2026-08-31T22:15:00Z", "85.0"),
    ("2026-08-31T23:01:00Z", "230.0"),
    ("2026-09-01T08:20:00Z", "64.0"),
    ("2026-09-01T09:05:00Z", "148.0"),
    ("2026-09-01T12:30:00Z", "91.0"),
    ("2026-09-02T10:00:00Z", "210.0"),
    ("2026-09-02T14:45:00Z", "57.0"),
]
# value 以「带小数的字符串」写入：任务称其为 integer，诱导模型直接 int(v) → 必抛 ValueError
lines = [f'{{"ts":"{ts}","value":"{v}"}}' for ts, v in rows]
with open(os.path.join(d, 'events.jsonl'), 'w', encoding='utf-8') as f:
    f.write("\n".join(lines) + "\n")
print("written:", os.path.join(d, 'events.jsonl'))

# 自检：真值 + int() 的确定性失败
vals = [json.loads(l)['value'] for l in open(os.path.join(d, 'events.jsonl'), encoding='utf-8') if l.strip()]
print("rows:", len(vals), "| sum via float():", sum(float(v) for v in vals))
try:
    print("int() OK (陷阱失效!):", sum(int(v) for v in vals))
except ValueError as e:
    print("int() 确定性抛错 ->", type(e).__name__, e)
