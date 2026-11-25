#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""pdf-font-fixer · _deps —— 依赖的持久化（环境重置不丢）。

背景：沙箱/临时环境每次重置都会清空 /usr 与 ~ 下的 pip 包。本 skill 依赖
pikepdf / pymupdf / fontTools / cairosvg，一旦丢失，门禁会在「未完整执行」
状态下静默放行——等于没门禁。所以把包装进持久目录，随用随激活。

用法（在每个脚本最顶部）::

    import _deps
    _deps.activate()          # 把持久目录插到 sys.path 最前；缺的自动装

设计：
- 只装必需包（pikepdf / pymupdf / fontTools）。cairosvg 只在转轮廓时用，
  走 ensure_optional('cairosvg')，用到才装，不拖累常规门禁。
- 已能 import 的包绝不重复安装。
- 安装失败不阻断：activate 只保证路径在 sys.path，装不上的包
  由调用方的「未完整执行」路径兜底（返回 3/4，不会误判通过）。
"""
import os
import subprocess
import sys
import importlib

REQUIRED = ('pikepdf', 'pymupdf', 'fontTools')
OPTIONAL = ('cairosvg',)


def _dir():
    if os.environ.get('PDF_FONT_FIXER_DEPS'):
        return os.environ['PDF_FONT_FIXER_DEPS']
    if os.path.isdir('/sandbox/workspace'):
        return '/sandbox/workspace/.pdf-font-fixer-deps'
    return os.path.expanduser('~/.pdf-font-fixer-deps')


def activate():
    """把持久目录插到 sys.path 最前，并保证必需包可 import。"""
    base = _dir()
    os.makedirs(base, exist_ok=True)
    if base not in sys.path:
        sys.path.insert(0, base)
    for pkg in REQUIRED:
        if not _importable(pkg):
            _install(base, pkg)
            _purge(pkg)          # 清掉「未找到」的 import 缓存，同进程立即可用
            importlib.invalidate_caches()
    return base


def ensure_optional(pkg):
    """按需安装可选包（如 cairosvg）。返回是否可用。"""
    if _importable(pkg):
        return True
    _install(_dir(), pkg)
    _purge(pkg)
    importlib.invalidate_caches()
    return _importable(pkg)


def _importable(mod):
    try:
        __import__(mod)
        return True
    except Exception:
        return False


def _purge(pkg):
    """pip 是子进程装的，父进程里「未找到」的缓存必须清掉，否则同进程仍 import 不到。"""
    for k in list(sys.modules):
        if k == pkg or k.startswith(pkg + '.'):
            del sys.modules[k]


def _install(base, pkg):
    try:
        subprocess.run(
            [sys.executable, '-m', 'pip', 'install', '--quiet',
             '--target', base, pkg],
            timeout=600, capture_output=True)
    except Exception:
        pass
