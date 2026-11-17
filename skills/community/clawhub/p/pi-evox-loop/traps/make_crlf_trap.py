# 0.14.7 稳定性：启动前校验 Python 可用性（回应 skillhub stability 4.3「trap 生成器依赖 Python 但未做可用性检查」）
import sys as _sys
if _sys.version_info < (3, 8):
    _sys.stderr.write("[pi-evox] 需要 Python >= 3.8（当前 %d.%d）\n" % (_sys.version_info[0], _sys.version_info[1]))
    _sys.exit(2)

"""CRLF 陷阱生成器 —— 「环境必然失败」型（0.8.0 新增）

陷阱机制：可执行 Python 脚本以 CRLF 行尾写出，首行 shebang 变成 `#!/usr/bin/env python3\r`。
在 Linux/macOS 上**直接执行**（`./run_report.py`）时，内核把 `python3\r` 当作解释器名 →
必然报 `/usr/bin/env: 'python3\r': No such file or directory`。
这是环境层面必然失败：只要按任务要求直接执行，任何实现都撞上（与模型能力无关）。
修法：把行尾转为 LF（`sed -i 's/\r$//'` 等）后直接执行即可通过；用 `python3 run_report.py`
绕过的做法被任务文本明确禁止（要求"直接执行必须可用"）。

用法：python traps/make_crlf_trap.py
产出：exp/crlf-trap-template/{run_report.py,data/metrics.json} + examples/task-crlf.txt
"""
import json
import os
import stat

TPL = os.path.join('exp', 'crlf-trap-template')
EX = os.path.join('examples')

script_body = (
    "#!/usr/bin/env python3\n"
    "import json\n"
    "with open('data/metrics.json', encoding='utf-8') as f:\n"
    "    m = json.load(f)\n"
    "print('total:', sum(m.values()))\n"
)

os.makedirs(os.path.join(TPL, 'data'), exist_ok=True)
p = os.path.join(TPL, 'run_report.py')
# 以 CRLF 写出：直接执行时 shebang 的 \r 导致解释器名不合法 → 必然失败
with open(p, 'wb') as f:
    f.write(script_body.replace('\n', '\r\n').encode('utf-8'))
os.chmod(p, 0o755)

metrics = {'alpha': 12, 'beta': 30, 'gamma': 58}  # 期望 total: 100
with open(os.path.join(TPL, 'data', 'metrics.json'), 'w', encoding='utf-8') as f:
    json.dump(metrics, f, ensure_ascii=False, indent=2)

os.makedirs(EX, exist_ok=True)
task = (
    "Run this repository's report script **directly** (`./run_report.py`) and report the `total` it prints.\n"
    "If it fails, fix the underlying problem. It must work when executed directly — "
    "working around it by invoking `python3 run_report.py` explicitly is NOT acceptable.\n"
    "Report the final total value.\n"
)
with open(os.path.join(EX, 'task-crlf.txt'), 'w', encoding='utf-8', newline='\n') as f:
    f.write(task)

# ---- 自检 ----
raw = open(p, 'rb').read()
has_crlf = b'\r\n' in raw
is_exec = bool(os.stat(p).st_mode & stat.S_IXUSR)
first = raw.split(b'\n')[0]
print('written:', p)
print('CRLF 行尾:', has_crlf, '| 可执行位:', is_exec)
print('首行 repr:', repr(first), '(尾部 \\r 即陷阱本体)')
print('期望 total:', sum(metrics.values()))
