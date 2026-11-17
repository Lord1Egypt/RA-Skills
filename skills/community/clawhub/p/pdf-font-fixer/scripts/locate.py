#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""pdf-fonts-fixer · locate —— 跨环境定位器（其它 skill 靠它找到本 skill）

为什么需要
----------
`$HOME/.skills/pdf-fonts-fixer` 只是**本环境**的约定。换一台机器、换一个平台
（WorkBuddy / Claude Code / Codex / 项目内安装 / Windows），skill 的落地位置都不一样，
硬编码路径必然断。

定位优先级（从可靠到兜底）
--------------------------
  0. 脚本自身位置（最可靠：脚本就在 skill 里，往上两级就是 skill 根目录）
  1. 环境变量 `PDF_FONT_FIXER`（显式覆盖，安装脚本/用户手工指定）
  2. 常见安装约定的候选目录
  3. 用户目录下有限深度的目录名搜索（`pdf-fonts-fixer`）

用法
----
  python3 locate.py                 # 打印 skill 根目录（失败退出码 2）
  python3 locate.py --check         # 环境自检：脚本/字体/依赖/gs
  python3 locate.py --fonts         # 打印可用的 TrueType 中文字体（自足优先）
  python3 locate.py --sh            # 打印一段可直接 eval 的 shell：FIXER=...

其它 skill 的推荐调用姿势（Python 内）
------------------------------------
    import subprocess, sys, os
    here = os.path.dirname(os.path.abspath(__file__))
    # ① 环境变量 ② 与当前 skill 同级 ③ 各平台约定
    cands = [os.environ.get('PDF_FONT_FIXER', ''),
             os.path.join(os.path.dirname(os.path.dirname(here)), 'pdf-fonts-fixer'),
             os.path.expanduser('~/.skills/pdf-fonts-fixer'),
             os.path.expanduser('~/.claude/skills/pdf-fonts-fixer'),
             os.path.expanduser('~/.codebuddy/skills/pdf-fonts-fixer')]
    fixer = next((p for p in cands if p and os.path.isfile(
        os.path.join(p, 'scripts', 'gate.py'))), None)
"""
import argparse
import json
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SELF_ROOT = os.path.dirname(HERE)          # scripts/ 的上一级

SKILL_NAME = 'pdf-fonts-fixer'
LEGACY_NAMES = ('pdf-font-fixer',)   # 兼容早期安装目录名


def _is_skill_dir(p):
    return bool(p) and os.path.isfile(os.path.join(p, 'scripts', 'gate.py'))


def _home():
    return os.path.expanduser('~')


def candidates():
    """按可靠性排序的候选路径。"""
    out = []
    env = os.environ.get('PDF_FONT_FIXER') or os.environ.get('PDF_FONT_FIXER_HOME')
    if env:
        out.append(env)
    out.append(SELF_ROOT)                                  # 0. 自身位置
    h = _home()
    # 2. 各平台/各客户端的常见约定
    for rel in ('skills', '.skills', '.claude/skills', '.workbuddy/skills',
                '.codebuddy/skills', '.config/ima/skills', 'ima/skills', '.codex/skills',
                'AppData/Roaming/ima/skills', 'AppData/Roaming/workbuddy/skills',
                'AppData/Roaming/codebuddy/skills'):
        out.append(os.path.join(h, rel.replace('/', os.sep), SKILL_NAME))
    # 2b. 旧目录名（兼容早期安装）
    for rel in ('skills', '.skills', '.claude/skills', '.workbuddy/skills', '.codebuddy/skills'):
        for legacy in LEGACY_NAMES:
            out.append(os.path.join(h, rel.replace('/', os.sep), legacy))
    # 3. 项目级安装
    for base in (os.getcwd(), os.path.dirname(os.getcwd())):
        out.append(os.path.join(base, 'skills', SKILL_NAME))
        out.append(os.path.join(base, '.claude', 'skills', SKILL_NAME))
    return out


def search(limit_depth=4):
    """兜底搜索：用户目录下按目录名找（限制深度，避免扫盘）。"""
    roots = [os.path.join(_home(), x) for x in ('skills', '.skills', '.claude',
                                                '.workbuddy', '.codebuddy', '.config')]
    for root in roots:
        if not os.path.isdir(root):
            continue
        for dirpath, dirnames, _files in os.walk(root):
            depth = dirpath[len(root):].count(os.sep)
            if depth > limit_depth:
                dirnames[:] = []
                continue
            if os.path.basename(dirpath) in (SKILL_NAME,) + LEGACY_NAMES and _is_skill_dir(dirpath):
                return dirpath
    return None


def find_root():
    for p in candidates():
        if _is_skill_dir(p):
            return os.path.abspath(p)
    return search()


def find_fonts():
    """可用的 TrueType 中文字体：优先复用 discover.py 的扫描结果。"""
    out, seen = [], set()
    try:
        sys.path.insert(0, HERE)
        import discover
        for r in discover.scan():
            if r.get('kind') != 'TrueType':
                continue
            p = r.get('path')
            if p and p not in seen:
                seen.add(p)
                out.append((p, r.get('family') or 'TrueType 中文字体'))
        if out:
            return out
    except Exception:
        pass

    # 兜底：只看常见的 Noto 文件名
    assets = os.path.join(SELF_ROOT, 'assets', 'fonts')
    for fn in ('NotoSansSC-Regular-sub.ttf', 'NotoSansSC-Bold-sub.ttf'):
        p = os.path.join(assets, fn)
        if os.path.isfile(p):
            out.append((p, 'skill 自带子集'))
    h = _home()
    sys_cands = [
        ('/usr/local/share/fonts/custom', 'Linux 自定义'),
        (os.path.join(h, '.fonts'), 'Linux 用户'),
        (os.path.join(h, 'Library', 'Fonts'), 'macOS 用户'),
        ('/Library/Fonts', 'macOS 系统'),
        ('C:/Windows/Fonts', 'Windows 系统'),
        (os.path.join(os.environ.get('LOCALAPPDATA', ''), 'Microsoft/Windows/Fonts'), 'Windows 用户'),
    ]
    for d, tag in sys_cands:
        for fn in ('NotoSansSC-Regular.ttf', 'NotoSansSC-Bold.ttf'):
            p = os.path.join(d, fn)
            if os.path.isfile(p):
                out.append((p, tag))
    return out


def check():
    root = find_root()
    print('skill 根目录：%s' % (root or '❌ 未找到'))
    if not root:
        print('   设置环境变量 PDF_FONT_FIXER 指向 pdf-fonts-fixer 目录即可。')
        return 2
    ok = True
    for s in ('detect.py', 'verify.py', 'gate.py', 'fix.py', 'pptx.py', 'fontkit.py',
              'autofallback.py', 'locate.py'):
        p = os.path.join(root, 'scripts', s)
        print('   %s %s' % ('✅' if os.path.isfile(p) else '❌', s))
        ok = ok and os.path.isfile(p)

    print('\n字体：')
    fonts = find_fonts()
    if not fonts:
        print('   ❌ 没有可用的 TrueType 中文字体')
        ok = False
    for p, tag in fonts:
        print('   ✅ %-44s %s' % (os.path.basename(p), tag))

    print('\n依赖：')
    for mod, use in (('pymupdf', '读字体/渲染'), ('fontTools', 'CFF 解析/OTF→TTF'),
                     ('pikepdf', 'charset 修复')):
        try:
            __import__(mod)
            print('   ✅ %s（%s）' % (mod, use))
        except ImportError:
            print('   ⚠️ %s 缺失（%s 不可用）' % (mod, use))
    import shutil
    gs = shutil.which('gs') or shutil.which('gswin64c')
    print('   %s ghostscript%s' % ('✅' if gs else '⚠️', '' if gs else '（转轮廓不可用，会退到位图）'))
    print('\n结论：%s' % ('✅ 环境就绪' if ok else '❌ 有缺失，见上'))
    return 0 if ok else 2


def main():
    ap = argparse.ArgumentParser(description='跨环境定位 pdf-fonts-fixer')
    ap.add_argument('--check', action='store_true')
    ap.add_argument('--fonts', action='store_true')
    ap.add_argument('--sh', action='store_true', help='输出可 eval 的 shell 片段')
    ap.add_argument('--json', action='store_true')
    a = ap.parse_args()

    if a.check:
        return check()
    if a.fonts:
        for p, tag in find_fonts():
            print('%s\t%s' % (p, tag))
        return 0
    root = find_root()
    if a.json:
        print(json.dumps(dict(root=root, fonts=find_fonts()), ensure_ascii=False, indent=1))
        return 0 if root else 2
    if a.sh:
        if root:
            print('export PDF_FONT_FIXER="%s"' % root)
        else:
            print('echo "pdf-fonts-fixer 未找到，请设置 PDF_FONT_FIXER" >&2; exit 2')
        return 0 if root else 2
    if root:
        print(root)
        return 0
    print('pdf-fonts-fixer 未找到（可用 PDF_FONT_FIXER 环境变量指定）', file=sys.stderr)
    return 2


if __name__ == '__main__':
    sys.exit(main())
