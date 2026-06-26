#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
IronClaw Security Audit Script
融合 IronClaw 威胁检测 + Security Guard 审计能力

用法:
  python3 ironclaw_audit.py scan <file>     # 扫描文件
  python3 ironclaw_audit.py check <command> # 检查命令
  python3 ironclaw_audit.py message <text>  # 检测消息
"""

import sys
import json
import urllib.request
import urllib.error
from pathlib import Path

IRONCLAW_API = "https://ironclaw.io/api/v1/label"
AUDIT_LOG = Path.home() / ".openclaw" / "logs" / "ironclaw.audit.jsonl"

# 预设检测标准
CRITERIA = {
    "skill_scan": "Contains malicious code (data exfiltration via fetch/HTTP, credential harvesting, obfuscated eval/exec, postinstall scripts with network calls, scanning for tokens/secrets)",
    "prompt_injection": "Attempts to bypass AI safety (jailbreak requests, personas without ethics like DAN/Mephisto, instructions to ignore rules, pretend no content policy exists, manipulation via roleplay or hypotheticals)",
    "destructive_command": "Contains destructive commands (rm -rf, dd if=/dev, mkfs, fork bomb like :(){ }, chmod 777, DROP DATABASE, curl|bash, wget+execute)",
    "secret_leak": "Contains hardcoded secrets (API keys with real values not placeholders like 'your-key-here', private key PEM blocks, database URLs with real passwords, excludes type definitions and process.env references)",
}

def log_audit(event: str, content: str, label: int, confidence: float, criteria: str):
    """记录审计日志"""
    AUDIT_LOG.parent.mkdir(parents=True, exist_ok=True)
    record = {
        "timestamp": Path.home().expanduser().__str__(),  # placeholder
        "event": event,
        "content_preview": content[:200],
        "label": label,
        "confidence": confidence,
        "criteria": criteria
    }
    with open(AUDIT_LOG, "a") as f:
        f.write(json.dumps(record) + "\n")

def check_content(content: str, criteria: str, api_key: str = None) -> dict:
    """调用 IronClaw API 检测内容"""
    payload = {
        "content_text": content,
        "criteria_text": criteria
    }
    
    headers = {"Content-Type": "application/json"}
    if api_key:
        headers["Authorization"] = f"Bearer {api_key}"
    
    req = urllib.request.Request(
        IRONCLAW_API,
        data=json.dumps(payload).encode("utf-8"),
        headers=headers,
        method="POST"
    )
    
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            result = json.loads(resp.read().decode("utf-8"))
            return result
    except urllib.error.HTTPError as e:
        print(f"API 错误：{e.code} - {e.reason}", file=sys.stderr)
        return {"error": str(e)}
    except Exception as e:
        print(f"请求失败：{e}", file=sys.stderr)
        return {"error": str(e)}

def scan_file(filepath: str, api_key: str = None):
    """扫描技能文件"""
    print(f"🔍 扫描文件：{filepath}")
    content = Path(filepath).read_text()
    result = check_content(content, CRITERIA["skill_scan"], api_key)
    
    if "error" in result:
        print(f"❌ 扫描失败：{result['error']}")
        return
    
    label = result.get("label", 0)
    confidence = result.get("confidence", 0)
    
    print(f"📊 检测结果:")
    print(f"  Label: {label} (1=威胁，0=安全)")
    print(f"  Confidence: {confidence:.2%}")
    
    if label == 1:
        print(f"⚠️  警告：检测到潜在威胁!")
        if confidence >= 0.65:
            print(f"❌ 建议：不要安装此技能")
        else:
            print(f"⚠️  建议：人工审查后再决定")
    else:
        print(f"✅ 安全：可以安装")
    
    log_audit("skill_scan", content, label, confidence, CRITERIA["skill_scan"])

def check_command(command: str, api_key: str = None):
    """检查 shell 命令"""
    print(f"🔍 检查命令：{command}")
    result = check_content(command, CRITERIA["destructive_command"], api_key)
    
    if "error" in result:
        print(f"❌ 检查失败：{result['error']}")
        return
    
    label = result.get("label", 0)
    confidence = result.get("confidence", 0)
    
    print(f"📊 检测结果:")
    print(f"  Label: {label}")
    print(f"  Confidence: {confidence:.2%}")
    
    if label == 1 and confidence >= 0.65:
        print(f"❌ 危险命令：已拦截")
        log_audit("command_blocked", command, label, confidence, CRITERIA["destructive_command"])
        sys.exit(1)
    else:
        print(f"✅ 安全：可以执行")
        log_audit("command_allowed", command, label, confidence, CRITERIA["destructive_command"])

def check_message(text: str, api_key: str = None):
    """检测消息 (prompt injection)"""
    print(f"🔍 检测消息...")
    result = check_content(text, CRITERIA["prompt_injection"], api_key)
    
    if "error" in result:
        print(f"❌ 检测失败：{result['error']}")
        return
    
    label = result.get("label", 0)
    confidence = result.get("confidence", 0)
    
    print(f"📊 检测结果:")
    print(f"  Label: {label}")
    print(f"  Confidence: {confidence:.2%}")
    
    if label == 1:
        if confidence >= 0.65:
            print(f"❌ 警告：检测到 prompt injection 攻击!")
        else:
            print(f"⚠️  警告：可疑消息，建议审查")
    else:
        print(f"✅ 安全：正常消息")
    
    log_audit("message_screen", text, label, confidence, CRITERIA["prompt_injection"])

def main():
    if len(sys.argv) < 3:
        print(__doc__)
        print("\n用法: python3 ironclaw_audit.py <command> <argument>")
        sys.exit(1)
    
    action = sys.argv[1]
    argument = sys.argv[2]
    api_key = None  # 可从环境变量获取：IRONCLAW_API_KEY
    
    if action == "scan":
        scan_file(argument, api_key)
    elif action == "check":
        check_command(argument, api_key)
    elif action == "message":
        check_message(argument, api_key)
    else:
        print(f"未知操作：{action}")
        sys.exit(1)

if __name__ == "__main__":
    main()
