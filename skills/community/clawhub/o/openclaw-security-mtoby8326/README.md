# OpenClaw Security Skill 🔒

A multi-region async PII (Personally Identifiable Information) detection engine that runs as an OpenClaw Skill. Scans session content for sensitive data across **10 country/region jurisdictions** and logs audit events locally in NDJSON format.
## 🛡️ 中文速览：PII 审计 Skill 信息

### 基本信息

**技能名称**: `openclaw-security`  
**描述**: 多区域异步 PII（敏感个人信息）检测引擎

### 核心功能

检测 **8 类敏感个人信息**，覆盖 **10 个国家/地区**：

- `PHONE`（手机号）
- `EMAIL`（电子邮箱）
- `PERSON_NAME`（真实姓名）
- `ADDRESS`（物理地址）
- `PASSPORT`（护照号码）
- `BANK_CARD`（银行卡号）
- `NATIONAL_ID`（身份证/国民ID）
- `SOCIAL_ACCOUNT`（社交账号）

支持区域：CN / US / AU / SG / MY / TH / ID / DE / UK / FR（并支持 `+CC` 国际手机号前缀）

### 检测来源类型

- `input` — 用户输入文本
- `prompt` — 系统或用户提示词
- `context` — 对话上下文
- `knowledge_base` — 知识库内容

### 风险等级

- **high**：检测到 `NATIONAL_ID` / `PASSPORT` / `BANK_CARD`，或组合信息（姓名 + 联系方式 + 地址）
- **low**：单一弱标识符（单独邮箱 / 社交账号 / 手机号）

### 智能采样策略

| 来源类型 | 扫描率 | 缓存 TTL | 说明 |
|---|---:|---|---|
| `input` | 100% | 5分钟 | 每条消息都扫描，重复内容跳过 |
| `prompt` | 20% | 24小时 | 提示词变化少 |
| `context` | 20% | 1小时 | 上下文重叠度高 |
| `knowledge_base` | 100% | 24小时 | 首次全扫，后续去重 |

采样与缓存决策由脚本内部处理，调用方只需送入内容。需要强制扫描时使用 `--no-cache`。

### 使用方式

```powershell
# 1) 文件扫描（推荐）
python scripts/audit_worker.py --session-id SESSION_001 --source-type input --file content.txt

# 2) 文件 + 自动删除（安全工作流）
python scripts/audit_worker.py --session-id SESSION_001 --source-type input --file tmp_scan.txt --delete-after-read

# 3) stdin
echo "张三的手机号是13812345678" | python scripts/audit_worker.py --session-id SESSION_001 --source-type input

# 4) 强制扫描（绕过缓存/采样）
python scripts/audit_worker.py --session-id SESSION_001 --source-type context --file context.txt --no-cache
```

> `--text` 仅建议手工快速测试；后台审计不要使用 `--text`，请使用 `--file` + `--delete-after-read`。

### 异步审计工作流（后台）

```powershell
# 步骤1：写入临时文件（命令行参数中不包含 PII）
$tmpFile = [System.IO.Path]::GetTempFileName()
[System.IO.File]::WriteAllText($tmpFile, $userInput, [System.Text.Encoding]::UTF8)

# 步骤2：后台扫描，脚本读取后自动删除临时文件
Start-Process -NoNewWindow -FilePath python -ArgumentList "scripts/audit_worker.py --session-id $sid --source-type input --file $tmpFile --delete-after-read"
```

### 审计记录格式（NDJSON）

每次扫描都会写一条记录（包括 `detected` / `clean` / `skipped`）：

- `event_id` — UUID
- `session_id` — 会话 ID
- `source_type` — 来源类型
- `status` — `detected` / `clean` / `skipped`
- `labels` — 检测到的 PII 类型数组
- `regions` — 命中区域数组
- `risk_level` — 风险等级
- `matched_count` — 匹配数量
- `matches` — 匹配详情（`label` / `confidence` / `masked_preview` / `region`）
- `content_hash` — 内容哈希（用于去重）
- `input_chars` — 输入字符数
- `truncated` — 是否被截断
- `created_at` — 时间戳

### 配置项

- 输入限制：最大 32,768 字符（超过则截断）
- 日志保留：默认 7 天
- 输出目录：`openclaw-security-audit/YYYY-MM-DD/events.ndjson`
- 缓存文件：`.scan-cache.json`

```powershell
# 环境变量覆盖输出目录
$env:OPENCLAW_AUDIT_DIR = "C:\path\to\custom\audit\dir"

# 清理旧日志
python scripts/cleanup.py --days 7
python scripts/cleanup.py --days 7 --dry-run
```

### 安全规则

- 永不存储原始敏感值（仅存脱敏预览 + 内容哈希）
- 后台扫描不使用 `--text`，必须使用 `--file` + `--delete-after-read`
- 审计日志仅本地保存，不外传
- UTF-8 编码 + 文件锁，保障并发安全
- 无外部依赖（仅 Python 标准库）

### 相关文件

- `scripts/audit_worker.py` — 主审计脚本
- `scripts/cleanup.py` — 清理脚本
- `references/patterns.md` — 检测模式详解

## ✨ Features

- **8 PII Categories** — Phone, Email, National ID, Passport, Bank Card, Person Name, Address, Social Account
- **10 Regions** — CN, US, AU, SG, MY, TH, ID, DE, UK, FR (+ any country via +CC phone prefix)
- **Zero Dependencies** — Pure Python stdlib, works out of the box
- **Async & Non-blocking** — Audit decoupled from main workflow
- **Smart False Positive Control** — Checksums (CN ID, AU TFN, TH ID, FR NIR), Luhn (bank card), keyword gating (SSN, passport, name, address)
- **Region Classification** — Each match tagged with ISO country code
- **Overlap Dedup** — Same text range: highest confidence wins
- **Risk Scoring** — Two-level (high/low) with single-label and combo rules
- **Smart Sampling** — Per-source-type sampling rates + content-hash cache dedup
- **Complete Audit Trail** — All outcomes (detected, clean, skipped) logged for compliance
- **Concurrent-Safe** — File locking on NDJSON + cache writes for parallel background scans
- **32K Input Cap** — Truncates oversized content; records original size + truncation flag
- **Secure Input Channel** — `--file` + `--delete-after-read` for background scans (no PII in process args)
- **Local NDJSON Storage** — Partitioned by date, grep/SIEM-friendly
- **Auto Cleanup** — Configurable retention (default: 7 days) + scan cache pruning

## 🌍 Supported Regions

| Region | National ID | Phone (local) | Address | Name |
|--------|------------|---------------|---------|------|
| CN | ID Card (18-digit, checksum) | 1[3-9]X mobile, landline | Province/City structural | Keyword-gated |
| US | SSN (keyword-gated) | (XXX) XXX-XXXX | State + ZIP | Mr./Mrs. + First Last |
| AU | TFN (9-digit, checksum) | 04XX mobile | State + postcode | Keyword-gated |
| SG | NRIC/FIN (keyword-gated) | +65 | — | — |
| MY | MyKad (12-digit, date check) | +60 | — | — |
| TH | National ID (13-digit, checksum) | +66 | — | — |
| ID | NIK/KTP (16-digit, date check) | +62 | — | — |
| DE | Steuer-ID (keyword-gated) | +49 | Street + PLZ | Keyword-gated |
| UK | NIN (keyword-gated) | 07XXX mobile | Postcode | — |
| FR | NIR/INSEE (mod-97 check) | +33 | Rue + code postal | Keyword-gated |

## 🚀 Quick Start

```bash
git clone https://github.com/mtoby8326/openclaw-security-skill.git
cd openclaw-security-skill
```

### Scan Text

```bash
# Scan from file (recommended)
python scripts/audit_worker.py --session-id S001 --source-type knowledge_base \
  --file path/to/content.txt

# Scan from file + auto-delete (secure temp-file workflow)
python scripts/audit_worker.py --session-id S001 --source-type input \
  --file tmp_scan.txt --delete-after-read

# Quick manual test (WARNING: content visible in process list)
python scripts/audit_worker.py --session-id S001 --source-type input \
  --text "Name: Zhang San, Phone: 13812345678" --json
```

### Sample Output

```json
{
  "status": "detected",
  "risk_level": "high",
  "labels": ["NATIONAL_ID", "PERSON_NAME", "PHONE"],
  "regions": ["CN", "INTL", "UK", "US"],
  "matched_count": 8,
  "audit_file": "openclaw-security-audit/2026-03-06/events.ndjson"
}
```

## 🏷️ Detection Labels

| Label | Description | Confidence | Validation |
|-------|-------------|------------|------------|
| `PHONE` | Mobile, landline, international | 0.85-0.92 | Format + country code mapping |
| `EMAIL` | Email address | 0.95 | RFC format match |
| `NATIONAL_ID` | CN/US/AU/SG/MY/TH/ID/DE/UK/FR IDs | 0.85-0.98 | Checksum / keyword-gated |
| `PASSPORT` | Passport number (multi-region) | 0.85 | Keyword-gated |
| `BANK_CARD` | Bank card (13-19 digits) | 0.92 | Luhn algorithm |
| `PERSON_NAME` | CN/Western/DE/FR names | 0.70-0.75 | Keyword / title gated |
| `ADDRESS` | CN/US/AU/UK/DE/FR addresses | 0.75-0.80 | Structural + keyword |
| `SOCIAL_ACCOUNT` | WeChat/QQ/Twitter etc. | 0.80 | Keyword-gated |

## 🎯 Smart Sampling

The audit worker includes built-in smart sampling to avoid redundant scans on large or repetitive context:

| Source Type | Scan Rate | Cache TTL | Rationale |
|---|---|---|---|
| `input` | 100% | 5 min | Every user message scanned; identical repeats within 5 min skipped |
| `prompt` | 20% | 24 hours | System prompts rarely change; scan once, cache long |
| `context` | 20% | 1 hour | Conversation context overlaps heavily; sample 1 in 5 |
| `knowledge_base` | 100% | 24 hours | Static content fully scanned once, then deduped |

**How it works**: The script computes a SHA256 content hash, checks a file-backed cache (`.scan-cache.json`), and applies the sampling rate. The caller (Agent) does not need to decide when to skip — just feed all content through, and the script handles the rest.

```bash
# Force scan (bypass cache + sampling)
python scripts/audit_worker.py --session-id S001 --source-type context --text "..." --no-cache
```

## ⚠️ Risk Level Rules

**HIGH**: `NATIONAL_ID`, `PASSPORT`, or `BANK_CARD` detected, or combo of `PERSON_NAME` + contact + `ADDRESS`

**LOW**: Single weak identifier (email, phone, or social account alone)

## 📋 Audit Record Schema

Every scan invocation writes an NDJSON record — including `clean` and `skipped` outcomes.

```json
{
  "event_id": "uuid",
  "session_id": "caller-provided session ID (required)",
  "source_type": "input | prompt | context | knowledge_base",
  "status": "detected | clean | skipped",
  "labels": ["PHONE", "NATIONAL_ID"],
  "regions": ["CN", "US"],
  "risk_level": "high",
  "matched_count": 3,
  "matches": [
    {"label": "PHONE", "confidence": 0.90, "masked_preview": "13*******00", "region": "CN"},
    {"label": "NATIONAL_ID", "confidence": 0.90, "masked_preview": "***-**-**20", "region": "US"}
  ],
  "content_hash": "sha256[:16]",
  "input_chars": 256,
  "truncated": false,
  "created_at": "ISO 8601 UTC"
}
```

> **Security Principle**: Raw sensitive values are never stored — only minimally masked previews and content hashes.

## 📁 Project Structure

```
openclaw-security/
├── SKILL.md                      # OpenClaw Skill definition
├── README.md
├── .gitignore
├── scripts/
│   ├── audit_worker.py           # Main entry: detect → risk score → NDJSON sink
│   ├── cleanup.py                # Audit log + cache cleanup (UTC-aware)
│   ├── file_lock.py              # Cross-platform file lock (O_CREAT|O_EXCL)
│   └── detectors/                # PII detector modules (multi-region)
│       ├── __init__.py           # Detector registry
│       ├── base.py               # Base class + Match dataclass (with region)
│       ├── phone.py              # Phone (CN/US/AU/UK local + INTL +CC)
│       ├── email_detector.py     # Email (universal)
│       ├── national_id.py        # National IDs (10 countries)
│       ├── passport.py           # Passport (multi-language keywords)
│       ├── bank_card.py          # Bank card (Luhn, universal)
│       ├── person_name.py        # Names (CN/Western/DE/FR)
│       ├── address.py            # Addresses (CN/US/AU/UK/DE/FR)
│       └── social_account.py     # Social accounts
├── references/
│   └── patterns.md               # Detection pattern reference
└── openclaw-security-audit/      # Audit log output (excluded by .gitignore)
    └── YYYY-MM-DD/
        └── events.ndjson
```

## 🧹 Log Cleanup

```bash
python scripts/cleanup.py              # default 7-day retention
python scripts/cleanup.py --days 30    # custom retention
python scripts/cleanup.py --dry-run    # preview only
```

## ⚙️ Configuration

```bash
# Override audit output directory
export OPENCLAW_AUDIT_DIR="/path/to/custom/audit/dir"          # Linux/macOS
$env:OPENCLAW_AUDIT_DIR = "C:\path\to\custom\audit\dir"        # PowerShell
```

## 🛡️ Security Design

- **Minimal Masking** — Only 2-3 characters exposed per sensitive value; raw values never stored
- **Secure Input Channel** — `--file` + `--delete-after-read` prevents PII exposure in process args
- **Concurrent-Safe** — FileLock on all shared files (NDJSON, cache) prevents corruption
- **32K Input Cap** — Truncation prevents ReDoS and memory exhaustion attacks
- **Local Only** — Audit logs never transmitted externally
- **Keyword Gating** — Weak signals require context keywords to fire
- **Algorithm Validation** — CN ID / AU TFN / TH ID / FR NIR checksums; Bank Card Luhn; US SSN range validation
- **Overlap Dedup** — Highest confidence result kept per character range
- **Complete Audit Trail** — All outcomes (detected, clean, skipped) logged for compliance proof

## 🗺️ Roadmap

- [x] Smart sampling with content-hash dedup (v0.2.0)
- [x] Security hardening: file locking, 32K cap, secure input channel, audit-all, tighter masking (v0.3.0)
- [ ] Batch scan mode (`--batch`)
- [ ] `tool_output` source type
- [ ] NER model enhancement for name/address
- [ ] HTML audit report generation
- [ ] PIPL / GDPR / CCPA compliance label mapping
- [ ] Scheduled audit (cron / Task Scheduler)
- [ ] More SEA regions (VN, PH)

## 📄 License

Apache 2.0

## 🤝 Contributing

Issues and PRs welcome! To add a new detector:
1. Create a module in `scripts/detectors/`, extending `BaseDetector`
2. Implement `detect(text)` returning `Match` objects with `region` set
3. Register in `__init__.py`

---

**Made with ❤️ for the OpenClaw community**
