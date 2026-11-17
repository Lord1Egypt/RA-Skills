# -*- coding: utf-8 -*-
"""
合理化审查（review_rationality）—— 章内逻辑与写作品质

检查维度：
  1. 重复段落/句：同章内重复（多为扩写时插入块误复制）／跨章重复
  2. 段落形态：超长段（阅读窒息）与过碎段（一句一段）
  3. 对话占比：引号内文字占比过高（以对话注水）
  4. 序数矛盾：章内「第N份/条/封」等序数重复或跳号
  5. 视角混用：第三人称叙事中混入第一人称「我」
  6. 伏笔回收：state/thread-ledger.md 登记的线索是否在后续章出现
  7. 大纲覆盖：章正文对大纲要点关键词的覆盖度（--outline，默认自动探测）

用法（在子项目根目录执行）：
    python "../GitHub Novel Serialization Skill/scripts/review_rationality.py"
    python "../GitHub Novel Serialization Skill/scripts/review_rationality.py" --chapters 031 034
    python "../GitHub Novel Serialization Skill/scripts/review_rationality.py" --outline worldbuilding/OUTLINE/第一卷.md

判定：FAIL —— 确定性缺陷（同章重复段落）；WARN —— 需人工复核。
"""
import sys
import os
import re
import glob
import argparse
from collections import Counter, defaultdict

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _review_lib as L

FUNC_CHARS = set('的一是不了在他有这个上们来到时大地为子中你生国年着就那和要她出也得里后自以会家可下而过天去能对小多然于心学都好看起发当没成只如事把还用第样道想作种开美总从无情己面最女但现前些所同日手又行意动方期它头经长儿回位分爱老因很给名法间知世什两次使身者被高已亲其进此话常与活正感')
CN_NUM = {'一': 1, '二': 2, '三': 3, '四': 4, '五': 5, '六': 6, '七': 7, '八': 8, '九': 9, '十': 10}
DEFAULTS = {'max_para': 500, 'min_para': 6, 'max_dialogue': 0.6, 'min_cover': 0.35,
            'repeat_len': 20, 'chapters': (), 'draft': '', 'outline': ''}


def find_outline(root):
    """自动探测含 `## 第N章` 的大纲/设定文件"""
    for p in sorted(glob.glob(os.path.join(root, 'worldbuilding', '**', '*.md'), recursive=True)):
        t = open(p, encoding='utf-8').read()
        if len([l for l in t.split('\n') if L.PAT_HEAD_CN.match(l)]) >= 3:
            return p
    return ''


def bigrams(text):
    """实词 2-gram 集合（跨标点不成词，故按连续中文段切分后取相邻二字）"""
    out = set()
    for seg in re.findall(r'[\u4e00-\u9fff]{2,}', text):
        for i in range(len(seg) - 1):
            g = seg[i:i + 2]
            if not any(c in FUNC_CHARS for c in g):
                out.add(g)
    return out


def outline_grams(path, num):
    """大纲中该章要点的用词集合（剔除【修改点】一类批注，那不是剧情要点）"""
    blocks = L.draft_blocks(path)
    if num not in blocks:
        return set()
    text = re.sub(r'【[^】]*】', '', blocks[num][1])
    text = '\n'.join(l for l in text.split('\n') if not l.strip().startswith('【'))
    return bigrams(text)


def load_threads(root):
    """[(关键词, 起始章号)] —— state/thread-ledger.md"""
    p = os.path.join(root, 'state', 'thread-ledger.md')
    if not os.path.exists(p):
        return []
    out = []
    for ln in open(p, encoding='utf-8').read().split('\n'):
        if not (ln.startswith('|') or ln.startswith('-')):
            continue
        cell = ln.strip('|').split('|')[0].strip('- ').strip() if ln.startswith('|') else ln[1:].strip()
        m = L.PAT_CN_CHAPTER.search(ln) or L.PAT_EN_CHAPTER.search(ln)
        kw = re.findall(r'[\u4e00-\u9fff]{2,8}', cell)
        if kw:
            out.append((kw[0], int(m.group(1)) if m else 0))
    return out


def audit(item, cfg, ctx):
    issues = []
    paras = L.paragraphs(item.text)
    body = '\n'.join(paras)

    # 1. 重复段落/句
    seen = Counter(p for p in paras if len(p) >= cfg['repeat_len'])
    for p, c in seen.items():
        if c > 1:
            issues.append(L.Issue('FAIL', '章内重复段落',
                                  '%d 次：「%s…」' % (c, p[:24]), item.name))
    # 跨章重复
    for p in paras:
        if len(p) >= cfg['repeat_len'] and ctx['para_chapters'].get(p, 0) > 1:
            issues.append(L.Issue('WARN', '跨章重复段落',
                                  '另见于 %d 章：「%s…」' % (ctx['para_chapters'][p], p[:24]), item.name))

    # 2. 段落形态
    longs = [len(p) for p in paras if len(p) > cfg['max_para']]
    if longs:
        issues.append(L.Issue('WARN', '超长段落',
                              '%d 段超过 %d 字（最长 %d）' % (len(longs), cfg['max_para'], max(longs)), item.name))
    # 过碎：只统计「无句末标点的残句」；「他记得。」这类是刻意强调的短句，不算缺陷
    shorts = [p for p in paras if len(p) < cfg['min_para']
              and not re.search(r'[。！？…”）】」"\s]$', p)]
    if len(shorts) > 3:
        issues.append(L.Issue('WARN', '段落过碎',
                              '%d 段为不足 %d 字的无标点残句，如「%s」' % (len(shorts), cfg['min_para'], shorts[0]),
                              item.name))

    # 3. 对话占比
    total = len(body)
    if total:
        quoted = sum(len(m.group(0)) for m in re.finditer(r'“[^”]*”', body))
        ratio = quoted / total
        if ratio > cfg['max_dialogue']:
            issues.append(L.Issue('WARN', '对话占比过高',
                                  '%.0f%%（上限 %.0f%%），叙述被对话挤占' % (ratio * 100, cfg['max_dialogue'] * 100),
                                  item.name))

    # 4. 序数矛盾
    ords = []
    # 只查物件序列（份/封/批/轮）；「第九条」「第二次」是条款与次数，非叙事序数
    for m in re.finditer(r'第([一二三四五六七八九十\d]+)[份封批轮]', body):
        s = m.group(1)
        ords.append(int(s) if s.isdigit() else CN_NUM.get(s, 0))
    # 只在章内存在较长序数序列时判跳号（单提「第2份」属正常叙述）
    # 只查中间跳号；缺「第1」多半是承接上章，不算问题
    if ords and max(ords) >= 3:
        miss = [n for n in range(2, max(ords)) if n not in ords]
        if miss:
            issues.append(L.Issue('WARN', '序数跳号',
                                  '章内出现至「第%d份/条」但缺第%s' % (max(ords), '、'.join(map(str, miss[:5]))),
                                  item.name))

    # 5. 视角混用
    if body.count('我') >= 3 and not re.search(r'“[^”]*我[^”]*”', body):
        issues.append(L.Issue('WARN', '视角混用',
                              '叙述中「我」出现 %d 次（非对话内），疑第一/三人称混用' % body.count('我'), item.name))

    # 7. 大纲用词覆盖（改写后措辞可不同，故按 2-gram 重叠度衡量，而非整词命中）
    if ctx['outline']:
        ograms = outline_grams(ctx['outline'], item.num)
        if len(ograms) >= 10:
            miss = ograms - bigrams(body)
            cover = 1 - len(miss) / len(ograms)
            if cover < cfg['min_cover']:
                issues.append(L.Issue('WARN', '大纲要点偏离',
                                      '用词覆盖 %d%%（未覆盖 %d/%d），如：%s'
                                      % (cover * 100, len(miss), len(ograms), '、'.join(sorted(miss)[:6])),
                                      item.name))
    return issues


def global_checks(items, cfg, ctx):
    """伏笔回收"""
    issues = []
    corpus = ctx['corpus']
    for kw, start in ctx['threads']:
        if not start:
            continue
        later = [it for it in items if it.num > start]
        if later and kw not in ''.join('\n'.join(L.body_lines(it.text)) for it in later):
            issues.append(L.Issue(
                'WARN', '伏笔未回收',
                '第%03d章 起的「%s」在后续 %d 章未再出现' % (start, kw, len(later)), '全书'))
    return issues


def run(root, cfg):
    cfg = dict(DEFAULTS, **cfg)
    items = L.collect_items(root, cfg.get('chapters', ()), cfg.get('draft', ''))
    outline = cfg.get('outline') or find_outline(root)
    ctx = {'outline': outline, 'threads': load_threads(root),
           'para_chapters': defaultdict(int), 'corpus': ''}
    for it in items:
        for p in set(L.paragraphs(it.text)):
            if len(p) >= cfg['repeat_len']:
                ctx['para_chapters'][p] += 1
        ctx['corpus'] += '\n'.join(L.body_lines(it.text)) + '\n'
    results = [L.make_result(it.name, it.path, audit(it, cfg, ctx), {'num': it.num}) for it in items]
    g = global_checks(items, cfg, ctx)
    if g:
        results.append(L.make_result('全书级检查', root, g))
    return results, None


def main():
    ap = L.add_common_args(argparse.ArgumentParser(description='合理化审查：章内逻辑与写作品质'))
    ap.add_argument('--outline', default='', help='大纲文件路径（默认自动探测 worldbuilding/ 下含 `## 第N章` 的文件）')
    ap.add_argument('--max-para', type=int, default=500, help='单段字数上限（默认 500）')
    ap.add_argument('--min-para', type=int, default=6, help='单段字数下限（默认 6）')
    ap.add_argument('--max-dialogue', type=float, default=0.6, help='对话占比上限（默认 0.6）')
    ap.add_argument('--min-cover', type=float, default=0.35, help='大纲用词覆盖率下限（默认 0.35）')
    a = ap.parse_args()
    root = L.find_root(a.root)
    cfg = dict(vars(a))
    results, _ = run(root, cfg)
    outline = cfg.get('outline') or find_outline(root)
    md = L.render('合理化审查报告', results,
                  intro=['- 检查维度：重复段落／段落形态／对话占比／序数矛盾／视角混用／伏笔回收／大纲覆盖',
                         '- 大纲来源：%s' % (outline or '未找到（跳过覆盖检查）')])
    L.emit(md, a.out or None)
    return 0


if __name__ == '__main__':
    sys.exit(main())
