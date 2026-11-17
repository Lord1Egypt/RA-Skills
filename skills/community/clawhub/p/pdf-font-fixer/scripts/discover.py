#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""pdf-fonts-fixer · discover —— 发现本机可用的「完善中文字体」，且必须是 TrueType

为什么要"发现"而不是写死 Noto
----------------------------
每个系统都有自己的中文正体：
  Windows  → 微软雅黑（Microsoft YaHei）、宋体（SimSun）、黑体（SimHei）  均为 TrueType ✅
  macOS    → Heiti SC / STHeiti 是 TrueType ✅；PingFang SC 是 CFF ❌
  Linux    → Noto Sans SC(TTF) / 文泉驿(WQY) / Droid Sans Fallback ✅；Noto Sans CJK 是 CFF ❌

所以不能写死某个字体名，做法是：**扫本机字体目录 → 判定轮廓格式 → 判定中文覆盖 → 排序取优**。
唯一硬约束是「轮廓必须是 TrueType(glyf)」——CFF/OTF 在部分手机上看不见字。

用法
----
  python3 discover.py                 # 人类可读列表（TrueType 优先，按覆盖降序）
  python3 discover.py --json          # 机器可读
  python3 discover.py --best          # 只输出最优的 Regular / Bold 两个路径（供脚本调用）
  python3 discover.py --no-cache      # 忽略缓存重新扫

退出码  0 找到可用 TrueType 中文字体 / 2 没找到（附官方获取方式）
"""
import argparse
import json
import logging
import os
import sys
import time

# fontTools 扫描时会对个别字体打印无害告警（如 post 表多余字节），统一静音
logging.getLogger('fontTools').setLevel(logging.ERROR)

CACHE_FILE = os.path.join(os.path.expanduser('~'), '.pdf-fonts-fixer-fonts.json')
CACHE_TTL = 7 * 24 * 3600

PROBE = '的一是不了在人有我他这为之大来以个中上们到说国和地也子时道出而要于就下得可你年生'


def font_dirs():
    """各平台字体目录（存在才返回）。"""
    home = os.path.expanduser('~')
    dirs = [
        # Linux
        '/usr/share/fonts', '/usr/local/share/fonts',
        os.path.join(home, '.fonts'), os.path.join(home, '.local/share/fonts'),
        # macOS
        '/System/Library/Fonts', '/Library/Fonts', os.path.join(home, 'Library/Fonts'),
        # Windows
        'C:/Windows/Fonts',
        os.path.join(os.environ.get('LOCALAPPDATA', ''), 'Microsoft', 'Windows', 'Fonts'),
        os.path.join(os.environ.get('WINDIR', 'C:/Windows'), 'Fonts'),
        # 本环境的持久备份目录（沙箱重启不丢）
        '/sandbox/workspace/fonts_ttc',
    ]
    seen, out = set(), []
    for d in dirs:
        if d and os.path.isdir(d) and d not in seen:
            seen.add(d)
            out.append(d)
    return out


def _sfnt_kind(path):
    """极快判轮廓类型：读文件头。'OTTO'=CFF，其余 sfnt=TrueType，'ttcf'=集合需再判。"""
    try:
        with open(path, 'rb') as f:
            tag = f.read(4)
    except OSError:
        return 'unknown'
    if tag == b'OTTO':
        return 'CFF'
    if tag == b'ttcf':
        return 'TTC'
    return 'TrueType'


def _inspect(path):
    """返回 [(family, kind, cmap_size, cjk_hits, path)]；TTC 里每个面各一条。"""
    from fontTools.ttLib import TTFont, TTCollection
    rows = []
    try:
        if _sfnt_kind(path) == 'TTC':
            fonts = TTCollection(path).fonts
        else:
            fonts = [TTFont(path, fontNumber=0)]
    except Exception:
        return rows
    for f in fonts:
        try:
            cff = ('CFF ' in f) or ('CFF2' in f)
            fam = f['name'].getDebugName(1) or os.path.basename(path)
            cm = f.getBestCmap() or {}
            hits = sum(1 for c in PROBE if ord(c) in cm)
            if hits < 12:
                continue                       # 不是中文正体
            rows.append((fam, 'CFF' if cff else 'TrueType', len(cm), hits, path))
        except Exception:
            continue
    return rows


def scan(use_cache=True):
    if use_cache and os.path.exists(CACHE_FILE):
        try:
            st = os.stat(CACHE_FILE)
            if time.time() - st.st_mtime < CACHE_TTL:
                return json.load(open(CACHE_FILE, encoding='utf-8'))
        except Exception:
            pass
    rows = []
    for d in font_dirs():
        for root, _dn, files in os.walk(d):
            for fn in files:
                if not fn.lower().endswith(('.ttf', '.ttc', '.otf')):
                    continue
                rows.extend(_inspect(os.path.join(root, fn)))
    # 去重 + 排序：TrueType 优先，其次覆盖（cmap 大小）降序
    uniq = {}
    for fam, kind, n, hits, p in rows:
        key = (fam, kind, p)
        uniq[key] = dict(family=fam, kind=kind, cmap=n, hits=hits, path=p)
    out = sorted(uniq.values(), key=lambda r: (r['kind'] != 'TrueType', -r['cmap']))
    try:
        json.dump(out, open(CACHE_FILE, 'w', encoding='utf-8'), ensure_ascii=False)
    except Exception:
        pass
    return out


def best_pair(rows=None):
    """挑最优的 (regular, bold|None, family)；只从 TrueType 里挑。"""
    rows = rows or scan()
    tt = [r for r in rows if r['kind'] == 'TrueType']
    if not tt:
        return None, None, None
    # 按 family 归组，取覆盖最大的 family
    fams = {}
    for r in tt:
        fams.setdefault(r['family'], []).append(r)
    fam = max(fams, key=lambda k: max(x['cmap'] for x in fams[k]))
    items = fams[fam]
    def score(r):
        low = os.path.basename(r['path']).lower() + r['family'].lower()
        return (0 if 'regular' in low or 'book' in low else 1, -r['cmap'])
    reg = sorted(items, key=score)[0]
    bolds = [r for r in items if 'bold' in (os.path.basename(r['path']) + r['family']).lower()]
    bold = sorted(bolds, key=lambda r: -r['cmap'])[0] if bolds else None
    return reg['path'], (bold['path'] if bold else None), fam


OFFICIAL = """
找不到可用的 TrueType 中文字体。请从**官方**渠道装一个（任选其一，都是开源/系统自带，无版权风险）：

  Windows（微软雅黑/宋体系统自带，通常不用装）：
      官方：https://learn.microsoft.com/typography/fonts/
  macOS（Heiti SC 系统自带，通常不用装）：
      官方：https://support.apple.com/  （字体册）
  Linux：
      Noto Sans SC（TrueType 版）：https://fonts.google.com/noto/specimen/Noto+Sans+SC
      文泉驿微米黑：https://wenq.org/wqy2/index.cgi?ZenHei
      Debian/Ubuntu：sudo apt-get install fonts-wqy-microhei fonts-noto-cjk（⚠️ noto-cjk 是 CFF，装了也用不上）
  通用（Google 官方字体站，选 Noto Sans SC 的 .ttf 而不是 .otf）：
      https://github.com/notofonts/noto-cjk/releases
"""


def main():
    ap = argparse.ArgumentParser(description='发现本机可用的 TrueType 中文字体')
    ap.add_argument('--json', action='store_true')
    ap.add_argument('--best', action='store_true')
    ap.add_argument('--no-cache', action='store_true')
    a = ap.parse_args()

    rows = scan(use_cache=not a.no_cache)
    if a.best:
        r, b, fam = best_pair(rows)
        if not r:
            print('', file=sys.stderr)
            print(OFFICIAL, file=sys.stderr)
            return 2
        print(r)
        if b:
            print(b)
        return 0
    if a.json:
        print(json.dumps(rows, ensure_ascii=False, indent=1))
        return 0 if any(r['kind'] == 'TrueType' for r in rows) else 2

    if not rows:
        print('本机没扫到任何中文字体。')
        print(OFFICIAL)
        return 2
    print('%-34s %-10s %8s  %s' % ('字体名', '轮廓', '字形数', '路径'))
    for r in rows:
        mark = '✅' if r['kind'] == 'TrueType' else '❌'
        print('%s %-32s %-10s %8d  %s' % (mark, r['family'][:32], r['kind'], r['cmap'], r['path']))
    r, b, fam = best_pair(rows)
    print()
    if r:
        print('建议使用：%s' % fam)
        print('  Regular: %s' % r)
        if b:
            print('  Bold   : %s' % b)
        print('\n（❌ 的是 CFF/OTF 轮廓，在部分手机上看不见字，不要用）')
        return 0
    print('只找到 CFF/OTF 中文字体，没有可用的 TrueType。')
    print(OFFICIAL)
    return 2


if __name__ == '__main__':
    sys.exit(main())
