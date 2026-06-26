# Privacy Guard / 隐私守护者

> 🔒 OpenClaw 敏感信息外泄自动检测工具
> 
> 🔒 Automated Sensitive Data Leakage Detection for OpenClaw

---

## 功能特性 / Features

### 🛡️ 三级检测机制 / Three-Level Detection

| 级别 Level | 说明 Description | 处理方式 Action |
|------------|------------------|------------------|
| 🔴 CRITICAL | 高风险：API密钥、密码、身份证、银行卡 | 立即报警 / Immediate Alert |
| 🟠 HIGH | 较高风险：手机号、OA账号、基金持仓、资产 | 立即报警 / Immediate Alert |
| 🟡 SUSPICIOUS | 可疑模式：大额数字、邮箱、6位数字 | 待确认 / Pending Review |

### 🤝 智能容错 / Smart Error Tolerance

- **不确定时不误报**：SUSPICIOUS 级别不直接报警，交给用户判断
- **Smart noise filtering**: Suspicious level doesn't alert directly, pending user confirmation
- **智能去重**：相同内容只记录一次
- **Duplicate removal**: Same content recorded only once
- **已知安全模式过滤**：自动跳过正常的时间戳、UUID、JSON数据等
- **Safe pattern filtering**: Auto-skip normal timestamps, UUIDs, JSON data

### 📚 交互学习 / Interactive Learning

发现可疑信息时，你可以 / When suspicious data is found:

- `确认安全 N` - 标记为安全，自动加入白名单 / Mark as safe, auto-add to whitelist
- `确认风险 N` - 标记为风险，需要进一步处理 / Mark as risk, needs further action
- `查看可疑` - 查看待确认的可疑项目列表 / View pending items
- `白名单` - 查看当前白名单 / View current whitelist
- `添加白名单 模式` - 手动添加新白名单规则 / Add custom whitelist pattern

### 🔄 自动进化 / Auto Evolution

- 每次扫描自动更新可疑列表
- Each scan auto-updates the suspicious list
- 用户确认后自动学习（加入白名单/规则）
- User confirmation triggers auto-learning (whitelist/rule update)
- 白名单持久化到本地文件
- Whitelist persisted to local file

---

## 工作原理 / How It Works

```
日志文件 (.log) / Log File (.log)
      ↓
OpenClaw 日志解析 / OpenClaw Log Parsing
      ↓
Privacy Guard 扫描 / Privacy Guard Scan
      ↓
  ┌───────────────────────┐
  │ CRITICAL / HIGH 风险   │ → 立即报警 / Immediate Alert
  └───────────────────────┘
  ┌───────────────────────┐
  │ SUSPICIOUS 可疑       │ → 加入待确认列表 / Pending Review
  └───────────────────────┘
      ↓
  用户交互确认 / User Confirmation
      ↓
  自动学习进化 / Auto Evolution
```

---

## 安装 / Installation

### 方式一：通过 ClawHub 安装（待上线）/ Via ClawHub (Coming Soon)

```bash
openclaw skills install privacy-guard
```

### 方式二：手动安装 / Manual Installation

```bash
# 克隆仓库 / Clone repo
git clone https://github.com/cq2000419/privacy-guard.git

# 进入目录 / Enter directory
cd privacy-guard

# 查看帮助 / View help
python privacy_guard.py --help
```

---

## 快速开始 / Quick Start

### 扫描日志 / Scan Logs

```bash
python privacy_guard.py --scan
```

### 查看报告 / View Report

```bash
python privacy_guard.py --report
```

### 交互模式 / Interactive Mode

```bash
python privacy_guard.py --interactive

# scan       - 执行扫描 / Execute scan
# report     - 查看报告 / View report
# list       - 查看可疑列表 / View suspicious list
# safe N     - 确认第N项为安全 / Mark item N as safe
# risk N     - 确认第N项为风险 / Mark item N as risk
# whitelist  - 查看白名单 / View whitelist
# add P      - 添加模式到白名单 / Add pattern to whitelist
# quit       - 退出 / Exit
```

---

## 检测规则 / Detection Rules

### 🔴 CRITICAL（立即报警 / Immediate Alert）

| 类型 Type | 说明 Description | 示例 Example |
|-----------|------------------|--------------|
| API密钥 | sk-开头的密钥字符串 | `sk-cp-aAbBcCdD...` |
| 明文密码 | password/passwd/pwd字段 | `password=123456` |
| 身份证号 | 18位身份证号码 | `110101199001011234` |
| 银行卡号 | 16-19位数字 | `6222021234567890` |

### 🟠 HIGH（立即报警 / Immediate Alert）

| 类型 Type | 说明 Description | 示例 Example |
|-----------|------------------|--------------|
| 手机号 | 中国大陆手机号 | `13800138000` |
| OA账号 | 公司OA系统账号 | `80024915` |
| 基金持仓 | 基金名称+金额组合 | `易方达稳健收益 12,800` |
| 资产总额 | 总资产/总持仓相关 | `总资产 1,200,000` |

### 🟡 SUSPICIOUS（待确认 / Pending Review）

| 类型 Type | 说明 Description | 示例 Example |
|-----------|------------------|--------------|
| 大额数字 | 超过4位的数组组合 | `12,800` / `100,000` |
| 邮箱地址 | 电子邮件格式 | `user@example.com` |
| 6位数字 | 可能为验证码或账号 | `123456` |

---

## 文件结构 / File Structure

```
privacy-guard/
├── SKILL.md              # Skill元数据 / Skill metadata
├── README.md             # 本文件 / This file
├── privacy_guard.py      # 核心脚本 / Core script
├── config.json           # 配置文件 / Configuration
├── whitelist.json        # 用户白名单（自动生成）/ User whitelist (auto)
├── suspicious.json       # 可疑列表（自动生成）/ Suspicious list (auto)
├── alert_log.md          # 告警日志 / Alert log
└── scan_report.md        # 扫描报告 / Scan report
```

---

## 安全声明 / Security Notice

- ✅ 所有检测在本地执行，不上传日志内容
- ✅ All detection runs locally, no log content uploaded
- ✅ 告警只发送元信息，不发送日志全文
- ✅ Alerts only contain metadata, no log content
- ✅ 白名单和可疑列表存储在本地
- ✅ Whitelist and suspicious list stored locally
- ✅ 不访问任何外部服务器（除非要发送飞书通知）
- ✅ No external server access (except Feishu notification if configured)

---

## 使用场景 / Usage Scenarios

### 定期巡检 / Regular Scan

```bash
# Windows 任务计划 / Windows Task Scheduler
schtasks /create /tn "Privacy-Guard" /tr "python PATH\to\privacy_guard.py --scan" /sc hourly /mo 4

# Linux crontab
0 */4 * * * python /path/to/privacy_guard.py --scan
```

### 即时检测 / On-Demand Scan

```bash
python privacy_guard.py --scan
python privacy_guard.py --report
```

---

## 更新日志 / Changelog

### v0.3.0 (2026-04-11)
- ✅ 新增三级检测机制 / Three-level detection
- ✅ 新增容错机制 / Error tolerance mechanism
- ✅ 新增交互学习 / Interactive learning
- ✅ 新增自动进化 / Auto evolution

### v0.2.0 (2026-04-11)
- ✅ 收紧检测规则，减少误报 / Tighter rules, fewer false positives
- ✅ 增加已知安全模式白名单 / Known safe patterns whitelist

### v0.1.0 (2026-04-11)
- ✅ 初版发布 / Initial release

---

## 贡献 / Contributing

欢迎提交 Issue 和 Pull Request！  
Issues and PRs are welcome!

## License

MIT License

---

**Privacy Guard** - 守护你的敏感信息安全  
**Privacy Guard** - Protecting Your Sensitive Information
