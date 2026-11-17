#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
NPC 觉醒 · 主引擎

用法：
  python -X utf8 scripts/npc.py --questions        出题（一屏 12 题）
  python -X utf8 scripts/npc.py --card "ABCD..."   判卡
  python -X utf8 scripts/npc.py --calibrate        枚举全组合标定锚点，写回 meta.json
  python -X utf8 scripts/npc.py --audit            九型可达性 + 卡片宽度 + 禁词 + 占位符
  python -X utf8 scripts/npc.py --selftest         确定性 + 解析容错
  python -X utf8 scripts/npc.py --list             列出九型
"""
import argparse
import itertools
import json
import random
import re
import sys
import zlib
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"

AXES = ["script", "route", "goal", "voice", "echo", "reset", "serve"]
AXIS_CN = {
    "script": "台词", "route": "路线", "goal": "目标",
    "voice": "表达", "echo": "回声", "reset": "重置", "serve": "服务",
}
BAR_FULL, BAR_EMPTY = "█", "░"
CARD_WIDTH = 52      # 卡片总宽（终端列）
RULE = "─" * CARD_WIDTH
TEXT_W = 48          # 正文区可用列宽
INDENT = "   "


def disp_width(s):
    """终端显示宽度：CJK 算 2 列。"""
    return sum(2 if ord(c) > 0x2E80 else 1 for c in s)


NO_LINE_START = "，。、）」』】》！？：；…—·!?,.;:)"


def wrap_text(s, width=TEXT_W):
    """按显示宽度折行 + 避头尾（禁则标点不落行首、行首不留空格）。"""
    out, line, cur = [], "", 0
    for ch in s:
        w = 2 if ord(ch) > 0x2E80 else 1
        if cur + w > width and line:
            if ch in NO_LINE_START:
                out.append(line + ch)
                line, cur = "", 0
                continue
            if ch == " ":
                out.append(line.rstrip())
                line, cur = "", 0
                continue
            if w == 1 and line.endswith(" "):
                out.append(line.rstrip() + ch)   # 不留孤字（"接近 0" 的 0）
                line, cur = "", 0
                continue
            out.append(line.rstrip())
            line, cur = ch, w
        else:
            line += ch
            cur += w
    if line.rstrip():
        out.append(line.rstrip())
    return out


def center_disp(s, width=CARD_WIDTH):
    """按显示宽度居中（中文算 2 列），纯 str.center 会算错。"""
    pad = max(0, width - disp_width(s))
    left = pad // 2
    return " " * left + s + " " * (pad - left)


def load():
    q = json.loads((DATA / "questions.json").read_text(encoding="utf-8"))
    t = json.loads((DATA / "types.json").read_text(encoding="utf-8"))
    m = json.loads((DATA / "meta.json").read_text(encoding="utf-8"))
    return q, t, m


# ---------------------------------------------------------------- 计分

def raw_scores(questions, option_ids):
    raw = {k: 0 for k in AXES}
    for q, oid in zip(questions, option_ids):
        for opt in q["options"]:
            if opt["id"] == oid:
                for k, v in opt["weights"].items():
                    raw[k] += v
                break
    return raw


def normalize(raw, anchors):
    out = {}
    for k in AXES:
        lo = anchors[k]["low"]
        hi = anchors[k]["high"]
        span = max(hi - lo, 1)
        out[k] = max(0.0, min(100.0, (raw[k] - lo) / span * 100.0))
    return out


def disc_scores(scores, types, stats):
    """特征轴判别。每型 2–3 条特征轴，得分 = mean(sign · z)。
    sign 为正 = 该轴越高越像这型，为负 = 越低越像。
    用「平均」而非「加权和」：避免负权重在低分端累积出虚假优势
    （加权和会让「什么都低」的人被酒馆老板这类负权重型全吃掉）。"""
    out = {}
    for t in types["types"]:
        d = t["disc"]
        s = 0.0
        for k, sign in d.items():
            st = stats[k]
            s += sign * (scores[k] - st["mean"]) / st["std"]
        out[t["key"]] = s / len(d)
    return out


def classify(scores, types, stats):
    cond = types["rare"]["condition"]
    if (scores["goal"] < cond["goal"]
            and scores["voice"] < cond["voice"]
            and scores["echo"] < cond["echo"]):
        return types["rare"]
    ds = disc_scores(scores, types, stats)
    key = max(ds, key=ds.get)
    return next(t for t in types["types"] if t["key"] == key)


def concentration(scores):
    """浓度 = 整体水平 60% + 峰值轴 40%。
    纯平均会稀释「只有一条轴极度严重」的情况——公告员就是这种。"""
    vals = [scores[k] for k in AXES]
    return round(0.6 * (sum(vals) / len(vals)) + 0.4 * max(vals))


def _pseudo(seed, salt, lo, hi):
    """确定性伪随机，与 JS 引擎逐位一致（Math.imul / >>> 0 同构）。"""
    h = (seed * 1103515245 + salt * 12345 + 1013904223) & 0xFFFFFFFF
    h %= 2147483647
    return lo + h % (hi - lo + 1)


def fill_numbers(text, seed):
    n1 = _pseudo(seed, 1, 180, 340)
    n2 = n1 * _pseudo(seed, 2, 84, 93) // 100
    p1 = _pseudo(seed, 3, 4, 11)
    return (text.replace("{n1}", f"{n1:,}").replace("{n2}", f"{n2:,}")
                .replace("{p1}", str(p1)))


# ---------------------------------------------------------------- 坐标

def coord_of(answer_str, meta, stance):
    c = zlib.crc32(answer_str.encode("utf-8")) & 0xFFFFFFFF
    zones = meta["zones"]
    zone = zones[c % len(zones)]
    num = c % 10000 + 1
    return f"{zone} · 第 {num:04d} 号刷新点 · {stance}"


# ---------------------------------------------------------------- 解析

def parse_answers(text, questions):
    """容错解析答案串：支持 1A 2B / A,B,C / 全角 / 空格 / 换行。"""
    t = text.strip()
    t = t.translate(str.maketrans(
        "ＡＢＣＤａｂｃｄ０１２３４５６７８９",
        "ABCDabcd0123456789"))
    t = t.replace("，", ",").replace("、", ",").replace("　", " ")
    # 剥掉题号前缀："12A" "1.A" "1)" "3：" 这类
    t = re.sub(r"\d+\s*[\.\、\)）:：]?\s*", "", t)
    letters = re.findall(r"[A-Da-d]", t)
    letters = [c.upper() for c in letters]
    valid = {o["id"] for q in questions for o in q["options"]}
    letters = [c for c in letters if c in valid]
    return letters


def complete(letters, questions):
    """漏答用默认项补齐，返回 (补全后的答案, 是否补过)"""
    n = len(questions)
    padded = False
    out = list(letters[:n])
    for i in range(len(out), n):
        out.append(questions[i]["default"])
        padded = True
    return out, padded


# ---------------------------------------------------------------- 渲染

def bar(v):
    filled = int(round(v / 10.0))
    filled = max(0, min(10, filled))
    return f"{BAR_FULL * filled}{BAR_EMPTY * (10 - filled)}"


def render_card(answers, questions, types, meta):
    answer_str = "".join(answers)
    raw = raw_scores(questions, answers)
    scores = normalize(raw, meta["calibration"]["anchors"])
    t = classify(scores, types, meta["calibration"]["stats"])
    conc = concentration(scores)
    seed = zlib.crc32(answer_str.encode("utf-8"))
    is_rare = t["key"] == "not_npc"

    lines = []
    lines.append(RULE)
    lines.append(center_disp("NPC 觉醒 · 检测报告"))
    lines.append(RULE)
    lines.append(f" 类型    {t['name']}")
    if not is_rare:
        lines.append(f" 浓度    {conc}%")
    lines.append(f" 坐标    {coord_of(answer_str, meta, t['stance'])}")
    lines.append(RULE)

    if not is_rare and t.get("line", "——") != "——":
        lines.append(" 固定台词")
        lines.append(f"   {t['line']}")
        lines.append(RULE)

    lines.append(" 系统留言")
    for s in t["verdict"]:
        for ln in wrap_text(fill_numbers(s, seed)):
            lines.append(f"   {ln}")
    lines.append(RULE)

    lines.append(" 参数面板")
    for k in AXES:
        v = scores[k]
        lines.append(f" {AXIS_CN[k]}  {bar(v)}  {round(v):>3}")
    lines.append(RULE)

    lines.append(" 破局支线")
    for i, qtxt in enumerate(t["quests"], 1):
        wrapped = wrap_text(fill_numbers(qtxt, seed + i), TEXT_W - 4)
        lines.append(f" {i}. {wrapped[0]}")
        for ln in wrapped[1:]:
            lines.append(f"    {ln}")
        lines.append("")

    lines.append(RULE)
    if is_rare:
        lines.append(" 你不是 NPC。这张卡很少出，记一下日期。")
    else:
        lines.append(" 不是性格标签，是机制诊断。")
        lines.append(" 要动的不是你自己，是上面那几条参数。")
    lines.append(RULE)
    for ln in wrap_text(meta["disclaimer"], TEXT_W - 2):
        lines.append(f" {ln}")

    # 认真模式出口：浓度够高 + 回声长期缺失，系统收起玩笑
    er = meta["exit_rule"]
    if not is_rare and conc >= er["concentration_min"] and scores["echo"] >= er["echo_min"]:
        lines.append("")
        lines.append(RULE)
        for s in meta["exit_text"]:
            for ln in wrap_text(s, TEXT_W - 2):
                lines.append(f" {ln}")

    return "\n".join(lines)


def render_questions(questions, meta):
    out = [RULE, center_disp("NPC 觉醒 · 检测程序 v1.0"), RULE]
    for s in meta["opening"]:
        out.append(f" {s}")
    out.append("")
    out.append(f" {len(questions)} 道题。没有正确答案，只有你的日志。")
    out.append("")
    out.append(RULE)
    for i, q in enumerate(questions, 1):
        flag = "" if q["id"] != "q10" else ""
        out.append(f" {i:02d}｜{q['text']}{flag}")
        for o in q["options"]:
            out.append(f"   {o['id']} {o['text']}")
        out.append("")
    out.append(RULE)
    out.append(" 答完把答案串发回来就行。格式随意：")
    out.append(" 「1A 2B 3C…」或者直接「ABCD…」都能认。")
    out.append(RULE)
    return "\n".join(out)


# ---------------------------------------------------------------- 子命令

def cmd_questions(args):
    q, t, m = load()
    print(render_questions(q["questions"], m))


def cmd_card(args):
    q, t, m = load()
    letters = parse_answers(args.card, q["questions"])
    if not letters:
        print("[系统] 没识别到答案。至少要给我一个 A/B/C/D。", file=sys.stderr)
        return 2
    answers, padded = complete(letters, q["questions"])
    card = render_card(answers, q["questions"], t, m)
    if padded:
        card += f"\n\n [注：你交的 {len(letters)} 道，剩下的系统替你答了——不算数，但也不重问。]"
    print(card)
    return 0


def cmd_list(args):
    q, t, m = load()
    print(f"{'key':<10} {'类型':<8} {'姿态':<10} 一句话")
    print("-" * 78)
    for x in t["types"]:
        print(f"{x['key']:<10} {x['name']:<8} {x['stance']:<10} {x['tagline']}")
    print("-" * 78)
    print(f"{t['rare']['key']:<10} {t['rare']['name']:<8} {t['rare']['stance']:<10} {t['rare']['tagline']}")


def all_combos(questions):
    choices = [[o["id"] for o in q["options"]] for q in questions]
    return itertools.product(*choices)


# ---- 快速扫描（calibrate / audit 共用；预编译权重元组 + 采样） ----

def _compile_q(questions):
    return [[tuple(o["weights"].get(k, 0) for k in AXES) for o in q["options"]]
            for q in questions]


def _sample_combos(questions, samples, seed=20260921):
    lens = [len(q["options"]) for q in questions]
    rnd = random.Random(seed)
    return [tuple(rnd.randrange(n) for n in lens) for _ in range(samples)]


def _raws_of(compiled, combos):
    out = []
    for combo in combos:
        a = b = c = d = e = f = g = 0
        for i, oi in enumerate(combo):
            w = compiled[i][oi]
            a += w[0]; b += w[1]; c += w[2]; d += w[3]
            e += w[4]; f += w[5]; g += w[6]
        out.append((a, b, c, d, e, f, g))
    return out


def _anchors_from(raws):
    anchors = {}
    for j, k in enumerate(AXES):
        vals = sorted(r[j] for r in raws)
        n = len(vals)
        lo = vals[int(n * 0.05)]
        hi = vals[int(n * 0.95)]
        if hi <= lo:
            hi = lo + 1
        anchors[k] = {"low": lo, "high": hi, "min": vals[0], "max": vals[-1]}
    return anchors


def _stats_from(raws, anchors):
    """归一化后算每轴均值/标准差，供 z-score 判别用。"""
    lo = [anchors[k]["low"] for k in AXES]
    span = [max(anchors[k]["high"] - anchors[k]["low"], 1) for k in AXES]
    acc = [0.0] * 7
    acc2 = [0.0] * 7
    n = len(raws)
    for r in raws:
        for j in range(7):
            v = min(100.0, max(0.0, (r[j] - lo[j]) / span[j] * 100.0))
            acc[j] += v
            acc2[j] += v * v
    stats = {}
    for j, k in enumerate(AXES):
        m = acc[j] / n
        var = max(acc2[j] / n - m * m, 1e-6)
        stats[k] = {"mean": round(m, 2), "std": round(var ** 0.5, 2)}
    return stats


def _hit_of(raws, anchors, stats, types):
    lo = [anchors[k]["low"] for k in AXES]
    span = [max(anchors[k]["high"] - anchors[k]["low"], 1) for k in AXES]
    mean = [stats[k]["mean"] for k in AXES]
    std = [stats[k]["std"] for k in AXES]

    keys = [t["key"] for t in types["types"]]
    idx_map = {k: i for i, k in enumerate(AXES)}
    d_terms = [[(idx_map[k], sign) for k, sign in t["disc"].items()]
               for t in types["types"]]
    d_len = [max(len(x), 1) for x in d_terms]
    rc = types["rare"]["condition"]

    hit = {t["key"]: 0 for t in types["types"]}
    hit[types["rare"]["key"]] = 0

    for r in raws:
        s = [min(100.0, max(0.0, (r[j] - lo[j]) / span[j] * 100.0)) for j in range(7)]
        if s[2] < rc["goal"] and s[3] < rc["voice"] and s[4] < rc["echo"]:
            hit[types["rare"]["key"]] += 1
            continue
        best, bk = -1e18, keys[0]
        for idx, terms in enumerate(d_terms):
            tot = 0.0
            for j, sign in terms:
                tot += sign * (s[j] - mean[j]) / std[j]
            tot /= d_len[idx]
            if tot > best:
                best, bk = tot, keys[idx]
        hit[bk] += 1
    return hit


def cmd_calibrate(args):
    q, t, m = load()
    questions = q["questions"]
    total = 1
    for x in questions:
        total *= len(x["options"])

    samples = min(total, 120000)
    combos = _sample_combos(questions, samples)
    compiled = _compile_q(questions)
    raws = _raws_of(compiled, combos)

    anchors = _anchors_from(raws)
    stats = _stats_from(raws, anchors)
    hit = _hit_of(raws, anchors, stats, t)
    m["calibration"] = {"anchors": anchors, "stats": stats,
                        "combos": total, "samples": samples}

    (DATA / "meta.json").write_text(
        json.dumps(m, ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"枚举空间：{total:,}，实测采样：{samples:,}")
    print(f"{'轴':<6}{'P5':>6}{'P95':>7}{'均值':>8}{'标准差':>8}")
    for k in AXES:
        a, s = anchors[k], stats[k]
        print(f"{AXIS_CN[k]:<6}{a['low']:>6}{a['high']:>7}{s['mean']:>8.1f}{s['std']:>8.1f}")
    print("\n九型可达性（采样）与占比：")
    for k, v in hit.items():
        pct = v / samples * 100
        flag = "   <<< 不可达！" if v == 0 else ""
        print(f"  {k:<10} {v:>8}  {pct:>5.2f}%{flag}")
    return 0


def cmd_audit(args):
    q, t, m = load()
    errs, warns = [], []
    questions = q["questions"]

    for x in questions:
        ids = [o["id"] for o in x["options"]]
        if len(set(ids)) != len(ids):
            errs.append(f"{x['id']} 选项 id 重复")
        if x["default"] not in ids:
            errs.append(f"{x['id']} default 不在选项里")
        for o in x["options"]:
            bad = set(o["weights"]) - set(AXES)
            if bad:
                errs.append(f"{x['id']}{o['id']} 未知轴 {bad}")

    for k in AXES:
        n = sum(1 for x in questions for o in x["options"] if o["weights"].get(k))
        if n < 4:
            warns.append(f"轴 {AXIS_CN[k]} 只有 {n} 个选项覆盖，偏少")

    anchors = m["calibration"]["anchors"]
    stats = m["calibration"]["stats"]
    samples = 120000
    raws = _raws_of(_compile_q(questions), _sample_combos(questions, samples))
    hit = _hit_of(raws, anchors, stats, t)

    for x in t["types"]:
        if hit.get(x["key"], 0) == 0:
            errs.append(f"类型 {x['name']} 不可达")
    if hit.get(t["rare"]["key"], 0) == 0:
        errs.append("稀有解不可达")

    for x in t["types"] + [t["rare"]]:
        for s in x["verdict"]:
            for ph in re.findall(r"\{(\w+)\}", s):
                if ph not in ("n1", "n2", "p1"):
                    errs.append(f"{x['name']} 未知占位符 {{{ph}}}")

    text_all = json.dumps(t, ensure_ascii=False) + json.dumps(q, ensure_ascii=False)
    for w in m["banned_words"]:
        if w in text_all:
            errs.append(f"出现禁词：{w}")

    widest, widest_src = 0, ""
    for combo in _sample_combos(questions, 600, seed=7):
        ans = [questions[i]["options"][oi]["id"] for i, oi in enumerate(combo)]
        card = render_card(ans, questions, t, m)
        for ln in card.split("\n"):
            if disp_width(ln) > widest:
                widest, widest_src = disp_width(ln), ln
    if widest > m["card_max_width"]:
        warns.append(f"卡片最宽 {widest} 列（上限 {m['card_max_width']}）：{widest_src[:36]}")

    # 稀有解不该泛滥
    rare_pct = hit.get(t["rare"]["key"], 0) / samples * 100
    if rare_pct > 6:
        warns.append(f"稀有解占比 {rare_pct:.1f}%，太高，不像稀有")

    print("\n九型分布：")
    for k, v in hit.items():
        print(f"  {k:<10} {v / samples * 100:>5.2f}%")

    for w in warns:
        print(f"[warn] {w}")
    for e in errs:
        print(f"[ERROR] {e}")
    if not errs:
        print(f"\n[ok] audit 通过（九型全可达，卡片最宽 {widest}）")
    return 1 if errs else 0


def cmd_selftest(args):
    q, t, m = load()
    questions = q["questions"]
    problems = []

    # 确定性
    a = render_card(["A"] * 12, questions, t, m)
    b = render_card(["A"] * 12, questions, t, m)
    if a != b:
        problems.append("同一输入两次结果不一致（不确定性）")

    # 解析容错
    cases = [
        ("ABCDABCDABCD", 12),
        ("1A 2B 3C 4D 5A 6B 7C 8D 9A 10B 11C 12D", 12),
        ("A，B、C D\nA B C D A B C D", 12),
        ("Ａ　Ｂ　Ｃ", 3),
        ("1.D 2、A 3）C", 3),
    ]
    for src, want in cases:
        got = len(parse_answers(src, questions))
        if got != want:
            problems.append(f"解析 '{src[:20]}' 得到 {got}，期望 {want}")

    # 缺卷号不应该崩
    letters = parse_answers("", questions)
    if letters:
        problems.append("空串不应解析出答案")

    # 漏答补齐
    answers, padded = complete(["A", "B"], questions)
    if len(answers) != 12 or not padded:
        problems.append("漏答补齐失败")

    # 非法选项被剔除
    if parse_answers("ABZQ1!@#", questions) != ["A", "B"]:
        problems.append("非法字符未剔除")

    for p in problems:
        print(f"[ERROR] {p}")
    if not problems:
        print("[ok] selftest 通过（确定性 / 解析容错 / 漏答补齐 / 非法字符）")
    return 1 if problems else 0


def main():
    ap = argparse.ArgumentParser(add_help=True)
    ap.add_argument("--questions", action="store_true")
    ap.add_argument("--card", metavar="ANSWERS")
    ap.add_argument("--calibrate", action="store_true")
    ap.add_argument("--audit", action="store_true")
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--list", action="store_true")
    args = ap.parse_args()

    if args.questions:
        return cmd_questions(args)
    if args.card:
        return cmd_card(args)
    if args.calibrate:
        return cmd_calibrate(args)
    if args.audit:
        return cmd_audit(args)
    if args.selftest:
        return cmd_selftest(args)
    if args.list:
        return cmd_list(args)
    ap.print_help()
    return 0


if __name__ == "__main__":
    sys.exit(main() or 0)
