---
name: hiq-cortex
description: Find carbon emission factors for any material or process. 1M+ LCA datasets (HiQLCD, Ecoinvent, CarbonMinds). AI-powered BOM carbon footprint calculation and material comparison.
homepage: https://www.hiqlcd.com
metadata: {"openclaw":{"emoji":"🌱","requires":{"env":["HIQ_API_KEY"],"bins":["node"]},"primaryEnv":"HIQ_API_KEY","os":["darwin","linux","win32"]}}
---

# HiQ Cortex — LCA Data Search & Carbon Footprint AI

Find carbon emission factors for any material, product, or process — covering China's full industrial system (HiQLCD), global data (Ecoinvent), and chemicals (CarbonMinds). Calculate carbon footprints from Bills of Materials. ISO 14040/14044 compliant.

## Privacy & Security

This skill reads `HIQ_API_KEY` from your environment and sends queries to `x.hiqlcd.com` only. No other data is collected or transmitted.

## MCP Server (Cursor / Claude Desktop / Claude Code)

If you use Cursor, Claude Desktop, or Claude Code, you can skip this skill and connect directly via MCP:

```json
{
  "mcpServers": {
    "cortex": {
      "url": "https://x.hiqlcd.com/api/deck/mcp",
      "headers": { "X-API-Key": "sk_xxx" }
    }
  }
}
```

Two tools available via MCP: `search_lca_data` (structured JSON) and `run_cortex` (natural language AI assistant).

## Setup (OpenClaw)

1. Get your API key at https://www.hiqlcd.com

2. Add to `~/.openclaw/openclaw.json`:
```json
{
  "skills": {
    "entries": {
      "hiq-cortex": {
        "enabled": true,
        "apiKey": "sk_xxx"
      }
    }
  }
}
```

Or set environment variable: `export HIQ_API_KEY=sk_xxx`

3. Install (first time only):
```bash
cd ~/.openclaw/workspace/skills/hiq-cortex && npm ci
```

## Tools

### 1. Search LCA Datasets

Search databases for emission factors. Returns structured data with GWP values, dataset links, region, and data quality.

```bash
./search.js "stainless steel 304"                          # Search all databases
./search.js "polyethylene HDPE" --sources "HiQLCD"         # Only HiQLCD
./search.js "cement" --sources "Ecoinvent:3.12.0"          # Specific version
./search.js "aluminum" --sources "HiQLCD|Ecoinvent:3.12.0" # Multiple sources
```

Available `--sources`: `HiQLCD`, `Ecoinvent`, `CarbonMinds`, `HiQLCD-AL`. Omit for all.

#### Example Output

```
Status: found
Summary: Found stainless steel 304 datasets.
Verified: 3  Restricted: 2

=== stainless steel 304 ===
--- market for steel, chromium steel 18/8, hot rolled ---
  Key:        a15b4954-808b-307f-8ad9-d58fd7e30597_3.12.0
  Source:     Ecoinvent 3.12.0
  Region:    GLO
  Unit:      kg
  Fit:       high
  GWP100:    5.23 kg CO2e
  Link:      https://www.hiqlcd.com/dataset/Ecoinvent/3.12.0/CUT_OFF/a15b4954-...
```

#### Output Fields

- **Name**: Full dataset name
- **Key**: Unique identifier (`{UUID}_{version}`)
- **Source/Version**: Database and version (e.g. Ecoinvent 3.12.0)
- **Region**: Geographic scope (GLO=Global, RER=Europe, CN=China, US=USA)
- **Unit**: Functional unit (kg, kWh, MJ)
- **GWP100**: Carbon footprint in kg CO2e (restricted datasets require authorization)
- **Fit**: Match quality (high/medium)
- **Link**: Detail page on HiQLCD platform

#### Status Values

- `found` — All results available
- `partial` — Some datasets are restricted (Ecoinvent paid data)
- `not_found` — No matching datasets

### 2. Ask LCA Questions

Natural language AI assistant for LCA, carbon footprint, sustainability. Supports calculations, comparisons, and research.

```bash
./ask.js "calculate carbon footprint for 100kg steel + 50kg aluminum"
./ask.js "compare environmental impact of PET vs HDPE"
./ask.js "what are the main contributors to cement carbon footprint?"
./ask.js "explain cut-off vs consequential system models"
./ask.js "中国钢铁行业的平均碳排放因子是多少？"
```

The assistant can:
- Calculate carbon footprints from BOM (Bill of Materials)
- Compare materials and suggest lower-impact alternatives
- Search and interpret Ecoinvent/HiQLCD datasets
- Answer LCA methodology questions (GWP, system boundaries, allocation, ISO 14040/44)
- Research sustainability topics, EPDs, and industry reports

## When to Use

- User asks about **carbon footprint**, **emission factors**, **GWP**, or **LCA**
- User wants to find **environmental impact data** for materials or processes
- User mentions **Ecoinvent**, **HiQLCD**, or **life cycle assessment**
- User has a **Bill of Materials** and wants carbon footprint calculations
- User asks about **sustainability**, **ISO 14040**, **EPD**, or **carbon neutrality**
- User mentions **Chinese supply chain**, **CBAM**, **battery passport**, or **Scope 3** emissions
- User asks about **China-specific emission factors** vs global averages

## When NOT to Use

- General chemistry or material science questions unrelated to environmental impact
- Financial carbon credits or carbon trading (this tool covers physical carbon footprint)

---

## About HiQ

[HiQ](https://www.hiqlcd.com) is a full lifecycle data platform providing LCA databases, tools, and API services for carbon footprint assessment.

### Databases

| Database | Coverage |
|---|---|
| **HiQLCD** | China's domestic LCA database — 25+ industries (energy, steel, non-ferrous metals, building materials, photovoltaics, batteries, new energy) |
| **HiQLCD-AL** | Specialized aluminum industry carbon footprint database |
| **Ecoinvent** | Global LCA database — 100+ countries, 18,000+ datasets |
| **CarbonMinds** | Chemicals & plastics carbon footprint database |

All data compliant with **ISO 14040 / ISO 14044 / ISO 14067** and the **ILCD framework**. Compatible with openLCA and SimaPro.

### Services

- **Cortex AI Assistant** — Natural language LCA Q&A, BOM carbon footprint calculation, data analysis: https://carbonx.hiqlcd.com/cortex
- **HiQLCD Platform** — Browse, compare, and export LCA datasets: https://www.hiqlcd.com
- **CarbonX** — Carbon footprint management platform: https://carbonx.hiqlcd.com
- **API & MCP** — Programmatic access for system integration and AI agent workflows
- **Blockchain Verification** — Traceable LCA data provenance

### All Integration Options

| Method | Endpoint | Best For |
|---|---|---|
| **Web App** | https://carbonx.hiqlcd.com/cortex | Browser — no install, ready to use |
| **This Skill** | CLI scripts (`search.js` / `ask.js`) | OpenClaw agents |
| **MCP Server** | `https://x.hiqlcd.com/api/deck/mcp` | Cursor, Claude Desktop, Claude Code |
| **REST API** | `https://x.hiqlcd.com/api/deck/search` | Backend services, automation pipelines |

### Contact

- Website: https://www.hiqlcd.com
- Email: info@hiqlcd.com
