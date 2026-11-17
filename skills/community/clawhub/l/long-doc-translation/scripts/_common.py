#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
_common.py — 各脚本共用的「友好错误」与参数校验。

为什么需要它：
  长篇翻译流水线里最危险的失败不是报错，而是**静默的假通过** ——
  目录路径写错时 glob 返回空，质检脚本会打印「0 个片段」然后每项都 ✅，
  使用者以为全书质检合格，实际什么都没查。

原则：凡是「使用者的操作失误」，都必须给出【可执行的下一步】，
      而不是抛 traceback，更不能静默输出全绿。
"""
import os
import sys
import glob

try:
    from _common_err import Lang
except Exception:
    pass


def die(msg, *hints):
    """打印友好错误 + 修复建议后退出（退出码 1）。"""
    print("\n[出错] " + msg, file=sys.stderr)
    for h in hints:
        print("   → " + h, file=sys.stderr)
    sys.exit(1)


def warn(msg):
    """非致命告警。"""
    print("[提醒] " + msg, file=sys.stderr)


def opt(args, name, default=None, cast=str, usage=""):
    """安全取 --name VALUE：缺值时友好报错，而非 IndexError 崩溃。"""
    if name not in args:
        return default
    i = args.index(name)
    if i + 1 >= len(args):
        die(f"选项 {name} 后面缺少取值。",
            f"正确写法：{name} <值>",
            usage or "例：python 本脚本.py <chunks_dir> --expect 140")
    try:
        return cast(args[i + 1])
    except (TypeError, ValueError):
        die(f"选项 {name} 的取值无法解析：{args[i + 1]!r}",
            f"期望类型：{cast.__name__}",
            usage or "")


def ensure_chunks(d, ext=".md", allow_empty=False, extra_skip=()):
    """校验译文片段目录：存在 + 含目标后缀文件。返回排序后的文件列表。

    extra_skip: 额外要排除的文件名（如 '04_index_003.md'）
    """
    if not d:
        die("未指定译文片段目录。",
            "用法：python 本脚本.py <chunks_dir>",
            "例：python qa_check.py output/chunks")

    if not os.path.isdir(d):
        die(f"目录不存在：{d}",
            "· 检查路径拼写，以及当前工作目录是否正确（相对路径是相对命令行的）",
            "· 路径含空格请加引号：\"C:/my project/chunks\"",
            "· 项目还没建？先跑：python init_project.py <项目目录>")

    files = sorted(glob.glob(os.path.join(d, "*" + ext)))
    files = [f for f in files
             if "_redundant" not in f
             and os.path.basename(f) not in extra_skip]

    if not files and not allow_empty:
        die(f"目录里没有 *{ext} 文件：{d}",
            f"· 确认译文是否放在该目录（期望一批 {ext} 片段文件）",
            f"· 若你的片段是别的后缀，加 --ext .txt 等试试",
            "· 项目还没起步？先跑：python init_project.py <项目目录>",
            "· 只想先看看报告长什么样？本目录需先有片段，无法空跑")

    return files


def safe_read(path, note=""):
    """读文本文件，失败时友好提示而非抛异常。"""
    try:
        with open(path, encoding="utf-8", errors="ignore") as f:
            return f.read()
    except OSError as e:
        die(f"读取文件失败：{path}",
            f"系统信息：{e}",
            "检查文件权限，或是否被其他程序占用" + (f"（{note}）" if note else ""))


def check_python_deps(*mods, hard=()):
    """检查可选依赖是否安装，缺失时给出安装命令（不阻断，仅提醒）。

    hard: 必装依赖的子集（缺了脚本会退出）。对这部分会明确提示「无法降级」，
          避免出现「仍可运行」与随后报错自相矛盾的提示。
    """
    import importlib
    missing = []
    for m in mods:
        try:
            importlib.import_module(m)
        except ImportError:
            missing.append(m)
    if missing:
        pkg = "pypinyin" if "pypinyin" in missing else " ".join(missing)
        warn("缺少依赖：%s" % ", ".join(missing))
        print("   → 安装：pip install %s" % pkg, file=sys.stderr)
        hard_missing = [m for m in missing if m in hard]
        if hard_missing:
            print("   → 注意：%s 是本脚本的必装依赖，缺了无法降级运行（详见下方错误提示）。"
                  % ", ".join(hard_missing), file=sys.stderr)
        else:
            print("   → 未安装时脚本仍可运行，但相关功能会降级（如术语表改按 Unicode 排序）",
                  file=sys.stderr)
    return not missing
