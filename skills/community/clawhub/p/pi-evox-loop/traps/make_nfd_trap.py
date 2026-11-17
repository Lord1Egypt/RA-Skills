# 0.14.7 稳定性：启动前校验 Python 可用性（回应 skillhub stability 4.3「trap 生成器依赖 Python 但未做可用性检查」）
import sys as _sys
if _sys.version_info < (3, 8):
    _sys.stderr.write("[pi-evox] 需要 Python >= 3.8（当前 %d.%d）\n" % (_sys.version_info[0], _sys.version_info[1]))
    _sys.exit(2)

"""Unicode NFD 陷阱生成器 —— 「环境必然失败」型（0.8.0 新增）

陷阱机制：磁盘上的文件名以 **NFD**（分解式，`cafe` + U+0301）写出，而任务文本以 **NFC**
（组合式，`café` U+00E9）给出该文件名。两者字节不同 → 直接按任务给的名字 `open()` 
必然 `FileNotFoundError`。这是环境层面必然失败：文件名由文件系统按字节存储，与模型能力无关。
修法：做 Unicode 规范化匹配（`unicodedata.normalize('NFC', ...)`）或列举目录按规范化名匹配。

用法：python traps/make_nfd_trap.py
产出：exp/nfd-trap-template/data/<NFD 文件名> + examples/task-nfd.txt（NFC 文件名）
"""
import json
import os
import unicodedata

TPL = os.path.join('exp', 'nfd-trap-template')
EX = os.path.join('examples')

nfc_name = 'café_report.json'                      # 任务文本给出的名字（NFC）
nfd_name = unicodedata.normalize('NFD', nfc_name)  # 磁盘上的实际文件名（NFD）

os.makedirs(os.path.join(TPL, 'data'), exist_ok=True)
p = os.path.join(TPL, 'data', nfd_name)
payload = {'store': 'café central', 'revenue': 4820, 'currency': 'CNY'}
with open(p, 'w', encoding='utf-8') as f:
    json.dump(payload, f, ensure_ascii=False, indent=2)

os.makedirs(EX, exist_ok=True)
# 任务文本用 NFC 名称（与磁盘 NFD 名称不同字节）
task = (
    f"Read `data/{nfc_name}` and report its `revenue` value.\n"
    "Use exactly the file name given above.\n"
)
with open(os.path.join(EX, 'task-nfd.txt'), 'w', encoding='utf-8', newline='\n') as f:
    f.write(task)

# ---- 自检：确认两种形式字节不同，且直接按 NFC 名打开失败 ----
same = (nfd_name == nfc_name)
direct_open_failed = False
try:
    open(os.path.join(TPL, 'data', nfc_name), encoding='utf-8')
except FileNotFoundError:
    direct_open_failed = True
print('written:', p)
print('磁盘名 repr:', repr(nfd_name), '(NFD)')
print('任务名 repr:', repr(nfc_name), '(NFC)')
print('两形式字节相同:', same, '(应为 False)')
print('按任务名直接打开失败:', direct_open_failed, '(True 即陷阱成立)')
print('期望 revenue:', payload['revenue'])
