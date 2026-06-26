#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

try:
    import yaml  # type: ignore
except Exception:  # pragma: no cover
    yaml = None

EXCLUDE_DIRS = {
    ".git",
    "node_modules",
    "dist",
    "build",
    "coverage",
    ".venv",
    "venv",
    "__pycache__",
}

TEXT_EXTENSIONS = {
    ".md", ".txt", ".json", ".yaml", ".yml", ".toml", ".ini", ".cfg", ".conf",
    ".py", ".sh", ".bash", ".zsh", ".js", ".ts", ".tsx", ".jsx", ".mjs", ".cjs",
    ".html", ".css", ".xml", ".sql", ".env", ".example", ".sample", ".lock",
}

EXECUTABLE_EXTENSIONS = {
    ".py", ".sh", ".bash", ".zsh", ".js", ".ts", ".tsx", ".jsx", ".mjs", ".cjs"
}

DOC_EXTENSIONS = {".md", ".txt"}

PATTERN_GROUPS = {
    "network_calls": [
        r"\bcurl\b", r"\bwget\b", r"fetch\(", r"axios", r"requests\.", r"httpx\.",
        r"urllib", r"https?://",
    ],
    "dynamic_execution": [
        r"eval\(", r"exec\(", r"bash -c", r"sh -c", r"subprocess", r"child_process",
        r"spawn\(", r"execFile\(", r"os\.system\(",
    ],
    "encoding_obfuscation": [
        r"base64", r"Buffer\.from\(.*base64", r"atob\(", r"btoa\(", r"gzip", r"zlib", r"decode",
    ],
    "sensitive_access": [
        r"\.env", r"~/.ssh", r"~/.aws", r"~/.config", r"MEMORY\.md", r"USER\.md",
        r"SOUL\.md", r"IDENTITY\.md", r"cookie", r"session", r"token", r"credential",
    ],
    "install_ops": [
        r"npm install", r"pnpm add", r"yarn add", r"pip install", r"uv pip", r"brew install",
        r"apt install", r"yum install", r"go install", r"cargo install",
    ],
    "persistence": [
        r"cron", r"systemd", r"launchd", r"daemon", r"service", r"nohup", r"tmux", r"screen", r"pm2",
    ],
    "elevated_privileges": [
        r"\bsudo\b", r"setcap", r"chmod 777", r"chown root",
    ],
    "direct_ips": [
        r"https?://(?:\d{1,3}\.){3}\d{1,3}",
    ],
}

MANIFEST_FILES = [
    "SKILL.md",
    "package.json",
    "package-lock.json",
    "pnpm-lock.yaml",
    "yarn.lock",
    "requirements.txt",
    "pyproject.toml",
    "Cargo.toml",
    "_meta.json",
    ".clawhub/origin.json",
]

DEFAULT_IGNORED_FILES = {
    "vet_scan.py",
    "vet-scan.sh",
}

RISK_WEIGHTS = {
    "network_calls": 2,
    "dynamic_execution": 4,
    "encoding_obfuscation": 3,
    "sensitive_access": 4,
    "install_ops": 3,
    "persistence": 3,
    "elevated_privileges": 5,
    "direct_ips": 5,
}

DOMAIN_REGEX = re.compile(r"https?://([^/\s\"']+)", re.IGNORECASE)
CODE_FENCE_START = re.compile(r"^```([A-Za-z0-9_+-]*)\s*$")
CODE_FENCE_END = re.compile(r"^```\s*$")
CLI_PATTERNS = {
    "gh": re.compile(r"\bgh\s+(issue|pr|run|api|repo|workflow)\b", re.IGNORECASE),
    "git": re.compile(r"\bgit\s+(clone|push|pull|fetch|checkout)\b", re.IGNORECASE),
    "curl": re.compile(r"\bcurl\b", re.IGNORECASE),
    "python": re.compile(r"\bpython3?\b", re.IGNORECASE),
    "openclaw": re.compile(r"\bopenclaw\b", re.IGNORECASE),
}


@dataclass
class Match:
    path: str
    line: int
    text: str
    pattern: str
    source_kind: str = "file"


@dataclass
class DocCodeBlock:
    path: str
    language: str
    start_line: int
    lines: list[tuple[int, str]]


@dataclass
class SkillFrontmatter:
    name: str | None = None
    description: str | None = None
    metadata: dict | None = None


def should_skip(path: Path) -> bool:
    return any(part in EXCLUDE_DIRS for part in path.parts)


def is_text_file(path: Path) -> bool:
    if path.suffix.lower() in TEXT_EXTENSIONS:
        return True
    try:
        with path.open("rb") as f:
            chunk = f.read(2048)
        return b"\x00" not in chunk
    except OSError:
        return False


def iter_files(root: Path) -> Iterable[Path]:
    for path in sorted(root.rglob("*")):
        if not path.is_file():
            continue
        rel = path.relative_to(root)
        if should_skip(rel):
            continue
        if path.name in DEFAULT_IGNORED_FILES:
            continue
        yield path


def file_kind(path: Path) -> str:
    suffix = path.suffix.lower()
    if suffix in EXECUTABLE_EXTENSIONS:
        return "code"
    if suffix in DOC_EXTENSIONS:
        return "doc"
    return "config"


def should_ignore_line(stripped: str) -> bool:
    return any(token in stripped for token in ["run_search ", "PATTERN_GROUPS =", "RISK_WEIGHTS =", 'r"', "re.compile("])


def parse_skill_frontmatter(skill_md: Path) -> SkillFrontmatter:
    if not skill_md.exists():
        return SkillFrontmatter()
    try:
        text = skill_md.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return SkillFrontmatter()

    if not text.startswith("---\n"):
        return SkillFrontmatter()
    end = text.find("\n---\n", 4)
    if end == -1:
        return SkillFrontmatter()

    raw = text[4:end]
    if yaml is not None:
        try:
            data = yaml.safe_load(raw) or {}
            metadata = data.get("metadata")
            if isinstance(metadata, str):
                try:
                    metadata = json.loads(metadata)
                except Exception:
                    metadata = {"raw": metadata}
            return SkillFrontmatter(
                name=data.get("name"),
                description=data.get("description"),
                metadata=metadata if isinstance(metadata, dict) else None,
            )
        except Exception:
            pass

    info = SkillFrontmatter()
    for line in raw.splitlines():
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        key = key.strip()
        value = value.strip().strip('"')
        if key == "name":
            info.name = value
        elif key == "description":
            info.description = value
        elif key == "metadata":
            try:
                info.metadata = json.loads(value)
            except Exception:
                info.metadata = {"raw": value}
    return info


def extract_doc_code_blocks(path: Path) -> list[DocCodeBlock]:
    try:
        lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
    except OSError:
        return []

    blocks: list[DocCodeBlock] = []
    in_block = False
    block_lang = ""
    block_start = 0
    block_lines: list[tuple[int, str]] = []

    for idx, line in enumerate(lines, start=1):
        if not in_block:
            m = CODE_FENCE_START.match(line.strip())
            if m:
                in_block = True
                block_lang = (m.group(1) or "text").lower()
                block_start = idx
                block_lines = []
            continue

        if CODE_FENCE_END.match(line.strip()):
            blocks.append(DocCodeBlock(str(path), block_lang, block_start, block_lines[:]))
            in_block = False
            block_lang = ""
            block_start = 0
            block_lines = []
            continue

        block_lines.append((idx, line))

    return blocks


def scan_lines(path_label: str, lines: list[tuple[int, str]], patterns: dict[str, list[re.Pattern[str]]], source_kind: str) -> dict[str, list[Match]]:
    results: dict[str, list[Match]] = {k: [] for k in patterns}
    for idx, line in lines:
        stripped = line.strip()
        if not stripped:
            continue
        if should_ignore_line(stripped):
            continue
        for group, regexes in patterns.items():
            for regex in regexes:
                if regex.search(line):
                    results[group].append(Match(path_label, idx, stripped, regex.pattern, source_kind=source_kind))
                    break
    return results


def scan_file(path: Path, patterns: dict[str, list[re.Pattern[str]]]) -> dict[str, list[Match]]:
    try:
        content = path.read_text(encoding="utf-8", errors="replace").splitlines()
    except OSError:
        return {k: [] for k in patterns}
    return scan_lines(str(path), list(enumerate(content, start=1)), patterns, source_kind="file")


def classify_level(score: int) -> str:
    if score <= 2:
        return "🟢 LOW"
    if score <= 5:
        return "🟡 MEDIUM"
    if score <= 8:
        return "🟠 HIGH"
    return "🔴 CRITICAL"


def verdict_from_score(score: int, hard_stop: bool) -> str:
    if hard_stop:
        return "❌ DO NOT INSTALL"
    if score <= 2:
        return "✅ SAFE TO INSTALL"
    if score <= 5:
        return "⚠️ INSTALL WITH CAUTION"
    if score <= 8:
        return "🛑 ONLY INSTALL WITH EXPLICIT HUMAN APPROVAL"
    return "❌ DO NOT INSTALL"


def extract_domains(matches: list[Match]) -> list[str]:
    domains: set[str] = set()
    for match in matches:
        for found in DOMAIN_REGEX.findall(match.text):
            domains.add(found)
        if "wttr.in" in match.text:
            domains.add("wttr.in")
        if "open-meteo.com" in match.text:
            domains.add("api.open-meteo.com")
        if re.search(r"\bgh\b", match.text, re.IGNORECASE):
            domains.add("api.github.com / github.com")
    return sorted(domains)


def detect_cli_capabilities(lines: list[str], metadata: dict | None) -> list[str]:
    capabilities: set[str] = set()
    for line in lines:
        for name, pattern in CLI_PATTERNS.items():
            if pattern.search(line):
                capabilities.add(name)
    requires = (((metadata or {}).get("clawdbot") or {}).get("requires") or {}) if isinstance(metadata, dict) else {}
    bins = requires.get("bins") or []
    if isinstance(bins, list):
        for item in bins:
            if isinstance(item, str):
                capabilities.add(item)
    return sorted(capabilities)


def capability_hints(cli_caps: list[str]) -> list[str]:
    hints: list[str] = []
    if "gh" in cli_caps:
        hints.append("通过 gh CLI 访问 GitHub 远程资源，可能读取或操作 issue/PR/run/API 数据")
    if "git" in cli_caps:
        hints.append("具备 git 远程仓库交互能力")
    if "curl" in cli_caps:
        hints.append("通过 curl 发起 HTTP 请求")
    if "python" in cli_caps:
        hints.append("可能依赖本地 Python 执行脚本")
    if "openclaw" in cli_caps:
        hints.append("会调用 OpenClaw 本地能力")
    return hints


def summarize_permissions(findings: dict[str, list[Match]]) -> dict[str, list[str]]:
    network = extract_domains(findings["network_calls"])
    commands: list[str] = []
    if findings["network_calls"]:
        commands.append("network/http requests")
    if findings["dynamic_execution"]:
        commands.append("dynamic shell/code execution")
    if findings["install_ops"]:
        commands.append("package installation")
    if findings["elevated_privileges"]:
        commands.append("elevated privilege operations")

    sensitive = sorted({m.text for m in findings["sensitive_access"]})
    persistence = sorted({m.text for m in findings["persistence"]})

    return {
        "files_read": sensitive or ["None identified automatically"],
        "files_write": ["Unknown from static pattern scan; requires manual review"],
        "commands": commands or ["None identified automatically"],
        "network": network or ["None identified automatically"],
        "persistence": persistence or ["None identified automatically"],
    }


def recommendation_line(verdict: str) -> str:
    if verdict.startswith("✅"):
        return "建议安装前做一次人工复核即可。"
    if verdict.startswith("⚠️"):
        return "建议限制权限范围，并在受控环境中安装。"
    if verdict.startswith("🛑"):
        return "建议先人工审批，再决定是否安装。"
    return "不建议安装，除非能明确解释并消除风险来源。"


def risk_status(present: bool, unknown: bool = False) -> str:
    if unknown:
        return "未发现证据"
    return "是" if present else "否"


def evidence_text(matches: list[Match], fallback_no: str = "未发现相关命中") -> str:
    if not matches:
        return fallback_no

    def priority(match: Match) -> tuple[int, int]:
        if match.source_kind == "doc_code":
            return (0, match.line)
        path_name = Path(match.path.split('#')[0]).name
        if path_name.endswith((".py", ".sh", ".js", ".ts")):
            return (1, match.line)
        if path_name == "SKILL.md":
            return (2, match.line)
        return (3, match.line)

    sample = sorted(matches, key=priority)[0]
    loc = f"{Path(sample.path.split('#')[0]).name}:{sample.line}"
    return f"命中 {loc} → {sample.text}"


def remote_interaction_evidence(cli_caps: list[str], capability_lines: list[str]) -> str:
    evidence_patterns = [
        r"\bgh\s+(issue|pr|run|api|repo|workflow)\b",
        r"\bgit\s+(clone|push|pull|fetch|checkout)\b",
        r"\bcurl\b",
        r"\bwget\b",
    ]
    compiled = [re.compile(p, re.IGNORECASE) for p in evidence_patterns]
    for line in capability_lines:
        for pattern in compiled:
            if pattern.search(line):
                return f"命中命令示例 → {line.strip()}"
    return "未发现远程交互命令示例"


def remote_write_status(cli_caps: list[str], capability_lines: list[str]) -> tuple[str, str]:
    write_patterns = [
        r"\bgh\s+(issue|pr)\s+(create|edit|close|reopen|merge)\b",
        r"\bgh\s+api\b.*\b(-X|--method)\s+(POST|PUT|PATCH|DELETE)\b",
        r"\bgit\s+push\b",
        r"\bcurl\b.*\b(-X|--request)\s+(POST|PUT|PATCH|DELETE)\b",
    ]
    compiled = [re.compile(p, re.IGNORECASE) for p in write_patterns]
    for line in capability_lines:
        for pattern in compiled:
            if pattern.search(line):
                return "是", f"命中远程写操作命令 → {line.strip()}"
    if "gh" in cli_caps or "git" in cli_caps or "curl" in cli_caps:
        return "未发现证据", "发现远程交互工具，但未命中明确写操作命令"
    return "否", "未发现远程交互工具或写操作命令"


def auth_context_status(cli_caps: list[str]) -> tuple[str, str]:
    if any(cap in cli_caps for cap in ["gh", "git"]):
        return "是", "依赖已登录 CLI，实际能力受当前认证上下文影响"
    return "否", "未发现依赖登录态 CLI 的证据"


def build_risk_matrix(findings: dict[str, list[Match]], cli_caps: list[str], capability_lines: list[str]) -> list[tuple[str, str, str]]:
    remote_write, remote_write_evidence = remote_write_status(cli_caps, capability_lines)
    auth_status, auth_evidence = auth_context_status(cli_caps)
    network_evidence = remote_interaction_evidence(cli_caps, capability_lines)
    if network_evidence == "未发现远程交互命令示例":
        network_evidence = evidence_text(findings["network_calls"])
    return [
        ("外网访问风险", risk_status(bool(findings["network_calls"] or cli_caps)), network_evidence),
        ("敏感文件访问风险", risk_status(bool(findings["sensitive_access"])), evidence_text(findings["sensitive_access"])) ,
        ("动态执行风险", risk_status(bool(findings["dynamic_execution"])), evidence_text(findings["dynamic_execution"])) ,
        ("安装/供应链风险", risk_status(bool(findings["install_ops"])), evidence_text(findings["install_ops"])) ,
        ("持久化风险", risk_status(bool(findings["persistence"])), evidence_text(findings["persistence"])) ,
        ("提权风险", risk_status(bool(findings["elevated_privileges"])), evidence_text(findings["elevated_privileges"])) ,
        ("远程资源写操作风险", remote_write, remote_write_evidence),
        ("认证上下文依赖风险", auth_status, auth_evidence),
    ]


def compact_chat_summary(skill: str, level: str, verdict: str, findings: dict[str, list[Match]], permissions: dict[str, list[str]], cli_caps: list[str], capability_lines: list[str]) -> str:
    matrix = build_risk_matrix(findings, cli_caps, capability_lines)
    lines = [f"Skill：{skill}", f"结论：{verdict}（{level}）"]
    if cli_caps:
        lines.append(f"工具/依赖：{'、'.join(cli_caps[:5])}")
    for name, status, evidence in matrix:
        lines.append(f"- {name}：{status}｜{evidence}")
    lines.append(f"建议：{recommendation_line(verdict)}")
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description="Static triage scanner and chat-oriented report generator for agent skills.")
    parser.add_argument("target", help="Path to the skill directory")
    parser.add_argument("--format", choices=["chat", "text", "json"], default="chat")
    parser.add_argument("--name", default="unknown")
    parser.add_argument("--source", default="local")
    parser.add_argument("--author", default="unknown")
    parser.add_argument("--version", default="unknown")
    parser.add_argument("--claimed-purpose", default="not provided")
    parser.add_argument("--include-docs", action="store_true", help="Also scan markdown/text documentation prose for suspicious patterns")
    args = parser.parse_args()

    root = Path(args.target).expanduser().resolve()
    if not root.is_dir():
        raise SystemExit(f"Target directory not found: {root}")

    frontmatter = parse_skill_frontmatter(root / "SKILL.md")

    compiled_patterns = {
        group: [re.compile(p, re.IGNORECASE) for p in pats]
        for group, pats in PATTERN_GROUPS.items()
    }

    all_files = list(iter_files(root))
    text_files = [p for p in all_files if is_text_file(p)]
    skipped_files = [str(p) for p in all_files if p not in text_files]

    code_files = [p for p in text_files if file_kind(p) == "code"]
    config_files = [p for p in text_files if file_kind(p) == "config"]
    doc_files = [p for p in text_files if file_kind(p) == "doc"]

    findings: dict[str, list[Match]] = {k: [] for k in PATTERN_GROUPS}
    capability_lines: list[str] = []

    if frontmatter.description:
        capability_lines.append(frontmatter.description)
    if frontmatter.metadata:
        capability_lines.append(json.dumps(frontmatter.metadata, ensure_ascii=False))

    scan_targets = code_files + config_files
    for file_path in scan_targets:
        file_findings = scan_file(file_path, compiled_patterns)
        for key, matches in file_findings.items():
            findings[key].extend(matches)

    doc_code_blocks_scanned = 0
    for doc_path in doc_files:
        if doc_path.name != "SKILL.md":
            continue
        blocks = extract_doc_code_blocks(doc_path)
        for block in blocks:
            doc_code_blocks_scanned += 1
            label = f"{block.path}#codeblock:{block.language or 'text'}:{block.start_line}"
            block_findings = scan_lines(label, block.lines, compiled_patterns, source_kind="doc_code")
            for key, matches in block_findings.items():
                findings[key].extend(matches)
            capability_lines.extend(line for _, line in block.lines)

        if args.include_docs:
            doc_findings = scan_file(doc_path, compiled_patterns)
            for key, matches in doc_findings.items():
                findings[key].extend(matches)

    cli_caps = detect_cli_capabilities(capability_lines, frontmatter.metadata)

    hard_stop = bool(findings["direct_ips"] or findings["elevated_privileges"])
    score = sum(RISK_WEIGHTS[key] for key, matches in findings.items() if matches)
    if "gh" in cli_caps:
        score += 2
    if "git" in cli_caps:
        score += 1
    level = classify_level(score)
    verdict = verdict_from_score(score, hard_stop)

    notable_files = [str(root / mf) for mf in MANIFEST_FILES if (root / mf).exists()]
    permissions = summarize_permissions(findings)
    if "gh" in cli_caps and "api.github.com / github.com" not in permissions["network"]:
        permissions["network"] = ["api.github.com / github.com", *permissions["network"]]

    report = {
        "skill": args.name,
        "source": args.source,
        "author": args.author,
        "version": args.version,
        "claimed_purpose": args.claimed_purpose,
        "file_inventory": {
            "files_reviewed": len(scan_targets),
            "total_files": len(all_files),
            "code_files": len(code_files),
            "config_files": len(config_files),
            "doc_files": len(doc_files),
            "doc_code_blocks_scanned": doc_code_blocks_scanned,
            "docs_scanned": args.include_docs,
            "unreviewed_files": skipped_files,
            "notable_files": notable_files,
        },
        "red_flags": {
            key: [m.__dict__ for m in matches[:20]] for key, matches in findings.items()
        },
        "permissions_needed": permissions,
        "inferred_tools": cli_caps,
        "risk_score": {
            "score": score,
            "level": level,
            "hard_stop": hard_stop,
        },
        "verdict": verdict,
        "safe_install_conditions": [
            "Manually review matched lines before installation.",
            "Use sandboxing if network, installs, or dynamic execution are present.",
            "Require explicit human approval for elevated, persistent, or sensitive-data access.",
        ],
        "executive_summary": [
            f"Scanned {len(scan_targets)} code/config files and {doc_code_blocks_scanned} code blocks from SKILL.md out of {len(all_files)} total files.",
            f"Detected pattern groups: {', '.join([k for k, v in findings.items() if v]) or 'none' }.",
            "This is a static triage report and must be followed by manual code review.",
        ],
        "claimed_vs_observed": {
            "claimed": args.claimed_purpose,
            "observed": "Derived from code/config files plus code blocks embedded in SKILL.md.",
            "gaps": [
                "Automatic scan cannot fully infer hidden writes, runtime behavior, or business justification.",
            ],
        },
        "supply_chain": {
            "dependencies_downloads": "Check manifests/lockfiles and installation scripts manually.",
            "version_pinning": "Unknown from generic scan; inspect manifests.",
            "install_time_risks": [m.text for m in findings["install_ops"][:20]] or ["None identified automatically"],
        },
        "chat_summary": compact_chat_summary(args.name, level, verdict, findings, permissions, cli_caps, capability_lines),
    }

    if args.format == "json":
        print(json.dumps(report, ensure_ascii=False, indent=2))
        return 0

    if args.format == "chat":
        print(report["chat_summary"])
        return 0

    print("SKILL VETTING REPORT")
    print("═══════════════════════════════════════")
    print(f"Skill: {report['skill']}")
    print(f"Source: {report['source']}")
    print(f"Author: {report['author']}")
    print(f"Version/Commit: {report['version']}")
    print(f"Claimed Purpose: {report['claimed_purpose']}")
    print("───────────────────────────────────────")
    print("SOURCE REVIEW:")
    print("• Trust Signals: Not assessed automatically")
    print("• Concerns: Static scan only; verify publisher, update history, and source integrity manually")
    print("\nFILE INVENTORY:")
    print(f"• Files Reviewed: {len(scan_targets)}/{len(all_files)}")
    print(f"• Breakdown: code={len(code_files)}, config={len(config_files)}, docs={len(doc_files)}, skill_doc_code_blocks={doc_code_blocks_scanned}, docs_scanned={args.include_docs}")
    print(f"• Unreviewed Files: {', '.join(skipped_files) if skipped_files else 'None'}")
    print(f"• Notable Files: {', '.join(notable_files) if notable_files else 'None'}")
    print("\nCLAIMED VS OBSERVED:")
    print(f"• Claimed: {report['claimed_vs_observed']['claimed']}")
    print(f"• Observed: {report['claimed_vs_observed']['observed']}")
    print(f"• Note: documentation prose is {'included' if args.include_docs else 'excluded'}; SKILL.md code blocks are always scanned")
    print(f"• Gaps/Mismatches: {'; '.join(report['claimed_vs_observed']['gaps'])}")
    print("\nRED FLAGS:")
    for key, matches in findings.items():
        label = key.replace("_", " ").title()
        sample = "; ".join(f"{Path(m.path.split('#')[0]).name}:{m.line}" for m in matches[:5]) or "None"
        print(f"• {label}: {sample}")
    print("\nPERMISSIONS NEEDED:")
    print(f"• Files (read): {', '.join(permissions['files_read'])}")
    print(f"• Files (write): {', '.join(permissions['files_write'])}")
    print(f"• Commands: {', '.join(permissions['commands'])}")
    print(f"• Network: {', '.join(permissions['network'])}")
    print(f"• Persistence: {', '.join(permissions['persistence'])}")
    print("\nSUPPLY CHAIN:")
    print(f"• Dependencies / Downloads: {report['supply_chain']['dependencies_downloads']}")
    print(f"• Version Pinning: {report['supply_chain']['version_pinning']}")
    print(f"• Install-Time Risks: {', '.join(report['supply_chain']['install_time_risks'])}")
    print("\nRISK SCORE:")
    print(f"• Score: {score}")
    print(f"• Level: {level}")
    print("• Rationale: Pattern-based static scan with SKILL.md code-block extraction")
    print("\nVERDICT:")
    print(verdict)
    print("\nSAFE-INSTALL CONDITIONS:")
    for item in report["safe_install_conditions"]:
        print(f"• {item}")
    print("\nEXECUTIVE SUMMARY:")
    for item in report["executive_summary"]:
        print(f"• {item}")
    print("═══════════════════════════════════════")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
