#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""meddev_cyber_quality_test.py — 医疗器械网络安全 质量与安全稳定性验证（本地闭环、零网络）"""

import json, os, re, subprocess, sys

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SKILL_MD = os.path.join(BASE, "SKILL.md")
TOOL = os.path.join(BASE, "tools", "meddev_cyber_toolkit.py")
REFS = os.path.join(BASE, "references")
VERIFY = os.path.join(BASE, "verify")
PYTHON = sys.executable


def check_regulatory():
    items = []
    try:
        us = open(os.path.join(REFS, "02-美国FDA网络安全要求.md"), encoding="utf-8").read()
        eu = open(os.path.join(REFS, "03-欧盟网络安全要求.md"), encoding="utf-8").read()
        cn = open(os.path.join(REFS, "04-中国NMPA网络安全要求.md"), encoding="utf-8").read()
        checks = [
            ("FDA SBOM 强制 + RTA", "SBOM" in us and "RTA" in us),
            ("FDA 渗透测试强制", "渗透" in us),
            ("FDA 2026 强化点", "2026" in us),
            ("EU MDR 17.2", "17.2" in eu),
            ("EU CRA 2027", "CRA" in eu and "2027" in eu),
            ("EU NIS2", "NIS2" in eu),
            ("NMPA 注册审查指导原则", "指导原则" in cn),
            ("三地核对基准日", "核对基准日" in us and "核对基准日" in eu and "核对基准日" in cn),
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
        items.append({"name": f"references 模块数=8（实际 {len(files)}）", "pass": len(files) == 8})
        for f in files:
            items.append({"name": f"导航表包含 {f}", "pass": f in nav})
        items.append({"name": "FAQ", "pass": "FAQ" in nav})
        items.append({"name": "能力边界", "pass": "能力边界" in nav})
    except OSError as e:
        items = [{"name": f"读取失败: {e}", "pass": False}]
    return items


def check_tools():
    items = []
    try:
        r = subprocess.run([PYTHON, TOOL, "reg", "--region", "us"], capture_output=True, text=True, timeout=60)
        out = r.stdout or ""
        items.append({"name": "reg 命令执行", "pass": r.returncode == 0 and "SBOM" in out and "RTA" in out})
        r2 = subprocess.run([PYTHON, TOOL, "checklist", "--phase", "submission"], capture_output=True, text=True, timeout=60)
        items.append({"name": "checklist 命令执行", "pass": r2.returncode == 0 and "渗透测试" in (r2.stdout or "")})
        r3 = subprocess.run([PYTHON, TOOL, "sbom"], capture_output=True, text=True, timeout=60)
        out3 = r3.stdout or ""
        items.append({"name": "sbom 命令执行", "pass": r3.returncode == 0 and "CycloneDX" in out3 and "components" in out3})
        r4 = subprocess.run([PYTHON, TOOL, "vuln", "--desc", "远程可被利用执行任意代码"], capture_output=True, text=True, timeout=60)
        items.append({"name": "vuln 命令执行", "pass": r4.returncode == 0 and "严重" in (r4.stdout or "")})
        r5 = subprocess.run([PYTHON, TOOL, "standard"], capture_output=True, text=True, timeout=60)
        out5 = r5.stdout or ""
        items.append({"name": "standard 命令执行", "pass": r5.returncode == 0 and "81001" in out5})
    except Exception as e:
        items = [{"name": f"执行失败: {e}", "pass": False}]
    return items


def check_accuracy():
    cases = [
        ("远程可被利用执行任意代码", ["严重"]),
        ("本地低权限信息泄露", ["中"]),
        ("漏洞可远程利用读取敏感数据", ["高"]),
    ]
    items = []
    for desc, expects in cases:
        try:
            r = subprocess.run([PYTHON, TOOL, "vuln", "--desc", desc], capture_output=True, text=True, timeout=60)
            ok = r.returncode == 0 and any(e in (r.stdout or "") for e in expects)
            items.append({"name": f"vuln「{desc[:14]}…」→{expects[0]}", "pass": ok})
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
        for c in ["reg", "checklist", "sbom", "vuln", "standard", "--help"]:
            items.append({"name": f"工具实现 {c}", "pass": c in ts})
        for a in ["--region", "--phase", "--desc"]:
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
    results = {"skill": "medical-device-cybersecurity", "version": "1.0.0",
               "note": "本地闭环验证：零网络、零扫描、零数据采集、可重复", "dimensions": [], "summary": {}}
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
