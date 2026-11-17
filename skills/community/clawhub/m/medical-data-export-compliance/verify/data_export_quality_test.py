#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""data_export_quality_test.py — 医械数据出海合规 质量与安全稳定性验证（本地闭环、零网络）"""

import json, os, re, subprocess, sys

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SKILL_MD = os.path.join(BASE, "SKILL.md")
TOOL = os.path.join(BASE, "tools", "data_export_toolkit.py")
REFS = os.path.join(BASE, "references")
VERIFY = os.path.join(BASE, "verify")
PYTHON = sys.executable


def check_regulatory_timeliness():
    items = []
    try:
        r1 = open(os.path.join(REFS, "01-数据出境监管体系.md"), encoding="utf-8").read()
        r2 = open(os.path.join(REFS, "02-三条合规路径.md"), encoding="utf-8").read()
        r6 = open(os.path.join(REFS, "06-落地流程与审计.md"), encoding="utf-8").read()
        checks = [
            ("3+2+4 监管体系", "3+2+4" in r1 or ("数据出境安全评估办法" in r1 and "个人信息出境认证办法" in r1)),
            ("出境认证办法 2026-01-01 施行", "2026-01-01" in r1 and "认证" in r1),
            ("三条路径（评估/合同/认证）", all(k in r2 for k in ["安全评估", "标准合同", "认证"])),
            ("10 万/100 万阈值", "10 万" in r2 and "100 万" in r2),
            ("累计计算规则", "累计" in r2),
            ("安全评估有效期 3 年", "3 年" in r2 and "60 个工作日" in r2),
            ("2026 集中到期窗口", "2026" in r6 and "到期" in r6),
            ("风险评估办法 2026-08-20", "2026-08-20" in r6),
            ("个保审计每两年", "两年" in r6 or "2 年" in r6),
            ("核对基准日", "核对基准日" in r1),
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
        items.append({"name": f"references 模块数=7（实际 {len(files)}）", "pass": len(files) == 7})
        for f in files:
            items.append({"name": f"导航表包含 {f}", "pass": f in nav})
        items.append({"name": "FAQ 专节", "pass": "FAQ" in nav})
        items.append({"name": "能力边界", "pass": "能力边界" in nav})
    except OSError as e:
        items = [{"name": f"读取失败: {e}", "pass": False}]
    return items


def check_tools():
    items = []
    try:
        r = subprocess.run([PYTHON, TOOL, "path", "--desc", "向海外CRO传输临床试验受试者个人信息，全年约50万人"],
                           capture_output=True, text=True, timeout=60)
        out = r.stdout or ""
        items.append({"name": "path 命令执行", "pass": r.returncode == 0 and "标准合同" in out})
        r2 = subprocess.run([PYTHON, TOOL, "threshold", "--personal", "2000000", "--sensitive", "500"],
                            capture_output=True, text=True, timeout=60)
        out2 = r2.stdout or ""
        items.append({"name": "threshold 命令执行", "pass": r2.returncode == 0 and "安全评估" in out2})
        r3 = subprocess.run([PYTHON, TOOL, "scene", "--type", "clinical"], capture_output=True, text=True, timeout=60)
        items.append({"name": "scene 命令执行", "pass": r3.returncode == 0 and "临床试验" in (r3.stdout or "")})
        r4 = subprocess.run([PYTHON, TOOL, "market", "--region", "eu"], capture_output=True, text=True, timeout=60)
        out4 = r4.stdout or ""
        items.append({"name": "market 命令执行", "pass": r4.returncode == 0 and "GDPR" in out4 and "EHDS" in out4})
        r5 = subprocess.run([PYTHON, TOOL, "audit"], capture_output=True, text=True, timeout=60)
        items.append({"name": "audit 命令执行", "pass": r5.returncode == 0 and "审计" in (r5.stdout or "")})
    except Exception as e:
        items = [{"name": f"执行失败: {e}", "pass": False}]
    return items


def check_accuracy():
    cases = [
        ("向海外CRO传输临床试验受试者个人信息，全年约50万人", ["标准合同"]),
        ("向境外总部传输客户信息120万人", ["安全评估"]),
    ]
    items = []
    for desc, expects in cases:
        try:
            r = subprocess.run([PYTHON, TOOL, "path", "--desc", desc], capture_output=True, text=True, timeout=60)
            ok = r.returncode == 0 and any(e in (r.stdout or "") for e in expects)
            items.append({"name": f"path「{desc[:14]}…」→{expects[0]}", "pass": ok})
        except Exception as e:
            items.append({"name": f"失败: {e}", "pass": False})
    thr = [
        (50000, 500, "标准合同"), (50000, 0, "未达"), (50000, 15000, "安全评估"), (2000000, 0, "安全评估"),
    ]
    for p, s, expect in thr:
        try:
            r = subprocess.run([PYTHON, TOOL, "threshold", "--personal", str(p), "--sensitive", str(s)],
                               capture_output=True, text=True, timeout=60)
            ok = r.returncode == 0 and expect in (r.stdout or "")
            items.append({"name": f"threshold({p},{s})→{expect}", "pass": ok})
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
        items.append({"name": "版权段", "pass": "版权与许可" in sk and "MIT" in sk})
        items.append({"name": "知识版权声明", "pass": "知识版权声明" in sk})
        items.append({"name": "免责声明 AS IS", "pass": "免责声明" in sk and "AS IS" in sk})
        items.append({"name": "LICENSE.md", "pass": os.path.exists(os.path.join(BASE, "LICENSE.md"))})
        ts = open(TOOL, encoding="utf-8").read()
        for c in ["path", "threshold", "scene", "market", "audit", "--help"]:
            items.append({"name": f"工具实现 {c}", "pass": c in ts})
        for a in ["--desc", "--personal", "--sensitive", "--type", "--region"]:
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
    ("regulatory_timeliness", "法规时效性", check_regulatory_timeliness),
    ("coverage_completeness", "覆盖完整性", check_coverage),
    ("template_usability", "工具可用性", check_tools),
    ("risk_accuracy", "判定准确性", check_accuracy),
    ("structure_compliance", "结构规范性", check_structure),
    ("security_cleanliness", "安全净度", check_security),
]


def main():
    results = {"skill": "medical-data-export-compliance", "version": "1.0.0",
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
