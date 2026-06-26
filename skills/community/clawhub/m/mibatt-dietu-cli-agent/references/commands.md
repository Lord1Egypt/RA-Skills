# Commands

## Base URL

**Default**: `https://dietu-api.mibatt.com`

Override via `--base-url`, `DIETU_BASE_URL`, or profile config.

```bash
dietu --base-url http://localhost:5001 auth status    # 本地开发
dietu --profile prod auth status                    # 使用 prod profile
```

## Output modes

Use these deliberately:

- `--format json` for agents, scripts, and structured parsing
- `--format markdown` for user-facing summaries or copy-paste into docs
- `--format table` for interactive terminal inspection
- `--format ndjson` for streaming-style list consumption

## Market

Overview:

```bash
dietu market overview --format json
dietu market overview --format table
```

Single stock:

```bash
dietu market stock 600519.SH --format json
dietu market stock 000001.SZ --format markdown
```

Search:

```bash
dietu market search 茅台 --limit 10 --format json
dietu market search 600519 --limit 10 --format table
```

Indices:

```bash
dietu market indices --format json
```

## Research

List strategy templates:

```bash
dietu research strategy list --format markdown
```

Run a template:

```bash
dietu research strategy screen white_horse_undervalued --top 10 --format json
```

Topic and recommendation style queries:

```bash
dietu research recommendation --topic 算力 --top 10 --format json
dietu research topics --format markdown
```

## Decision

Plan generation requires an account id:

```bash
dietu decision plan --account 1 --format json
dietu decision context --account 1 --format markdown
```

Single symbol council:

```bash
dietu decision council 600519.SH --account 1 --format json
```

## Trading

Accounts and account snapshot:

```bash
dietu trading accounts --format table
dietu trading account 1 --format json
```

Positions, orders, transactions, performance:

```bash
dietu trading positions --account 1 --format json
dietu trading orders --account 1 --limit 20 --format json
dietu trading transactions --account 1 --limit 20 --format json
dietu trading performance --account 1 --days 30 --format markdown
```

## Review

Executions and decisions:

```bash
dietu review executions --limit 20 --format json
dietu review decisions --limit 20 --format json
dietu review plans --account 1 --limit 20 --format markdown
dietu review performance --account 1 --days 90 --format json
```

## Discovery and diagnostics

Use these before guessing command shapes:

```bash
dietu schema
dietu schema market.stock
dietu doctor
```

## Agent usage notes

- Prefer `json` unless a human explicitly asked for table or markdown
- Use `schema` if the task is ambiguous
- Use `doctor` when auth, base URL, or backend reachability may be wrong
- Do not fabricate unsupported commands such as `dietu ping`
