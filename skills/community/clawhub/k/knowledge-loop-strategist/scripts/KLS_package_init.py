#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""KLS 项目包初始化：把模板组复制成正式命名的项目包

用法:
    python KLS_package_init.py <父目录> [--name 项目名]

默认项目名: 产品拆解优化作业包
默认模板目录: 本脚本同级的 ../templates

做的事:
  1. 检查模板八件套是否齐全（缺任何一件即中止，不做半成品）
  2. 在父目录下建文件夹，文件夹名 = 项目名
  3. 按映射表复制，去掉 KLS-package- 前缀
  4. 把 项目信息.md 第一节的项目名改写为同一名字（保证两处一致）
  5. 打印结果清单

不做什么:
  - 不覆盖已存在的目标文件夹（防止误伤）
  - 不修改模板原件

退出码: 0=成功, 1=模板不全, 2=目标已存在, 3=用法错误
"""
import argparse
import io
import os
import shutil
import sys

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

    dest = os.path.join(args.parent, args.name)
    if os.path.exists(dest):
        print("FAIL 目标已存在: %s" % dest)
        print("换一个项目名，或先处理已有目录。脚本不覆盖。")
        return 2

    os.makedirs(dest)
    for src_name, dst_name in MAP:
        shutil.copy2(os.path.join(tpl, src_name), os.path.join(dest, dst_name))

    set_project_name(os.path.join(dest, "项目信息.md"), args.name)

    print("=" * 56)
    print("KLS 项目包已生成")
    print("=" * 56)
    print("文件夹: %s" % dest)
    print("项目名: %s（与文件夹名一致）" % args.name)
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
