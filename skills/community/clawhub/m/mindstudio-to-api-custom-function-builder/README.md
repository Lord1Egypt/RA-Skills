# MindStudio To API Custom Function Builder — Claude Skill

A Claude skill that generates complete, ready-to-paste **MindStudio Run Function** integrations for any API you want to drop into your Run Function block.

---

## What it does

Point Claude at any API — paste the docs URL, a code snippet, or just describe what you want — and it produces all three sections you need to paste into MindStudio:

- **Code Tab** — JavaScript that calls the API, validates inputs, logs progress, and stores outputs
- **Configuration Tab** — the config JSON that renders fields in the MindStudio block panel (API key, inputs, output variable names)
- **Test Data Tab** — realistic test values so you can click Test immediately

If you paste API docs or a code example, Claude extracts everything it needs from that directly and only asks for what's missing.

---

## Example usage

> "Build me a MindStudio function for the Finnhub company profile API"

> "I want to connect the OpenAI chat completions endpoint to MindStudio"

> "Write me a MindStudio Run Function for Airtable — here are the docs: [url]"

> "Build a MindStudio function for Stripe to look up a customer by email"

---

## What gets generated

### Code Tab
- Reads all configurable values from `ai.config.*`
- `inputVariable` fields are resolved by MindStudio before the code runs — Claude reads them as `ai.config.fieldName` directly, never via `ai.vars`
- `outputVariableName` fields hold the name of a user-chosen workflow variable — Claude writes outputs as `ai.vars[ai.config.outputVarName]` so results land where you expect
- Validates required fields with clear error messages
- Uses `ai.log()` to show progress during long calls
- Wraps fetch in try/catch with readable error output
- Builds query strings manually — no `URLSearchParams` (not available in Sandbox)

### Configuration Tab
- `secret` type for API keys (never plain text)
- `inputVariable` type for fields that accept `{{workflow variables}}`
- `select` type with options for fixed-choice fields (model names, effort levels, etc.)
- `outputVariableName` type so you name your own output variables
- `helpText` on every field

### Test Data Tab
- Mirrors every `ai.config.*` variable used in the code
- `inputVariable` values are set directly in `config`, not in `vars` — matching how MindStudio resolves them at runtime
- Uses realistic placeholder values, not "test123"
- Ready to run immediately after pasting your API key

---

## Installation

### Claude.ai
1. Download `mindstudio-to-api-custom-function-builder.skill`
2. Go to **Settings → Customize → Skills**
3. Upload the `.skill` file

### Claude Code
```bash
mkdir -p ~/.claude/skills/mindstudio-to-api-custom-function-builder
cp SKILL.md ~/.claude/skills/mindstudio-to-api-custom-function-builder/SKILL.md
```

---

## MindStudio Sandbox limitations

The skill is aware of what's available in MindStudio's Sandbox execution environment:

| Available | Not available |
|-----------|---------------|
| `fetch` | `URLSearchParams` |
| `JSON` | `Buffer` |
| `ai.config`, `ai.vars`, `ai.log()` | `process`, `require` |
| `ai.searchGoogle()`, `ai.scrapeUrl()` | `crypto`, `fs`, `path` |
| `encodeURIComponent()` | npm packages |
| Python via Pyodide | pip installs |

For functions that need npm packages, the skill will use the **Virtual Machine** environment instead, which requires exporting a `handler` function and has a ~5s startup cost.

---

## Authentication patterns supported

| Type | Implementation |
|------|----------------|
| API key header | `"X-API-Key": apiKey` |
| Bearer token | `"Authorization": "Bearer " + apiKey` |
| Basic auth | `"Authorization": "Basic " + btoa(user + ":" + pass)` |
| Query param | `"?token=" + apiKey` appended to URL |
| No auth | Headers omitted |

---

## Common mistakes the skill avoids

- Using `ai.vars[ai.config.fieldName]` for input fields (wrong — inputs are already resolved strings in `ai.config`)
- Using `URLSearchParams` in Sandbox (not available — query strings are built manually)
- Using `Buffer`, `process`, `require`, `crypto`, or `fs` in Sandbox (Node.js only)
- Using `query` instead of `input` for You.com APIs
- Using backtick template literals to inject `{{variables}}` into HTML (use `<script type="application/json">` instead)
- Hardcoding API keys in the Code Tab
- Using `ai.vars.outputName = value` when the output variable name is user-configured

---

## File structure

```
mindstudio-to-api-custom-function-builder/
├── SKILL.md          — Claude skill instructions (install this)
├── README.md         — This file
└── skill.json        — Metadata for skill registries
```

---

## Built from real experience

This skill was built and tested while connecting the **You.com Research API** and **Finnhub Company Profile API** to MindStudio. Every rule and gotcha in the skill comes from something that actually broke during that process — including the `URLSearchParams` Sandbox error, the You.com `input` vs `query` field naming issue, and the dynamic output variable naming pattern.

---

## License

MIT — use freely, modify as needed, attribution appreciated but not required.
