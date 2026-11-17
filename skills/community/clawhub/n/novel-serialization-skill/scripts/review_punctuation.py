# -*- coding: utf-8 -*-
"""
标点审查（review_punctuation）—— 标点、引号与用字规范

检查维度：
  1. 引号错位：中文引号 “ ” 数量不等（扩写插入块最易踩的坑）
  2. 半角标点：中文语境中的 , ; : ? ! 与半角括号
  3. 直引号：正文出现 " ' 而非 “ ” ‘ ’
  4. 繁体混入：按词组扫描（单字扫描会误伤「候／有／也」等简繁同形字）
  5. 英文残留：中文叙述中混入的拉丁词（如把「大连」写成「大 connected」）
  6. 省略号/破折号/感叹号：非标准写法与密度（阈值与 humanizer_check.py 一致）
  7. 重复标点与行首标点：？？ ！！ ，， 以及段落以标点开头
  8. 书名号配对：《 》 数量不等

用法（在子项目根目录执行）：
    python "../GitHub Novel Serialization Skill/scripts/review_punctuation.py"
    python "../GitHub Novel Serialization Skill/scripts/review_punctuation.py" --chapters 031 034
    python "../GitHub Novel Serialization Skill/scripts/review_punctuation.py" --draft notes-personal/正文草稿.md

判定：FAIL —— 确定性错误（引号错位）；WARN —— 需人工复核。
"""
import sys
import os
import re
import argparse
from collections import Counter

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _review_lib as L

# 繁体词组：只收含繁体专用字的词（「警察」「东西」一类简繁同形词入表会误报）
TRAD = ['時候', '發現', '對於', '關係', '這個', '我們', '他們', '應該', '已經', '這樣',
        '裡面', '以後', '幾歲', '於是', '什麼', '為什麼', '從來', '將來', '業務', '實際',
        '發展', '數字', '學習', '國家', '實現', '會議', '時間', '長官', '軍隊', '軍事',
        '製造', '繼續', '認識', '護照', '建議', '認為', '討論', '議會', '設備', '計畫',
        '計劃', '經濟', '總統', '總理', '鐵路', '鋼鐵', '礦產', '農業', '工業', '商業',
        '聽說', '能夠', '習慣', '醫院', '醫生', '學校', '學生', '老師', '圖書', '標準',
        '機器', '機關', '機會', '檔案', '證據', '證明', '評估', '評價', '試驗', '實驗',
        '語言', '翻譯', '資本', '資料', '資源', '貨幣', '財務', '費用', '銀行', '處理',
        '處罰', '這裡', '那裡', '哪裡', '東西', '開關', '關門', '發現什麼', '還沒有']
DEFAULTS = {'max_dash': 5, 'max_ellipsis': 2, 'max_excl': 2, 'chapters': (), 'draft': ''}


def audit(item, cfg):
    issues = []
    body = '\n'.join(L.body_lines(item.text))
    paras = L.paragraphs(item.text)
    k = max(1, L.cn(item.text) / 1000.0)

    # 1. 引号配对
    o, c = body.count('“'), body.count('”')
    if o != c:
        issues.append(L.Issue('FAIL', '引号错位',
                              '“ %d 个 ≠ ” %d 个（差 %d）' % (o, c, abs(o - c)), item.name))
    ob, cb = body.count('《'), body.count('》')
    if ob != cb:
        issues.append(L.Issue('WARN', '书名号不配对', '《 %d 个 ≠ 》 %d 个' % (ob, cb), item.name))

    # 2. 半角标点（前接中文）
    half = Counter()
    for m in re.finditer(r'([\u4e00-\u9fff])([,;:?!])', body):
        half[m.group(2)] += 1
    if half:
        issues.append(L.Issue('WARN', '半角标点',
                              '中文后直接跟半角标点：%s（共 %d 处）'
                              % ('、'.join('%s×%d' % (a, b) for a, b in half.most_common(4)), sum(half.values())),
                              item.name))

    # 3. 直引号
    if body.count('"') or body.count("'"):
        issues.append(L.Issue('WARN', '直引号',
                              '正文出现直引号 " ×%d、\' ×%d，应为 “ ” ‘ ’'
                              % (body.count('"'), body.count("'")), item.name))

    # 4. 繁体混入
    trad_hits = []
    for i, ln in enumerate(L.body_lines(item.text), 1):
        for w in TRAD:
            if w in ln:
                trad_hits.append((i, w))
    if trad_hits:
        issues.append(L.Issue('WARN', '繁体混入', '%d 处，如 %s'
                              % (len(trad_hits), '、'.join('L%d:%s' % (a, b) for a, b in trad_hits[:3])),
                              item.name))

    # 5. 英文残留（中文语境中的拉丁词）
    en = [w for w in re.findall(r'(?<=[\u4e00-\u9fff])[A-Za-z]{2,}|[A-Za-z]{2,}(?=[\u4e00-\u9fff])', body)]
    if en:
        issues.append(L.Issue('WARN', '英文残留', '%d 处：%s'
                              % (len(en), '、'.join(sorted(set(en))[:6])), item.name))

    # 6. 省略号/破折号/感叹号
    bad_ell = len(re.findall(r'\.{2,}|。。|‥', body))
    if bad_ell:
        issues.append(L.Issue('WARN', '省略号写法', '%d 处非标准（应为 ……）' % bad_ell, item.name))
    narr = L.narr(item.text)
    for name, ch, lim in (('破折号', '——', cfg['max_dash']),
                          ('省略号', '……', cfg['max_ellipsis']),
                          ('感叹号', '！', cfg['max_excl'])):
        # 与 humanizer_check.py 同阈值，另加 0.5/千字容差，避免两份报告在边界上打架
        d = narr.count(ch) / k
        if d > lim + 0.5:
            issues.append(L.Issue('WARN', '%s密度' % name,
                                  '%.1f/千字（限 %g），共 %d 处' % (d, lim, narr.count(ch)), item.name))

    # 7. 重复标点 / 行首标点
    dup = re.findall(r'([？！，。；、])\1', body)
    if dup:
        issues.append(L.Issue('WARN', '重复标点', '%d 处：%s'
                              % (len(dup), '、'.join(a * 2 for a in set(dup))), item.name))
    head = [p[:6] for p in paras if p and p[0] in '，。！？；：、']
    if head:
        issues.append(L.Issue('WARN', '行首标点', '%d 处，如「%s…」' % (len(head), head[0]), item.name))
    return issues


def run(root, cfg):
    cfg = dict(DEFAULTS, **cfg)
    items = L.collect_items(root, cfg.get('chapters', ()), cfg.get('draft', ''))
    return [L.make_result(it.name, it.path, audit(it, cfg), {'num': it.num}) for it in items], None


def main():
    ap = L.add_common_args(argparse.ArgumentParser(description='标点审查：标点、引号与用字规范'))
    ap.add_argument('--max-dash', type=float, default=5, help='破折号密度上限（每千字，默认 5）')
    ap.add_argument('--max-ellipsis', type=float, default=2, help='省略号密度上限（每千字，默认 2）')
    ap.add_argument('--max-excl', type=float, default=2, help='感叹号密度上限（每千字，默认 2）')
    a = ap.parse_args()
    root = L.find_root(a.root)
    results, _ = run(root, dict(vars(a)))
    md = L.render('标点审查报告', results,
                  intro=['- 检查维度：引号配对／半角标点／直引号／繁体混入／英文残留／标点密度／重复与行首标点／书名号',
                         '- 审查范围：%s ｜ 密度阈值：破折号 %g、省略号 %g、感叹号 %g（每千字）'
                         % (a.draft or 'chapters/ 定稿', a.max_dash, a.max_ellipsis, a.max_excl)])
    L.emit(md, a.out or None)
    return 0


if __name__ == '__main__':
    sys.exit(main())
