#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""gov-disclosure-check — 政务公开披露校验纵深工具（零依赖）。
校验公开信息是否含强制披露字段(决策依据/责任部门/时限/救济渠道/数据来源)。
理论真源：LGD 凡自治之物三律（SynomosAI）。"""
import argparse, json, sys
NAME = "gov-disclosure-check"
REQUIRED = [
    ("决策依据", ["依据", "法", "条例", "规定", "policy"]),
    ("责任部门", ["责任部门", "主办", "牵头", "负责单位"]),
    ("时限", ["时限", "期限", "截止", "ddl", "deadline"]),
    ("救济渠道", ["复议", "诉讼", "救济", "申诉", "投诉"]),
    ("数据来源", ["来源", "数据", "统计", "口径"]),
]
def check(text):
    t = (text or "").lower()
    missing = [name for name, hints in REQUIRED if not any(h.lower() in t for h in hints)]
    return {"missing": missing, "complete": len(missing) == 0}
def main():
    ap = argparse.ArgumentParser(description=NAME + " · 公开披露校验")
    ap.add_argument("--text", help="公开信息文本")
    ap.add_argument("--file", help="文本文件")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()
    if not a.text and not a.file: print("用法: --text <str> | --file <path>", file=sys.stderr); sys.exit(2)
    text = a.text or open(a.file, encoding="utf-8-sig").read()
    r = check(text)
    if a.json: print(json.dumps(r, ensure_ascii=False, indent=2))
    else:
        print("=== " + NAME + " · 公开披露校验 ===")
        print("  缺失字段: " + (",".join(r["missing"]) or "无"))
        print("  结论: " + ("披露完整 ✅" if r["complete"] else "缺强制披露 ⛔"))
    sys.exit(0 if r["complete"] else 1)
if __name__ == "__main__":
    main()
