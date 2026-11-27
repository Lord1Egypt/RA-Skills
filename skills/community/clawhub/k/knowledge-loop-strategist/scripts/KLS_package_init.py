#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""KLS 项目包初始化：把模板组复制成正式命名的项目包

用法:
    python KLS_package_init.py <父目录> [--name 项目名]

默认项目名: 产品拆解优化作业包
默认模板目录: 本脚本同级的 ../templates

做的事:
  1. 检查模板八件套是否齐全（缺任何一件即中止，不做半成品）
  2. 检查四份正式文档落款是否含开包日期占位（模板与脚本须配套）
  3. 在父目录下建文件夹，文件夹名 = 项目名
  4. 按映射表复制，去掉 KLS-package- 前缀
  5. 把 项目信息.md 第一节的项目名改写为同一名字（保证两处一致）
  6. 在四份正式文档落款写入开包日期（脚本运行当天）
  7. 打印结果清单

不做什么:
  - 不覆盖已存在的目标文件夹（防止误伤）
  - 不修改模板原件

退出码: 0=成功, 1=模板不全或落款缺占位, 2=目标已存在, 3=用法错误

原子结构（依赖序）:
  ① 常量原子：DEFAULT_NAME → MAP（八件套全集）→ OPEN_DATE_FILES/OPEN_DATE_RE（正式文档落款子集与占位模式）
  ② 函数原子：set_project_name（身份同步）/ stamp_open_date（出生日期盖章）——单一职责，互不调用，只依赖①与标准库
  ③ 编排：main 按「预检 → 建目录 → 复制 → 身份同步 → 日期盖章 → 输出」的执行依赖序串联②
"""
import argparse
import io
import os
import re
import shutil
import sys
import time

# ── 原子层①：常量原子（零依赖，被②③引用）──
# DEFAULT_NAME → MAP：八件套全集（复制映射）；OPEN_DATE_*：其中四份正式文档的落款子集与占位模式（全集的子集）
DEFAULT_NAME = "产品拆解优化作业包"

MAP = [
    ("KLS-package-README.md", "产品拆解优化作业包（README）.md"),
    ("KLS-package-项目信息.md", "项目信息.md"),
    ("KLS-package-归属与许可.md", "归属与许可.md"),
    ("KLS-package-作业契约.md", "产品拆解优化作业契约.md"),
    ("KLS-package-作业契约.html", "产品拆解优化作业契约.html"),
    ("KLS-package-轮次页模板.md", "轮次页模板.md"),
    ("KLS-package-配对数据册.md", "配对数据册.md"),
    ("KLS-package-判据台账.md", "判据台账.md"),
]

# 正式文档落款子集（MAP 的四行子集）：开包日期占位所在，由 stamp_open_date 盖章
OPEN_DATE_FILES = [
    "KLS-package-README.md",
    "KLS-package-作业契约.md",
    "KLS-package-归属与许可.md",
    "KLS-package-作业契约.html",
]
OPEN_DATE_RE = re.compile(r"开包日期：_+（开包时写入实际日期）")

# ── 原子层②：函数原子（单一职责、互不调用，只依赖①与标准库）──
# 身份同步原子：项目名 = 文件夹名（KLS6-01 身份表）
def set_project_name(path, name):
    """把 项目信息.md 里 '| 项目名 | ... |' 这一行改成指定名字。"""
    with io.open(path, "r", encoding="utf-8") as f:
        lines = f.read().splitlines()
    for i, ln in enumerate(lines):
        if ln.startswith("| 项目名 |"):
            lines[i] = "| 项目名 | %s |" % name
            break
    else:
        raise RuntimeError("未找到「项目名」行，模板可能已变更")
    with io.open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")


# 出生日期盖章原子：开包日期 = 脚本运行当天（四份正式文档落款）
def stamp_open_date(path, date_str):
    """把落款占位「开包日期：______（开包时写入实际日期）」改写为实际开包日期。"""
    with io.open(path, "r", encoding="utf-8") as f:
        text = f.read()
    new_text, n = OPEN_DATE_RE.subn("开包日期：%s（开包日期）" % date_str, text)
    if n == 0:
        raise RuntimeError("未找到「开包日期」占位，模板可能已变更: %s" % path)
    with io.open(path, "w", encoding="utf-8") as f:
        f.write(new_text)


# ── 原子层③：编排 main（执行依赖序：预检① → 建目录 → 复制 → 身份同步② → 日期盖章② → 输出）──
def main():
    ap = argparse.ArgumentParser(description="把 KLS 项目包模板复制成正式项目包")
    ap.add_argument("parent", help="父目录（项目包将建在其下）")
    ap.add_argument("--name", default=DEFAULT_NAME,
                    help="项目名，同时作为文件夹名（默认: %s）" % DEFAULT_NAME)
    ap.add_argument("--templates", default=None, help="模板目录，默认取脚本同级 ../templates")
    args = ap.parse_args()

    tpl = args.templates or os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "templates")
    tpl = os.path.normpath(tpl)
    if not os.path.isdir(tpl):
        print("FAIL 模板目录不存在: %s" % tpl)
        return 3

    missing = [s for s, _ in MAP if not os.path.isfile(os.path.join(tpl, s))]
    if missing:
        print("FAIL 模板八件套不齐，缺 %d 件:" % len(missing))
        for m in missing:
            print("   - %s" % m)
        print("中止，不生成半成品。")
        return 1

    for s in OPEN_DATE_FILES:
        with io.open(os.path.join(tpl, s), "r", encoding="utf-8") as f:
            if not OPEN_DATE_RE.search(f.read()):
                print("FAIL 模板落款缺开包日期占位: %s" % s)
                print("中止，不生成半成品。模板与脚本须配套更新。")
                return 1

    dest = os.path.join(args.parent, args.name)
    if os.path.exists(dest):
        print("FAIL 目标已存在: %s" % dest)
        print("换一个项目名，或先处理已有目录。脚本不覆盖。")
        return 2

    os.makedirs(dest)
    for src_name, dst_name in MAP:
        shutil.copy2(os.path.join(tpl, src_name), os.path.join(dest, dst_name))

    set_project_name(os.path.join(dest, "项目信息.md"), args.name)

    open_date = time.strftime("%Y-%m-%d")
    for s, dst_name in MAP:
        if s in OPEN_DATE_FILES:
            stamp_open_date(os.path.join(dest, dst_name), open_date)

    print("=" * 56)
    print("KLS 项目包已生成")
    print("=" * 56)
    print("文件夹: %s" % dest)
    print("项目名: %s（与文件夹名一致）" % args.name)
    print("开包日期: %s（已写入 4 份正式文档落款）" % open_date)
    print("-" * 56)
    for _, dst_name in MAP:
        print("  %s" % dst_name)
    print("-" * 56)
    print("下一步:")
    print("  1. 打开 项目信息.md 第一节，补齐领域与三方参与人")
    print("  2. 过第二节开包清单（第一条是归属与许可三方签署）")
    print("  3. 按 作业包（README） 第四节的四步开工")
    return 0


if __name__ == "__main__":
    sys.exit(main())
