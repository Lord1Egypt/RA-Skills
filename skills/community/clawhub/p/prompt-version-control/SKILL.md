---
name: Prompt Version Control
slug: prompt-version-control
description: Git-like version control for AI prompts: track changes, A/B test variants, measure metrics, rollback with confidence.
tags: [prompt-engineering, version-control, ab-testing, llm, dev-tools, git]
version: 1.0.0
license: MIT-0
---

# Prompt Version Control (Prompt 版本控制器)

Git-inspired version control system for AI prompts. Track every edit, run A/B tests, measure quality metrics, and rollback instantly — treat your prompts like code.

## Core Capabilities

- **Version tracking**: Every prompt change auto-commits with semantic versioning (major.minor.patch)
- **A/B testing**: Run v1 vs v2 side-by-side, measure response quality, latency, and token cost
- **Diff engine**: Compare prompt versions with semantic-aware diffs (not just text)
- **Rollback**: Instantly revert to any previous version with full history preservation
- **Remote sync**: Push/pull prompts to GitHub/GitLab for team collaboration
- **Metrics dashboard**: Track improvement/degradation trends across versions
- **Conflict resolution**: Merge divergent prompt branches with structured conflict markers

## Workflow (9 Steps)

### Step 1: Initialize Prompt Repository
**Input**: `prompt init [directory]` — user runs init command in a project or empty directory.
**Output**: Creates `.prompt/` directory structure:
```
.prompt/
  config.yaml      # repo settings, LLM provider config, test dataset path
  prompts/         # individual prompt files
  history/         # version history (git-compatible)
  metrics/         # A/B test results
  branches/        # branch references
```
**Logic**: Auto-detect if already inside a git repo; if so, integrate `.prompt/` as a subdirectory. Generate initial `config.yaml` with sensible defaults. Prompt user for LLM API key if not in environment.

### Step 2: Register a New Prompt
**Input**: `prompt add <name> [--template <type>] [--description "..."]`
**Output**: Creates `prompts/<name>.yaml` with metadata and initial version v0.1.0.

```yaml
name: customer-support-classifier
version: 0.1.0
description: Classify customer inquiries into 5 categories
model: gpt-4
temperature: 0.3
system: |
  You are a customer support classifier...
user_template: |
  {{query}}
variables:
  - name: query
    type: string
    required: true
test_cases:
  - input: "Where is my order #12345?"
    expected_category: "order_status"
metrics:
  quality_score: null
  avg_latency_ms: null
  avg_tokens: null
```

**Logic**: Templates include `chat`, `classifier`, `generator`, `extractor`, `custom`. Auto-extract variables from `{{...}}` patterns.

### Step 3: Edit and Auto-Version
**Input**: User edits `prompts/<name>.yaml` directly or via `prompt edit <name>`.
**Output**: On save, auto-increments version:
- **Patch bump** (0.1.0 → 0.1.1): wording changes, examples, minor parameter tweaks
- **Minor bump** (0.1.0 → 0.2.0): new variables, restructured prompt, changed model
- **Major bump** (0.1.0 → 1.0.0): fundamentally different approach, breaking output format change

**Logic**: LLM-assisted semantic diff determines bump magnitude. User can override: `prompt edit <name> --bump major`.

### Step 4: Run A/B Test
**Input**: `prompt test <name>` — runs the current version against the previous version.
**Action**:
1. Load test cases from `test_cases` in the prompt YAML
2. Send each test case to both prompt versions
3. Collect responses and compute metrics

**Output**: A/B comparison table.

| Test Case | Metric | v0.1.2 | v0.1.3 | Δ |
|-----------|--------|--------|--------|---|
| order_status | Quality (1-10) | 8.2 | 9.1 | +0.9 ⬆ |
| order_status | Latency (ms) | 1240 | 1180 | -60 ⬇ |
| order_status | Tokens | 340 | 312 | -28 ⬇ |
| refund_request | Quality | 7.5 | 7.3 | -0.2 ⬇ |
| ... | ... | ... | ... | ... |
| **Overall Quality** | | **7.9** | **8.0** | **+0.1** |

**Logic**: Quality scoring uses LLM-as-judge with predefined rubrics. Statistical significance check (p < 0.05) when ≥20 test cases. Flag degradation in red.

### Step 5: Diff Two Versions
**Input**: `prompt diff <name> v0.1.2 v0.1.3`
**Output**: Semantic-aware diff highlighting:
- **Text changes**: Standard line diff with context
- **Structural changes**: Added/removed variables, parameter changes
- **Intent changes**: LLM-summarized description of what changed and why it matters

```
--- customer-support-classifier v0.1.2
+++ customer-support-classifier v0.1.3
@@ system @@
- You are a helpful customer support classifier.
+ You are an expert customer support triage agent with 10 years of experience.

@@ variables @@
+ added: priority_level (enum: low, medium, high, urgent)

Summary: Added urgency classification dimension and elevated persona specificity.
```

### Step 6: View Version History
**Input**: `prompt log <name> [--limit N]`
**Output**: Git-log-style history with metrics overlay.

```
v0.3.0 (2026-06-15)  Alice  Added priority classification, bumped to gpt-4o
v0.2.1 (2026-06-12)  Bob    Fixed edge case: empty query → graceful fallback
v0.2.0 (2026-06-10)  Alice  Added examples for refund flow
v0.1.0 (2026-06-01)  Alice  Initial prompt
---
Quality trend: ████▌ 7.2 → 7.9 → 8.4 → 9.1
```

### Step 7: Rollback
**Input**: `prompt rollback <name> --to v0.2.1`
**Output**: Restores v0.2.1 as current working version, creates a new commit marking the rollback.
**Logic**: Rollback is itself a versioned action (bumps patch). History is never destroyed. `prompt rollback <name> --undo` to return to pre-rollback state.

### Step 8: Remote Sync
**Input**: `prompt push [--remote origin]` / `prompt pull`
**Output**: Syncs `.prompt/` to/from configured remote (GitHub/GitLab).
**Logic**: Standard git push/pull under the hood. Merge conflicts surfaced with structured markers for manual resolution. `prompt merge --tool` opens interactive merge UI.

### Step 9: Generate Iteration Report
**Input**: `prompt report <name> [--from v0.1.0] [--format markdown|html]`
**Output**: Full version history report with:
- Version timeline (Mermaid chart)
- Quality score trend (sparkline)
- Token cost trend
- Top 3 most impactful changes (by quality delta)
- Regression alerts

## Sample Prompts

### Prompt 1: Initialize and First Prompt
**User**: `prompt init ./my-prompts && prompt add email-generator --template generator --description "Generate marketing emails"`
**Expected Output**: Repository created, first prompt registered at v0.1.0.

### Prompt 2: A/B Test
**User**: `prompt test email-generator`
**Expected Output**: Side-by-side comparison of current vs previous version across all test cases, with overall quality delta.

### Prompt 3: Rollback After Degradation
**User**: `prompt rollback email-generator --to v1.2.0`
**Expected Output**: v1.2.0 restored as working version, commit logged. "Rolled back from v1.3.1 to v1.2.0 (quality dropped 12% in v1.3.0)".

### Prompt 4: Diff Understanding
**User**: `prompt diff email-generator v1.2.0 v1.3.0`
**Expected Output**: Semantic diff with text changes, structural changes, and LLM-generated summary of what changed.

### Prompt 5: Team Collaboration
**User**: `prompt push` (after editing prompts locally) then `prompt pull` (on teammate's machine)
**Expected Output**: Remote sync with conflict markers if both edited same prompt.

### Prompt 6: Full Report
**User**: `prompt report email-generator --from v0.1.0 --format markdown`
**Expected Output**: Complete iteration history with quality/cost trends and top-impact changes.

## Real Task Examples

### Example 1: Solo Developer Iterating
**Scenario**: Developer building a customer-facing chatbot, iterating the system prompt daily.
**Input**: Series of `prompt edit` sessions over 2 weeks, with periodic `prompt test` runs.
**Steps**:
1. `prompt init` → repo created
2. `prompt add chatbot --template chat` → v0.1.0
3. Edit 5 times over week 1 → versions 0.1.1 through 0.3.0
4. `prompt test chatbot` → discovers v0.2.1 had best quality (9.2)
5. `prompt rollback chatbot --to v0.2.1` → restores best version
6. Continue iterating from v0.2.1 → v0.4.0 surpasses old best
7. `prompt report chatbot` → shows quality journey: "V-shaped recovery after rollback"
**Output**: 14 versions tracked, best version identified, recovery path documented.

### Example 2: Team Prompt Collaboration
**Scenario**: 3-person AI team managing 50+ prompts for a product.
**Input**: Multiple team members editing prompts, pushing/pulling.
**Steps**:
1. Alice: `prompt init` + `prompt add pricing-prompt` → pushes to GitHub
2. Bob: `prompt pull` → gets pricing-prompt v0.1.0
3. Alice edits → v0.2.0, Bob edits → v0.2.0-bob (branch)
4. `prompt push` from both → merge conflict detected
5. `prompt merge --tool` → interactive resolution showing both versions side-by-side
6. Resolved → v0.3.0 on main
7. `prompt test pricing-prompt` → validates merged version
**Output**: Conflict resolved, merged version tested, team workflow established.

### Example 3: Production Rollback Emergency
**Scenario**: Production chatbot quality suddenly drops after latest prompt deploy.
**Input**: Alert from monitoring: user satisfaction down 15%.
**Steps**:
1. `prompt log chatbot --limit 3` → identifies v2.4.0 as latest deploy
2. `prompt diff chatbot v2.3.0 v2.4.0` → shows new "be more concise" instruction caused incomplete answers
3. `prompt rollback chatbot --to v2.3.0` → instant revert
4. Verification: quality metrics return to baseline within minutes
5. Post-mortem: `prompt report chatbot --from v2.3.0` documents the incident
**Output**: Rollback completed in <1 minute. Incident documented for team review.

## 🚀 First-Success Path (3 Steps)

1. **Step 1**: Run `prompt init ./my-prompts && prompt add hello --template chat`
2. **Step 2**: Edit the prompt, then run `prompt log hello` to see your first version
3. **Step 3**: Edit again, run `prompt diff hello v0.1.0 v0.2.0` — see your changes tracked instantly

## Boundary Conditions

| Condition | Behavior |
|-----------|----------|
| Prompt file deleted manually | Detect in next `prompt log`, offer recovery from `.prompt/history/` |
| Concurrent edits (team) | Merge conflict on push; structured markers for resolution |
| Empty test_cases | Warn; A/B test requires ≥1 test case, proceed with manual review mode |
| LLM API key missing | Test commands fail gracefully; editing/log/diff still work |
| Large repository (>500 prompts) | Pagination on `prompt log --all`; recommend splitting into sub-repos |
| Git remote not configured | `prompt push` prompts to set remote URL |
| Model change (gpt-4 → gpt-4o) | Auto-detected as minor bump; flag in diff as "model change" |
| Binary/incompatible changes | Warn if output schema changes; recommend major version bump |

## Error Handling

| Error Code | Scenario | Handling |
|-----------|----------|----------|
| E-NOT-INIT | Command run outside a prompt repo | "No prompt repo found. Run `prompt init` first." |
| E-PROMPT-NOT-FOUND | Referenced prompt name doesn't exist | Show similar prompt names (Levenshtein distance) |
| E-VERSION-NOT-FOUND | Referenced version doesn't exist | Show available versions for that prompt |
| E-MERGE-CONFLICT | Push/pull conflict detected | Show conflicting sections, offer `prompt merge --tool` |
| E-API-FAIL | LLM API call fails during test | Skip failed test case, report in results, don't block remaining |
| E-TEST-INSUFFICIENT | A/B test with <10 test cases | Show results but flag low confidence |

## Security Requirements

- **API key storage**: Store in environment variables or OS keychain only; never in `.prompt/config.yaml` or git history
- **Prompt content privacy**: Prompt files may contain proprietary business logic; respect `.gitignore` patterns
- **Team access control**: Remote sync via standard git permissions; no additional auth layer
- **Production data safety**: Test cases should use synthetic or anonymized data; never real user data in version control
- **Audit trail**: All version changes are immutable and attributed; no history rewriting

---

## Implementation

### Project Structure

| File | Purpose |
|------|---------|
| `SKILL.md` | Full design document (this file) |
| `skill.json` | Skill metadata with script/schema references |
| `scripts/prompt-vc.sh` | **Main CLI script** — implements all workflow steps |
| `schemas/input.schema.json` | JSON Schema for prompt YAML files |
| `schemas/output.schema.json` | JSON Schema for test results / diff / log output |
| `references/config.yaml` | Default `.prompt/config.yaml` template |

### CLI Usage

```bash
# Initialise repository
./scripts/prompt-vc.sh init ./my-prompts

# Add a prompt with a template
./scripts/prompt-vc.sh add email-generator --template generator

# Edit (opens $EDITOR)
./scripts/prompt-vc.sh edit email-generator

# Diff two versions
./scripts/prompt-vc.sh diff email-generator v0.1.0 v0.2.0

# View version history
./scripts/prompt-vc.sh log email-generator

# Run A/B test
./scripts/prompt-vc.sh test email-generator

# Rollback
./scripts/prompt-vc.sh rollback email-generator --to v0.1.0

# Generate report
./scripts/prompt-vc.sh report email-generator
```

### Dependencies

- **bash** 4+ (macOS: modern bash via Homebrew, or use default system bash)
- **diff** (standard Unix utility)
- **python3** (optional — used for YAML parsing in test/report)
- **git** (optional — auto-detected for `.gitignore` integration)
- **$EDITOR** (defaults to `vi`; set `EDITOR` env var to customise)

All test output is simulated offline (no LLM API calls). The A/B test engine generates deterministic metrics based on prompt length to validate the CLI workflow without requiring API keys.
