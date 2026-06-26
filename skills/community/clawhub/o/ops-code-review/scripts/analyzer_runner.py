#!/usr/bin/env python3
"""
多语言代码分析调度器 v2 - 优化版
支持：Django/Python、React+TS、PHP、Java
"""
import subprocess
import sys
import os
import json
import re
from pathlib import Path
from typing import List, Dict, Any

REPOS = {
    "ops_api": {"lang": "django", "local": "/tmp/svn_repos/ops_api"},
    "ops_web": {"lang": "react", "local": "/tmp/svn_repos/ops_web"},
    "ops_api_trunk": {"lang": "django", "local": "/tmp/svn_repos/ops_api_trunk"},
    "ops_web_trunk": {"lang": "react", "local": "/tmp/svn_repos/ops_web_trunk"},
    "gm": {"lang": "mixed", "local": "/tmp/svn_repos/gm"},
    # gm full scan 时按语言切分后的 key
    "gm_php": {"lang": "php", "local": "/tmp/svn_repos/gm"},
    "gm_react": {"lang": "react", "local": "/tmp/svn_repos/gm"},
}

# 高置信度 Bandit 规则（只报告这些，减少误报）
BANDIT_HIGH_CONFIDENCE = {
    "B101", "B102", "B103", "B104", "B105", "B106", "B107", "B108",
    "B201", "B202", "B203",
    "B301", "B302", "B303", "B304", "B305", "B306", "B307", "B308", "B309",
    "B310", "B311", "B312", "B313", "B314", "B315", "B316", "B317",
    "B401", "B402", "B403", "B404", "B405", "B406", "B407", "B408",
    "B411", "B412", "B413", "B414", "B415", "B416", "B417", "B418", "B419",
    "B501", "B502", "B503", "B504", "B505", "B506",
    "B601", "B602", "B603", "B604", "B605", "B606", "B607", "B608",
    "B701", "B702", "B703",
}

# Pylint 只关注的严重问题类型
PYLINT_SEVERE_MSGS = {
    "fatal", "syntax-error", "parse-error", "import-error",
    "no-member", "no-name-in-module", "unsubscriptable-object",
    "not-callable", "invalid-unary-operand-type",
    "unsupported-assignment-operation", "unsupported-delete-operation",
}


def run_bandit(base_path: str) -> Dict[str, Any]:
    """运行 Bandit 安全扫描 - 只返回高置信度结果"""
    result = subprocess.run(
        ["bandit", "-r", base_path, "-f", "json"],
        capture_output=True,
        text=True,
        cwd=base_path,
    )

    issues = []
    try:
        # 跳过 INFO 日志行
        for line in result.stdout.splitlines():
            if not line.startswith("["):
                output = json.loads(line)
                for finding in output.get("results", []):
                    test_id = finding.get("issue_id", "")
                    conf = finding.get("issue_confidence", "")
                    sev = finding.get("issue_severity", "")

                    # 只报高置信度的安全问题
                    if test_id in BANDIT_HIGH_CONFIDENCE and conf in ("HIGH", "MEDIUM"):
                        issues.append({
                            "severity": "ERROR" if sev == "HIGH" else "WARNING",
                            "file": finding.get("filename", ""),
                            "line": finding.get("line_number", 0),
                            "test_id": test_id,
                            "message": finding.get("issue_text", ""),
                        })
    except (json.JSONDecodeError, Exception):
        pass

    return {"issues": issues, "summary": {"total": len(issues)}}


def run_pylint_heavy(base_path: str) -> Dict[str, Any]:
    """Pylint 只报严重错误（语法/导入/逻辑错误），不报风格问题"""
    result = subprocess.run(
        ["pylint",
         "--output-format=json",
         "--disable=all",
         "--enable=fatal,syntax-error,parse-error,import-error,no-member,"
         "no-name-in-module,unsubscriptable-object,not-callable,"
         "invalid-unary-operand-type,unsupported-assignment-operation,"
         "unsupported-delete-operation,inherit-non-class,",
         "--max-line-length=200",
         base_path,
        ],
        capture_output=True,
        text=True,
        cwd=base_path,
    )

    issues = []
    try:
        for item in json.loads(result.stdout):
            issues.append({
                "severity": "WARNING",
                "file": item.get("path", ""),
                "line": item.get("line", 0),
                "message": item.get("message", "")[:120],
                "symbol": item.get("symbol", ""),
            })
    except json.JSONDecodeError:
        pass

    return {"issues": issues, "summary": {"total": len(issues)}}


def check_syntax_errors(base_path: str) -> List[Dict]:
    """Python 语法检查 - 所有无法被 AST 解析的文件"""
    issues = []
    for root, _, files in os.walk(base_path):
        # 跳过非源码目录
        skip = ["__pycache__", ".git", "node_modules", "migrations", "venv", ".venv"]
        if any(s in root for s in skip):
            continue
        for f in files:
            if f.endswith(".py"):
                path = os.path.join(root, f)
                rc = subprocess.run(["python3", "-m", "py_compile", path],
                                    capture_output=True, text=True)
                if rc.returncode != 0:
                    # 提取行号
                    line_num = 0
                    for line in rc.stderr.splitlines():
                        m = re.search(r"line (\d+)", line)
                        if m:
                            line_num = int(m.group(1))
                            break
                    issues.append({
                        "severity": "ERROR",
                        "file": path,
                        "line": line_num,
                        "message": "Python syntax error",
                    })
    return issues


SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SKILL_DIR = os.path.dirname(SCRIPT_DIR)
ESLINT_CONFIG = os.path.join(SKILL_DIR, "configs", "eslint.react.ts.js")


def run_eslint(base_path: str) -> Dict[str, Any]:
    """ESLint + TypeScript 检查 - 使用内置配置，忽略项目原有 eslintrc"""
    # 构建命令：使用 --no-config-lookup 忽略项目原有配置，用内置 config
    # ESLint v9+ 用 --no-config-lookup 替代了 --no-eslintrc
    import os
    env = {**os.environ, "NODE_PATH": "/usr/lib/node_modules"}
    cmd = [
        "npx", "eslint", "src",
        "--ext", ".ts,.tsx",
        "--no-config-lookup",
        "-c", ESLINT_CONFIG,
        "--format=json",
    ]

    result = subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        cwd=base_path,
        timeout=120,
        env=env,
    )

    issues = []
    try:
        output = json.loads(result.stdout)
        for file_result in output:
            for msg in file_result.get("messages", []):
                sev = msg.get("severity", 0)
                if sev < 1:  # 只报 warning + error
                    continue
                rule = msg.get("ruleId", "")
                # 过滤掉噪音规则（但保留 no-unused-vars，这是真实警告）
                if rule in ("", "no-undef"):
                    continue
                severity_map = {2: "ERROR", 1: "WARNING"}
                issues.append({
                    "severity": severity_map.get(sev, "WARNING"),
                    "file": os.path.basename(file_result.get("filePath", "")),
                    "line": msg.get("line", 0),
                    "message": msg.get("message", ""),
                    "rule": rule,
                })
    except (json.JSONDecodeError, Exception):
        pass

    # TypeScript 类型检查默认跳过（tsc 需要完整 node_modules + 正确 tsconfig 路径配置）
    # SVN 仓库通常没有完整 node_modules，且路径别名配置与本地不同，tsc 会报大量误报
    # 如需开启，改为: tsc_result = subprocess.run(["npx", "tsc", "--noEmit", ...

    return {"issues": issues[:50], "summary": {"total": len(issues)}}


def run_phpcs(files: List[str], base_path: str) -> Dict[str, Any]:
    """PHP CodeSniffer - 只报严重问题"""
    if not files:
        return {"issues": [], "summary": "No PHP files"}

    php_files = [f for f in files if f.endswith(".php")]
    if not php_files:
        return {"issues": [], "summary": "No PHP files"}

    # 只报 ERROR 级别
    result = subprocess.run(
        ["phpcs", "--standard=PSR12", "--severity=5,4,3", "-q"] + php_files,
        capture_output=True,
        text=True,
        cwd=base_path,
    )

    issues = []
    for line in result.stdout.splitlines():
        if ": error" in line or ": warning" in line.lower():
            parts = line.split(":")
            if len(parts) >= 4:
                issues.append({
                    "severity": "WARNING",
                    "file": parts[0],
                    "line": parts[1],
                    "message": ":".join(parts[3:]).strip()[:100],
                })
    return {"issues": issues, "summary": {"total": len(issues)}}


def scan_repo(repo_name: str, files: List[str], base_path: str, lang: str = None) -> Dict[str, Any]:
    """根据仓库类型调度分析"""
    if lang is None:
        lang = REPOS.get(repo_name, {}).get("lang", "django")
    all_issues = []

    if lang in ("python", "django"):
        # 1. 语法错误检查
        syntax_issues = check_syntax_errors(base_path)
        all_issues.extend(syntax_issues)

        # 2. Bandit 安全扫描
        bandit_result = run_bandit(base_path)
        all_issues.extend(bandit_result.get("issues", []))

        # 3. Pylint 严重错误
        pylint_result = run_pylint_heavy(base_path)
        all_issues.extend(pylint_result.get("issues", []))

    elif lang == "react":
        eslint_result = run_eslint(base_path)
        all_issues.extend(eslint_result.get("issues", []))

    elif lang == "php":
        phpcs_result = run_phpcs(files, base_path)
        all_issues.extend(phpcs_result.get("issues", []))

    elif lang == "mixed":
        # PHP 后端
        phpcs_result = run_phpcs(files, base_path)
        all_issues.extend(phpcs_result.get("issues", []))
        # React 前端
        eslint_result = run_eslint(base_path)
        all_issues.extend(eslint_result.get("issues", []))

    # 去重
    seen = set()
    unique = []
    for issue in all_issues:
        key = f"{os.path.basename(issue.get('file', ''))}:{issue.get('line', 0)}:{issue.get('message', '')[:50]}"
        if key not in seen:
            seen.add(key)
            unique.append(issue)

    return {
        "issues": unique,
        "summary": {
            "total": len(unique),
            "errors": sum(1 for i in unique if i.get("severity") == "ERROR"),
            "warnings": sum(1 for i in unique if i.get("severity") == "WARNING"),
        },
    }


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python3 analyzer_runner.py <repo_name> <base_path>", file=sys.stderr)
        sys.exit(1)

    repo_name = sys.argv[1]
    base_path = sys.argv[2]

    # 全量扫描：先找所有文件
    valid_exts = (".py", ".ts", ".tsx", ".js", ".jsx", ".php", ".java")
    all_files = []
    for root, dirs, files in os.walk(base_path):
        dirs[:] = [d for d in dirs if d not in ("__pycache__", ".git", "node_modules", "migrations", "venv", ".venv")]
        for f in files:
            if f.endswith(valid_exts):
                all_files.append(os.path.join(root, f))

    result = scan_repo(repo_name, all_files, base_path)
    print(json.dumps(result, ensure_ascii=False, indent=2))
