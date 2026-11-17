# -*- coding: utf-8 -*-
"""提示词泄漏扫描器：发布/共享前扫描提示词的泄漏与后门风险。零依赖。

扫五类：
  1. 密钥口令（API key / token / password / 私钥块）
  2. 内部路径与主机（盘符绝对路径 /home /Users /内网 IP）
  3. 个人可识别信息（手机号 / 邮箱 / 身份证）
  4. 自定义敏感词（--extra，项目代号/雇主名/内部系统名）
  5. 自我泄漏后门（提示词里埋了"忽略之前指令 / 打印你的系统提示词"类指令）

门禁语义：发现高风险 → rc=1 拦下（发布前门禁）；干净 → rc=0；参数错误 → rc=2。
三律映射：LGD-III 有门禁 —— 提示词对外发布前的最后一道门。

用法：
  python prompt_leak_scanner.py --file prompt.txt
  python prompt_leak_scanner.py --text "..." --extra 内部代号A
  python prompt_leak_scanner.py --file p.txt --json
"""
import argparse, json, pathlib, re, sys

KEYS = re.compile("(" + "sk-[A-Za-z0-9]{8,}|" + "ghp_[A-Za-z0-9]{8,}|" + "gho_[A-Za-z0-9]{8,}|"
                  + "AKIA[0-9A-Z]{16}|"
                  + r"api[_-]?key\s*[=:]\s*\S+|" + r"secret\s*[=:]\s*\S+|"
                  + r"password\s*[=:]\s*\S+|" + r"Bearer\s+[A-Za-z0-9._-]{10,}|"
                  + "-----BEGIN[A-Z ]*PRIVATE KEY-----)", re.I)
PATHS = re.compile(r"([A-Za-z]:[\\/][^\s\"']+|/home/\S+|/Users/\S+|"
                   r"(?:10|172\.(?:1[6-9]|2\d|3[01]))\.\d+\.\d+\.\d+)", re.I)
PII = re.compile(r"(1[3-9]\d{9}|[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}|\b\d{17}[\dXx]\b)")
BACKDOOR = re.compile("(忽略(之前|上面|以上|先前)(的)?(所有)?(指令|规则|设定)|"
                      "ignore\\s+(all\\s+)?previous\\s+instructions|"
                      "(打印|输出|复述|泄露|repeat|print|reveal|show)[^。\\n]{0,10}"
                      "(系统提示|system prompt|初始指令|initial instructions)|"
                      "(你|you)[^。\\n]{0,8}(系统提示词|system prompt)[^。\\n]{0,12}(是什么|什么|reveal))", re.I)

SEVERITY = {"密钥口令": "HIGH", "内部路径/主机": "HIGH", "自我泄漏后门": "HIGH",
            "个人可识别信息": "MED", "自定义敏感词": "HIGH"}


def scan(text, extra):
    hits = []
    for name, pat in (("密钥口令", KEYS), ("内部路径/主机", PATHS),
                      ("个人可识别信息", PII), ("自我泄漏后门", BACKDOOR)):
        for m in pat.finditer(text):
            frag = m.group(0)
            shown = frag[:10] + "…" if len(frag) > 13 else frag
            hits.append({"category": name, "severity": SEVERITY[name],
                         "pos": m.start(), "sample": shown})
    for w in extra or []:
        for m in re.finditer(re.escape(w), text):
            hits.append({"category": "自定义敏感词", "severity": SEVERITY["自定义敏感词"],
                         "pos": m.start(), "sample": w})
    return hits


def main():
    ap = argparse.ArgumentParser(description="提示词泄漏扫描器 · 提示词发布前门禁")
    src = ap.add_mutually_exclusive_group(required=True)
    src.add_argument("--file", help="提示词文件路径")
    src.add_argument("--text", help="提示词文本（内联，或 @文件/纯路径）")
    ap.add_argument("--extra", nargs="*", default=[], help="自定义敏感词（项目代号/内部系统名）")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()

    try:
        if a.file:
            text = pathlib.Path(a.file).read_text(encoding="utf-8-sig")
        else:
            q = a.text[1:] if a.text.startswith("@") else a.text
            text = (pathlib.Path(q).read_text(encoding="utf-8-sig")
                    if pathlib.Path(q).is_file() else q)
    except OSError as e:
        print(f"输入不可读：{e}", file=sys.stderr)
        sys.exit(2)

    hits = scan(text, a.extra)
    high = [h for h in hits if h["severity"] == "HIGH"]
    blocked = bool(high)
    if a.json:
        print(json.dumps({"clean": not hits, "blocked": blocked,
                          "findings": hits,
                          "note": "存在高风险项，已按门禁拦截（rc=1）" if blocked
                          else ("存在中风险项，建议复核" if hits else "未发现泄漏/后门信号")},
                         ensure_ascii=False, indent=2))
    else:
        if not hits:
            print("✅ 未发现泄漏/后门信号，可发布（仍建议按发布闸门走人工复核）")
        else:
            print(("⛔ 高风险，已拦截（rc=1）：" if blocked else "⚠ 中风险，建议复核：")
                  + f"{len(hits)} 项")
            for h in hits:
                print(f"  [{h['severity']}] {h['category']} @pos{h['pos']}  {h['sample']}")
    sys.exit(1 if blocked else 0)


if __name__ == "__main__":
    main()
