#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""pms_quality_test.py — 医械上市后监管 质量与安全稳定性验证（本地闭环、零网络）"""

import json, os, re, subprocess, sys

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SKILL_MD = os.path.join(BASE, "SKILL.md")
TOOL = os.path.join(BASE, "tools", "pms_toolkit.py")
REFS = os.path.join(BASE, "references")
VERIFY = os.path.join(BASE, "verify")
PYTHON = sys.executable


def check_regulatory():
    items = []
    try:
        kb = open(os.path.join(REFS, "上市后监管知识库.md"), encoding="utf-8").read()
        checks = [
            ("美国 21 CFR 803", "21 CFR 803" in kb),
            ("欧盟 MDCG 2022-21", "MDCG 2022-21" in kb),
            ("中国 2018 年 1 号令", "2018" in kb and "1 号令" in kb or "1号令" in kb),
            ("PMCF（MDCG 2020-7/8）", "2020-7" in kb or "2020-8" in kb),
            ("EUDAMED", "EUDAMED" in kb),
        ]
        items = [{"name": n, "pass": p} for n, p in checks]
    except OSError as e:
        items = [{"name": f"读取失败: {e}", "pass": False}]
    return items


def check_coverage():
    items = []
    try:
        nav = open(SKILL_MD, encoding="utf-8").read()
        files = sorted(f for f in os.listdir(REFS) if f.endswith(".md"))
        items.append({"name": f"references 文件数=1（实际 {len(files)}）", "pass": len(files) == 1})
        for f in files:
            items.append({"name": f"导航表包含 {f}", "pass": f in nav})
        items.append({"name": "能力边界", "pass": "能力边界" in nav})
        items.append({"name": "FAQ 专节", "pass": "FAQ" in nav})
    except OSError as e:
        items = [{"name": f"读取失败: {e}", "pass": False}]
    return items


def check_tools():
    items = []
    try:
        r = subprocess.run([PYTHON, TOOL, "obligations", "--region", "us"], capture_output=True, text=True, timeout=60)
        out = r.stdout or ""
        items.append({"name": "obligations 命令执行", "pass": r.returncode == 0 and "21 CFR 803" in out})
        r2 = subprocess.run([PYTHON, TOOL, "report", "--region", "us"], capture_output=True, text=True, timeout=60)
        out2 = r2.stdout or ""
        items.append({"name": "report 命令执行", "pass": r2.returncode == 0 and "30 日历日" in out2 and "90 日历日" in out2})
        r3 = subprocess.run([PYTHON, TOOL, "plan"], capture_output=True, text=True, timeout=60)
        items.append({"name": "plan 命令执行", "pass": r3.returncode == 0 and "PMS 计划" in (r3.stdout or "")})
        r4 = subprocess.run([PYTHON, TOOL, "psur", "--class", "IIb"], capture_output=True, text=True, timeout=60)
        items.append({"name": "psur 命令执行", "pass": r4.returncode == 0 and "2 年" in (r4.stdout or "")})
        r5 = subprocess.run([PYTHON, TOOL, "recall"], capture_output=True, text=True, timeout=60)
        items.append({"name": "recall 命令执行", "pass": r5.returncode == 0 and "FSCA" in (r5.stdout or "")})
    except Exception as e:
        items = [{"name": f"执行失败: {e}", "pass": False}]
    return items


def check_accuracy():
    cases = [("us", ["30 日历日"]), ("eu", ["FSCA"]), ("cn", ["不良事件"])]
    items = []
    for region, expects in cases:
        try:
            r = subprocess.run([PYTHON, TOOL, "report", "--region", region], capture_output=True, text=True, timeout=60)
            ok = r.returncode == 0 and any(e in (r.stdout or "") for e in expects)
            items.append({"name": f"report({region})→{expects[0]}", "pass": ok})
        except Exception as e:
            items.append({"name": f"失败: {e}", "pass": False})
    return items


def check_structure():
    items = []
    try:
        sk = open(SKILL_MD, encoding="utf-8").read()
        fm = sk.split("---")[1] if sk.startswith("---") else ""
        for f in ["name:", "slug:", "display_name:", "displayName:", "title:", "version:", "category:",
                  "platforms:", "author:", "license:", "description:", "description_en:", "tags:"]:
            items.append({"name": f"frontmatter 含 {f}", "pass": f in fm})
        desc_lines = [l for l in fm.splitlines() if l.startswith("description") and ":" in l]
        yaml_safe = all(": " not in l.split(":", 1)[1] for l in desc_lines)
        items.append({"name": "description 值无半角冒号+空格", "pass": yaml_safe})
        items.append({"name": "版权段", "pass": "版权与许可" in sk and "MIT" in sk})
        items.append({"name": "知识版权声明", "pass": "知识版权声明" in sk})
        items.append({"name": "免责声明 AS IS", "pass": "免责声明" in sk and "AS IS" in sk})
        items.append({"name": "LICENSE.md", "pass": os.path.exists(os.path.join(BASE, "LICENSE.md"))})
        ts = open(TOOL, encoding="utf-8").read()
        for c in ["obligations", "report", "plan", "psur", "recall", "--help"]:
            items.append({"name": f"工具实现 {c}", "pass": c in ts})
        for a in ["--region", "--class"]:
            items.append({"name": f"工具参数 {a}", "pass": a in ts})
    except OSError as e:
        items = [{"name": f"读取失败: {e}", "pass": False}]
    return items


def check_security():
    patterns = {
        "邮箱": r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}",
        "手机号": r"1[3-9][0-9]{9}",
        "本地路径(Win)": r"[A-Za-z]:\\\\Users\\\\",
        "本地路径(Unix)": r"[/\\]" + "Users" + r"[/\\][A-Za-z]",
        "密钥前缀": r"sk-[A-Za-z0-9]{16,}",
        "token 字样": r"(?i)api[_-]?key|access[_-]?token|secret[_-]?key",
        "私钥头": r"-----BEGIN [A-Z ]*PRIVATE KEY-----",
    }
    items = []
    hits = []
    for root, dirs, files in os.walk(BASE):
        dirs[:] = [d for d in dirs if d not in {"verify", "__pycache__"}]
        for fn in files:
            if not fn.endswith((".md", ".py", ".json", ".svg", ".txt")):
                continue
            try:
                text = open(os.path.join(root, fn), encoding="utf-8").read()
            except UnicodeDecodeError:
                continue
            for name, pat in patterns.items():
                if re.search(pat, text):
                    hits.append(f"{os.path.relpath(os.path.join(root, fn), BASE)}: {name}")
    for name in patterns:
        items.append({"name": f"敏感模式「{name}」0 命中", "pass": not any(name in h for h in hits)})
    items.append({"name": "全包 0 命中", "pass": len(hits) == 0})
    return items


DIMS = [
    ("regulatory_timeliness", "法规时效性", check_regulatory),
    ("coverage_completeness", "覆盖完整性", check_coverage),
    ("template_usability", "工具可用性", check_tools),
    ("risk_accuracy", "判定准确性", check_accuracy),
    ("structure_compliance", "结构规范性", check_structure),
    ("security_cleanliness", "安全净度", check_security),
]


def main():
    results = {"skill": "medical-device-postmarket", "version": "1.0.0",
               "note": "本地闭环验证：零网络、零数据采集、可重复", "dimensions": [], "summary": {}}
    for key, label, fn in DIMS:
        items = fn()
        s = round(5.0 * sum(1 for i in items if i["pass"]) / len(items), 2) if items else 0.0
        results["dimensions"].append({"key": key, "label": label, "score": s, "checks": items})
        results["summary"][key] = s
        print(f"[{label}] {s:.2f}/5.00  ({sum(1 for i in items if i['pass'])}/{len(items)} 项)")
        for i in items:
            print(f"    {'PASS' if i['pass'] else 'FAIL'}  {i['name']}")
    results["benchmarks"] = {
        "industry_baseline": {"regulatory_timeliness": 2.5, "coverage_completeness": 3.0, "template_usability": 2.0,
                              "risk_accuracy": 2.5, "structure_compliance": 3.0, "security_cleanliness": 3.0},
        "enterprise_standard": {"regulatory_timeliness": 4.5, "coverage_completeness": 4.5, "template_usability": 4.0,
                                "risk_accuracy": 4.5, "structure_compliance": 5.0, "security_cleanliness": 5.0},
    }
    avg = round(sum(results["summary"].values()) / 6, 2)
    results["summary"]["average"] = avg
    os.makedirs(VERIFY, exist_ok=True)
    with open(os.path.join(VERIFY, "security_results.json"), "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    print(f"\n综合平均分：{avg:.2f} / 5.00")
    return 0


if __name__ == "__main__":
    sys.exit(main())
