#!/usr/bin/env python3
"""rebuild_free.py —— 行业专项技能包：**确定性重建免费包引擎**（本产品的自证脚本，非门禁）。

为什么要它：免费包引擎不是手写的，而是
    付费版引擎（唯一真源） --tools/strip_free_engine.py 的 strip()--> 免费包引擎
只要有人改过付费版引擎，就必须重跑这一步；否则免费包里可能残留付费实现（或反过来缺东西）。
本脚本把这条链路做成**一条命令 + 全程自证**（任一步不过就非零退出，绝不静默通过）：

  1. 付费版引擎必须含付费块 MARKER（否则免费包会带上完整实现 ⇒ 拒绝继续）；
  2. 跑 strip()，打印删掉的付费函数清单；
  3. 写回免费包引擎；
  4. **残渣检查**：免费包里不许出现任何台账实现符号（buildLedger / ledgerCsv / exportLedger …）；
  5. `node --check` + 烟测（免费档 0 命中、status=success）+ 泄漏守卫 + 付费档烟测。

用法：
    python3 rebuild_free.py            # 重建并自证
    python3 rebuild_free.py --check    # 只自证（不写文件）：确认"免费包引擎 == strip(付费版引擎)"
"""
from __future__ import annotations

import argparse
import importlib.util
import pathlib
import re
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent.parent   # 仓库根（本脚本在 products/<包>/ 下）
PAID = ROOT / 'products' / 'skillpay-industry-vertical-pack' / 'scripts' / 'engine' / 'industry-vertical-pack-full.js'
FREE = ROOT / 'products' / 'industry-vertical-pack-free' / 'scripts' / 'engine' / 'industry-vertical-pack.js'

# 免费包里**不许出现**的付费实现符号（台账那一层的实现）
PAID_ONLY_SYMBOLS = (
    'buildLedger', 'ledgerMatrix', 'ledgerCommonIssues', 'ledgerActionItems',
    'ledgerMarkdown', 'ledgerCsv', 'csvCell', 'mdCell', 'riskSort', 'exportLedger',
    'PAID_SWITCH_KEYS',
)


def load(name: str, path: pathlib.Path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument('--check', action='store_true', help='只自证不写文件')
    a = ap.parse_args()

    strip_mod = load('stripmod', ROOT / 'tools' / 'strip_free_engine.py')
    paid_src = PAID.read_text(encoding='utf8')
    print(f'付费版引擎：{len(paid_src)} 字节 / {paid_src.count(chr(10)) + 1} 行')
    if strip_mod.MARKER not in paid_src:
        print('❌ 付费版里找不到付费块 MARKER —— 免费包会带上完整实现，拒绝继续')
        return 1

    new, removed = strip_mod.strip(paid_src)
    print(f'strip 删掉的付费函数（{len(removed)}）：{removed}')
    residue = [s for s in PAID_ONLY_SYMBOLS if re.search(r'\b' + s + r'\b', new)]
    print('strip 结果里的付费实现符号残留：', residue or '（无）')
    if a.check:
        same = FREE.exists() and FREE.read_text(encoding='utf8') == new
        print('免费包引擎 == strip(付费版引擎)：', same)
        return 0 if (same and not residue) else 1

    FREE.write_text(new, encoding='utf8')
    print(f'免费版引擎已写回：{len(new)} 字节 / {new.count(chr(10)) + 1} 行')

    rc = subprocess.run(['node', '--check', str(FREE)], capture_output=True, text=True)
    print('node --check rc =', rc.returncode, rc.stderr.strip()[:200])
    smoke_ok = strip_mod.smoke(FREE, 'free')
    print('烟测 free =', smoke_ok)
    leaker = load('leakmod', ROOT / 'tools' / 'free_engine_leak_check.py')
    probs = leaker.check_one(ROOT / 'products' / 'industry-vertical-pack-free')
    print('泄漏守卫：', probs or '✅ 不泄漏')
    print('付费包烟测：', end=' ')
    strip_mod.smoke(PAID, 'full')

    bad = bool(residue) or rc.returncode != 0 or not smoke_ok or bool(probs)
    print('结论：' + ('❌ 需要人工处理' if bad else '✅ 免费包是干净子集、付费包仍是完整档'))
    return 1 if bad else 0


if __name__ == '__main__':
    sys.exit(main())
