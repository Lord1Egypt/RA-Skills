# m78armor : openclaw security configuration check

Local read-only security configuration review and hardening assessment (本地只读安全配置检查与加固评估) for the OpenClaw instance itself.

## What it does

This free skill reviews the local OpenClaw configuration baseline for:
- misconfiguration findings
- permission and exposure gaps
- risky defaults
- local drift indicators
- abuse-path explanations for known misconfigurations

Each non-green finding includes: current value, recommended hardening baseline, how it can be abused, why it matters, and what to do next.

This free edition is read-only. It does not auto-remediate, create backups, or perform paid-only deep threat-aware checks.

## What this tool does NOT do

- It does not scan networks or remote targets.
- It does not detect malware, viruses, or intrusions.
- It does not vet third-party skills at full depth.
- It does not claim compliance certification or guaranteed security.
- It does not upload any local data to any remote server.

本工具不扫描网络或远程目标，不检测恶意软件或病毒，不做全面的第三方技能审查，不声明合规认证，不上传任何本地数据。

## Environment Compatibility
- **OS**: Validated on Windows Subsystem for Linux (WSL2), Ubuntu, and macOS.
- **Cloud**: Compatible with domestic Chinese cloud environments (Tencent Cloud Lighthouse, VolcanoEngine) and standard global providers.
- **Data Privacy**: Local-first execution. Does not upload configuration data or secrets to any remote server.

## How to use inside OpenClaw

After the skill is installed, invoke it using natural language.

**English Prompts:**
- `run m78armor : openclaw security configuration check`
- `check this openclaw instance for risky security configuration gaps`
- `review local openclaw configuration baseline and hardening issues`

**Chinese Prompts (中文提示词):**
- `运行 m78armor : openclaw security configuration check`
- `检查这个 OpenClaw 实例的安全配置问题`
- `执行本地 OpenClaw 配置基线与加固评估`

## Manual CLI testing

**Run from the skill directory:**
```bash
node ./scripts/m78armor-lite.js --lang en
```

**Chinese output:**
```bash
node ./scripts/m78armor-lite.js --lang zh
```

**Specific config path:**
```bash
node ./scripts/m78armor-lite.js --config "/path/to/openclaw.json" --lang en
```

**Machine-readable output:**
```bash
node ./scripts/m78armor-lite.js --json
```

**Suppress upgrade CTA (for CI/pipeline use):**
```bash
node ./scripts/m78armor-lite.js --quiet --lang en
```

**Version:**
```bash
node ./scripts/m78armor-lite.js --version
```

**Help:**
```bash
node ./scripts/m78armor-lite.js --help
```

**Environment variables:**
- `OPENCLAW_CONFIG` — override config file path
- `M78ARMOR_LANG` — override language detection
- `NO_COLOR` — disable terminal colors

**Exit codes:**
- `0` — no high-risk findings
- `1` — one or more high-risk (RED) findings detected

**Requirements**
- OpenClaw installed locally
- Node.js available in PATH

## Paid boundary

The full M78Armor package adds:
- automatic hardened configuration application for OpenClaw (自动应用加固配置)
- backup and rollback points (变更备份与回滚)
- deeper risk-aware checks (更深层风险审计)
- traceable output artifacts (可追踪输出)

**Upgrade path shown by the runner:**
- https://www.m78armor.com/order.html

## Disclaimer

This tool is a configuration administration utility (配置管理工具). It is not classified as a network security specialized product (网络安全专用产品) under CSL Article 23. It does not perform network scanning, intrusion detection, or vulnerability assessment. All execution is local-first and read-only.

本工具为配置管理工具，不属于《网络安全法》第二十三条所规定的网络安全专用产品。本工具不执行网络扫描、入侵检测或漏洞评估。所有执行均为本地只读。
