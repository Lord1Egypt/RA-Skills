# mcp-bazi-partner

MCP server for Chinese BaZi (Four Pillars of Destiny) analysis and AI partner matching.

## Install

```bash
pip install mcp-bazi-partner
```

Or install from source:

```bash
pip install git+https://github.com/ZoezoeCookie/mcp-bazi-partner.git
```

## Usage

### As MCP server (for OpenClaw / Claude Code)

```json
{
  "mcpServers": {
    "bazi-partner": {
      "command": "mcp-bazi-partner"
    }
  }
}
```

### Tools

- **bazi_analyze** — Input birth date, get four pillars + pattern determination
- **bazi_partner** — Input pattern result, get matched AI partner type + system prompt

## Method

Based on Shen Xiaozhan's "Ziping Zhenquan" (子平真诠) pattern method.
Covers 38 pattern sub-types × 3 status types = 114 combinations.
