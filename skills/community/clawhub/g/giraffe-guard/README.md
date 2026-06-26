# 🦒 Giraffe Guard — 长颈鹿卫士

**Standing tall, watching over your code.**

[English](#english) | [中文](#中文)

---

<a id="english"></a>
## English

A security scanner for [OpenClaw](https://github.com/openclaw/openclaw) skills — detect supply chain attacks, malicious code, and suspicious patterns before they compromise your system.

> Born from a real supply chain poisoning incident in the OpenClaw community. Stand tall, stay safe. 🦒

### Features

- **55+ detection rules** — 38 grep-based + 17 AST-based for semantic Python analysis
- **AST deep analysis** — catches variable concatenation, eval/exec evasion, dynamic imports, getattr obfuscation (requires Python 3)
- **Context-aware** — distinguishes documentation from executable code (low false positives)
- **Pre-install mode** — scan git repos *before* `npm install` / `pip install`
- **Zero dependencies** — only uses bash, grep, sed, find, awk; AST module uses Python stdlib
- **Cross-platform** — macOS (BSD) and Linux (GNU) compatible
- **Multiple output formats** — colored terminal, JSON, SARIF (GitHub Code Scanning)
- **Configurable** — severity thresholds, rule skipping, whitelist, quiet mode
- **CI/CD ready** — exit codes, JSON output, SARIF, `--quiet` for minimal output

### Quick Start

#### As an OpenClaw Skill

```bash
git clone https://github.com/lida408/openclaw-skill-giraffe-guard.git \
  ~/.openclaw/workspace/skills/security-pro

bash ~/.openclaw/workspace/skills/security-pro/scripts/audit.sh ~/.openclaw/workspace/skills/
```

#### Standalone

```bash
git clone https://github.com/lida408/openclaw-skill-giraffe-guard.git
cd openclaw-skill-giraffe-guard
bash scripts/audit.sh /path/to/scan
```

#### Pre-install scan (recommended)

```bash
# Scan a git repo BEFORE installing
bash scripts/audit.sh --pre-install https://github.com/user/some-skill.git

# Scan a local directory before installing
bash scripts/audit.sh --pre-install /path/to/downloaded/skill
```

### Usage

```bash
# Basic scan
bash scripts/audit.sh /path/to/skills

# Pre-install mode (scan before npm/pip install)
bash scripts/audit.sh --pre-install https://github.com/user/skill-repo.git

# Quiet mode (summary only, ideal for CI/CD)
bash scripts/audit.sh --quiet --fail-on CRITICAL /path/to/skills

# SARIF output (for GitHub Code Scanning)
bash scripts/audit.sh --sarif /path/to/skills > results.sarif

# JSON output
bash scripts/audit.sh --json /path/to/skills

# Verbose mode (show context lines around findings)
bash scripts/audit.sh --verbose /path/to/skills

# Skip specific rules
bash scripts/audit.sh --skip-rule pipe-execution --skip-rule dangerous-permissions /path/to/skills

# Only report critical findings
bash scripts/audit.sh --min-severity CRITICAL /path/to/skills

# Strict mode (enable high entropy detection)
bash scripts/audit.sh --strict /path/to/skills

# List all available rules
bash scripts/audit.sh --list-rules

# With whitelist
bash scripts/audit.sh --whitelist whitelist.txt /path/to/skills
```

### All Options

| Flag | Description |
|------|-------------|
| `--verbose` | Show context lines around findings |
| `--json` | JSON output |
| `--sarif` | SARIF output (GitHub Code Scanning) |
| `--strict` | Enable high entropy string detection |
| `--quiet` | Quiet mode: summary + exit code only |
| `--whitelist F` | Specify whitelist file |
| `--context N` | Context lines for verbose mode (default: 2) |
| `--skip-dir D` | Skip directory (repeatable) |
| `--skip-rule R` | Skip rule by name (repeatable, see `--list-rules`) |
| `--min-severity S` | Minimum severity: INFO, WARNING, CRITICAL |
| `--fail-on S` | Exit code threshold: WARNING (default), CRITICAL |
| `--pre-install` | Scan before install (accepts git URL or local dir) |
| `--list-rules` | List all detection rules with descriptions |
| `--version` | Show version |

### Detection Rules

Run `bash scripts/audit.sh --list-rules` for the full list with descriptions.

#### Grep-based rules (38 rules, always active)

**Critical:**
pipe-execution, base64-decode-pipe, base64-echo-decode, security-bypass, tor-onion-address, reverse-shell, anti-sandbox, covert-downloader-python, covert-downloader-node, covert-downloader-powershell, persistence-launchagent, hardcoded-aws-key, hardcoded-github-token, hardcoded-stripe-key, hardcoded-slack-token, hardcoded-private-key, actions-script-injection, pyproject-suspicious-hook

**Warning:**
long-base64-string, dangerous-permissions, suspicious-network-ip, netcat-listener, covert-exec-python, covert-exec-eval, file-disguise, sensitive-data-access, cron-injection, encoding-obfuscation, suspicious-npm-package, postinstall-script, skillmd-injection, dockerfile-privileged, zero-width-chars, hardcoded-slack-webhook, hardcoded-generic-secret, actions-unpinned, actions-excessive-permissions, build-script-download, build-script-obfuscation, npm-obfuscated-lifecycle, gemfile-untrusted-source

#### AST-based rules (17 rules, Python files, requires python3)

**Critical:**
ast-eval-dynamic, ast-dynamic-import, ast-getattr-dangerous, ast-command-concat, ast-command-fstring, ast-b64-exec, ast-system-write, ast-string-concat-cmd

**Warning:**
ast-compile-exec, ast-dangerous-import, ast-getattr-dynamic, ast-suspicious-command, ast-codec-obfuscation, ast-high-entropy-string

**Info:**
ast-system-read, ast-env-access, ast-bare-except-pass

### Whitelist File Format

```txt
# Whitelist entire file
path/to/trusted-file.sh

# Whitelist specific line number
path/to/file.sh:42

# Whitelist specific rule for a file
path/to/file.sh:pipe-execution
```

### Exit Codes

| Code | Meaning |
|------|---------|
| 0 | Clean — no findings above threshold |
| 1 | Warnings found |
| 2 | Critical findings |

### CI/CD Integration

```yaml
# GitHub Actions — fail on critical only
- name: Security Audit
  run: |
    bash scripts/audit.sh --quiet --fail-on CRITICAL ./skills
    
# GitHub Actions — SARIF upload
- name: Security Audit (SARIF)
  run: bash scripts/audit.sh --sarif ./skills > results.sarif
- name: Upload SARIF
  uses: github/codeql-action/upload-sarif@v3
  with:
    sarif_file: results.sarif
```

### Automation with OpenClaw

Add to your `TOOLS.md` to enforce scanning on every skill install:

```markdown
## Skill Security Audit (mandatory)
Every new skill must be scanned before activation:
1. Run: `bash skills/security-pro/scripts/audit.sh --pre-install <new-skill-url>`
2. Exit 0 → safe to use
3. Exit 1 → report warnings to user
4. Exit 2 → block activation, notify user
```

---

<a id="中文"></a>
## 中文

[OpenClaw](https://github.com/openclaw/openclaw) 技能安全扫描器 —— 在供应链攻击、恶意代码和可疑模式危害你的系统之前将其检测出来。

> 诞生于 OpenClaw 社区中一起真实的供应链投毒事件。站得高，看得远。🦒

### 特性

- **55+ 条检测规则** — 38 条 grep 规则 + 17 条 AST 语义分析规则
- **AST 深度分析** — 捕获变量拼接、eval/exec 逃逸、动态导入、getattr 混淆等 grep 无法发现的高级攻击（需要 Python 3）
- **上下文感知** — 自动区分文档描述和可执行代码，大幅降低误报
- **安装前扫描** — 在 `npm install` / `pip install` 之前扫描 git 仓库
- **零外部依赖** — 仅使用 bash、grep、sed、find、awk；AST 模块仅用 Python 标准库
- **跨平台** — 兼容 macOS (BSD) 和 Linux (GNU)
- **多种输出格式** — 彩色终端、JSON、SARIF（GitHub Code Scanning）
- **高度可配置** — 严重级别过滤、规则跳过、白名单、静默模式
- **CI/CD 就绪** — 退出码、JSON 输出、SARIF、`--quiet` 最小输出

### 快速开始

#### 作为 OpenClaw Skill 使用

```bash
git clone https://github.com/lida408/openclaw-skill-giraffe-guard.git \
  ~/.openclaw/workspace/skills/security-pro

bash ~/.openclaw/workspace/skills/security-pro/scripts/audit.sh ~/.openclaw/workspace/skills/
```

#### 独立使用

```bash
git clone https://github.com/lida408/openclaw-skill-giraffe-guard.git
cd openclaw-skill-giraffe-guard
bash scripts/audit.sh /path/to/scan
```

#### 安装前扫描（推荐）

```bash
# 安装前扫描（推荐）
bash scripts/audit.sh --pre-install https://github.com/user/some-skill.git

# 扫描本地下载的 skill
bash scripts/audit.sh --pre-install /path/to/downloaded/skill
```

### 使用方法

```bash
# 基本扫描
bash scripts/audit.sh /path/to/skills

# 安装前扫描
bash scripts/audit.sh --pre-install https://github.com/user/skill-repo.git

# 静默模式（仅输出摘要 + 退出码，适合 CI/CD）
bash scripts/audit.sh --quiet --fail-on CRITICAL /path/to/skills

# SARIF 输出（GitHub Code Scanning 集成）
bash scripts/audit.sh --sarif /path/to/skills > results.sarif

# 跳过特定规则
bash scripts/audit.sh --skip-rule pipe-execution /path/to/skills

# 仅报告严重级别
bash scripts/audit.sh --min-severity CRITICAL /path/to/skills

# 查看所有可用规则
bash scripts/audit.sh --list-rules
```

### 退出码

| 退出码 | 含义 |
|--------|------|
| 0 | 安全 — 无发现 |
| 1 | 有警告级别发现 |
| 2 | 有严重级别发现 |

### CI/CD 集成

```yaml
# GitHub Actions — 仅在有严重发现时失败
- name: Security Audit
  run: bash scripts/audit.sh --quiet --fail-on CRITICAL ./skills
```

### 在 OpenClaw 中自动化

在 `TOOLS.md` 中添加规则，强制每次安装 skill 前扫描：

```markdown
## Skill 安全审计（强制规则）
每个新 skill 必须扫描后才能启用：
1. 运行：`bash skills/security-pro/scripts/audit.sh --pre-install <新skill的URL>`
2. 退出码 0 → 安全可用
3. 退出码 1 → 告知用户警告内容
4. 退出码 2 → 禁止启用，通知用户
```

---

## License / 许可证

[Apache License 2.0](LICENSE)

## Contributing / 贡献

Issues and PRs welcome! / 欢迎提交 Issue 和 PR！

When adding new detection rules / 添加新检测规则时请：

1. Add the check function in `scripts/audit.sh` / 在脚本中添加检测函数
2. Call it from `scan_file()` or `main()` / 在扫描流程中调用
3. Test with `--list-rules` to verify rule is listed / 用 `--list-rules` 验证规则已列出
4. Test against both clean skills and malicious samples / 用正常和恶意样本测试
5. Ensure zero false positives via self-scan / 通过自扫描确保零误报
