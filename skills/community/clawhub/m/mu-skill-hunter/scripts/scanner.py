#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
mu-skill-hunter: 安全扫描脚本（静态代码分析）
规则来源：mu-lobster-guard Red Flags R1~R10 + AI特有威胁检测
⚠️ 扫描器只输出报告摘要，不将原始代码喂入 Agent 上下文（防 prompt injection）
"""
import sys
import os
import re
import json
import argparse
from pathlib import Path

# ============================================================
# 规则定义（来源：mu-lobster-guard R1~R10 + AI特有威胁）
# ============================================================

HARD_REJECT_RULES = [
    {
        "id": "R1",
        "name": "外部 URL 请求",
        "pattern": r'(curl|wget)\s+["\']?https?://(?!github\.com|api\.github\.com|clawhub\.ai|skills\.sh|raw\.githubusercontent\.com|skillhub\.cn|skillhub-1388575217\.cos\.ap-guangzhou\.myqcloud\.com)',
        "desc": "向未知外部 URL 发送请求（数据外泄风险）",
        "level": "🚨 HARD REJECT",
    },
    {
        "id": "R2",
        "name": "base64 解码执行",
        "pattern": r'(base64\s+-[dD]|base64\s+--decode|atob\s*\()',
        "desc": "base64 解码执行（经典隐藏 payload 手法）",
        "level": "🚨 HARD REJECT",
    },
    {
        "id": "R3",
        "name": "eval/exec 动态执行",
        "pattern": r'(eval\s*\(|exec\s*\()',
        "desc": "动态代码执行（可能执行外部输入）",
        "level": "🚨 HARD REJECT",
    },
    {
        "id": "R4",
        "name": "读取系统凭证路径",
        "pattern": r'(~/\.ssh|~/\.aws|~/\.config/gcloud|~/\.gnupg|/etc/shadow|/etc/passwd)',
        "desc": "访问系统凭证目录（凭证窃取风险）",
        "level": "🚨 HARD REJECT",
    },
    {
        "id": "R5",
        "name": "访问 Agent 记忆/身份文件",
        "pattern": r'(MEMORY\.md|USER\.md|SOUL\.md|IDENTITY\.md|agent-config\.json|paired\.json|device\.json|device-auth\.json)',
        "desc": "访问 Agent 私密文件（隐私泄露风险）",
        "level": "🚨 HARD REJECT",
    },
    {
        "id": "R6",
        "name": "混淆/超长单行代码",
        "pattern": r'.{500,}',
        "desc": "单行超500字符（可能隐藏恶意逻辑）",
        "level": "🚨 HARD REJECT",
        "line_check": True,
    },
    {
        "id": "R7",
        "name": "裸 IP 网络请求",
        "pattern": r'https?://\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}',
        "desc": "使用裸 IP 地址（绕过域名审查）",
        "level": "🚨 HARD REJECT",
    },
    {
        "id": "R8",
        "name": "提权操作",
        "pattern": r'(sudo\s|chmod\s+777|chown\s+root)',
        "desc": "请求 sudo/root 权限（提权攻击）",
        "level": "🚨 HARD REJECT",
    },
    {
        "id": "R9",
        "name": "凭证外发",
        "pattern": r'(token|key|secret|password|apikey|api_key).{0,50}(curl|fetch|request|wget|http)',
        "desc": "发送凭证到外部（凭证泄露风险）",
        "level": "🚨 HARD REJECT",
        "case_insensitive": True,
    },
    {
        "id": "R10",
        "name": "未声明包安装",
        "pattern": r'(pip\s+install|npm\s+install\s+-g|apt\s+install|brew\s+install)',
        "desc": "安装未在文档说明的包（供应链投毒风险）",
        "level": "🚨 HARD REJECT",
    },
    # AI 特有威胁（来源：skill-scanner + skill-guard 设计）
    {
        "id": "AI1",
        "name": "Prompt Injection",
        "pattern": r'(ignore\s+(previous|all|prior)\s+instructions?|forget\s+(everything|all)|you\s+are\s+now\s+a|disregard\s+(your|all)|new\s+instructions?:)',
        "desc": "Prompt Injection 攻击（隐藏指令）",
        "level": "🚨 HARD REJECT",
        "case_insensitive": True,
    },
    {
        "id": "AI2",
        "name": "挖矿特征",
        "pattern": r'(stratum\+tcp|mining\.pool|xmrig|cryptonight|monero|coinhive)',
        "desc": "加密货币挖矿特征",
        "level": "🚨 HARD REJECT",
        "case_insensitive": True,
    },
]

YELLOW_FLAG_RULES = [
    {
        "id": "Y1",
        "name": "写入 Agent 持久化目录",
        "pattern": r'~/\.[a-z]+/',
        "desc": "写入 Agent 持久化目录（需确认写入范围是否合理）",
        "level": "⚠️ 需人工确认",
    },
    {
        "id": "Y2",
        "name": "已知外部网络请求",
        "pattern": r'(requests\.get|urllib\.request|fetch\(|axios\.get|http\.get)',
        "desc": "包含网络请求代码（需确认目标域名是否在 Skill 声明范围内）",
        "level": "⚠️ 需人工确认",
    },
    {
        "id": "Y3",
        "name": "环境变量修改",
        "pattern": r'os\.environ\[.+\]\s*=|export\s+[A-Z_]+=',
        "desc": "修改环境变量（确认是否影响其他工具）",
        "level": "⚠️ 需人工确认",
    },
    {
        "id": "Y4",
        "name": "后台进程/子进程",
        "pattern": r'(subprocess\.Popen|nohup|&\s*$|threading\.Thread|asyncio\.create_task)',
        "desc": "启动后台进程（确认是否有终止条件）",
        "level": "⚠️ 需人工确认",
    },
]

SCAN_EXTENSIONS = {".md", ".py", ".sh", ".js", ".ts", ".json", ".yaml", ".yml"}


def scan_file(filepath):
    """扫描单个文件，返回命中的规则列表"""
    findings = []
    try:
        content = Path(filepath).read_text(encoding="utf-8", errors="ignore")
    except Exception as e:
        return [{"rule_id": "ERR", "level": "⚠️", "desc": f"文件读取失败: {e}", "line": 0, "snippet": ""}]

    lines = content.split("\n")
    all_rules = HARD_REJECT_RULES + YELLOW_FLAG_RULES

    for rule in all_rules:
        flags = re.IGNORECASE if rule.get("case_insensitive") else 0
        pattern = re.compile(rule["pattern"], flags)

        if rule.get("line_check"):
            # 逐行检查
            for i, line in enumerate(lines, 1):
                if pattern.search(line):
                    findings.append({
                        "rule_id": rule["id"],
                        "rule_name": rule["name"],
                        "level": rule["level"],
                        "desc": rule["desc"],
                        "file": str(filepath),
                        "line": i,
                        "snippet": line[:120] + ("..." if len(line) > 120 else ""),
                    })
                    break  # 每条规则只报一次
        else:
            for m in pattern.finditer(content):
                line_no = content[:m.start()].count("\n") + 1
                snippet = lines[line_no - 1][:120] if line_no <= len(lines) else ""
                findings.append({
                    "rule_id": rule["id"],
                    "rule_name": rule["name"],
                    "level": rule["level"],
                    "desc": rule["desc"],
                    "file": str(filepath),
                    "line": line_no,
                    "snippet": snippet.strip(),
                })
                break  # 每条规则每文件只报一次

    return findings


def scan_directory(path):
    """扫描目录下所有相关文件"""
    p = Path(path)
    if not p.exists():
        return None, f"路径不存在: {path}"

    all_findings = []
    scanned_files = []

    if p.is_file():
        files = [p]
    else:
        files = [f for f in p.rglob("*") if f.is_file() and f.suffix in SCAN_EXTENSIONS]

    for f in files:
        if ".git" in f.parts:
            continue
        scanned_files.append(str(f.relative_to(p) if p.is_dir() else f))
        findings = scan_file(f)
        all_findings.extend(findings)

    return {
        "path": str(path),
        "files_scanned": len(scanned_files),
        "file_list": scanned_files,
        "findings": all_findings,
    }, None


def risk_level(findings):
    """根据发现计算整体风险等级"""
    hard = [f for f in findings if "HARD" in f.get("level", "")]
    yellow = [f for f in findings if "需人工" in f.get("level", "")]
    if hard:
        return "🔴 HIGH" if len(hard) <= 2 else "⛔ EXTREME"
    if yellow:
        return "🟡 MEDIUM"
    return "🟢 LOW"


def generate_report(scan_result, skill_name="未知"):
    """生成审查报告（只包含摘要，不暴露原始代码内容）"""
    findings = scan_result["findings"]
    hard_flags = [f for f in findings if "HARD" in f.get("level", "")]
    yellow_flags = [f for f in findings if "需人工" in f.get("level", "")]
    risk = risk_level(findings)

    verdict_map = {
        "🟢 LOW": "✅ 可安装",
        "🟡 MEDIUM": "⚠️ 安装前需人工确认",
        "🔴 HIGH": "❌ 建议拒绝安装",
        "⛔ EXTREME": "❌ 拒绝安装",
    }
    verdict = verdict_map.get(risk, "⚠️ 未知")

    lines = [
        "╔══════════════════════════════════════════════════╗",
        f"  🔒 Skill 安全审查报告",
        "╚══════════════════════════════════════════════════╝",
        f"Skill 路径 : {scan_result['path']}",
        f"扫描文件数 : {scan_result['files_scanned']}",
        f"",
        f"── 发现问题 ─────────────────────────────────────",
    ]

    if hard_flags:
        lines.append(f"🚨 硬拒绝项（{len(hard_flags)} 条）：")
        for f in hard_flags:
            lines.append(f"  [{f['rule_id']}] {f['rule_name']} — {f['desc']}")
            lines.append(f"       位置：{os.path.basename(f['file'])} 第{f['line']}行")
    else:
        lines.append("🚨 硬拒绝项：无")

    lines.append("")
    if yellow_flags:
        lines.append(f"⚠️ 需人工确认项（{len(yellow_flags)} 条）：")
        for f in yellow_flags:
            lines.append(f"  [{f['rule_id']}] {f['rule_name']} — {f['desc']}")
            lines.append(f"       位置：{os.path.basename(f['file'])} 第{f['line']}行")
    else:
        lines.append("⚠️ 需人工确认项：无")

    lines += [
        "",
        f"── 综合评估 ─────────────────────────────────────",
        f"风险等级 : {risk}",
        f"最终结论 : {verdict}",
        "══════════════════════════════════════════════════",
    ]

    if hard_flags:
        lines.append("⛔ 检测到高风险项，建议拒绝安装。如确需使用，请人工逐行审查上述文件。")
    elif yellow_flags:
        lines.append("⚠️ 存在需确认项，请人工核实后再决定是否安装。")
    else:
        lines.append("✅ 未检测到已知威胁，可安装。安装后如发现异常请立即卸载并报告。")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="mu-skill-hunter 安全扫描器")
    parser.add_argument("path", help="要扫描的 Skill 路径（文件或目录）")
    parser.add_argument("--json", action="store_true", help="输出 JSON 格式")
    parser.add_argument("--name", default="", help="Skill 名称（用于报告）")
    args = parser.parse_args()

    result, err = scan_directory(args.path)
    if err:
        print(f"❌ 扫描失败：{err}", file=sys.stderr)
        sys.exit(1)

    if args.json:
        # JSON 模式：输出结构化结果（供程序处理，不含原始代码片段）
        output = {
            "path": result["path"],
            "files_scanned": result["files_scanned"],
            "hard_reject_count": len([f for f in result["findings"] if "HARD" in f.get("level", "")]),
            "yellow_flag_count": len([f for f in result["findings"] if "需人工" in f.get("level", "")]),
            "risk_level": risk_level(result["findings"]),
            "findings_summary": [
                {"rule_id": f["rule_id"], "rule_name": f["rule_name"],
                 "file": os.path.basename(f["file"]), "line": f["line"]}
                for f in result["findings"]
            ]
        }
        print(json.dumps(output, ensure_ascii=False, indent=2))
    else:
        print(generate_report(result, args.name or args.path))


if __name__ == "__main__":
    main()
