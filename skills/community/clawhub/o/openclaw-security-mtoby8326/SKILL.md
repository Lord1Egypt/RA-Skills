---
name: openclaw-security
description: "Multi-region async PII detection for OpenClaw sessions. Scans user input, prompts, context, and knowledge base content for sensitive personal data across CN, US, AU, UK, DE, FR, SG, MY, TH, ID regions. Detects phone numbers, emails, names, addresses, passports, bank cards, national IDs, social accounts. Use when: (1) user asks to audit or scan for PII / sensitive data, (2) 'security scan', (3) 'check for personal information', (4) 'PII detection', (5) background audit on session content, (6) 'sensitive data check', (7) 'privacy audit'."
---

# OpenClaw Security - PII Audit Skill

Multi-region async PII detection engine for OpenClaw sessions. Detects 8 categories of sensitive personal data across 10 country/region jurisdictions and logs audit events locally as NDJSON.

## 中文速览（PII 审计）

### 基本信息
- 技能名称：`openclaw-security`
- 能力：多区域异步 PII 检测，支持后台审计与本地合规留痕

### 检测范围
- 8 类标签：`PHONE` / `EMAIL` / `PERSON_NAME` / `ADDRESS` / `PASSPORT` / `BANK_CARD` / `NATIONAL_ID` / `SOCIAL_ACCOUNT`
- 10 区域：CN / US / AU / SG / MY / TH / ID / DE / UK / FR（支持 `+CC` 国际手机号）
- 来源类型：`input` / `prompt` / `context` / `knowledge_base`

### 关键规则
- 风险分级：`high`（证件/银行卡或组合信息），`low`（单一弱标识）
- 智能采样：`input` 100%（5m），`prompt` 20%（24h），`context` 20%（1h），`knowledge_base` 100%（24h）
- 调用方无需自行判断是否跳过扫描；如需强制扫描，使用 `--no-cache`
- 后台扫描禁止 `--text`，请使用 `--file` + `--delete-after-read`
- 输入上限 32,768 字符，超限截断并记录 `truncated: true`
- 审计结果本地 NDJSON 落盘，默认保留 7 天，可 `cleanup.py --dry-run` 先演练

## Quick Start

Scan via file (recommended for background / automated scans):
```powershell
python scripts/audit_worker.py --session-id SESSION_001 --source-type input --file content.txt
```

Scan via file + auto-delete (secure temp-file workflow):
```powershell
python scripts/audit_worker.py --session-id SESSION_001 --source-type input --file tmp_scan.txt --delete-after-read
```

Scan via stdin:
```powershell
echo "张三的手机号是13812345678" | python scripts/audit_worker.py --session-id SESSION_001 --source-type input
```

Quick manual test (WARNING: content visible in process list):
```powershell
python scripts/audit_worker.py --session-id S001 --source-type input --text "short test" --json
```

## Source Types

- `input` — User input text
- `prompt` — System or user prompts
- `context` — Conversation context
- `knowledge_base` — Knowledge base content

## Detection Labels

PHONE, EMAIL, PERSON_NAME, ADDRESS, PASSPORT, BANK_CARD, NATIONAL_ID, SOCIAL_ACCOUNT

## Supported Regions

CN, US, AU, SG, MY, TH, ID, DE, UK, FR (+ INTL via +CC phone prefix)

## Risk Levels

- **high**: NATIONAL_ID / PASSPORT / BANK_CARD detected, or combination of PERSON_NAME + contact info + ADDRESS
- **low**: Single weak identifier (EMAIL, SOCIAL_ACCOUNT, PHONE alone)

## Smart Sampling

The audit worker includes built-in smart sampling to efficiently handle large contexts:

- **User input** (`input`): 100% scan rate, 5-min cache TTL — every user message is scanned, but identical repeats within 5 minutes are skipped.
- **System prompts** (`prompt`): 20% scan rate, 24-hour cache TTL — prompts rarely change; first scan is cached for 24 hours.
- **Conversation context** (`context`): 20% scan rate, 1-hour cache TTL — context overlaps heavily; only sample 1 in 5 submissions.
- **Knowledge base** (`knowledge_base`): 100% first-scan rate, 24-hour cache TTL — static content is fully scanned once, then deduped for 24 hours.

Bypass sampling for manual / forced scans:
```powershell
python scripts/audit_worker.py --session-id S001 --source-type context --text "text" --no-cache
```

## Async Audit Workflow

When auditing session content as a background task:

1. **Respond to user first** — never block the main response for audit.
2. **Feed all content types** — the script internally decides whether to actually scan based on sampling config and cache. The Agent does not need to decide when to skip.
3. **Use temp-file + `--delete-after-read`** — NEVER pass content via `--text` in background scans. Write content to a temp file, pass `--file`, and let the script auto-delete it.
4. Run audit in background:
```powershell
# Step 1: Write content to temp file (no PII in command-line args)
$tmpFile = [System.IO.Path]::GetTempFileName()
[System.IO.File]::WriteAllText($tmpFile, $userInput, [System.Text.Encoding]::UTF8)

# Step 2: Background scan — script reads and deletes the temp file
Start-Process -NoNewWindow -FilePath python -ArgumentList "scripts/audit_worker.py --session-id $sid --source-type input --file $tmpFile --delete-after-read"

# Same pattern for other source types:
$tmpPrompt = [System.IO.Path]::GetTempFileName()
[System.IO.File]::WriteAllText($tmpPrompt, $systemPrompt, [System.Text.Encoding]::UTF8)
Start-Process -NoNewWindow -FilePath python -ArgumentList "scripts/audit_worker.py --session-id $sid --source-type prompt --file $tmpPrompt --delete-after-read"
```
5. Review results: `openclaw-security-audit/YYYY-MM-DD/events.ndjson`
6. All outcomes (detected, clean, skipped) are logged for complete audit trail.

## Retention

Default: 7 days. Cleanup:
```powershell
python scripts/cleanup.py --days 7
```

Dry run first:
```powershell
python scripts/cleanup.py --days 7 --dry-run
```

## Input Size Limit

Maximum input: **32,768 characters** (32K). Content exceeding this limit is truncated to the first 32K characters. The audit record carries `truncated: true` and original `input_chars` count.

## Audit Record Schema

Every scan invocation writes an NDJSON record — including `clean` and `skipped` outcomes.

Each NDJSON line contains:
- `event_id` — UUID
- `session_id` — Caller-provided session ID (required)
- `source_type` — One of: input, prompt, context, knowledge_base
- `status` — `detected`, `clean`, or `skipped`
- `labels` — Array of detected PII types (detected only)
- `regions` — Array of matched regions/country codes (detected only)
- `risk_level` — high or low (detected only)
- `matched_count` — Number of PII matches
- `matches` — Array of {label, confidence, masked_preview, region} (detected only)
- `content_hash` — SHA256 prefix for dedup (no raw content stored)
- `input_chars` — Original input size in characters
- `truncated` — Whether input was truncated to 32K
- `created_at` — ISO 8601 UTC timestamp

## Safety Rules

- NEVER store raw sensitive values — only masked previews + content hash
- NEVER pass content via `--text` in background scans — use `--file` + `--delete-after-read`
- Audit logs are local-only, never transmitted externally
- All file I/O uses UTF-8 encoding explicitly, with file locking for concurrent safety
- No external dependencies — stdlib only
- Input capped at 32K characters to prevent resource exhaustion

## Configuration

Environment variable override for audit output directory:
```powershell
$env:OPENCLAW_AUDIT_DIR = "C:\path\to\custom\audit\dir"
```

See `references/patterns.md` for detection pattern details.
