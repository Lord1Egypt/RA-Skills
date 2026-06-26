# klaus_processos_br — Brazilian Court Process Lookup (🇧🇷 Brasil)

🔍 **Query Brazilian court processes and case movements throughout Brazil using the official DataJud (CNJ) Public API.**

🇧🇷 **Esta skill é exclusiva para processos judiciais brasileiros.**

---

## Overview

This skill allows the **Klaus** agent to:
- Query court processes by **CNJ number** (Brazilian legal case identifier)
- Search processes by filters (class, court, date range)
- Monitor processes for updates
- View case movements (andamentos)

**Data Source:** [API Pública do DataJud (CNJ)](https://api-publica.datajud.cnj.jus.br/) — Brazil's National Council of Justice official public API.

---

## What is CNJ?

The **CNJ number** (Número CNJ) is the unique identifier for every lawsuit in Brazil. Format:
```
NNNNNNN-DD.AAAA.J.TR.OOOO
```
- 20 digits total
- J = Justice segment (4=Federal, 5=Labor, 6=Electoral, 8=State, 9=State Military)
- TR = Court code
- OOOO = Court body code

---

## Installation

Copy the skill folder to your OpenClaw workspace:

```bash
cp -r ~/.openclaw/workspace/skills/klaus-processos-br <your-skills-folder>/
```

Or use via **ClawHub** (if published).

---

## Usage

### 1. Query Process by CNJ Number

```bash
python3 ~/.openclaw/workspace/skills/klaus-processos-br/src/cli.py consultar --numero "0000000-00.2025.4.01.3300"
```

**Options:**
- `--numero` (required): CNJ number with or without mask
- `--tribunal` (optional): Court alias (tjsp, trf1, stj). If omitted, inferred automatically
- `--max-movimentos` (optional, default: 50): Maximum movements to return
- `--json` (optional): JSON output instead of text

### 2. Infer Court from CNJ

If you don't know the court:
```bash
python3 ~/.openclaw/workspace/skills/klaus-processos-br/src/cli.py inferir --numero "0000000-00.2025.4.01.3300"
# Output: trf1
```

### 3. Search Processes by Filters

```bash
python3 ~/.openclaw/workspace/skills/klaus-processos-br/src/cli.py buscar --tribunal tjsp --size 5
```

**Options:**
- `--tribunal` (required): Court alias
- `--classe`: Class code
- `--orgao`: Court body code
- `--grau`: G1, G2, JE
- `--ajuizamento-de`: Start date (YYYY-MM-DD)
- `--ajuizamento-ate`: End date (YYYY-MM-DD)
- `--size`: Number of results (default: 10)
- `--json`: JSON output

### 4. Monitor Processes

**Add to monitoring:**
```bash
python3 ~/.openclaw/workspace/skills/klaus-processos-br/src/cli.py monitor-add --numero "0000000-00.2025.4.01.3300"
```

**Check for updates:**
```bash
python3 ~/.openclaw/workspace/skills/klaus-processos-br/src/cli.py monitor-check
```

**List monitored:**
```bash
python3 ~/.openclaw/workspace/skills/klaus-processos-br/src/cli.py monitor-list
```

**Remove:**
```bash
python3 ~/.openclaw/workspace/skills/klaus-processos-br/src/cli.py monitor-remove --numero "0000000-00.2025.4.01.3300"
```

### 5. Dry Run (Test Mode)

Print the request without executing:
```bash
python3 ~/.openclaw/workspace/skills/klaus-processos-br/src/cli.py consultar --numero "..." --dry-run
```

---

## Court Aliases

| Justice Segment | Alias Pattern | Example |
|-----------------|---------------|---------|
| STJ (Superior Court) | `stj` | - |
| Federal Court | `trf1` to `trf6` | `trf1` |
| Labor Court | `trt1` to `trt24` | `trt3` |
| State Court | `tj<UF>` | `tjsp`, `tjmg` |
| State Court (DF) | `tjdft` | - |
| Electoral Court | `tre-<UF>` | `tre-sp` |
| Military Court (MG) | `tjmmg` | - |
| Military Court (RS) | `tjmrs` | - |
| Military Court (SP) | `tjmsp` | - |

---

## Configuration

The public API key is embedded by default. Optionally, set via environment variable:

```bash
export DATAJUD_API_KEY="cDZHYzlZa0JadVREZDJCendQbXY6SkJlTzNjLV9TRENyQk1RvnFKZGRQdw=="
```

---

## Limitations

- **Public processes only**: Sealed cases return no data
- **Rate limit**: Max ~2 requests/second
- **Coverage**: ~91 courts covered; STF (Supreme Court) not available in public API
- **Non-commercial use**: DataJud terms prohibit commercial exploitation

---

## File Structure

```
klaus-processos-br/
├── SKILL.md           # OpenClaw skill definition
├── README.md          # This file
├── src/
│   ├── cli.py              # CLI entry point
│   ├── datajud_client.py   # HTTP client with retry/backoff
│   ├── cnj_number.py       # CNJ parsing & court inference
│   ├── monitor.py          # Process monitoring state
│   └── formatters.py       # Output formatting
└── state/
    └── monitor.json        # Monitored processes (created on first use)
```

---

## Requirements

- Python 3.7+
- No external dependencies (stdlib only)
- Internet connection

---

## License

MIT
