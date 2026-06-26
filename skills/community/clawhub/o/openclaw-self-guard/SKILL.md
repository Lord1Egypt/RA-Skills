---
name: openclaw-self-guard
description: OpenClaw Security Vulnerability Monitor - Checks for OpenClaw security vulnerabilities from NVD CVE database and GitHub Security Advisories. Compares local OpenClaw version against known CVEs, outputs vulnerability details and remediation if found, otherwise runs silently. Auto-installs daily cron job. Data sources: NVD (nist.gov), GitHub Security Advisories.
description_zh: OpenClaw 安全漏洞监控器 - 从 NVD CVE 数据库和 GitHub Security Advisories 检查 OpenClaw 安全漏洞。对比本地版本与已知 CVE，有漏洞则输出详情和补救方案，无漏洞则静默执行。自动安装每日定时任务。数据来源：NVD (nist.gov)、GitHub Security Advisories。
---

# OpenClaw Self Guard - Security Vulnerability Monitor

Monitors OpenClaw for known security vulnerabilities by checking multiple threat intelligence sources.

## Features

- **Version Detection**: Automatically detects local OpenClaw version
- **CVE Monitoring**: Checks NVD, GitHub Security Advisories for OpenClaw-related CVEs
- **Smart Alerting**: Outputs vulnerability details + remediation if found
- **Silent Mode**: Runs silently if no vulnerabilities found
- **Auto Cron**: Installs daily cron job (06:00 Beijing time) during skill setup

## Data Sources

| Source | URL | Description |
|--------|-----|-------------|
| **NVD** | `services.nvd.nist.gov` | NIST National Vulnerability Database |
| **GitHub Advisories** | `api.github.com/advisories` | GitHub Security Advisory Database |

## Usage

### Run Manual Check

```
/openclaw 安全检查
/openclaw-self-guard check
```

### View Current Version

```
/openclaw-self-guard version
```

## Cron Job

Installed automatically during skill setup:
- **Schedule**: Daily at 06:00 (Beijing time)
- **Behavior**: Checks for vulnerabilities, reports if found
- **Delivery**: Console output only (no external channel by default)

To customize delivery channel, edit `~/.openclaw/cron/jobs.json` after installation:
```json
"delivery": {
    "mode": "announce",
    "channel": "feishu"  // or "telegram", etc.
}
```

## Output Format

When vulnerabilities found:
```
# 🔒 OpenClaw 安全漏洞报告
**检查时间**: 2026-03-31
**本地版本**: x.x.x
**检测到漏洞**: X 个

## 漏洞详情
| CVE ID | 严重性 | 描述 | 受影响版本 | 补救方案 |
```

When no vulnerabilities:
```
✅ OpenClaw v{x.x.x} - 未检测到安全漏洞
```

## Skill Structure

```
openclaw-self-guard/
├── SKILL.md
├── scripts/
│   ├── check_vulns.py       # Main vulnerability check
│   ├── fetch_nvd.py        # Fetch CVE from NVD
│   ├── fetch_github.py      # Fetch from GitHub
│   ├── get_version.py      # Get local version
│   └── setup_cron.sh       # Cron auto-installation
└── references/
    └── requirements.txt
```

## Notes

- Requires Python packages: `requests`, `beautifulsoup4`, `lxml`
- Cron job auto-installs during skill setup
- No external channel by default - user configurable
