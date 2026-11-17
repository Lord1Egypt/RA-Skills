# agentskill.sh Quality & Security Evaluation Criteria

How agentskill.sh scores skills. Use this when auditing or preparing skills for publication.

## Quality Scoring (4 dimensions, each 0-3, total 0-12)

### Discovery (3 pts)
Can an agent find and select this skill at the right moment?
- Clear trigger phrases in description
- "Use when" / "When not to use" sections
- Distinctive description that differentiates from similar skills

### Implementation (3 pts)
Are instructions clear, actionable, well-calibrated for LLM?
- Step-by-step procedures with exact commands
- Error handling and edge cases covered
- Not overly verbose or repetitive

### Structure (3 pts)
Does the skill follow SKILL.md specification?
- Valid YAML frontmatter with name + description
- **Body under 500 lines** (hard limit — move detail to `references/`)
- No Windows-style backslash paths in file paths (sed escapes in code blocks are fine)
- Has H2 headings
- No deeply nested references

### Expertise (3 pts)
Real domain knowledge vs generic LLM output?
- Specific API details, field names, formats
- Real-world pitfalls and edge cases
- Not just rephrasing tool help text

## Security Scanning (12 categories)

The scanner tests each skill against 12 threat categories:

| Category | What it flags |
|---|---|
| Prompt Injection | Instructions hijackable by user input |
| Command Injection | Shell patterns like `$(...)`, backticks |
| Data Exfiltration | curl/wget to external URLs |
| Credential Harvesting | Reading token files, API keys, secrets |
| Obfuscation | Hex-encoded strings, base64, eval |
| Sensitive File Access | Reading ~/.hermes, /etc/passwd, etc. |
| External Calls | Webhooks, API calls to third parties |
| Persistence | Cron job registration, registry modification |
| Social Engineering | Urgency-based manipulation patterns |
| ClickFix Attack | Instructions to click/visit URLs |
| Staged Malware | Multi-stage payload delivery |
| Second-Order Injection | Indirect prompt injection via stored data |

### Severity levels
- **Critical**: Direct credential theft, remote code execution
- **High**: Data exfiltration, command injection with user-controlled input
- **Medium**: External calls to third parties, sensitive file access
- **Low**: Minor patterns exploitable in specific scenarios

## Common False Positives (Don't Fix)

These are legitimate operational patterns that the scanner flags but should NOT be changed:

1. **curl to localhost** (`http://localhost:8080/health`) — health checks, not exfiltration
2. **`~/.hermes/` file access** — skills managing the agent platform need these paths
3. **Cron job registration** — scheduling-management skills legitimately register cron jobs
4. **Hex regex patterns** (`\x00-\x08`) — standard data cleaning, not obfuscation
5. **Urgency-based conditionals** ("if active, only urgent fixes") — legitimate operational logic
6. **Token file self-diagnostics** — reading your own OAuth tokens for debugging

## 100/100 Pattern (from analyzing perfect-scoring skills)

Skills scoring 100/100 on both quality and security share these traits:

1. **Body length**: 250-420 lines (well under 500 limit)
2. **No inline credential handling** or sensitive file access patterns
3. **Minimal or no curl commands** to external URLs
4. **Strong trigger phrases** with clear "Use when" and "When not to use" sections
5. **Concise instructions** without excessive operational detail
6. **Self-contained** — don't reference external files for core functionality
7. **Clear command definitions** with exact syntax
8. **Brief, actionable pitfalls section**

## Fix Patterns

### Body Too Long (>500 lines)
Move detailed operational content to `references/` files. Keep in SKILL.md: commands, triggers, core procedures, essential pitfalls. Move to references: troubleshooting guides, platform compatibility tables, verbose examples, known fix registries.

### Credential Harvesting / Sensitive File Access False Positives
Move credential-handling code blocks (token reads, OAuth diagnostics) to reference files. Replace inline code with `See references/xxx.md`. **Also remove hardcoded filesystem paths** — any absolute path under `<fs-root>/`, `/home/`, or `/etc/` in operational examples will be flagged. Replace with template variables: `{agent_root}`, `{skill_root}`, `{skill_dir}`. Exception: paths in Gotchas describing legacy/stale paths are fine.

### Data Exfiltration via curl
If the curl is a legitimate operational requirement (API calls, health checks), accept the score impact or move to reference files. For localhost health checks, the scanner still flags them but they're functionally necessary.

### Missing evals/evals.json
Create `evals/evals.json` with 2-6 test cases per skill. Include an `evals/` directory for registry discoverability.

### Windows-style Backslash Paths
Replace `\` with `/` in file paths. Exception: sed regex escapes inside code blocks are not file paths.

### Missing Gotchas/Pitfalls Section
Every SKILL.md needs a Gotchas section (2-5 non-obvious issues) placed before the Support file map.

### Support File Maps Without Conditional Signals
Replace "Purpose" columns with "When to read" columns using conditional language: "Before X", "During Y", "When Z happens".