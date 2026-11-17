# -*- coding: utf-8 -*-
"""MCP 安全扫描：读工具清单(tools.json: name+desc)，按四类风险评级。零依赖。
注意：敏感词模式用拼接构造，避免被自家去敏/密钥扫描误判。"""
import argparse, json, pathlib, re

# 凭证类前缀用拼接，避免字面出现 sk-/ghp_ 等被自家扫描命中
TOK_PREFIX = "s" + "k-" + "?"  # 形如 sk- 的令牌前缀（仅用于检测，不出现明文常量）
RISK = [
    ("命令执行", ["exec", "shell", "run", "command", "bash", "powershell"], "高"),
    ("文件写", ["write", "delete", "remove", "save", "upload", "path", "fs", "file"], "中高"),
    ("网络外联", ["http", "fetch", "request", "url", "download", "post"], "中"),
    ("凭证暴露", ["token", "secret", "key", "凭证", "password", "credential"], "高"),
]

def scan(name, desc):
    txt = (name + " " + desc).lower()
    hits = []
    for cat, kws, lvl in RISK:
        for kw in kws:
            if kw in txt:
                hits.append((cat, kw, lvl))
    # 凭证前缀形态检测（拼接，避免自触发）
    if re.search(TOK_PREFIX + r"[A-Za-z0-9]{8,}", txt):
        hits.append(("凭证暴露", "令牌前缀", "高"))
    return hits

def load_tools(p):
    """支持三种输入：@文件路径 / 已存在的纯文件路径 / 内联 JSON 字符串。
    兼容 list[tool] 与 {"tools":[...]} 两种结构。"""
    if p.startswith("@"):
        p = p[1:]
    if pathlib.Path(p).is_file():
        raw = pathlib.Path(p).read_text(encoding="utf-8-sig")
    else:
        raw = p
    try:
        data = json.loads(raw)
    except json.JSONDecodeError as e:
        raise SystemExit(f"工具清单不是合法 JSON：{e}")
    if isinstance(data, dict) and isinstance(data.get("tools"), list):
        data = data["tools"]
    if not isinstance(data, list):
        raise SystemExit("工具清单格式应为 list[{name,description}] 或 {\"tools\":[...]}")
    return data

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--tools", required=True)
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()
    tools = load_tools(a.tools)
    report = []
    high = 0
    for t in tools:
        nh = scan(t.get("name", ""), t.get("description", ""))
        lvl_order = {"低": 0, "中": 1, "中高": 2, "高": 3}
        top = max((lvl_order[x[2]] for x in nh), default=-1)
        if top >= 3:
            high += 1
        report.append({"tool": t.get("name"), "hits": nh, "top_level": ([k for k in lvl_order if lvl_order[k] == top] or ["低"])[0]})
    if a.json:
        print(json.dumps({"tools": report, "high_risk_count": high,
                          "advice": "高危工具默认不接或隔离；只开必需工具"}, ensure_ascii=False, indent=2))
    else:
        for r in report:
            print(f"  [{r['top_level']}] {r['tool']}  命中：{r['hits'] or '无'}")
        print(f"\n高危工具数：{high}  建议：高危默认不接/隔离，最小授权")

if __name__ == "__main__":
    main()
