# 0.14.7 稳定性：启动前校验 Python 可用性（回应 skillhub stability 4.3「trap 生成器依赖 Python 但未做可用性检查」）
import sys as _sys
if _sys.version_info < (3, 8):
    _sys.stderr.write("[pi-evox] 需要 Python >= 3.8（当前 %d.%d）\n" % (_sys.version_info[0], _sys.version_info[1]))
    _sys.exit(2)

"""只读文件陷阱生成器 —— 「环境必然失败」型（0.8.0 新增）

陷阱机制：目标配置文件以只读权限（0444）写出。任务要求更新其中字段 →
任何写入实现（open('w') / 原地编辑 / sed -i 在此权限下）都必然失败，
报 `PermissionError: [Errno 13] Permission denied`（Linux）或 EACCES（Windows 只读属性）。
这是环境层面必然失败：权限位由文件系统强制，与模型能力无关。
修法：先恢复写权限（`chmod u+w config/settings.json`）再更新，最后可选恢复只读。

用法：python traps/make_readonly_trap.py
产出：exp/readonly-trap-template/config/settings.json（0444）+ examples/task-readonly.txt
"""
import json
import os

TPL = os.path.join('exp', 'readonly-trap-template')
EX = os.path.join('examples')

os.makedirs(os.path.join(TPL, 'config'), exist_ok=True)
p = os.path.join(TPL, 'config', 'settings.json')
settings = {'max_retries': 3, 'timeout_seconds': 30, 'log_level': 'info'}
with open(p, 'w', encoding='utf-8') as f:
    json.dump(settings, f, ensure_ascii=False, indent=2)
os.chmod(p, 0o444)  # 只读 → 写入必然失败

os.makedirs(EX, exist_ok=True)
task = (
    "Update `config/settings.json`: set `max_retries` to 5 and `timeout_seconds` to 60, "
    "keeping all other fields unchanged.\n"
    "Then read the file back and report its final JSON content.\n"
)
with open(os.path.join(EX, 'task-readonly.txt'), 'w', encoding='utf-8', newline='\n') as f:
    f.write(task)

# ---- 自检：确认只读且写入会失败 ----
mode = os.stat(p).st_mode & 0o777
write_blocked = False
try:
    with open(p, 'a', encoding='utf-8') as f:
        f.write('')
except PermissionError:
    write_blocked = True
print('written:', p)
print('权限:', oct(mode), '(期望 0o444)')
print('写入被拒绝:', write_blocked, '(True 即陷阱成立)')
print('原始字段:', settings)
