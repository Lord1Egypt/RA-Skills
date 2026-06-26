# OpenClaw Skill Authoring Reference

Complete reference for writing, testing, deploying, and evaluating OpenClaw skills.
Load when building new skills, evaluating community skills, or optimizing existing skill packs.

## Table of Contents
1. Skill Anatomy
2. YAML Frontmatter Specification
3. Three-Tier Loading Architecture
4. Body Writing Best Practices
5. Reference Files
6. Directory Structure Patterns
7. ClawHub Registry
8. Security Model
9. Testing & Validation
10. Multi-Agent Skill Sharing
11. Skill Evaluation Framework

---

## 1. Skill Anatomy

A skill is a directory containing one required file (`SKILL.md`) plus optional supporting files.

```
my-skill/
├── SKILL.md           # REQUIRED: Agent instructions with YAML frontmatter
├── references/        # Optional: Deep knowledge files
│   ├── api-docs.md
│   └── schemas.md
├── scripts/           # Optional: Helper scripts
│   └── helper.sh
├── bins/              # Optional: Executables (auto-added to PATH)
│   └── my-tool
├── skill.json         # Optional: Metadata (alternative to frontmatter)
├── templates/         # Optional: Output templates
└── README.md          # Optional: Human documentation
```

**Key Principle:** SKILL.md is an INDEX, not a dump. The agent should be able to handle simple tasks from the body alone. Deep knowledge lives in reference files.

## 2. YAML Frontmatter Specification

The frontmatter is the contract between your skill and OpenClaw's loader.

**Required Fields:**
```yaml
---
name: my-skill
description: "Short summary matching how users ask for this task"
---
```

**Full Specification:**
```yaml
---
name: my-skill
description: "Trigger phrase — write like describing to a coworker in chat"
version: "1.0.0"
metadata: { "openclaw": { "emoji": "🔬", "requires": { "bins": ["curl", "jq"], "binsOneOf": ["python3", "python"], "env": ["API_KEY"], "config": ["browser.enabled"] }, "primaryEnv": "API_KEY", "alwaysActive": true, "os": ["darwin", "linux"], "homepage": "https://github.com/example/skill", "install": [ { "id": "brew", "kind": "brew", "formula": "my-tool", "bins": ["my-tool"], "label": "Install my-tool (brew)" }, { "id": "npm", "kind": "node", "package": "@scope/my-package", "label": "Install via npm" } ] } }
---
```

**Field Details:**

| Field | Purpose | Notes |
|-------|---------|-------|
| `name` | Skill identifier | Lowercase, hyphens, matches folder name |
| `description` | Trigger matching | NOT marketing — use words users actually type |
| `version` | Semver | For ClawHub versioning |
| `metadata.openclaw.requires.bins` | Required binaries (ALL must exist) | Checked on host at load time |
| `metadata.openclaw.requires.binsOneOf` | Required binaries (at least ONE) | For alternate toolchains |
| `metadata.openclaw.requires.env` | Required env vars | Skill won't load if missing |
| `metadata.openclaw.requires.config` | Required config flags | From openclaw.json |
| `metadata.openclaw.primaryEnv` | Main credential env var | For UI display |
| `metadata.openclaw.alwaysActive` | Skip install requirement | Always eligible |
| `metadata.openclaw.os` | Platform filter | `darwin`, `linux`, `win32` |
| `metadata.openclaw.emoji` | Visual indicator | Shown when skill activates |
| `metadata.openclaw.install` | Installer specs | brew/node/go/uv/download |

**CRITICAL:** Metadata must be single-line JSON. Multi-line YAML objects break the parser.

**Aliases:** `metadata.clawdbot`, `metadata.clawdis`, and `metadata.openclaw` are all accepted.

## 3. Three-Tier Loading Architecture

OpenClaw uses progressive disclosure to minimize token cost:

**Tier 1 — Name Tag (always loaded, ~30-50 tokens/skill):**
- Session start: agent sees only `name` + `description` for all eligible skills
- Cost: 97 characters + field lengths per skill
- Agent decides relevance from this alone

**Tier 2 — Full Body (loaded on demand):**
- When agent determines skill is relevant to current task
- Reads complete SKILL.md body via `read` tool
- Should contain: common operations, overview, pointers to references
- **Target: under 500 lines**

**Tier 3 — Deep References (loaded only when needed):**
- Individual reference files read on-demand
- Table schemas, full API docs, channel lists, examples
- Can be thousands of lines across dozens of files
- Cost at idle: zero

**Design Implications:**
- Description is a trigger, not documentation — "when to use" goes here
- Body is an index, not a dump — points to references for depth
- Each piece of info lives in ONE place (body OR reference, never both)
- References organized by access pattern (what's needed together?)
- No secrets in files — reference env var names only

## 4. Body Writing Best Practices

**Description (Tier 1 — the trigger):**
```
GOOD: "Manage GitHub issues, PRs, repos. Webhook triggers. Workflow automation."
BAD:  "An advanced AI-powered GitHub integration solution leveraging..."
```
- Use nouns users actually type
- Include key verbs (manage, search, create, monitor)
- Describe the task, not the technology
- Test: would a coworker understand this in chat?

**Body Structure (Tier 2 — the index):**
```markdown
# Skill Name

## What It Does
[1-2 sentence summary]

## Quick Start
[Most common operation — agent can execute immediately]

## Operations
### [Operation Category 1]
- Brief description
- Key parameters
- Reference: `references/detailed-docs.md`

### [Operation Category 2]
...

## Guardrails
- What NOT to do
- Error handling
- When to ask for confirmation

## Reference Map
- `references/api-docs.md` — Full API documentation
- `references/schemas.md` — Data schemas and types
```

**Anti-Patterns:**
- Dumping entire API docs into body (use references)
- Putting "when to use" in body instead of description (body loads AFTER trigger)
- Duplicating content between body and references
- Including secrets or credentials
- Verbose instructions that could be concise

## 5. Reference Files

**Organization Principles:**
- One topic per file
- Group by access pattern (what's needed together?)
- Files over 100 lines: add table of contents
- Use `{baseDir}` to reference skill folder path

**Naming Convention:**
```
references/
├── api-endpoints.md      # Full API documentation
├── data-schemas.md        # Types, schemas, validation rules
├── error-handling.md      # Error codes, recovery procedures
├── examples.md            # Worked examples, common patterns
├── channel-config.md      # Integration-specific configuration
└── troubleshooting.md     # Known issues, debugging steps
```

**Cross-Referencing Between Files:**
```markdown
For API details, load `references/api-endpoints.md`.
For schema validation, see `references/data-schemas.md`.
```

## 6. Directory Structure Patterns

**Minimal Skill (simple tool):**
```
greeting/
└── SKILL.md
```

**Standard Skill (single integration):**
```
github/
├── SKILL.md
├── references/
│   └── api-patterns.md
└── README.md
```

**Complex Skill (multi-capability):**
```
k-deep-research/
├── SKILL.md
├── references/
│   ├── sourcing-strategies.md
│   ├── research-frameworks.md
│   ├── output-templates.md
│   ├── openclaw-architecture.md
│   ├── openclaw-skill-authoring.md
│   ├── autonomy-patterns.md
│   └── adversarial-analysis.md
├── scripts/
│   └── validate-report.sh
├── templates/
│   └── report-frontmatter.yaml
└── README.md
```

**Skill with Bundled Binary:**
```
my-tool/
├── SKILL.md
├── bins/
│   └── my-tool          # Auto-added to PATH
└── skill.json
```

## 7. ClawHub Registry

**ClawHub** = public skill registry (https://clawhub.ai / https://clawhub.com)
**OnlyCrabs** = SOUL.md registry (https://onlycrabs.ai)

**CLI Operations:**
```bash
# Search
clawhub search "github"

# Install
clawhub install <slug>

# Inspect without installing
clawhub inspect <slug>

# List installed
clawhub list

# Update all
clawhub update --all

# Publish
clawhub publish <path>

# Sync all
clawhub sync --all
```

**Install Location:** `./skills` under CWD (or configured workspace)

**Registry Features:**
- Versioned releases with changelogs + tags
- Vector search (OpenAI embeddings) instead of keyword-only
- Star + comment system
- Moderation hooks (admins/mods can curate)
- Security analysis (checks declared vs actual behavior)

**ClawHavoc Incident (February 2026):**
- 341 malicious skills found out of 2,857 audited
- Attack patterns: credential theft, malware, data exfiltration
- Mitigations: read skills before enabling, sandbox untrusted, check metadata

## 8. Security Model

**Treat skills as untrusted code.** Always.

**Before Installing Community Skills:**
1. Read SKILL.md completely
2. Skim any scripts for remote downloads, suspicious commands
3. Check metadata declarations match actual behavior
4. Verify author reputation and maintenance history
5. Test in sandboxed environment first

**Metadata Mismatch Detection:**
ClawHub's security analysis checks that frontmatter declarations match actual skill behavior.
If code references `API_KEY` but frontmatter doesn't declare it under `requires.env`, it flags.

**Principle of Least Privilege:**
- Approve only permissions the skill actually needs
- Reject skills requesting unnecessary scope
- Use `ask:always` for side-effects

**Environment Variable Injection:**
- `skills.entries.*.env` and `skills.entries.*.apiKey` inject into host process for agent turn
- Scoped to agent run, not global shell
- Original environment restored after run

## 9. Testing & Validation

**Pre-Flight Checklist:**
- [ ] SKILL.md parses without frontmatter errors
- [ ] Description matches user language (trigger test)
- [ ] Required bins exist on target system
- [ ] Required env vars are set
- [ ] Simple task works from body alone
- [ ] References load correctly when needed
- [ ] No secrets in any files
- [ ] Scripts tested and verified

**Debugging Protocol:**
1. Reproduce: run same input with debug logging
2. Classify: permission, dependency, config, or logic failure
3. Isolate: disable optional steps, test smallest failing unit
4. Confirm: one fix at a time, re-run same test
5. Document: write cause/fix into SKILL.md guardrails

**Session Snapshot Gotcha:**
OpenClaw snapshots skills when session starts. Config changes may need new session.
Skills watcher can hot-reload, but test this explicitly.

## 10. Multi-Agent Skill Sharing

**Scope Rules:**
- Workspace skills (`<workspace>/skills`): per-agent only
- Managed skills (`~/.openclaw/skills`): shared across all agents on machine
- Extra dirs (`skills.load.extraDirs`): lowest precedence, good for shared packs
- Bundled skills: shipped with OpenClaw

**Precedence (highest → lowest):**
```
<workspace>/skills → ~/.openclaw/skills → bundled skills
```

**Multi-Agent Research Pattern:**
- Shared research skill in `~/.openclaw/skills/k-deep-research/`
- Agent-specific configs in workspace (topic focus, output preferences)
- Shared memory via common memory plugin
- Sub-agents inherit shared skills

## 11. Skill Evaluation Framework

When evaluating any community skill, score across four layers:

**Layer 1 — Spec Clarity:**
- Does SKILL.md clearly describe input/output/requirements/boundaries?
- Can a new user run minimal workflow in 5 minutes?

**Layer 2 — Execution Reliability:**
- Does it do what it claims?
- Gap between promise and outcome?
- Edge case handling?

**Layer 3 — Maintenance Signal:**
- Update frequency, issue resolution, version history
- Does maintainer document breaking changes?
- Is it alive or frozen?

**Layer 4 — Security Posture:**
- Least privilege? Only requests needed permissions?
- Metadata matches actual behavior?
- No hidden network calls or filesystem access?

**Fail ANY layer → drop from consideration.**
**Pass all four → candidate for adoption.**

---

## Quick Reference: File Types Accepted by ClawHub

Only text-based files accepted by publish:
- Markdown (.md)
- JSON, YAML, TOML
- JavaScript, TypeScript
- SVG
- Shell scripts
- Content types starting with `text/`

Binary files, images, and compiled code cannot be published to ClawHub.
