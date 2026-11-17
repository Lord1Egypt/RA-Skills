# -*- coding: utf-8 -*-
"""
一致性审稿（review_continuity）—— 跨章事实一致性

检查维度：
  1. 专名异写：已知实体（characters/ · worldbuilding/ · state/）在正文中的形近写法
  2. 角色属性冲突：对照 characters/ 档案生年，检查正文「N 年 · M 岁」是否自相矛盾
  3. 时间线倒流：按章序检查主年份是否回退（倒叙需人工确认）
  4. 标题与正文不符：章标题中的专名在本章 0 次、却在其它章高频出现
  5. 时间线登记：state/timeline.md 中的日期未在对应章出现
  6. 章标题零差异：草稿与定稿章标题集合比对

用法（在子项目根目录执行）：
    python "../GitHub Novel Serialization Skill/scripts/review_continuity.py"
    python "../GitHub Novel Serialization Skill/scripts/review_continuity.py" --chapters 028 050
    python "../GitHub Novel Serialization Skill/scripts/review_continuity.py" --out .workbuddy/reports/一致性审稿.md

判定：FAIL —— 确定冲突（角色年龄矛盾、章标题不一致）；WARN —— 疑似冲突，需人工复核。
说明：脚本只负责挑出可疑处，最终以主编人工复核为准。
"""
import sys
import os
import re
import glob
import argparse
from collections import defaultdict, Counter

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _review_lib as L

# 标题/候选词过滤用的高频虚词字（含这些字的短串多半不是专名）
FUNC_CHARS = set('的一是不了在他有这个上们来到时大地为子中你生国年着就那和要她出也得里后自以会家可下而过天去能对小多然于心学都好看起发当没成只如事把还用第样道想作种开美总从无情己面最女但现前些所同日手又行意动方期它头经长儿回位分爱老因很给名法间知世什两次使身者被高已亲其进此话常与活正感')


def load_characters(root):
    """{角色名: 生年 or None}"""
    out = {}
    for p in glob.glob(os.path.join(root, 'characters', '*.md')):
        name = os.path.splitext(os.path.basename(p))[0]
        t = open(p, encoding='utf-8').read()
        m = re.search(r'(?:出?生[于於]|出生)\s*(\d{4})', t) or re.search(r'(\d{4})\s*年生', t)
        out[name] = int(m.group(1)) if m else None
    return out


def load_timeline(root):
    """[(章号, 日期原文)] —— state/timeline.md"""
    p = os.path.join(root, 'state', 'timeline.md')
    if not os.path.exists(p):
        return []
    out = []
    for ln in open(p, encoding='utf-8').read().split('\n'):
        m = L.PAT_CN_CHAPTER.search(ln) or L.PAT_EN_CHAPTER.search(ln)
        if not m:
            continue
        d = re.search(r'(\d{4}\s*年\s*\d{1,2}\s*月|\d{1,2}\s*月|\d{4}\s*年)', ln)
        if d:
            out.append((int(m.group(1)), re.sub(r'\s+', '', d.group(1))))
    return out


def load_entities(root):
    """已知专名：角色名 + 世界观文件标题 + state 表格首列"""
    ents = set()

    def add(s):
        s = s.strip().strip('：:| ')
        if 2 <= len(s) <= 8 and re.fullmatch(r'[\u4e00-\u9fff]+', s):
            ents.add(s)

    for p in glob.glob(os.path.join(root, 'characters', '*.md')):
        add(os.path.splitext(os.path.basename(p))[0])
    for p in glob.glob(os.path.join(root, 'worldbuilding', '**', '*.md'), recursive=True):
        add(os.path.splitext(os.path.basename(p))[0])
        for m in re.finditer(r'^#{1,4}\s*(.+?)\s*$', open(p, encoding='utf-8').read(), re.M):
            add(m.group(1))
    for p in glob.glob(os.path.join(root, 'state', '*.md')):
        for ln in open(p, encoding='utf-8').read().split('\n'):
            if ln.startswith('|'):
                add(ln.strip('|').split('|')[0])
            else:
                m = re.match(r'^[-*]\s*([^:：]{2,8})[:：]', ln)
                if m:
                    add(m.group(1))
    return ents


CN_DIGIT = {'一': 1, '二': 2, '三': 3, '四': 4, '五': 5, '六': 6, '七': 7, '八': 8, '九': 9}


def parse_age(s):
    """解析年龄：阿拉伯数字或中文数字（1—99），如 35 / 三十五 / 十"""
    if s.isdigit():
        return int(s)
    if s in CN_DIGIT:
        return CN_DIGIT[s]
    if '十' not in s:
        return 0
    t, o = s.split('十', 1)
    return (CN_DIGIT.get(t, 1) if t else 1) * 10 + CN_DIGIT.get(o, 0)


def year_of(text):
    """文本主年份（民国年折算 +1911）。

    只采信正文（不含 `>` 元数据行）；年份出现 ≥2 次才认定，仅出现 1 次的一律不参与
    时间线判定——孤例多半来自回忆、展望或引文，据此判倒流必然误报。
    """
    seq = []
    for m in re.finditer(r'(1[89]\d{2}|20\d{2})\s*年|民国(\d{1,2})年', text):
        seq.append(int(m.group(1)) if m.group(1) else int(m.group(2)) + 1911)
    if not seq:
        return None
    top, n = Counter(seq).most_common(1)[0]
    return top if n >= 2 else None


def typo_candidate(w, ent):
    """是否为 ent 的疑似异写：等长且仅 1 字之差，差异字均为实词字。

    长度差 1 的增删一律不判——那种情况必然是子串关系（如「于凤至」/「于凤至说」），
    属于词边界噪声而非异写。
    """
    if w == ent or len(w) != len(ent):
        return False
    diff = [(x, y) for x, y in zip(w, ent) if x != y]
    if len(diff) != 1:
        return False
    a, b = diff[0]
    return a not in FUNC_CHARS and b not in FUNC_CHARS


def build_ctx(root, items):
    """预计算：正文窗口计数、标题用短串章频、实体表"""
    ctx = {'chars': load_characters(root), 'timeline': load_timeline(root),
           'ents': load_entities(root), 'wins': defaultdict(Counter), 'succ': defaultdict(Counter),
           'ent_count': Counter(), 'short_chapters': defaultdict(int)}
    corpus = '\n'.join('\n'.join(L.body_lines(it.text)) for it in items)
    ctx['corpus'] = corpus
    for ent in ctx['ents']:
        ctx['ent_count'][ent] = corpus.count(ent)
    lens = sorted({len(e) for e in ctx['ents'] if ctx['ent_count'][e] > 0 and 2 <= len(e) <= 8}) or [2]
    for seg in re.findall(r'[\u4e00-\u9fff]{%d,%d}' % (min(lens, default=2), max(lens, default=2)), corpus):
        for n in lens:
            if len(seg) < n:
                continue
            for i in range(len(seg) - n + 1):
                w = seg[i:i + n]
                ctx['wins'][(w[0], n)][w] += 1
                if i + n < len(seg):
                    ctx['succ'][w][seg[i + n]] += 1
    for it in items:
        body = '\n'.join(L.body_lines(it.text))
        for w in set(re.findall(r'[\u4e00-\u9fff]{2,3}', body)):
            ctx['short_chapters'][w] += 1
    return ctx


def audit(item, cfg, ctx):
    """单章一致性"""
    issues = []
    body = '\n'.join(L.body_lines(item.text))

    # 2. 角色属性冲突（年龄 vs 档案生年）
    for name, birth in ctx['chars'].items():
        if not birth or name not in body:
            continue
        for m in re.finditer(re.escape(name), body):
            win = body[max(0, m.start() - 40):m.end() + 40]
            am = re.search(r'([0-9]{1,2}|[一二三四五六七八九十]{1,3})\s*岁', win)
            ym = re.search(r'(1[89]\d{2}|20\d{2})\s*年', win)
            if am and ym:
                got = parse_age(am.group(1))
                if not got:
                    continue
                implied = int(ym.group(1)) - birth
                if abs(implied - got) > 2:
                    issues.append(L.Issue(
                        'FAIL', '角色年龄冲突',
                        '%s：文中「%s 年 · %d 岁」，按档案生年 %d 应为约 %d 岁'
                        % (name, ym.group(1), got, birth, implied), item.name))

    # 4. 标题与正文不符
    title = L.chapter_title(item.text) or item.name
    for g in set(re.findall(r'[\u4e00-\u9fff]{2,3}', title)):
        if any(c in FUNC_CHARS for c in g):
            continue
        if body.count(g) == 0 and ctx['short_chapters'].get(g, 0) >= 3:
            issues.append(L.Issue(
                'WARN', '标题与正文不符',
                '标题「%s」中的「%s」在本章 0 次，却在其它 %d 章出现' % (title, g, ctx['short_chapters'][g]),
                item.name))

    # 5. 时间线登记日期未在正文出现
    for num, date in ctx['timeline']:
        if num == item.num and date not in body.replace(' ', ''):
            issues.append(L.Issue('WARN', '时间线登记缺失',
                                  'state/timeline.md 记「%s」未在正文出现' % date, item.name))
    return issues


def global_checks(items, cfg, ctx):
    """全书级：专名异写、时间线倒流、章标题零差异"""
    issues = []

    # 1. 专名异写（已知实体 → 形近变体）
    for ent in sorted(ctx['ents']):
        base = ctx['ent_count'].get(ent, 0)
        if base < cfg['min_freq']:
            continue
        n = len(ent)
        if n < cfg['min_ent_len']:
            continue
        esucc = {c for c, _ in (ctx['succ'].get(ent) or Counter()).most_common(6)}
        for w, c in ctx['wins'].get((ent[0], n), {}).items():
            if c < cfg['min_variant'] or w in ctx['ents'] or not typo_candidate(w, ent):
                continue
            # 低频变体才是疑似错写；变体出现多了说明它本身是另一个实体
            if c > min(cfg['max_variant'], max(2, base * 0.3)):
                continue
            # 用法相近（后继字有交集）才可能是同一对象的异写，过滤跨词边界噪声
            wsucc = {x for x, _ in (ctx['succ'].get(w) or Counter()).most_common(6)}
            if esucc and not (esucc & wsucc):
                continue
            issues.append(L.Issue(
                'WARN', '疑似专名异写',
                '「%s」(%d 次) 与已知实体「%s」(%d 次) 仅差 1 字，疑同一对象两种写法' % (w, c, ent, base),
                '全书'))

    # 3. 时间线倒流
    prev = None
    for it in items:
        y = year_of('\n'.join(L.body_lines(it.text)))
        if y is None:
            continue
        if prev and prev[1] - y > cfg['year_tol']:
            issues.append(L.Issue(
                'WARN', '时间线倒流',
                '第%03d章 主年份 %d 早于第%03d章 的 %d（倒叙/回忆可忽略）' % (it.num, y, prev[0], prev[1]),
                it.name))
        if not prev or y >= prev[1]:
            prev = (it.num, y)

    # 6. 草稿与定稿章标题零差异
    draft = cfg.get('draft', '')
    if draft:
        p = draft if os.path.isabs(draft) else os.path.join(cfg['root'], draft)
        dblocks = L.draft_blocks(p)
        idx = L.chapter_index(cfg['root'])
        for n in sorted(set(dblocks) & set(idx)):
            dt = L.chapter_title(dblocks[n][0]) or dblocks[n][0]
            ct = L.chapter_title(open(idx[n], encoding='utf-8').read())
            if dt.strip() != (ct or '').strip():
                issues.append(L.Issue('FAIL', '章标题不一致',
                                      '第%03d章 草稿「%s」≠ 定稿「%s」' % (n, dt, ct), idx[n]))
    # 去重（同一变体可能命中多个长度）
    uniq, seen = [], set()
    for i in issues:
        k = (i.category, i.detail)
        if k not in seen:
            seen.add(k)
            uniq.append(i)
    return [i for i in uniq if i.level != 'INFO'][:cfg['limit']]


DEFAULTS = {'min_freq': 5, 'min_variant': 2, 'max_variant': 4, 'min_ent_len': 3,
            'year_tol': 1, 'limit': 40, 'chapters': (), 'draft': ''}


def run(root, cfg):
    cfg = dict(DEFAULTS, **cfg)
    items = L.collect_items(root, cfg.get('chapters', ()), cfg.get('draft', ''))
    cfg = dict(cfg, root=root)
    ctx = build_ctx(root, items)
    results = [L.make_result(it.name, it.path, audit(it, cfg, ctx), {'num': it.num}) for it in items]
    g = global_checks(items, cfg, ctx)
    if g:
        results.append(L.make_result('全书级检查', root, g))
    return results, None


def main():
    ap = L.add_common_args(argparse.ArgumentParser(description='一致性审稿：跨章事实冲突'))
    ap.add_argument('--min-freq', type=int, default=5, help='实体最低出现次数，低于此不查异写（默认 5）')
    ap.add_argument('--min-variant', type=int, default=2, help='变体最低出现次数（默认 2）')
    ap.add_argument('--min-ent-len', type=int, default=3,
                    help='参与异写检测的实体最短字数（默认 3，2 字实体噪声过大）')
    ap.add_argument('--max-variant', type=int, default=4,
                    help='变体最高出现次数，超过则视为另一实体（默认 4）')
    ap.add_argument('--year-tol', type=int, default=1, help='年份回退容差，默认 1 年')
    ap.add_argument('--limit', type=int, default=40, help='全书级问题最多列出条数（默认 40）')
    a = ap.parse_args()
    root = L.find_root(a.root)
    cfg = {'chapters': a.chapters, 'draft': a.draft, 'min_freq': a.min_freq,
           'min_variant': a.min_variant, 'max_variant': a.max_variant,
           'min_ent_len': a.min_ent_len, 'year_tol': a.year_tol, 'limit': a.limit}
    results, _ = run(root, cfg)
    md = L.render('一致性审稿报告', results,
                  intro=['- 检查维度：专名异写／角色属性／时间线倒流／标题与正文／timeline 登记／章标题零差异',
                         '- 审查范围：%s ｜ 角色档案：%s ｜ 已知专名：%d'
                         % (a.draft or 'chapters/ 定稿',
                            'characters/' if os.path.isdir(os.path.join(root, 'characters')) else '无',
                            len(load_entities(root)))])
    L.emit(md, a.out or None)
    return 0


if __name__ == '__main__':
    sys.exit(main())
