# -*- coding: utf-8 -*-
"""
规模审查（review_scale）—— 章节字数达标审查

用法（脚本存于技能仓库 scripts/，在子项目根目录执行）：
    python "../GitHub Novel Serialization Skill/scripts/review_scale.py"
    python "../GitHub Novel Serialization Skill/scripts/review_scale.py" --target 4000 --chapters 031 034
    python "../GitHub Novel Serialization Skill/scripts/review_scale.py" --draft notes-personal/正文草稿.md
    python "../GitHub Novel Serialization Skill/scripts/review_scale.py" --out .workbuddy/reports/规模审查_2026-09-27.md

判定：
    FAIL —— 严重不足（低于目标 60%），必须扩写
    WARN —— 未达标或超出上限，需人工确认
    PASS —— 达到目标字数
"""
import sys
import os
import argparse

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _review_lib as L

SERIOUS = 0.6   # 低于目标该比例判 FAIL


def audit(item, cfg):
    """单章规模审查"""
    issues = []
    n = L.cn(item.text)
    target, maxn = cfg['target'], cfg['max']
    if n < target * SERIOUS:
        issues.append(L.Issue('FAIL', '字数严重不足', '%d 字（目标 %d，缺 %d）' % (n, target, target - n), item.name))
    elif n < target:
        issues.append(L.Issue('WARN', '字数未达标', '%d 字（目标 %d，缺 %d）' % (n, target, target - n), item.name))
    if maxn and n > maxn:
        issues.append(L.Issue('WARN', '字数超上限', '%d 字（上限 %d，超出 %d）' % (n, maxn, n - maxn), item.name))
    return issues, {'words': n}


def summary(items, stats, cfg):
    """全书规模概览"""
    if not stats:
        return '无审查对象。'
    target = cfg['target']
    ws = [s['words'] for s in stats]
    total, mean = sum(ws), sum(ws) / len(ws)
    ok = sum(1 for w in ws if w >= target)
    gap = sum(max(0, target - w) for w in ws)
    buckets = [(0, .5), (.5, .75), (.75, 1.0), (1.0, 99)]
    names = ['< 50% 目标', '50%—75% 目标', '75%—100% 目标', '达标']
    lines = ['- 章数：**%d** ｜ 总字数：**%s** ｜ 均值：%d 字' % (len(ws), format(total, ','), int(mean)),
             '- 达标（≥ %d 字）：**%d / %d**（%.0f%%）｜ 总缺口：%s 字'
             % (target, ok, len(ws), 100.0 * ok / len(ws), format(gap, ',')),
             '- 最短：%d 字 ｜ 最长：%d 字 ｜ 中位数：%d 字'
             % (min(ws), max(ws), sorted(ws)[len(ws) // 2]),
             '', '| 区间 | 章数 |', '|---|---|']
    for (lo, hi), nm in zip(buckets, names):
        c = sum(1 for w in ws if target * lo <= w < target * hi)
        rng = '≥ %d 字' % target if hi >= 99 else '%d—%d 字' % (int(target * lo), int(target * hi))
        lines.append('| %s（%s）| %d |' % (nm, rng, c))
    lines += ['', '### 缺口 TOP 10（建议按此分批扩写）', '',
              '| 章 | 字数 | 缺口 |', '|---|---|---|']
    for it, s in sorted(zip(items, stats), key=lambda x: x[1]['words'])[:10]:
        if s['words'] >= target:
            continue
        lines.append('| %s | %d | %d |' % (it.name, s['words'], target - s['words']))
    return '\n'.join(lines)


def run(root, cfg):
    items = L.collect_items(root, cfg.get('chapters', ()), cfg.get('draft', ''))
    results, stats = [], []
    for it in items:
        iss, st = audit(it, cfg)
        results.append(L.make_result(it.name, it.path, iss, st))
        stats.append(st)
    return results, summary(items, stats, cfg)


def main():
    ap = L.add_common_args(argparse.ArgumentParser(description='规模审查：章节字数达标情况'))
    ap.add_argument('--target', type=int, default=4000, help='每章目标中文字数（默认 4000）')
    ap.add_argument('--max', type=int, default=0, help='每章字数上限（0 = 不限）')
    a = ap.parse_args()
    root = L.find_root(a.root)
    cfg = {'target': a.target, 'max': a.max, 'chapters': a.chapters, 'draft': a.draft}
    results, summ = run(root, cfg)
    md = L.render('规模审查报告', results,
                  intro=['- 目标字数：%d 字 ｜ 上限：%s ｜ 严重不足线：%d 字'
                         % (a.target, a.max or '不限', int(a.target * SERIOUS)),
                         '- 审查范围：%s' % (a.draft or 'chapters/ 定稿')],
                  extra_sections=[('三、规模概览', summ)])
    L.emit(md, a.out or None)
    return 0


if __name__ == '__main__':
    sys.exit(main())
