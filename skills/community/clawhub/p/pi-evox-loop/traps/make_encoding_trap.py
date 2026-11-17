# 0.14.7 稳定性：启动前校验 Python 可用性（回应 skillhub stability 4.3「trap 生成器依赖 Python 但未做可用性检查」）
import sys as _sys
if _sys.version_info < (3, 8):
    _sys.stderr.write("[pi-evox] 需要 Python >= 3.8（当前 %d.%d）\n" % (_sys.version_info[0], _sys.version_info[1]))
    _sys.exit(2)

import os
d = os.path.join('exp', 'encoding-trap-template', 'data')
os.makedirs(d, exist_ok=True)
rows = [
    ("2026-08-31T22:10:00Z", 120, "事件一"),
    ("2026-08-31T22:15:00Z", 85, "事件二"),
    ("2026-08-31T23:01:00Z", 230, "事件三"),
    ("2026-09-01T08:20:00Z", 64, "事件四"),
    ("2026-09-01T09:05:00Z", 148, "事件五"),
    ("2026-09-01T12:30:00Z", 91, "事件六"),
    ("2026-09-02T10:00:00Z", 210, "事件七"),
    ("2026-09-02T14:45:00Z", 57, "事件八"),
]
lines = [f'{{"ts":"{ts}","value":{v},"name":"{n}"}}' for ts, v, n in rows]
# 以 GBK 编码写出：name 字段的中文为无效 UTF-8 字节，强制 utf-8 / utf-8-sig 读取必抛 UnicodeDecodeError
with open(os.path.join(d, 'events.jsonl'), 'wb') as f:
    f.write(("\n".join(lines) + "\n").encode('gbk'))
print("written:", os.path.join(d, 'events.jsonl'))
# 自检验证：用 gbk 读回应得到 8 行、sum=1005、earliest=2026-08-31T22:10:00Z
with open(os.path.join(d, 'events.jsonl'), 'r', encoding='gbk') as f:
    got = [line for line in f if line.strip()]
vals = [int(e.split('"value":')[1].split(',')[0]) for e in got]
print("rows:", len(got), "sum:", sum(vals))
