# Skill Baseline

## Install policy

- Install only from allowlisted names/sources.
- Show plan before installing.
- Mark API-key requirements.
- Non-ClawHub skills require explicit link + manual/confirmed install.
- After install, verify `SKILL.md` exists.

## A. Survival package: skill discovery / install / docs

```text
clawhub
find-skill
openclawmp
markdown
```

| Skill | Purpose | Source |
|---|---|---|
| `clawhub` | Search/install/update/publish skills | `npm i -g clawhub`; `clawhub install <skill>` |
| `find-skill` | Skill search + local file search | ClawHub/local |
| `openclawmp` | OpenClaw asset market guidance | local/market |
| `markdown` | Markdown docs/memory/kb maintenance | ClawHub/local |

## B. Web search / research

```text
mcp-skill
tavily
china-web-search
multi-search-engine
just-scrape
hv-analysis
```

- `mcp-skill`: Exa search/deep research/code/company research; may need `MCP_API_KEY`.
- `tavily`: web search; may need Tavily API key.
- `china-web-search`: Chinese web search.
- `multi-search-engine`: broad multi-engine search.
- `just-scrape`: page scraping.
- `hv-analysis`: systematic deep research / competitive analysis.

## C. Document processing

```text
docx
pdf
excel
pptx
markdown
summarize-1
```

- If no `docx` skill exists, use/offer a `python-docx` or mammoth-based template.
- If no `excel` skill exists, use/offer `pandas`/`openpyxl`, `data-analysis`, or sheets-related skills.
- `pdf`, `pptx`, `markdown`, `summarize-1` are strongly recommended.

## D. Summary / humanized writing

```text
summarize-1
humanizer / afrexai-humanizer-1
khazix-writer
copywriting
```

## E. System / self-evolution

```text
skill-vetter
self-improving-1
agent-autonomy-kit
knowledge-health-checker
control-mirror
openclaw-engineering-lifecycle
```

## F. Programming / engineering

```text
superpowers
code-review
gstack-openclaw-investigate
changelog-generator
mcp-builder
```

## G. Frontend / UI / product

```text
frontend
local-frontend-design
superdesign-ui
superdesign
seo-audit
```

## H. Skill creation / optimization lab

```text
skill-creator
nuwa-skill
darwin-skill
skill-vetter
self-improving-1
```

### nuwa-skill

GitHub:

```text
https://github.com/alchaincyf/nuwa-skill
```

Install:

```bash
npx skills add alchaincyf/nuwa-skill
```

### darwin-skill

GitHub:

```text
https://github.com/alchaincyf/darwin-skill
```

Install:

```bash
npx skills add alchaincyf/darwin-skill
```

Backup zip:

```text
https://pub-161ae4b5ed0644c4a43b5c6412287e03.r2.dev/skills/darwin-skill.zip
```

## Recommended packages

### bootstrap-minimal

```text
clawhub
find-skill
openclawmp
markdown
```

### bootstrap-search

```text
mcp-skill
tavily
china-web-search
multi-search-engine
just-scrape
hv-analysis
```

### bootstrap-docs

```text
docx
pdf
excel
pptx
markdown
summarize-1
```

### bootstrap-agentos-core

```text
agent-autonomy-kit
skill-creator
skill-vetter
self-improving-1
knowledge-health-checker
control-mirror
openclaw-engineering-lifecycle
```

### bootstrap-engineering

```text
superpowers
code-review
gstack-openclaw-investigate
changelog-generator
mcp-builder
```

### bootstrap-design

```text
frontend
local-frontend-design
superdesign-ui
superdesign
seo-audit
```

### bootstrap-creator

```text
khazix-writer
copywriting
humanizer
```

### bootstrap-skill-lab

```text
skill-creator
nuwa-skill
skill-vetter
darwin-skill
self-improving-1
```
