# -*- coding: utf-8 -*-
"""learn_guards.py — 术语守卫自学习（v2.2.0）。

把「这次扫描误报了这个词」变成一条可复用的守卫，存进 scripts/user_guards.json，
之后每次 scan 自动生效——不再需要手改 patterns_*.json（升级会被覆盖）。

守卫语义与内置 term_guards 完全一致：命中词左右 ~30 字符窗口里出现任一
allow_before/allow_after 上下文词 → 该次命中豁免（正当用法不扣分）。

用法:
    python scripts/learn_guards.py add 沉淀 --before "化学,析出" --after "反应,物"
    python scripts/learn_guards.py from-text 沉淀 误报样本.txt   # 从真实语料自动提取上下文
    python scripts/learn_guards.py list
    python scripts/learn_guards.py remove 沉淀
    python scripts/learn_guards.py test "免疫复合物在管底形成大量沉淀反应后离心"

退出码: 0 成功 | 2 用法/文件错误
"""

import argparse
import json
import os
import re
import sys
import datetime

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import hxt_core

GUARDS_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                           "user_guards.json")


def load_store():
    if not os.path.exists(GUARDS_PATH):
        return {"_meta": {}, "term_guards": []}
    with open(GUARDS_PATH, encoding="utf-8") as f:
        data = json.load(f)
    if not isinstance(data.get("term_guards", []), list):
        raise ValueError("user_guards.json 结构损坏：term_guards 不是列表——"
                         "请删除该文件后重建，或用 list 检查当前内容")
    return data


def save_store(data):
    data.setdefault("_meta", {})
    data["_meta"]["updated"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    data["_meta"]["note"] = "learn_guards.py 生成；语义同 term_guards，lang 缺省=中英都生效"
    tmp = GUARDS_PATH + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    os.replace(tmp, GUARDS_PATH)


def detect_term_lang(term):
    return "zh" if re.search(r"[\u4e00-\u9fff]", term) else "en"


def extract_context(text, term, n_each=6):
    """从真实语料里取 term 每次出现位置的上下文词。

    中文：左右各取 n_each 字连续片段去标点（guard_hit 对中文按子串锚定）。
    英文（v2.2.1 修）：在 ±30 字符窗内按词切——guard_hit 的上下文窗口保留
    空格，若把空白剥掉会学出永不触发的「死守卫」。
    返回 (before_list, after_list)。"""
    before, after = [], []
    pat = re.escape(term)
    flags = 0 if re.search(r"[\u4e00-\u9fff]", term) else re.IGNORECASE
    is_zh = bool(re.search(r"[\u4e00-\u9fff]", term))
    for m in re.finditer(pat, text, flags):
        s, e = m.span()
        if is_zh:
            b = re.sub(r"[\s，。、；：！？「」（）(),.:;!?\"']+", "",
                       text[max(0, s - n_each):s])
            a = re.sub(r"[\s，。、；：！？「」（）(),.:;!?\"']+", "", text[e:e + n_each])
            if b:
                before.append(b)
            if a:
                after.append(a)
        else:
            wb = re.findall(r"[A-Za-z][A-Za-z\-']*", text[max(0, s - 30):s])
            wa = re.findall(r"[A-Za-z][A-Za-z\-']*", text[e:e + 30])
            before.extend(w.lower() for w in wb[-3:])
            after.extend(w.lower() for w in wa[:3])
    # 去重保序，各留 8 个
    return list(dict.fromkeys(before))[:8], list(dict.fromkeys(after))[:8]


def main():
    ap = argparse.ArgumentParser(
        description="术语守卫自学习：误报 → 可复用守卫（存 user_guards.json）")
    ap.add_argument("--version", action="version",
                    version="%(prog)s " + hxt_core.__version__)
    sub = ap.add_subparsers(dest="cmd", required=True)

    p_add = sub.add_parser("add", help="手工添加守卫：add 术语 --before 词1,词2 --after 词3,词4")
    p_add.add_argument("term")
    p_add.add_argument("--before", default="", help="允许的前文，逗号分隔")
    p_add.add_argument("--after", default="", help="允许的后文，逗号分隔")
    p_add.add_argument("--lang", choices=["zh", "en"], default=None,
                       help="守卫生效词库（缺省=自动：含汉字 zh，否则 en）")

    p_ctx = sub.add_parser("from-text", help="从真实语料自动提取上下文：from-text 术语 样本文件")
    p_ctx.add_argument("term")
    p_ctx.add_argument("sample", help="含该术语正当用法的 .txt/.md 样本")
    p_ctx.add_argument("--lang", choices=["zh", "en"], default=None)

    sub.add_parser("list", help="列出现有用户守卫")

    p_rm = sub.add_parser("remove", help="删除守卫：remove 术语")
    p_rm.add_argument("term")

    p_t = sub.add_parser("test", help="验证守卫效果：test \"样本文本\"")

    p_exp = sub.add_parser("export", help="导出守卫库到 JSON 文件（多项目/多机共享）："
                                          "export 导出文件.json")
    p_exp.add_argument("out", help="导出目标 .json 路径")

    p_imp = sub.add_parser("import", help="从 JSON 导入守卫（合并策略=术语级去重："
                                          "同术语已存在则跳过并计数，新术语追加）:"
                                          "import 导出文件.json")
    p_imp.add_argument("src", help="导入源 .json 路径")
    p_imp.add_argument("--dry-run", action="store_true",
                       help="只统计将导入的条数，不写库")
    p_t.add_argument("text")

    args = ap.parse_args()

    try:
        if args.cmd == "add":
            if not args.before and not args.after:
                print("至少提供 --before 或 --after 之一（纯 term 无上下文等于永不豁免）",
                      file=sys.stderr)
                sys.exit(2)
            data = load_store()
            g = {"term": args.term,
                 "allow_before": [w.strip() for w in args.before.split(",") if w.strip()],
                 "allow_after": [w.strip() for w in args.after.split(",") if w.strip()],
                 "lang": args.lang or detect_term_lang(args.term)}
            data["term_guards"] = [x for x in data.get("term_guards", [])
                                   if x.get("term") != args.term]
            data["term_guards"].append(g)
            save_store(data)
            print("已保存守卫：%s（lang=%s，前文 %d 项 / 后文 %d 项）"
                  % (args.term, g["lang"], len(g["allow_before"]), len(g["allow_after"])))
            print("立即生效：下次 scan 自动豁免这些上下文下的命中。")

        elif args.cmd == "from-text":
            text = hxt_core.read_text(args.sample)
            before, after = extract_context(text, args.term)
            if not before and not after:
                print("样本中未找到「%s」的出现——请确认样本含该词的正当用法" % args.term,
                      file=sys.stderr)
                sys.exit(2)
            data = load_store()
            g = {"term": args.term, "allow_before": before, "allow_after": after,
                 "lang": args.lang or detect_term_lang(args.term)}
            data["term_guards"] = [x for x in data.get("term_guards", [])
                                   if x.get("term") != args.term]
            data["term_guards"].append(g)
            save_store(data)
            print("已从样本提取并保存守卫：%s（lang=%s）" % (args.term, g["lang"]))
            print("  前文:", ", ".join(before) or "（无）")
            print("  后文:", ", ".join(after) or "（无）")
            print("提醒：自动提取的上下文来自这份样本，若样本外的正当用法仍被误报，"
                  "用 add 补充或用 test 验证。")

        elif args.cmd == "list":
            data = load_store()
            gs = data.get("term_guards", [])
            if not gs:
                print("（无用户守卫——用 add / from-text 添加）")
                return
            print("用户守卫 %d 条（%s）：" % (len(gs), GUARDS_PATH))
            for g in gs:
                print("  %-12s lang=%-3s 前:[%s] 后:[%s]"
                      % (g.get("term", "?"), g.get("lang", "-"),
                         ",".join(g.get("allow_before", [])) or "-",
                         ",".join(g.get("allow_after", [])) or "-"))

        elif args.cmd == "remove":
            data = load_store()
            n0 = len(data.get("term_guards", []))
            data["term_guards"] = [x for x in data.get("term_guards", [])
                                   if x.get("term") != args.term]
            if len(data["term_guards"]) == n0:
                print("未找到术语「%s」的守卫" % args.term, file=sys.stderr)
                sys.exit(2)
            save_store(data)
            print("已删除守卫：%s" % args.term)

        elif args.cmd == "test":
            hxt_core.clear_pattern_cache()
            text = args.text
            r_after = hxt_core.scan(text)
            print("扫描结果：score=%s level=%s" % (r_after["score"], r_after["level"]))
            if r_after["guards_applied"]:
                for g in r_after["guards_applied"]:
                    print("  豁免：命中「%s」← 守卫「%s」" % (g["hit"], g["guard"]))
            else:
                print("  本次扫描无守卫豁免记录——若该词仍被计分，说明上下文不在守卫窗口内，"
                      "用 add 补充更精确的前/后文。")
            for cid, c in r_after["categories"].items():
                if c["count"]:
                    print("  [%s] ×%d %s" % (cid, c["count"], c["label"]))
    except (OSError, ValueError) as e:
        print("错误: %s" % e, file=sys.stderr)
        sys.exit(2)


    if args.cmd == "export":
        data = load_store()
        guards = data.get("term_guards", [])
        out_obj = {"_meta": {"exported_by": "learn_guards export",
                             "version": hxt_core.__version__,
                             "count": len(guards)},
                   "term_guards": guards}
        with open(args.out, "w", encoding="utf-8") as f:
            json.dump(out_obj, f, ensure_ascii=False, indent=1)
        print("已导出 %d 条守卫 → %s" % (len(guards), args.out))
        return

    if args.cmd == "import":
        with open(args.src, encoding="utf-8") as f:
            src = json.load(f)
        incoming = src.get("term_guards", [])
        if not isinstance(incoming, list):
            hxt_core.fail("导入文件结构损坏：term_guards 不是列表")
        data = load_store()
        have = {g.get("term") for g in data.get("term_guards", [])}
        new_items, skipped = [], 0
        for g in incoming:
            term = g.get("term")
            if not term:
                continue
            if term in have:
                skipped += 1
                continue
            data["term_guards"].append(g)
            have.add(term)
            new_items.append(term)
        if args.dry_run:
            print("dry-run：将导入 %d 条新守卫，跳过 %d 条已存在"
                  % (len(new_items), skipped))
            return
        if new_items:
            save_store(data)
        print("导入完成：新增 %d 条、跳过 %d 条已存在（现库共 %d 条）"
              % (len(new_items), skipped, len(data["term_guards"])))
        return


if __name__ == "__main__":
    hxt_core.cli_entry(main)
