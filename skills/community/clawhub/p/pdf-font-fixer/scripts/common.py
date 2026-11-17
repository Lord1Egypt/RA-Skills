#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""pdf-fonts-fixer · common —— 各脚本共用的工具函数（不对外当命令用）

设计要点
------------------------------
1. **不内嵌任何字体**。字体靠 discover.py 扫本机：Windows→微软雅黑/宋体，
   macOS→Heiti SC，Linux→文泉驿/Droid/Noto Sans SC。唯一硬约束是轮廓必须是 TrueType。
2. **不自动安装 ghostscript**。缺了就打印官方获取方式，然后由调用方直接回退「扫描版」。
3. 所有路径基于 __file__，不假设安装位置。
"""
import os
import shutil
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SKILL_ROOT = os.path.dirname(HERE)

_discover_mod = None


def _discover():
    """惰性导入同目录的 discover.py。"""
    global _discover_mod
    if _discover_mod is None:
        if HERE not in sys.path:
            sys.path.insert(0, HERE)
        import discover as _d
        _discover_mod = _d
    return _discover_mod


# ---- 字体：一律发现，不写死 ----

def pick_ttf_cjk():
    """本机最优的 (regular, bold|None, family)；找不到返回 (None, None, None)。

    Windows 通常是「微软雅黑 / 宋体」，macOS 是「Heiti SC」，Linux 是「文泉驿 / Droid / Noto Sans SC」。
    CFF/OTF 一律跳过——它们嵌进 PDF 后部分手机上看不见字。
    """
    try:
        return _discover().best_pair()
    except Exception:
        return None, None, None


def list_ttf_cjk():
    """本机所有可用的 TrueType 中文字体记录（供报错/诊断时展示）。"""
    try:
        return [r for r in _discover().scan() if r['kind'] == 'TrueType']
    except Exception:
        return []


# ---- ghostscript ----

GS_HINT = """\
未检测到 ghostscript（把文字转成矢量轮廓时需要它）。
请从**官方**渠道安装（以下均为官方源，任选其一）：

  Debian/Ubuntu : sudo apt-get install ghostscript
  Fedora        : sudo dnf install ghostscript
  macOS         : brew install ghostscript
  Windows       : winget install ArtifexSoftware.GhostScript
  官方下载页     : https://ghostscript.com/releases/gsdnld.html

⚠️ 不会自动安装，也不会从任何非官方来源取二进制。
   装不上也没关系：脚本会跳过「转轮廓」这一级，直接出【扫描版】。
"""


def find_gs(auto_install=False):
    """ghostscript 可执行文件路径；找不到返回 None（并打印官方获取方式）。

    auto_install 参数只为兼容旧调用，**语义已废止**：本项目不会替用户装任何软件。
    """
    for name in ('gs', 'gswin64c', 'gswin32c'):
        p = shutil.which(name)
        if p:
            return p
    print(GS_HINT, file=sys.stderr)
    return None


def run(cmd, timeout=300):
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
        return r.returncode, (r.stdout or '') + (r.stderr or '')
    except Exception as e:
        return 1, str(e)


# ---- 杂项 ----

def unique_path(path):
    if not os.path.exists(path):
        return path
    stem, ext = os.path.splitext(path)
    i = 2
    while os.path.exists('%s_%d%s' % (stem, i, ext)):
        i += 1
    return '%s_%d%s' % (stem, i, ext)


def tag_path(path, tag):
    """给文件名加前缀标签，如 tag_path('a/b/报告.pdf', '【轮廓版】') -> 'a/b/【轮廓版】报告.pdf'。"""
    d, fn = os.path.split(path)
    return os.path.join(d, tag + fn)


# 同设计的对照（仅用于文案：告诉用户该把 CFF 字体换成哪个 TrueType）
SAME_DESIGN = {
    'noto sans cjk': 'Noto Sans SC（思源黑体简体 TrueType 版）',
    'noto serif cjk': 'Noto Serif SC（思源宋体简体 TrueType 版）',
    'source han sans': 'Noto Sans SC / 思源黑体 TTF 版',
    'source han serif': 'Noto Serif SC / 思源宋体 TTF 版',
    'pingfang': 'Heiti SC（macOS 自带 TrueType）或任意 TrueType 中文字体',
    'heiti': 'Heiti SC',
    'songti': 'Songti SC（TTF 版）或任意 TrueType 中文宋体',
    '微软雅黑': '微软雅黑本身即 TrueType，直接用',
    'microsoft yahei': '微软雅黑本身即 TrueType，直接用',
    'simsun': '宋体本身即 TrueType，直接用',
    'simhei': '黑体本身即 TrueType，直接用',
}


def suggest_replacement(basefont):
    """PDF 里那个出问题的字体，建议换成本机哪个 TrueType。"""
    low = (basefont or '').lower().split('+')[-1].replace('-', ' ').replace('_', ' ')
    for k, v in SAME_DESIGN.items():
        if k.replace(' ', '') in low.replace(' ', ''):
            return v
    _r, _b, fam = pick_ttf_cjk()
    if fam:
        return '%s（本机已装的 TrueType 中文字体）' % fam
    return '任意 TrueType 中文字体（见 discover.py 的官方获取方式）'


def human(n):
    for unit in ('B', 'KB', 'MB'):
        if n < 1024:
            return '%.0f %s' % (n, unit)
        n /= 1024.0
    return '%.1f GB' % n


def die(msg, code=1):
    print('[X] ' + msg, file=sys.stderr)
    sys.exit(code)
