#!/usr/bin/env python3
"""rhythm_scan.py — 结构层 AI 味扫描（hekouwang-writer-skill）

锯末词查的是"用了什么词"，本脚本查的是"句子怎么排"。这几种结构最难靠换词去掉：

  - 节奏均匀：正文句长的变异系数（标准差 ÷ 均值）偏低，读起来像一个人在念稿
  - 等长连句：连续 4 句以上字数相差不超过 3
  - 「不是A，而是B」：先立一个没人说过的靶子再推倒，AI 最顺手的转折
  - 段末拔高：多句段落最后一句很短，又落在「才是/真正/本质/意义」这类词上
  - 三连排比：同一段里连续 3 个分句用同样的两个字开头
  - 重复口径/免责：同一类限定（不替你选、以…为准、没算利息）在正文里说了 3 次以上，
    属于防御性写作；「来源」「口径」标题之后的内容不计

全部只报告、不改稿，由人判断。真人写作也会命中，看密度和组合，不看单条。

用法：
    rhythm_scan.py FILE [FILE ...]
    echo "文本" | rhythm_scan.py
    rhythm_scan.py --json FILE

退出码：恒为 0（advisory）；读文件失败为 2。
"""

import argparse
import json
import re
import statistics
import sys

CJK_RE = re.compile(r"[\u4e00-\u9fff]")
SENT_END = "。！？!?"
CLAUSE_SPLIT = re.compile(r"[，,；;。！？!?]")
LIST_RE = re.compile(r"^\s*([-*+]|\d+[.、)])\s+")
SKIP_LINE = re.compile(r"^\s*(\||#|---|\*\*\*|【插图|〖|!\[|::)")

NOT_BUT = re.compile(r"(不是|并非|不在于)[^。！？!?，,；;]{1,24}?[，,]\s*(而是|而在于|是)")
RATHER = re.compile(r"与其说[^。！？]{1,24}不如说")
UPLIFT_WORDS = ("才是", "真正", "本质", "意义", "答案", "力量", "温度", "底气", "从来不是", "终将", "不止是", "价值所在")

HEDGE_FAMILIES = (
    ("免责", re.compile(r"不替(你|读者|大家)|不构成[^。！？]{0,8}建议|仅供参考|不是在(劝|推荐)|不作推荐|不荐")),
    ("以…为准", re.compile(r"以[^。！？，,]{1,16}为准")),
    ("计算口径", re.compile(r"(没|未|不)(算|计)[^。！？，,]{0,6}(利息|上调|涨|在内)|只算[^。！？，,]{1,10}(部分|账户)|按[^。！？，,]{0,6}岁(起领|领取)[^。！？，,]{0,4}算")),
    ("不能推出", re.compile(r"不能(从|据|凭)[^。！？]{0,12}(推出|得出|推断)|不能当[^。！？，,]{1,10}(用|看|读)")),
)
SOURCE_HEAD = re.compile(r"^\s*#{1,6}\s*.*(来源|口径|参考资料|数据说明)")
HEDGE_MAX = 2

UNIFORM_CV = 0.35
MIN_SENTENCES = 12
EQUAL_RUN = 4
EQUAL_DELTA = 3
UPLIFT_MAX = 16
NOT_BUT_PER_K = 1.5


def cjk_len(s):
    return len(CJK_RE.findall(s))


def strip_frontmatter(lines):
    if lines and lines[0].strip() == "---":
        for i in range(1, len(lines)):
            if lines[i].strip() == "---":
                return [(n, "") if n <= i + 1 else (n, l) for n, l in enumerate(lines, 1)]
    return list(enumerate(lines, 1))


def paragraphs(text):
    """返回 [(起始行号, 段落文本, 是否列表项)]；跳过标题、表格、代码、插图占位。"""
    out, buf, start, in_fence = [], [], 0, False

    def flush():
        nonlocal buf
        if buf:
            out.append((start, "".join(buf), False))
        buf = []

    for ln, line in strip_frontmatter(text.splitlines()):
        s = line.strip()
        if s.startswith("```"):
            in_fence = not in_fence
            flush()
            continue
        if in_fence or not s or SKIP_LINE.match(s):
            flush()
            continue
        if LIST_RE.match(s):
            flush()
            out.append((ln, LIST_RE.sub("", s), True))
            continue
        s = s.lstrip("> ").strip()
        if not buf:
            start = ln
        buf.append(s)
    flush()
    return out


def split_sentences(para):
    sents, buf = [], ""
    for ch in para:
        buf += ch
        if ch in SENT_END:
            if cjk_len(buf):
                sents.append(buf.strip())
            buf = ""
    if cjk_len(buf):
        sents.append(buf.strip())
    return sents


def body_only(text):
    """截掉「来源/口径」标题及之后的内容：那里本来就该集中写限定。"""
    lines = text.splitlines()
    for i, line in enumerate(lines):
        if SOURCE_HEAD.match(line):
            return "\n".join(lines[:i])
    return text


def find_hedges(text):
    hits = []
    for ln, line in enumerate(body_only(text).splitlines(), 1):
        for family, rx in HEDGE_FAMILIES:
            for m in rx.finditer(line):
                hits.append({"line": ln, "family": family, "text": m.group(0)})
    counts = {}
    for h in hits:
        counts[h["family"]] = counts.get(h["family"], 0) + 1
    return hits, {k: v for k, v in counts.items() if v > HEDGE_MAX}


def analyze(text):
    paras = paragraphs(text)
    prose = []                     # (行号, 句子)，只算正文段，不算列表项
    not_but, uplift, parallel = [], [], []
    total_cjk = 0

    for ln, para, is_list in paras:
        sents = split_sentences(para)
        total_cjk += cjk_len(para)
        for m in NOT_BUT.finditer(para):
            not_but.append({"line": ln, "text": m.group(0)})
        for m in RATHER.finditer(para):
            not_but.append({"line": ln, "text": m.group(0)})
        if is_list:
            continue
        prose.extend((ln, s) for s in sents)
        if len(sents) >= 3:
            last = sents[-1]
            if cjk_len(last) <= UPLIFT_MAX and not re.search(r"\d", last) and any(w in last for w in UPLIFT_WORDS):
                uplift.append({"line": ln, "text": last})
        clauses = [c.strip() for c in CLAUSE_SPLIT.split(para) if cjk_len(c) >= 4]
        run = 1
        for i in range(1, len(clauses)):
            head = "".join(CJK_RE.findall(clauses[i]))[:2]
            prev = "".join(CJK_RE.findall(clauses[i - 1]))[:2]
            run = run + 1 if head and head == prev else 1
            if run == 3:
                trio = clauses[i - 2:i + 1]
                kind = "数据串" if all(re.search(r"\d", c) for c in trio) else "排比"
                parallel.append({"line": ln, "kind": kind, "text": "，".join(trio)})

    lengths = [cjk_len(s) for _, s in prose]
    cv = None
    if len(lengths) >= MIN_SENTENCES and statistics.mean(lengths):
        cv = round(statistics.pstdev(lengths) / statistics.mean(lengths), 2)

    equal_runs = []
    i = 0
    while i < len(prose):
        j = i
        while j + 1 < len(prose) and abs(lengths[j + 1] - lengths[i]) <= EQUAL_DELTA:
            j += 1
        if j - i + 1 >= EQUAL_RUN:
            run_sents = [text for _, text in prose[i:j + 1]]
            kind = "数据串" if sum(bool(re.search(r"\d", t)) for t in run_sents) * 2 > len(run_sents) else "叙述"
            equal_runs.append({"line": prose[i][0], "count": j - i + 1, "kind": kind,
                               "lengths": lengths[i:j + 1]})
            i = j + 1
        else:
            i += 1

    per_k = round(len(not_but) * 1000 / total_cjk, 2) if total_cjk else 0.0
    warnings = []
    if cv is not None and cv < UNIFORM_CV:
        warnings.append(f"句长变异系数 {cv} < {UNIFORM_CV}，节奏偏均匀")
    prose_runs = [r for r in equal_runs if r["kind"] == "叙述"]
    data_runs = [r for r in equal_runs if r["kind"] == "数据串"]
    if prose_runs:
        warnings.append(f"叙述段等长连句 {len(prose_runs)} 处：长短句交错着重写")
    if data_runs:
        warnings.append(f"数字串连写 {len(data_runs)} 处：同一模板的数字改成表格或列表")
    if per_k > NOT_BUT_PER_K:
        warnings.append(f"「不是A，而是B」{len(not_but)} 处（{per_k}/千字）")
    if uplift:
        warnings.append(f"段末拔高短句 {len(uplift)} 处")
    rhetoric = [p for p in parallel if p["kind"] == "排比"]
    if rhetoric:
        warnings.append(f"三连排比 {len(rhetoric)} 处")
    hedges, hedge_repeat = find_hedges(text)
    for family, n in hedge_repeat.items():
        warnings.append(f"「{family}」类限定正文出现 {n} 次（> {HEDGE_MAX}）：首个关键数旁说一次、来源里说一次")

    return {
        "sentences": len(prose),
        "cjk": total_cjk,
        "length_cv": cv,
        "equal_runs": equal_runs,
        "not_but": not_but,
        "not_but_per_k": per_k,
        "uplift": uplift,
        "parallel": parallel,
        "hedges": hedges,
        "hedge_repeat": hedge_repeat,
        "warnings": warnings,
    }


def selftest():
    flat = "".join(f"第{i}步我们把这一项材料仔细核对清楚。" for i in range(14))
    lively = (
        "上个月群里有人转截图。你可能转发了，也可能在评论里跟人吵过两句，想回一句却说不清这八万多辆是卖出去了还是开出去了。"
        "我拆开算了一遍。只有五万是卖给中国用户的，剩下三万多当天就上了船，再把时间拉长到前八个月，出口已经超过了国内零售。"
        "两句都对。混着用就都错。同一张成绩单能读出五个名次，第六和未进前十说的不是同一个榜。"
        "我自己也开这款车，写这期不是为了站台，只是被问烦了。"
        "下次有人发销量图，先问它是哪一列。"
        "零售加出口等于批发，这是四张表里最硬的一条。"
        "七月最极端。批发创了年内新高，国内零售却排到第十三，差的那部分全是出口，占当月批发七成。"
        "所以别急着下结论。"
    )
    cases = [
        ("均匀节奏检出", flat, lambda r: r["length_cv"] is not None and r["length_cv"] < UNIFORM_CV),
        ("等长连句检出", flat, lambda r: len(r["equal_runs"]) >= 1),
        ("真人节奏不误报", lively, lambda r: r["length_cv"] is not None and r["length_cv"] >= UNIFORM_CV and not r["equal_runs"]),
        ("不是而是检出", "这不是工具的问题，而是习惯的问题。", lambda r: len(r["not_but"]) == 1),
        ("事实否定不误报", "批发新高不是停产。八月是批发。", lambda r: not r["not_but"]),
        ("三分句否定不误报", "他不是不懂，预算不够，是执行没跟上。", lambda r: not r["not_but"]),
        ("CV 偏高标正常", "", lambda _: "偏均匀" not in cv_label(0.73)[1] and "节奏正常" in cv_label(0.73)[1]),
        ("CV 偏低标偏均匀", "", lambda _: "偏均匀" in cv_label(0.2)[1]),
        ("CV 样本不足", "", lambda _: "样本不足" in cv_label(None)[0]),
        ("段末拔高检出", "我们查了表。我们算了账。我们对了口径。这才是真正的答案。", lambda r: len(r["uplift"]) == 1),
        ("短句带数字不误报", "我们查了表。我们算了账。最后差了2.9元。", lambda r: not r["uplift"]),
        ("三连排比检出", "它是一种方法，它是一种态度，它是一种习惯。", lambda r: [p["kind"] for p in r["parallel"]] == ["排比"]),
        ("数字串单列", "交 200 元每月 1.73 元，交 300 元每月 2.48 元，交 1000 元每月 7.77 元。",
         lambda r: [p["kind"] for p in r["parallel"]] == ["数据串"] and not any("排比" in w for w in r["warnings"])),
        ("重复免责检出", "这篇不替你选档。我不替你选。还是不替你选。再说一次不替你决定。",
         lambda r: r["hedge_repeat"].get("免责") == 4),
        ("两次限定不报", "金额以窗口核定为准。到账时间以短信为准。",
         lambda r: not r["hedge_repeat"] and len(r["hedges"]) == 2),
        ("来源节之后不计", "正文以窗口为准。\n\n## 来源与口径\n\n以A为准。以B为准。以C为准。",
         lambda r: len(r["hedges"]) == 1 and not r["hedge_repeat"]),
        ("列表与插图不计句长", "- 第一项内容\n- 第二项内容\n\n【插图 1 · 01.png】", lambda r: r["sentences"] == 0),
    ]
    ok = True
    for name, text, check in cases:
        good = check(analyze(text))
        ok = ok and good
        print(f"  [{'PASS' if good else 'FAIL'}] {name}")
    print("selftest:", "全部通过" if ok else "有失败项")
    return 0 if ok else 1


def cv_label(cv):
    if cv is None:
        return f"样本不足（正文句 <{MIN_SENTENCES}）", ""
    if cv < UNIFORM_CV:
        return str(cv), f"（< {UNIFORM_CV} 偏均匀）"
    return str(cv), f"（≥ {UNIFORM_CV} 节奏正常）"


def show(path, r):
    print(f"文件：{path}")
    cv_text, cv_note = cv_label(r["length_cv"])
    print(f"正文句：{r['sentences']}　中文字数：{r['cjk']}　句长变异系数：{cv_text}{cv_note}")
    print("-" * 64)
    for run in r["equal_runs"]:
        print(f"  L{run['line']:<5} 等长连句（{run['kind']}）{run['count']} 句：{run['lengths']}")
    for item in r["not_but"]:
        print(f"  L{item['line']:<5} 不是…而是 / 不是…是：{item['text']}")
    for item in r["uplift"]:
        print(f"  L{item['line']:<5} 段末拔高：{item['text']}")
    for item in r["parallel"]:
        print(f"  L{item['line']:<5} 三连{item['kind']}：{item['text']}")
    for item in r["hedges"]:
        if item["family"] in r["hedge_repeat"]:
            print(f"  L{item['line']:<5} 重复{item['family']}：{item['text']}")
    print("-" * 64)
    if r["warnings"]:
        for w in r["warnings"]:
            print(f"⚠️ {w}")
        print("判读：单条命中不定罪，看密度和组合。改法是重写整段，不是换词；不要为了压数字故意打乱句子。")
    else:
        print("✅ 未见明显的结构层 AI 味。")
    print()


def main(argv=None):
    ap = argparse.ArgumentParser(description="结构层 AI 味扫描（只报告，不修改）")
    ap.add_argument("files", nargs="*", help="待扫描文件；省略时读 stdin")
    ap.add_argument("--json", action="store_true", help="JSON 输出")
    ap.add_argument("--selftest", action="store_true", help="运行内置自测")
    args = ap.parse_args(argv)
    if args.selftest:
        return selftest()

    texts = []
    if args.files:
        for f in args.files:
            try:
                with open(f, encoding="utf-8") as fh:
                    texts.append((f, fh.read()))
            except OSError as e:
                print(f"读取失败：{f}（{e}）", file=sys.stderr)
                return 2
    else:
        texts.append(("<stdin>", sys.stdin.read()))

    results = [dict(path=p, **analyze(t)) for p, t in texts]
    if args.json:
        print(json.dumps(results[0] if len(results) == 1 else results, ensure_ascii=False, indent=2))
        return 0
    for r in results:
        show(r["path"], r)
    return 0


if __name__ == "__main__":
    sys.exit(main())
