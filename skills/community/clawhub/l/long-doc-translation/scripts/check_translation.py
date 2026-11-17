#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""check_translation.py — long-doc-translation 包内自带自测面（零网络，纯 stdlib）。

用法：
    python3 check_translation.py --selftest     三档自证（好样链／坏样必红／反证与缺目录封死）
    python3 check_translation.py --help         本说明

三档（判定全集在本脚本；SKILL §五 质检七项与 §六 脚本表是验收合同）：
    一档 好样链   fixtures/good 三片走完 overlap_check → qa_check → dedup_boundary（dry-run）→ merge_build，
                  逐项断言面上已承诺的形制：七项质检全 ✅、相邻无重叠、dry-run 不改盘、主稿含全书新术语总表。
    二档 坏样必红 fixtures/bad 每片各带一处病灶，断言判定真的发生并点名到文件与行：缺节／未译残留／
                  正文 OCR 残痕／页码断档／重复行／空文件／重叠退码 2／边界重复对数。
    三档 反证与封死 ①对好样做单点破坏（只在临时副本上，不落包内），每枚必须让对应那一项由 ✅ 转红——
                  红不了就说明该判定是恒真的；②一枚正向不误拦（注释区里的 OCR 残痕必须仍 ✅）；
                  ③目录写错或目录为空时五支脚本各自退码 1、给「[出错]」与「→」下一步、零 Traceback。

夹具命名不是随意的：overlap_check 的 GROUP_RE 与 dedup_boundary 的同部比较都要求「<部>_<篇>_<编号>.md」，
命名不合式时比较一次都不会发生却照样打印全绿（SKILL 硬规则 8 与 pitfalls §1c 记的就是这一类静默假通过）。

出口形制：全过 = 逐条 ok 行 + 末行 "selftest: ALL GREEN（…）"，退码 0；
任一不符 = 逐条 FAIL 行说明实得与规格，末行计数，退码 1。打印只出文件基名与相对标签，
不打印临时根路径，故双跑逐字节可比。
"""
from __future__ import annotations

import hashlib
import os
import re
import shutil
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
FIX = os.path.join(HERE, 'fixtures')
SCRIPTS = {
    'qa': os.path.join(HERE, 'qa_check.py'),
    'overlap': os.path.join(HERE, 'overlap_check.py'),
    'dedup': os.path.join(HERE, 'dedup_boundary.py'),
    'merge': os.path.join(HERE, 'merge_build.py'),
    'reader': os.path.join(HERE, 'build_reader.py'),
}
GOOD, BAD = 'good', 'bad'
CHUNKS = ['01_phil_001.md', '01_phil_002.md', '01_phil_003.md']

CHECKS = []


def check(name, cond, detail):
    CHECKS.append(bool(cond))
    print(('  ok   ' if cond else '  FAIL ') + name + '：' + detail)
    return cond


def run(script, *args):
    r = subprocess.run([sys.executable, '-B', script] + [str(a) for a in args],
                       capture_output=True, text=True)
    return r.returncode, r.stdout + r.stderr


def copy_set(kind, workdir, tag=''):
    dst = os.path.join(workdir, kind + (tag or ''))
    shutil.copytree(os.path.join(FIX, kind), dst)
    return dst


def shas(d):
    return {n: hashlib.sha256(open(os.path.join(d, n), 'rb').read()).hexdigest() for n in CHUNKS}


_CTR = [0]


def newdir(kind, workdir):
    """每枚反证一份独立副本：单点破坏互不污染，也不落包内。"""
    _CTR[0] += 1
    return copy_set(kind, workdir, '-%d' % _CTR[0])


# 被检件里唯一两条「说明行」的完整形状（动态位只允许数字与节名清单，其余一律算判定行）
NOTE_RX = (re.compile(r'^（豁免 \d+ 个索引/格式件：[^）]+）$'),
           re.compile(r'^· 正常接缝（缺 1–\d+ 页，切片边界常见）：\d+ 处，无需处理$'))


def verdict_lines(blk: str):
    """取一块质检报告里的**判定行**：qa_check 把判定打在两空格缩进、明细打在更深缩进。

    同缩进还有两类说明行（「（豁免 …）」「· 正常接缝…」），它们报的是计数不是结论，不参与判定。
    """
    out = []
    for ln in blk.split('\n'):
        if not ln.strip():
            continue
        if ln.startswith('  ') and not ln.startswith('   '):
            t = ln.strip()
            # 说明行的豁免是**有限且可核的语法**：只认被检件自己那两条打全了的话
            # （（豁免 N 个索引/格式件：…）与 · 正常接缝（缺 1–N 页…）：N 处，无需处理），
            # 且整行必须按形状走到头——末尾挂任何别的话就不算说明行。
            # 旧写法是「以（或·开头就跳过」，于是「· 不合格：…」这类明确结论会被当成说明行漏掉（6.1 的 L2 第二形制）。
            if NOTE_RX[0].match(t) or NOTE_RX[1].match(t):
                continue
            out.append(t)
    return out


def lane_ok(blk: str) -> bool:
    """一项质检是不是真的绿（结构判定，不是 token 黑名单）：

    该块的判定行必须**恰好一枚**且以放行标记开头。
    注入任何一枚额外判定行——不论它用 ❌、⚠、⛔、[X] 还是 "FAIL:" 起手——判定行数就变 2，当场不符；
    只留红行（无放行行）同样不符。旧写法是列一串红标记去拒，换一枚没见过的符号就穿透（L2 治的正是这格）。
    """
    v = verdict_lines(blk)
    return len(v) == 1 and v[0].startswith('✅')


def block(report, head):
    """取质检报告里某一节的正文（到下一个【n】或文末）。"""
    parts = re.split(r'(【\d】[^\n]*)', report)
    out = []
    grab = False
    for p in parts:
        if p.startswith('【'):
            grab = p.startswith(head)
            continue
        if grab:
            out.append(p)
    return ''.join(out)


def tier1(work):
    d = copy_set(GOOD, work)
    rc, out = run(SCRIPTS['overlap'], d)
    check('A1 好样·重叠判定放行', rc == 0 and '✅ 未发现相邻片段重叠' in out,
          f'overlap_check 实得退码 {rc}，报告含放行句＝{"是" if "✅ 未发现相邻片段重叠" in out else "否"}（规格 0 且放行）')
    rc, out = run(SCRIPTS['qa'], d, '--expect', '3')
    lanes = {k: block(out, '【%d】' % k) for k in range(1, 8)}
    green = [k for k in range(2, 8) if lane_ok(lanes[k])]
    check('A2 好样·质检退码', rc == 0, f'qa_check 实得退码 {rc}（规格 0）')
    check('A3 好样·七项里【2】—【7】逐项判定行唯一且为放行行', green == [2, 3, 4, 5, 6, 7],
          '逐项判绿的项＝%s（规格 2,3,4,5,6,7 全绿；各块判定行数实得 %s）' % (
              green, {k: len(verdict_lines(lanes[k])) for k in range(2, 8)}))
    check('A4 好样·片段数对账', '✅ 一致' in lanes[1],
          '【1】实得：%s（规格「实际片段数：3；预期：3 → ✅ 一致」）' % lanes[1].strip().splitlines()[0][:56] if lanes[1].strip() else '【1】缺位')
    check('A5 好样·注释区豁免生效且【4】判定行唯一', '注释区的纠错说明已正确豁免' in lanes[4] and lane_ok(lanes[4]),
          '【4】实得：%s｜该块判定行＝%s（规格：好样把 ζ.B. 放在原注区，必须不报正文残痕，且该块只许一枚判定行）' % (
              lanes[4].strip().splitlines()[0][:48] if lanes[4].strip() else '缺位',
              '、'.join(verdict_lines(lanes[4])) or '无'))
    before = shas(d)
    rc, out = run(SCRIPTS['dedup'], d)
    check('A6 好样·边界去重放行', rc == 0 and '✅ 未发现边界重复' in out,
          f'dedup 实得退码 {rc}，放行句＝{"是" if "✅ 未发现边界重复" in out else "否"}（规格 0 且放行）')
    check('A7 好样·dry-run 不改盘', shas(d) == before,
          '三片摘要逐枚比：改前后%s（规格：不加 --apply 一律不落盘）' % ('相同' if shas(d) == before else '不同'))
    outdir = os.path.join(work, 'merged1')
    rc, out = run(SCRIPTS['merge'], d, outdir)
    md = os.path.join(outdir, '译著主稿.md') if os.path.isdir(outdir) else outdir + '.md'
    if not os.path.isfile(md):
        cand = [f for f in ([outdir + '.md'] + ([os.path.join(outdir, n)] if os.path.isdir(outdir) else []))
                if os.path.isfile(f)]
        md = cand[0] if cand else md
    body = open(md, encoding='utf-8').read() if os.path.isfile(md) else ''
    check('A8 好样·合并退码与主稿在场', rc == 0 and bool(body),
          f'merge 实得退码 {rc}，主稿字节 {len(body.encode("utf-8"))}（规格 0 且非空）')
    check('A9 好样·文末全书新术语总表', '全书新术语总表' in body,
          '主稿含「全书新术语总表」＝%s（规格：面上承诺合并时汇总各片新术语）' % ('是' if '全书新术语总表' in body else '否'))
    terms = len(re.findall(r'^- \w+ → ', body.split('全书新术语总表')[-1], re.M)) if '全书新术语总表' in body else 0
    check('A10 好样·总表收齐三条译名', terms == 3, f'总表条目实得 {terms} 条（规格 3，按三片各一条）')
    heads = len(re.findall(r'^## 第00[123]片', body, re.M))
    check('A11 好样·三片标题各进一次稿', heads == 3, f'片标题实得 {heads} 处（规格 3）')
    html = md[:-3] + '.html'
    if os.path.isfile(html):
        check('A12 好样·HTML 两态合式', os.path.getsize(html) > 0, 'HTML 在场且非空（装了 markdown 的一态）')
    else:
        check('A12 好样·HTML 两态合式', 'markdown' in out and '跳过' in out,
              '无 markdown 时必须明说跳过并给安装指引；实得句：%s' % [l.strip() for l in out.splitlines() if 'HTML' in l][:1])


def tier2(work):
    d = copy_set(BAD, work)
    rc, out = run(SCRIPTS['overlap'], d)
    check('B1 坏样·重叠发红并点名片段对', rc == 2 and '01_phil_001.md ⟷ 01_phil_002.md' in out,
          f'overlap 实得退码 {rc}，点名对＝{"是" if "01_phil_001.md ⟷ 01_phil_002.md" in out else "否"}（规格 2 并点名）')
    rc, out = run(SCRIPTS['qa'], d, '--expect', '3')
    lanes = {k: block(out, '【%d】' % k) for k in range(1, 8)}
    check('B2 坏样·缺体例三节逐条点名', '❌ 3 处缺失' in lanes[2]
          and all(s in lanes[2] for s in ('01_phil_001.md 缺 #### 新术语', '01_phil_003.md 缺 #### 原注', '01_phil_003.md 缺 #### 新术语')),
          '【2】实得：%s（规格：三处各点名到文件与节名）' % [l.strip() for l in lanes[2].splitlines() if l.strip()][:1])
    check('B3 坏样·未译残留点名到行号', '⚠ 1 处' in lanes[3] and '01_phil_002.md:5 |' in lanes[3],
          '【3】实得：%s（规格：点名 01_phil_002.md 第 5 行）' % [l.strip() for l in lanes[3].splitlines() if l.strip()][:1])
    check('B4 坏样·正文 OCR 残痕点名到行', '❌ 正文区 1 处' in lanes[4] and '01_phil_001.md:5 [Sdiell' in lanes[4],
          '【4】实得：%s（规格：正文那处发红并点名 01_phil_001.md 第 5 行）' % [l.strip() for l in lanes[4].splitlines() if l.strip()][:1])
    check('B5 坏样·注释区残痕不得误报', '01_phil_003' not in lanes[4],
          '【4】块内出现 01_phil_003＝%s（规格：否——坏样故意把 Sdiell 写进 003 的译注区，必须被豁免）' % ('是' if '01_phil_003' in lanes[4] else '否'))
    check('B6 坏样·页码断档分级并给出缺页', '疑似断档' in lanes[5] and '缺 49 页' in lanes[5],
          '【5】实得：%s（规格：002 止 S.30 → 003 起 S.80，缺 49 页）' % [l.strip() for l in lanes[5].splitlines() if '缺' in l][:1])
    check('B7 坏样·重复行按次数报出', '⚠ 1 条' in lanes[6] and '2× ' in lanes[6],
          '【6】实得：%s（规格：那一句 2× 且被列出）' % [l.strip() for l in lanes[6].splitlines() if l.strip()][:1])
    check('B8 坏样·占位短片发红点名', '❌ 1 个文件行数 < 15' in lanes[7] and '01_phil_003.md: 10 行' in lanes[7],
          '【7】实得：%s（规格：点名 01_phil_003.md 与其行数）' % [l.strip() for l in lanes[7].splitlines() if l.strip()][:1])
    before = shas(d)
    rc, out = run(SCRIPTS['dedup'], d)
    check('B9 坏样·边界重复被检出', '检测到：1 对' in out and '删除 1 行' in out,
          'dedup 实得：%s（规格：1 对、删除 1 行）' % [l.strip() for l in out.splitlines() if '检测到' in l][:1])
    check('B10 坏样·dry-run 同样不改盘', rc == 0 and shas(d) == before,
          f'实得退码 {rc}（规格 0）且三片摘要逐枚相同＝{shas(d) == before}')


def mutate(d, name, sub):
    p = os.path.join(d, name)
    text = open(p, encoding='utf-8').read()
    new = sub(text)
    if new == text:
        return False
    open(p, 'w', encoding='utf-8').write(new)
    return True


def miss(name):
    return '锚失配：好样 %s 里没命中要改的那处，这枚反证无从进行（夹具漂移要先修夹具）' % name


def first(lines):
    return [l.strip() for l in lines.splitlines() if l.strip()][:1]


def tier3(work):
    # ① 单点破坏：每枚必须让对应判定转红（防恒真）
    d = newdir(GOOD, work)
    hit = mutate(d, '01_phil_001.md', lambda t: t.replace('#### 新术语', '#### 术语'))
    b = block(run(SCRIPTS['qa'], d, '--expect', '3')[1], '【2】') if hit else ''
    check('D1 反证·缺新术语节必红', bool(hit) and '❌' in b and '01_phil_001.md 缺 #### 新术语' in b,
          miss('01_phil_001.md') if not hit else
          '【2】实得：%s（规格：改名即缺节，必须发红并点名）' % [l.strip() for l in b.splitlines() if '缺 ####' in l][:2])

    d = newdir(GOOD, work)
    hit = mutate(d, '01_phil_002.md', lambda t: t.replace('〔S. 21〕', '〔S. 19〕', 1))
    rc, out = run(SCRIPTS['overlap'], d)
    check('D2 反证·首页码前移必判重叠', bool(hit) and rc == 2 and '重叠约' in out,
          miss('01_phil_002.md') if not hit else
          f'overlap 实得退码 {rc}（规格 2），点名重叠＝{"是" if "重叠约" in out else "否"}')

    d = newdir(GOOD, work)
    hit = mutate(d, '01_phil_002.md', lambda t: t.replace(
        '002 辰行：新术语条目在本片末尾逐条列出，便于汇总。',
        'Die Einheit der Bildung ist ein langwieriger Streitpunkt der Forschung.'))
    b = block(run(SCRIPTS['qa'], d, '--expect', '3')[1], '【3】') if hit else ''
    check('D3 反证·正文塞整行外文必红', bool(hit) and '⚠ 1 处' in b and '01_phil_002.md:' in b,
          miss('01_phil_002.md') if not hit else
          '【3】实得：%s（规格：发红并点名行号）' % first(b))

    d = newdir(GOOD, work)
    hit = mutate(d, '01_phil_003.md', lambda t: t.replace('〔S. 44〕', '正文里混入 ζ.B. 这一处 OCR 残痕。\n〔S. 44〕', 1))
    b = block(run(SCRIPTS['qa'], d, '--expect', '3')[1], '【4】') if hit else ''
    check('D4 反证·正文残痕必红而注释区同串不红', bool(hit) and '❌ 正文区 1 处' in b and '01_phil_003.md:' in b,
          miss('01_phil_003.md') if not hit else
          '【4】实得：%s（规格：正文一枚即发红；好样里同一串在原注区是 ✅）' % first(b))

    d = newdir(GOOD, work)
    hit = mutate(d, '01_phil_003.md', lambda t: '\n'.join(t.split('\n')[:6]))
    b = block(run(SCRIPTS['qa'], d, '--expect', '3')[1], '【7】') if hit else ''
    check('D5 反证·截成短片必红', bool(hit) and '❌ 1 个文件行数 < 15' in b and '01_phil_003.md:' in b,
          miss('01_phil_003.md') if not hit else
          '【7】实得：%s（规格：发红并点名行数）' % first(b))

    d = newdir(GOOD, work)
    hit = mutate(d, '01_phil_003.md', lambda t: t.replace('〔S. 33〕', '〔S. 60〕', 1))
    b = block(run(SCRIPTS['qa'], d, '--expect', '3')[1], '【5】') if hit else ''
    check('D6 反证·页码后移必判断档', bool(hit) and '疑似断档' in b and '缺 27 页' in b,
          miss('01_phil_003.md') if not hit else
          '【5】实得：%s（规格：002 止 S.32 → 003 起 S.60，缺 27 页）' % [l.strip() for l in b.splitlines() if '缺 27' in l][:1])

    d = newdir(GOOD, work)
    head = open(os.path.join(FIX, GOOD, '01_phil_001.md'), encoding='utf-8').read().split('\n')[3]
    hit = mutate(d, '01_phil_002.md', lambda t: t.replace('〔S. 21〕', '〔S. 21〕\n' + head, 1))
    out = run(SCRIPTS['dedup'], d)[1] if hit else ''
    check('D7 反证·边界重复必被检出', bool(hit) and '检测到：1 对' in out,
          miss('01_phil_002.md') if not hit else
          'dedup 实得：%s（规格：复制上一片正文行到本片开头即判 1 对）' % [l.strip() for l in out.splitlines() if '检测到' in l][:1])

    # ② 正向不误拦：同一残痕串留在注释区，判定必须仍 ✅
    d = newdir(GOOD, work)
    hit = mutate(d, '01_phil_002.md', lambda t: t.replace(
        '002 原注一：脚注译文，保留原编号以便与底本对读。',
        '002 原注一：注文里留下 Sdiell 与 ζ.B. 两处，属注释区应被豁免。'))
    b = block(run(SCRIPTS['qa'], d, '--expect', '3')[1], '【4】') if hit else ''
    check('P1 正向·注释区残痕不误拦', bool(hit) and lane_ok(b) and '01_phil_002' not in b,
          miss('01_phil_002.md') if not hit else
          '【4】判定行＝%s（规格：仍唯一一枚放行行，不得把注文里的纠错说明判成病灶）' % ('、'.join(verdict_lines(b)) or '无'))

    # ③ 缺目录／空目录封死（SKILL「一条重要保证」承诺的那一类静默假通过）
    missing = os.path.join(work, 'no-such-dir')
    empty = os.path.join(work, 'empty-dir')
    os.makedirs(empty, exist_ok=True)
    for tag, path in (('缺目录', missing), ('空目录', empty)):
        bad = []
        for name, script in sorted(SCRIPTS.items()):
            if name == 'reader':
                rc, out = run(script, path, os.path.join(work, 'r-' + name))
            elif name == 'merge':
                rc, out = run(script, path, os.path.join(work, 'm-' + tag))
            elif name == 'qa':
                rc, out = run(script, path, '--expect', '3')
            else:
                rc, out = run(script, path)
            if rc != 1 or '[出错]' not in out or '→' not in out or 'Traceback' in out:
                bad.append('%s：退码 %s，出错句%s，下一步提示%s，Traceback%s' % (
                    os.path.basename(script), rc, '有' if '[出错]' in out else '无',
                    '有' if '→' in out else '无', '有' if 'Traceback' in out else '无'))
        check('E-%s·五支脚本一律报错退出' % tag, not bad,
              '不合式：%s（规格：五支全部退码 1＋给「[出错]」与「→」下一步＋零 Traceback）' % (bad if bad else '无'))


if __name__ == '__main__':
    if '--help' in sys.argv or '-h' in sys.argv or len(sys.argv) == 1:
        print(__doc__)
        sys.exit(0)
    if '--selftest' not in sys.argv:
        print('check_translation: 本件只作包内自测面，用法是 --selftest（其余形制见 --help）')
        sys.exit(1)
    for kind in (GOOD, BAD):
        if not os.path.isdir(os.path.join(FIX, kind)):
            print('SELFTEST FAIL: 缺夹具目录 fixtures/%s（规格：好样与坏样随包交付，缺一不发绿）' % kind)
            sys.exit(1)
    for n in CHUNKS:
        for kind in (GOOD, BAD):
            if not os.path.isfile(os.path.join(FIX, kind, n)):
                print('SELFTEST FAIL: 缺夹具 fixtures/%s/%s（规格：三片齐）' % (kind, n))
                sys.exit(1)
    work = tempfile.mkdtemp(prefix='ldt-selftest-')
    try:
        work_arg = work
        tier1(work_arg)
        tier2(work_arg)
        tier3(work_arg)
    finally:
        shutil.rmtree(work, ignore_errors=True)
    n_bad = sum(1 for ok in CHECKS if not ok)
    print('selftest: %s（一档 好样链 · 二档 坏样必红 · 三档 反证与缺目录封死；断言 %d 条，不符 %d 条）' % (
        'ALL GREEN' if not n_bad else 'FAIL', len(CHECKS), n_bad))
    sys.exit(0 if not n_bad else 1)
