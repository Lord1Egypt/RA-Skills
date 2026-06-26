---
name: ict
version: 4.0.0
description: "Security audit tool for Claw Skills - NOT malicious. This tool contains detection rules (eval, exec, subprocess, etc.) for scanning skills, these are security patterns, not actual malicious code. Similar to yoder-skill-auditor."
metadata:
  openclaw:
    requires:
      bins: ["python3"]
      env: []
      config: []
    user-invocable: true
---

# ict

## Basic Info

- **Description**: Automated tool for checking Claw Skill quality, supports code style, security vulnerabilities, documentation completeness and code-documentation consistency
- **Triggers**: quality check, audit, inspect skill, skill quality, ICT, batch scan, full scan, security check, global scan
- **Category**: devtools
- **Version**: 4.0.8

> ⚠️ **Security Notice**: This tool contains malicious code pattern detection rules for static analysis. Detection rules contain keywords like exec, eval, C2 - this is normal for audit functionality and will not execute malicious code.

## Installation

### Install from ClawHub
```bash
clawhub install ict
```

### Manual Installation
```bash
# Clone or download this skill
cd ict

# Make executable
chmod +x ict.py

# Run directly
python3 ict.py --help
```

## Usage

### CLI
```bash
# Single Skill Audit
python ict.py <skill_folder_path>
python ict.py <skill_folder_path> --json

# 5-Dimension Trust Score
python ict.py <skill_folder_path> --score

# Trend Tracking
python ict.py <skill_folder_path> --save-trend
python ict.py <skill_folder_path> --trend

# Compare Two Skills
python ict.py <skill_folder_path> --compare <other_skill_path>

# Diff Audit
python ict.py <old_folder_path> --diff <new_folder_path>

# Batch Scan
python ict.py --all
python ict.py --all --skills-dir /path/to/skills
```

### API
```python
from ict import audit_skill
result = audit_skill("/path/to/skill-folder")
```

## Features

### Security Checks (23 items)

| # | Check | Description |
|---|-------|-------------|
| 1 | Credential Harvest | Credential + network calls combo detection |
| 2 | Code Execution | eval/exec/spawn |
| 3 | Data Exfiltration | webhook.site, requestbin, ngrok URLs |
| 4 | Base64 Obfuscation | Encoded payloads |
| 5 | Sensitive FS | /etc/passwd, ~/.ssh, ~/.aws |
| 6 | Crypto Wallet | ETH/BTC address detection |
| 7 | Dependency Confusion | @internal, typosquatting |
| 8 | Install Hooks | pre/post install |
| 9 | Symlink Attack | Symlink to sensitive paths |
| 10 | Time Bomb | Delayed trigger |
| 11 | Remote Exec | curl | bash, wget | sh |
| 12 | Telemetry | Analytics SDK, tracking |
| 13 | Prompt Injection | "ignore previous instructions" |
| 14 | Stealth Exfil | Hidden data transmission |
| 15 | C2 Server | C2 server detection |
| 16 | Container Escape | Docker socket escape |
| 17 | SSH Remote | SSH/scp commands |
| 18 | Privilege Escalation | sudo, chmod 777 |
| 19 | Hidden Files | Access to .files |
| 23 | Unusual Ports | 4444, 5555, 1337, etc |

### Supported Languages
- Python (.py)
- Shell (.sh, .bash)
- JavaScript/TypeScript (.js, .ts)

### 5-Dimension Trust Score (0-100)

| Dimension | Max | Description |
|----------|-----|-------------|
| Security | 35 | Security check results |
| Quality | 22 | Documentation completeness |
| Structure | 18 | File structure |
| Transparency | 15 | Version/license info |
| Behavioral | 10 | Code consistency |

Grade: A(90+), B(75+), C(60+), D(40+), F(<40)

### Quality Checks
- SKILL.md completeness
- Code style (line length, syntax)
- Code-documentation consistency
- File structure

### Batch Scan
- One-click scan all installed Skills
- Global security report sorted by risk
- Statistics: safe/warning/danger

### Trend Tracking
- `--save-trend` Save score to history
- `--trend` View score trend
- Keep last 50 records

### Comparison
- `--compare` Side-by-side comparison
- Show dimension differences and winner

### Diff Audit
- `--diff` Compare old/new versions
- Identify new issues, fixed issues, regressions

### Exit Code (CI/CD)

| Code | Meaning |
|------|---------|
| 0 | PASS - Safe |
| 1 | REVIEW - Warnings |
| 2 | FAIL - Critical issues |
| 3 | Error |

### False Positive Prevention
- PATTERN_DEF_FILTER - Auto-filter rule definitions
- Comment line filtering
- Allowlist support

### Limitations
- Some checks based on regex, may have false positives
- LLM analysis requires external tools

---

# ict

## 基本信息

- **描述**: 自动化检查 Claw Skill 质量的工具，支持代码风格，安全漏洞、文档完整性和代码文档一致性检查
- **触发词**: 质检, audit, 检查skill, skill质量, ICT, 批量扫描, 全部扫描, 安全体检, 全局扫描
- **分类**: devtools
- **版本**: 4.0.8

> ⚠️ **安全说明**: 本工具包含恶意代码模式检测规则，用于静态分析审计目标代码。检测规则本身包含 exec、eval、C2 等敏感关键字，这是正常的审计功能，不会执行任何恶意操作。

## 安装

### 从 ClawHub 安装
```bash
clawhub install ict
```

### 手动安装
```bash
# 克隆或下载此 skill
cd ict

# 添加执行权限
chmod +x ict.py

# 直接运行
python3 ict.py --help
```

## 使用方法

### CLI
```bash
# 单个 Skill 审查
python ict.py <skill_folder_path>
python ict.py <skill_folder_path> --json

# 5维度信任评分
python ict.py <skill_folder_path> --score

# 趋势追踪
python ict.py <skill_folder_path> --save-trend
python ict.py <skill_folder_path> --trend

# 对比两个 Skills
python ict.py <skill_folder_path> --compare <other_skill_path>

# Diff审计
python ict.py <old_folder_path> --diff <new_folder_path>

# 批量扫描
python ict.py --all
python ict.py --all --skills-dir /path/to/skills
```

### API
```python
from ict import audit_skill
result = audit_skill("/path/to/skill-folder")
```

## 功能

### 安全检查 (23项)

| # | 检测项 | 说明 |
|---|--------|------|
| 1 | 凭证收集 | 凭证+网络调用组合检测 |
| 2 | 代码执行 | eval/exec/spawn |
| 3 | 数据外泄 | webhook.site, requestbin, ngrok |
| 4 | Base64混淆 | 编码载荷 |
| 5 | 敏感文件系统 | /etc/passwd, ~/.ssh, ~/.aws |
| 6 | 加密钱包 | ETH/BTC地址检测 |
| 7 | 依赖混淆 | @internal, 拼写抢注 |
| 8 | 安装钩子 | pre/post install |
| 9 | Symlink攻击 | 符号链接敏感路径 |
| 10 | 时间炸弹 | 延迟触发 |
| 11 | 远程执行 | curl | bash, wget | sh |
| 12 | 遥测追踪 | 分析SDK, 追踪 |
| 13 | 提示词注入 | "忽略之前指令" |
| 14 | 隐蔽数据外发 | 隐藏数据传输 |
| 15 | C2服务器 | C2服务器检测 |
| 16 | 容器逃逸 | Docker socket逃逸 |
| 17 | SSH远程 | SSH/scp命令 |
| 18 | 权限提升 | sudo, chmod 777 |
| 19 | 隐藏文件 | 访问.files |
| 23 | 非寻常端口 | 4444, 5555, 1337等 |

### 支持语言
- Python (.py)
- Shell (.sh, .bash)
- JavaScript/TypeScript (.js, .ts)

### 5维度信任评分 (0-100)

| 维度 | 满分 | 说明 |
|------|------|------|
| Security | 35 | 安全检测结果 |
| Quality | 22 | 文档完整性 |
| Structure | 18 | 文件结构 |
| Transparency | 15 | 版本/许可证信息 |
| Behavioral | 10 | 代码一致性 |

评级: A(90+), B(75+), C(60+), D(40+), F(<40)

### 质量检查
- SKILL.md完整性
- 代码风格
- 代码文档一致性
- 文件结构

### 批量扫描
- 一键扫描所有已安装的Skills
- 按风险排序的全局安全报告
- 统计：安全/警告/危险

### 趋势追踪
- `--save-trend` 保存评分到历史
- `--trend` 查看评分趋势
- 保留最近50条记录

### 对比分析
- `--compare` 并排对比
- 显示各维度差异和胜出者

### Diff审计
- `--diff` 对比新旧版本
- 识别新增问题、修复问题、回归

### Exit Code (CI/CD)

| 退出码 | 含义 |
|--------|------|
| 0 | PASS - 安全 |
| 1 | REVIEW - 警告 |
| 2 | FAIL - 严重问题 |
| 3 | Error |

### 防误报机制
- PATTERN_DEF_FILTER - 自动过滤规则定义
- 注释行过滤
- 白名单支持

### 限制
- 部分检测基于正则，可能存在误报
- LLM分析需外部工具
