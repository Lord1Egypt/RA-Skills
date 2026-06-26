#!/usr/bin/env python3
"""
skill-audit scanner — Static analysis of OpenClaw skill folders.
Detects security risks, API usage, data exfiltration patterns, and prompt injection.
"""

import ast
import json
import os
import re
import sys
import zipfile
import tempfile
import shutil
from pathlib import Path
from dataclasses import dataclass, field
from typing import Optional


# ── Risk levels ──────────────────────────────────────────────────────────────

class Risk:
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

RISK_EMOJI = {
    Risk.LOW: "🟢",
    Risk.MEDIUM: "🟡",
    Risk.HIGH: "🔴",
    Risk.CRITICAL: "⛔",
}

RISK_ORDER = {Risk.LOW: 0, Risk.MEDIUM: 1, Risk.HIGH: 2, Risk.CRITICAL: 3}


@dataclass
class Finding:
    category: str
    risk: str
    title: str
    detail: str
    file: str = ""
    line: int = 0

    def to_dict(self):
        d = {"category": self.category, "risk": self.risk, "title": self.title, "detail": self.detail}
        if self.file:
            d["file"] = self.file
        if self.line:
            d["line"] = self.line
        return d


@dataclass
class AuditReport:
    skill_name: str = ""
    skill_description: str = ""
    overall_risk: str = Risk.LOW
    findings: list = field(default_factory=list)
    required_env: list = field(default_factory=list)
    required_bins: list = field(default_factory=list)
    referenced_urls: list = field(default_factory=list)
    referenced_apis: list = field(default_factory=list)
    file_count: int = 0
    script_count: int = 0

    def add(self, finding: Finding):
        self.findings.append(finding)
        if RISK_ORDER.get(finding.risk, 0) > RISK_ORDER.get(self.overall_risk, 0):
            self.overall_risk = finding.risk

    def to_dict(self):
        return {
            "skill_name": self.skill_name,
            "skill_description": self.skill_description,
            "overall_risk": self.overall_risk,
            "overall_risk_emoji": RISK_EMOJI.get(self.overall_risk, "❓"),
            "total_findings": len(self.findings),
            "findings_by_risk": {
                r: len([f for f in self.findings if f.risk == r])
                for r in [Risk.CRITICAL, Risk.HIGH, Risk.MEDIUM, Risk.LOW]
                if any(f.risk == r for f in self.findings)
            },
            "required_env_vars": self.required_env,
            "required_binaries": self.required_bins,
            "referenced_urls": sorted(set(self.referenced_urls)),
            "referenced_apis": sorted(set(self.referenced_apis)),
            "file_count": self.file_count,
            "script_count": self.script_count,
            "findings": [f.to_dict() for f in sorted(self.findings, key=lambda x: -RISK_ORDER.get(x.risk, 0))],
        }

    def to_text(self):
        """Human-readable report."""
        d = self.to_dict()
        lines = []
        lines.append(f"{'='*60}")
        lines.append(f"  SKILL AUDIT REPORT")
        lines.append(f"  {d['overall_risk_emoji']} Overall Risk: {d['overall_risk'].upper()}")
        lines.append(f"{'='*60}")
        lines.append(f"")
        lines.append(f"Skill:       {d['skill_name']}")
        lines.append(f"Description: {d['skill_description'][:120]}")
        lines.append(f"Files:       {d['file_count']} total, {d['script_count']} executable scripts")
        lines.append(f"Findings:    {d['total_findings']}")
        if d["findings_by_risk"]:
            parts = [f"{RISK_EMOJI.get(r,'?')} {r}: {c}" for r, c in d["findings_by_risk"].items()]
            lines.append(f"             {' | '.join(parts)}")
        lines.append("")

        if d["required_env_vars"]:
            lines.append(f"📋 Required Environment Variables:")
            for e in d["required_env_vars"]:
                lines.append(f"   • {e}")
            lines.append("")

        if d["required_binaries"]:
            lines.append(f"📋 Required Binaries:")
            for b in d["required_binaries"]:
                lines.append(f"   • {b}")
            lines.append("")

        if d["referenced_urls"]:
            lines.append(f"🌐 URLs / External Connections:")
            for u in d["referenced_urls"]:
                lines.append(f"   • {u}")
            lines.append("")

        if d["referenced_apis"]:
            lines.append(f"🔌 APIs / Services Referenced:")
            for a in d["referenced_apis"]:
                lines.append(f"   • {a}")
            lines.append("")

        if d["findings"]:
            lines.append(f"{'─'*60}")
            lines.append(f"  DETAILED FINDINGS")
            lines.append(f"{'─'*60}")
            for i, f in enumerate(d["findings"], 1):
                emoji = RISK_EMOJI.get(f["risk"], "?")
                loc = ""
                if f.get("file"):
                    loc = f" ({f['file']}"
                    if f.get("line"):
                        loc += f":{f['line']}"
                    loc += ")"
                lines.append(f"")
                lines.append(f"  {emoji} [{f['risk'].upper()}] {f['title']}{loc}")
                lines.append(f"     Category: {f['category']}")
                lines.append(f"     {f['detail']}")

        lines.append("")
        lines.append(f"{'='*60}")
        lines.append(f"  END OF REPORT")
        lines.append(f"{'='*60}")
        return "\n".join(lines)


# ── Parsers ──────────────────────────────────────────────────────────────────

def parse_frontmatter(text: str) -> dict:
    """Parse YAML frontmatter from SKILL.md (simple key: value)."""
    fm = {}
    match = re.match(r'^---\s*\n(.*?)\n---', text, re.DOTALL)
    if not match:
        return fm
    block = match.group(1)
    for line in block.split('\n'):
        m = re.match(r'^(\w[\w-]*):\s*(.*)', line)
        if m:
            key = m.group(1).strip()
            val = m.group(2).strip().strip('"').strip("'")
            fm[key] = val
    # Try to parse metadata as JSON
    if 'metadata' in fm:
        # metadata might span multiple lines in the frontmatter block
        meta_match = re.search(r'metadata:\s*(\{.*\})', block, re.DOTALL)
        if meta_match:
            try:
                fm['metadata_parsed'] = json.loads(meta_match.group(1))
            except json.JSONDecodeError:
                pass
    return fm


def extract_metadata(fm: dict) -> dict:
    """Extract openclaw metadata from frontmatter."""
    meta = fm.get('metadata_parsed', {})
    if isinstance(meta, dict):
        return meta.get('openclaw', meta)
    return {}


# ── URL / API detection ─────────────────────────────────────────────────────

URL_RE = re.compile(r'https?://[^\s\'"<>\)]+', re.IGNORECASE)
IP_RE = re.compile(r'\b(?:\d{1,3}\.){3}\d{1,3}(?::\d+)?\b')

KNOWN_API_PATTERNS = {
    "api.openai.com": "OpenAI API",
    "api.anthropic.com": "Anthropic API",
    "api.telegram.org": "Telegram Bot API",
    "slack.com/api": "Slack API",
    "discord.com/api": "Discord API",
    "api.github.com": "GitHub API",
    "graph.microsoft.com": "Microsoft Graph API",
    "googleapis.com": "Google APIs",
    "api.twilio.com": "Twilio API",
    "api.sendgrid.com": "SendGrid API",
    "api.stripe.com": "Stripe API",
    "hooks.slack.com": "Slack Webhooks",
    "webhook.site": "Webhook.site (data capture)",
    "ngrok.io": "Ngrok Tunnel",
    "requestbin": "RequestBin (data capture)",
    "pipedream.net": "Pipedream (data capture)",
    "burpcollaborator": "Burp Collaborator (security testing)",
    "interact.sh": "Interactsh (data capture)",
    "oast.fun": "OAST (data exfiltration)",
    "dnslog.cn": "DNSLog (data exfiltration)",
    "canarytokens.com": "Canary Tokens",
    "pastebin.com": "Pastebin",
}

SAFE_URL_PREFIXES = [
    "https://docs.", "https://github.com/", "https://stackoverflow.com/",
    "https://en.wikipedia.org/", "https://www.python.org/",
    "https://nodejs.org/", "https://example.com", "https://example.invalid",
    "http://localhost", "http://127.0.0.1",
]


# ── Suspicious patterns ─────────────────────────────────────────────────────

EXFIL_PATTERNS = [
    (r'base64[.\s]*(encode|b64encode)', "Base64 encoding (potential data obfuscation)", Risk.MEDIUM),
    (r'requests\.(post|put|patch)\s*\(', "HTTP POST/PUT request (outbound data)", Risk.MEDIUM),
    (r'urllib\.request\.(urlopen|Request)', "urllib outbound request", Risk.MEDIUM),
    (r'http\.client\.HTTP', "http.client outbound connection", Risk.MEDIUM),
    (r'curl\s+-X?\s*(POST|PUT)', "curl POST/PUT (outbound data)", Risk.MEDIUM),
    (r'wget\s+', "wget download", Risk.LOW),
    (r'socket\.connect|socket\.send', "Raw socket connection", Risk.HIGH),
    (r'paramiko|fabric|ssh', "SSH library usage", Risk.MEDIUM),
    (r'smtplib|sendmail', "Email sending capability", Risk.MEDIUM),
]

DANGEROUS_PATTERNS = [
    (r'\beval\s*\(', "eval() call (arbitrary code execution)", Risk.HIGH),
    (r'\bexec\s*\(', "exec() call (arbitrary code execution)", Risk.HIGH),
    (r'subprocess\.(call|run|Popen|check_output)', "subprocess execution", Risk.MEDIUM),
    (r'os\.system\s*\(', "os.system() call", Risk.HIGH),
    (r'os\.popen\s*\(', "os.popen() call", Risk.HIGH),
    (r'__import__\s*\(', "Dynamic import", Risk.HIGH),
    (r'importlib\.import_module', "Dynamic module import", Risk.MEDIUM),
    (r'compile\s*\(.*exec', "Dynamic code compilation", Risk.HIGH),
    (r'ctypes|cffi', "C FFI usage (native code)", Risk.HIGH),
    (r'pickle\.loads?|yaml\.unsafe_load', "Unsafe deserialization", Risk.CRITICAL),
    (r'shutil\.rmtree|os\.remove|os\.unlink', "File deletion", Risk.MEDIUM),
    (r'rm\s+-rf?\s+/', "Recursive delete from root", Risk.CRITICAL),
    (r'chmod\s+777|chmod\s+\+s', "Dangerous permission change", Risk.HIGH),
    (r'sudo\s+', "Sudo usage", Risk.HIGH),
    (r'/etc/passwd|/etc/shadow', "System file access", Risk.HIGH),
    (r'~/.ssh|id_rsa|authorized_keys', "SSH key access", Risk.CRITICAL),
    (r'~/.openclaw/openclaw\.json', "OpenClaw config access (may contain secrets)", Risk.HIGH),
    (r'OPENAI_API_KEY|ANTHROPIC_API_KEY|API_KEY|SECRET|TOKEN', "Secret/key reference in code", Risk.MEDIUM),
]

ENV_ACCESS_PATTERNS = [
    (r'os\.environ\[', "Direct environment variable access"),
    (r'os\.environ\.get\s*\(', "Environment variable read"),
    (r'os\.getenv\s*\(', "Environment variable read"),
    (r'\$\{?\w*(?:KEY|TOKEN|SECRET|PASSWORD|CREDENTIAL)\w*\}?', "Secret env var reference"),
]

FILE_ACCESS_PATTERNS = [
    (r'open\s*\([^)]*["\']/(etc|var|tmp|home|root)', "Absolute path file access outside skill", Risk.MEDIUM),
    (r'open\s*\([^)]*\.\./\.\./', "Path traversal (../../)", Risk.HIGH),
    (r'Path\s*\([^)]*["\']/', "pathlib absolute path", Risk.LOW),
    (r'glob\.(glob|iglob)\s*\([^)]*["\']/', "Filesystem glob from root", Risk.MEDIUM),
    (r'os\.walk\s*\([^)]*["\']/', "Directory walk from absolute path", Risk.MEDIUM),
    (r'os\.listdir\s*\([^)]*["\']/', "Directory listing from absolute path", Risk.LOW),
]

# ── Prompt injection patterns ────────────────────────────────────────────────

PROMPT_INJECTION_PATTERNS = [
    (r'ignore\s+(all\s+)?previous\s+instructions', "Prompt injection: ignore previous instructions", Risk.CRITICAL),
    (r'you\s+are\s+now\s+', "Prompt injection: identity override", Risk.HIGH),
    (r'system\s*:\s*you\s+are', "Prompt injection: fake system message", Risk.CRITICAL),
    (r'<\|?system\|?>', "Prompt injection: system token injection", Risk.CRITICAL),
    (r'do\s+not\s+(mention|reveal|tell|say|report)', "Prompt injection: suppression instruction", Risk.HIGH),
    (r'pretend\s+(you\s+are|to\s+be)', "Prompt injection: role override", Risk.HIGH),
    (r'forget\s+(everything|all|your)', "Prompt injection: memory wipe", Risk.HIGH),
    (r'(?:new|override|replace)\s+(?:system\s+)?instructions?', "Prompt injection: instruction override", Risk.CRITICAL),
    (r'<!--.*?(ignore|override|system|instruction).*?-->', "Hidden HTML comment with instructions", Risk.CRITICAL),
    (r'\x00|\x1b\[', "Null bytes or ANSI escape sequences", Risk.HIGH),
    (r'(?:act|behave)\s+as\s+(?:if|though)', "Prompt injection: behavioral override", Risk.MEDIUM),
    (r'(?:don.t|do\s+not)\s+(?:scan|audit|report|flag|check)', "Prompt injection: audit evasion", Risk.CRITICAL),
]


# ── Scanners ─────────────────────────────────────────────────────────────────

def scan_frontmatter(skill_md_text: str, report: AuditReport):
    """Analyze SKILL.md frontmatter for metadata and requirements."""
    fm = parse_frontmatter(skill_md_text)
    report.skill_name = fm.get('name', '(unknown)')
    report.skill_description = fm.get('description', '(no description)')

    meta = extract_metadata(fm)
    requires = meta.get('requires', {})

    # Extract required bins
    bins = requires.get('bins', []) + requires.get('anyBins', [])
    report.required_bins = bins

    # Extract required env vars
    envs = requires.get('env', [])
    report.required_env = envs
    if meta.get('primaryEnv'):
        if meta['primaryEnv'] not in report.required_env:
            report.required_env.append(meta['primaryEnv'])

    # Flag suspicious binaries
    suspicious_bins = {'curl', 'wget', 'nc', 'ncat', 'netcat', 'nmap', 'ssh', 'scp', 'rsync', 'telnet', 'socat'}
    for b in bins:
        if b in suspicious_bins:
            report.add(Finding(
                category="binary",
                risk=Risk.MEDIUM,
                title=f"Network-capable binary required: {b}",
                detail=f"The skill requires '{b}' which can make network connections or transfer data.",
                file="SKILL.md"
            ))


def scan_skill_md_body(skill_md_text: str, report: AuditReport):
    """Scan SKILL.md body for suspicious content."""
    # Remove frontmatter
    body = re.sub(r'^---\s*\n.*?\n---\s*\n', '', skill_md_text, flags=re.DOTALL)

    # Check for prompt injection
    for pattern, title, risk in PROMPT_INJECTION_PATTERNS:
        for m in re.finditer(pattern, body, re.IGNORECASE):
            report.add(Finding(
                category="prompt_injection",
                risk=risk,
                title=title,
                detail=f"Matched: '{m.group()[:80]}...' — This could manipulate the agent's behavior.",
                file="SKILL.md"
            ))

    # Check for hidden instructions in code blocks or HTML comments
    hidden_blocks = re.findall(r'<!--(.*?)-->', body, re.DOTALL)
    for block in hidden_blocks:
        if len(block.strip()) > 20:
            report.add(Finding(
                category="prompt_injection",
                risk=Risk.HIGH,
                title="Hidden HTML comment with content",
                detail=f"HTML comment contains: '{block.strip()[:100]}...'",
                file="SKILL.md"
            ))

    # Check for invisible unicode or zero-width characters
    zwc = re.findall(r'[\u200b\u200c\u200d\u2060\ufeff]', body)
    if zwc:
        report.add(Finding(
            category="prompt_injection",
            risk=Risk.HIGH,
            title=f"Zero-width / invisible unicode characters found ({len(zwc)}x)",
            detail="Invisible characters can hide malicious instructions from human reviewers.",
            file="SKILL.md"
        ))

    # Extract URLs
    urls = URL_RE.findall(body)
    for url in urls:
        report.referenced_urls.append(url)
        for pattern, api_name in KNOWN_API_PATTERNS.items():
            if pattern in url.lower():
                report.referenced_apis.append(api_name)

    # Flag suspicious URLs (not docs/github/etc.)
    for url in urls:
        if not any(url.startswith(safe) for safe in SAFE_URL_PREFIXES):
            for pattern, api_name in KNOWN_API_PATTERNS.items():
                if pattern in url.lower() and "data capture" in api_name.lower():
                    report.add(Finding(
                        category="network",
                        risk=Risk.CRITICAL,
                        title=f"Data capture service URL: {api_name}",
                        detail=f"URL: {url[:120]} — This service is commonly used for data exfiltration.",
                        file="SKILL.md"
                    ))


def scan_python_file(filepath: Path, content: str, report: AuditReport):
    """Scan a Python file using regex and AST analysis."""
    rel = str(filepath)

    # Regex-based scanning
    for pattern, title, risk in EXFIL_PATTERNS + DANGEROUS_PATTERNS + FILE_ACCESS_PATTERNS:
        for m in re.finditer(pattern, content, re.IGNORECASE):
            line_no = content[:m.start()].count('\n') + 1
            report.add(Finding(
                category="code",
                risk=risk,
                title=title,
                detail=f"Matched: '{m.group()[:80]}'",
                file=rel,
                line=line_no,
            ))

    for pattern, title in ENV_ACCESS_PATTERNS:
        for m in re.finditer(pattern, content):
            line_no = content[:m.start()].count('\n') + 1
            report.add(Finding(
                category="env_access",
                risk=Risk.MEDIUM,
                title=title,
                detail=f"Matched: '{m.group()[:80]}'",
                file=rel,
                line=line_no,
            ))

    # Extract URLs from code
    for m in URL_RE.finditer(content):
        url = m.group()
        report.referenced_urls.append(url)
        for pattern, api_name in KNOWN_API_PATTERNS.items():
            if pattern in url.lower():
                report.referenced_apis.append(api_name)

    # Extract IPs
    for m in IP_RE.finditer(content):
        ip = m.group()
        if not ip.startswith("127.") and not ip.startswith("0.") and ip != "0.0.0.0":
            report.add(Finding(
                category="network",
                risk=Risk.MEDIUM,
                title=f"Hardcoded IP address: {ip}",
                detail="Hardcoded IPs may indicate unexpected network connections.",
                file=rel,
                line=content[:m.start()].count('\n') + 1,
            ))

    # AST analysis for Python
    try:
        tree = ast.parse(content)
        for node in ast.walk(tree):
            # Detect dynamic imports
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id == '__import__':
                report.add(Finding(
                    category="code",
                    risk=Risk.HIGH,
                    title="Dynamic __import__() call",
                    detail="Can load arbitrary modules at runtime.",
                    file=rel,
                    line=node.lineno,
                ))
            # Detect exec/eval with dynamic content
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id in ('exec', 'eval'):
                if node.args and not isinstance(node.args[0], ast.Constant):
                    report.add(Finding(
                        category="code",
                        risk=Risk.HIGH,
                        title=f"{node.func.id}() with dynamic argument",
                        detail="Executing dynamic/user-supplied code is dangerous.",
                        file=rel,
                        line=node.lineno,
                    ))
    except SyntaxError:
        pass  # Not valid Python, regex results still apply


def scan_shell_file(filepath: Path, content: str, report: AuditReport):
    """Scan a shell script for dangerous patterns."""
    rel = str(filepath)

    for pattern, title, risk in EXFIL_PATTERNS + DANGEROUS_PATTERNS + FILE_ACCESS_PATTERNS:
        for m in re.finditer(pattern, content, re.IGNORECASE):
            line_no = content[:m.start()].count('\n') + 1
            report.add(Finding(
                category="code",
                risk=risk,
                title=title,
                detail=f"Matched: '{m.group()[:80]}'",
                file=rel,
                line=line_no,
            ))

    for pattern, title in ENV_ACCESS_PATTERNS:
        for m in re.finditer(pattern, content):
            line_no = content[:m.start()].count('\n') + 1
            report.add(Finding(
                category="env_access",
                risk=Risk.MEDIUM,
                title=title,
                detail=f"Matched: '{m.group()[:80]}'",
                file=rel,
                line=line_no,
            ))

    # Shell-specific dangerous patterns
    shell_patterns = [
        (r'eval\s+"?\$', "eval with variable expansion", Risk.HIGH),
        (r'\$\(.*curl.*\)', "Command substitution with curl", Risk.HIGH),
        (r'>\s*/dev/tcp/', "Bash /dev/tcp network connection", Risk.CRITICAL),
        (r'mkfifo|mknod.*pipe', "Named pipe creation (potential reverse shell)", Risk.CRITICAL),
        (r'bash\s+-i\s+>&\s*/dev/tcp', "Reverse shell pattern", Risk.CRITICAL),
        (r'nc\s+-[elp]', "Netcat listener (potential backdoor)", Risk.CRITICAL),
        (r'python.*-c.*import\s+socket', "Python one-liner socket (potential reverse shell)", Risk.CRITICAL),
        (r'base64\s+-d\s*\|.*sh', "Base64 decode piped to shell", Risk.CRITICAL),
        (r'echo\s+.*\|\s*base64\s+-d\s*\|\s*(bash|sh)', "Obfuscated shell command", Risk.CRITICAL),
    ]

    for pattern, title, risk in shell_patterns:
        for m in re.finditer(pattern, content, re.IGNORECASE):
            line_no = content[:m.start()].count('\n') + 1
            report.add(Finding(
                category="code",
                risk=risk,
                title=title,
                detail=f"Matched: '{m.group()[:80]}'",
                file=rel,
                line=line_no,
            ))

    # URLs and IPs
    for m in URL_RE.finditer(content):
        report.referenced_urls.append(m.group())
        for p, api_name in KNOWN_API_PATTERNS.items():
            if p in m.group().lower():
                report.referenced_apis.append(api_name)


def scan_js_file(filepath: Path, content: str, report: AuditReport):
    """Scan a JavaScript/Node.js file."""
    rel = str(filepath)

    js_patterns = [
        (r'eval\s*\(', "eval() call", Risk.HIGH),
        (r'Function\s*\(', "Function() constructor (dynamic code)", Risk.HIGH),
        (r'child_process', "child_process module (command execution)", Risk.MEDIUM),
        (r'\.exec\s*\(', ".exec() call", Risk.MEDIUM),
        (r'\.spawn\s*\(', ".spawn() call", Risk.MEDIUM),
        (r'require\s*\(\s*[\'"]fs[\'"]', "Filesystem access (fs module)", Risk.LOW),
        (r'require\s*\(\s*[\'"]net[\'"]', "Network access (net module)", Risk.MEDIUM),
        (r'require\s*\(\s*[\'"]http', "HTTP module usage", Risk.LOW),
        (r'fetch\s*\(', "fetch() network request", Risk.LOW),
        (r'XMLHttpRequest', "XMLHttpRequest", Risk.LOW),
        (r'process\.env', "Environment variable access", Risk.MEDIUM),
        (r'Buffer\.from\(.*base64', "Base64 buffer operation", Risk.MEDIUM),
        (r'WebSocket', "WebSocket connection", Risk.MEDIUM),
    ]

    for pattern, title, risk in js_patterns:
        for m in re.finditer(pattern, content, re.IGNORECASE):
            line_no = content[:m.start()].count('\n') + 1
            report.add(Finding(
                category="code",
                risk=risk,
                title=title,
                detail=f"Matched: '{m.group()[:80]}'",
                file=rel,
                line=line_no,
            ))

    for m in URL_RE.finditer(content):
        report.referenced_urls.append(m.group())
        for p, api_name in KNOWN_API_PATTERNS.items():
            if p in m.group().lower():
                report.referenced_apis.append(api_name)


def scan_generic_text(filepath: Path, content: str, report: AuditReport):
    """Scan any text file for prompt injection and URLs."""
    rel = str(filepath)

    for pattern, title, risk in PROMPT_INJECTION_PATTERNS:
        for m in re.finditer(pattern, content, re.IGNORECASE):
            line_no = content[:m.start()].count('\n') + 1
            report.add(Finding(
                category="prompt_injection",
                risk=risk,
                title=title,
                detail=f"Matched: '{m.group()[:80]}'",
                file=rel,
                line=line_no,
            ))

    for m in URL_RE.finditer(content):
        report.referenced_urls.append(m.group())


# ── Main scanner ─────────────────────────────────────────────────────────────

def scan_skill(skill_path: str, output_format: str = "text") -> str:
    """
    Scan a skill folder or .skill file and return an audit report.
    
    Args:
        skill_path: Path to skill folder or .skill file
        output_format: "text" or "json"
    
    Returns:
        Formatted report string
    """
    path = Path(skill_path).resolve()
    cleanup_dir = None

    # Handle .skill files (zip archives)
    if path.is_file() and path.suffix == '.skill':
        tmpdir = tempfile.mkdtemp(prefix='skill-audit-')
        cleanup_dir = tmpdir
        try:
            with zipfile.ZipFile(path, 'r') as zf:
                zf.extractall(tmpdir)
            # Find the skill folder inside
            entries = list(Path(tmpdir).iterdir())
            if len(entries) == 1 and entries[0].is_dir():
                path = entries[0]
            else:
                path = Path(tmpdir)
        except zipfile.BadZipFile:
            return "ERROR: Not a valid .skill file (bad zip archive)"

    if not path.is_dir():
        return f"ERROR: '{skill_path}' is not a directory or .skill file"

    skill_md = path / 'SKILL.md'
    if not skill_md.exists():
        return f"ERROR: No SKILL.md found in '{skill_path}'"

    report = AuditReport()

    # Count files
    all_files = list(path.rglob('*'))
    report.file_count = len([f for f in all_files if f.is_file()])

    # Scan SKILL.md
    skill_md_text = skill_md.read_text(errors='replace')
    scan_frontmatter(skill_md_text, report)
    scan_skill_md_body(skill_md_text, report)

    # Scan all files
    script_exts = {'.py', '.sh', '.bash', '.js', '.mjs', '.cjs', '.ts'}
    text_exts = {'.md', '.txt', '.yaml', '.yml', '.json', '.toml', '.cfg', '.ini', '.conf'}

    for fpath in all_files:
        if not fpath.is_file():
            continue

        rel_path = fpath.relative_to(path)

        # Skip hidden files and common non-text
        if any(part.startswith('.') for part in rel_path.parts):
            continue

        try:
            content = fpath.read_text(errors='replace')
        except Exception:
            continue

        suffix = fpath.suffix.lower()

        if suffix in script_exts:
            report.script_count += 1
            if suffix == '.py':
                scan_python_file(rel_path, content, report)
            elif suffix in {'.sh', '.bash'}:
                scan_shell_file(rel_path, content, report)
            elif suffix in {'.js', '.mjs', '.cjs', '.ts'}:
                scan_js_file(rel_path, content, report)
        elif suffix in text_exts and str(rel_path) != 'SKILL.md':
            scan_generic_text(rel_path, content, report)

    # Add informational findings
    if not report.findings:
        report.add(Finding(
            category="info",
            risk=Risk.LOW,
            title="No issues detected",
            detail="Static analysis found no suspicious patterns. Note: this does not guarantee safety — review manually for logic-level attacks.",
        ))

    if cleanup_dir:
        shutil.rmtree(cleanup_dir, ignore_errors=True)

    if output_format == "json":
        return json.dumps(report.to_dict(), indent=2)
    else:
        return report.to_text()


# ── CLI ──────────────────────────────────────────────────────────────────────

def main():
    if len(sys.argv) < 2:
        print("Usage: scan_skill.py <skill-path> [--json]")
        print("  skill-path: path to skill folder or .skill file")
        print("  --json: output as JSON instead of text")
        sys.exit(1)

    skill_path = sys.argv[1]
    fmt = "json" if "--json" in sys.argv else "text"
    print(scan_skill(skill_path, fmt))


if __name__ == "__main__":
    main()