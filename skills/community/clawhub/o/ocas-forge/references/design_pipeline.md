# Design Pipeline

The mandatory pipeline Forge runs before writing any files. Seven phases total.

## Phase 1: Existence Gate (HARD GATE — must pass all 3 checks before proceeding)

### Check A — Parent search (mandatory first step)
Call `skills_list` to enumerate all existing skills. For each skill whose domain overlaps the proposed capability, call `skill_view` to read its full content. Ask: "Does this existing skill already own this domain?" If yes → **STOP. Do not create a new skill.** Add the content to the parent as a `references/` doc, `scripts/` file, or new SKILL.md section. Record the decision in `decisions.jsonl`.

### Check B — Standalone test (all 3 must be true)
A new skill is only justified if it has: (a) its own independent invocation path (user or cron triggers it directly by name), (b) its own cron jobs or background tasks, AND (c) its own journal output. If any of these is missing → it's a support file, not a skill. Absorb into parent.

### Check C — Absorption test
Can this content fit as a `references/<topic>.md` or `scripts/<name>.py` inside an existing skill? If yes → **absorb, don't spawn.** Creating a standalone skill for content that fits in a reference file is the #1 cause of skill proliferation. Default to absorption.

**Only proceed to phase 2 if all 3 checks pass.** If the answer is "absorb," execute the absorption immediately: add the content to the parent skill's appropriate subdirectory, update the parent's reference table, and record the decision.

## Phase 1.5: Research (MANDATORY before Classify — applies to ALL forge operations including improvements)

**Trigger:** Phase 1 passed — no local parent owns the domain. Before classifying and scoping a new skill, research whether the capability already exists externally.

**For improvements/updates:** Research is NOT optional just because the skill already exists. When asked to "improve" a skill, you MUST still search external sources (GitHub, arxiv, skill registries, community patterns) to find new taxonomies, patterns, and techniques the skill doesn't yet cover. The user will call it out if you skip.

**Goal:** Avoid building what already exists. Understand existing approaches, synthesize the best patterns, build something better. A skill that duplicates an existing GitHub repo or published skill package without adding value is waste.

### Step A — Skill Library Search (FIRST — skills often backed by GitHub repos)

Search the OCAS skill library and other skill registries for packages that cover the proposed domain. These repos often have associated GitHub repos you can deep-read in Step B.

**Sources (in priority order):**

1. **Local OCAS skills** — `skills_list` + `skill_view` for any `ocas-*` skill with domain overlap
2. **GitHub OCAS repos** — `gh search repos "ocas-* user:<agent-handle>" --json fullName,description,url`
3. **AgentSkill.sh** — `agentskill search <keywords>` (already installed)
4. **SkillsMP** — API: https://skillsmp.com/docs/api (key below)
5. **LobeHub** — `lobehub search <keywords>` (see https://lobehub.com/cli)
6. **Skills.sh** — API: https://www.skills.sh/docs/api
7. **OpenClaw ClawHub** — `clawhub search <keywords>` (see https://docs.openclaw.ai/clawhub/cli)

**API keys (load on demand, do not hardcode in scripts):**
- SkillsMP: load from config or prompt user if needed

For each skill found, note: name, description, how it works (architecture), what patterns it uses, and what the new skill can learn from it.

### Step B — GitHub Search (via `gh` CLI, NEVER browser search)

Search GitHub for repos that solve the proposed capability. Use `gh search repos` with multiple query variants for broad coverage:

```bash
# Primary search with the capability name / key terms
gh search repos "<capability keywords>" --sort stars --limit 10 --json fullName,description,url,stargazersCount,language,updatedAt

# Secondary search with alternative terms
gh search repos "<alternative keywords>" --sort stars --limit 5 --json fullName,description,url,stargazersCount,language,updatedAt
```

**Selection criteria:** Pick top 10 repos by relevance + stars. Prioritize:
- Updated within last 6 months (active maintenance)
- ≥10 stars (community validation)
- Direct domain overlap (not tangential)
- **Also include GitHub repos discovered in Step A** (skill library entries often link to their source repos)

### Step C — Deep-read repos and skills (via `gh` API + skill_view, NEVER browser)

For each selected repo, fetch structure and key files using `gh api`:

```bash
# Get repo README
gh api repos/{owner}/{repo}/readme --jq '.content' | base64 -d

# Get top-level file structure
gh api repos/{owner}/{repo}/git/trees/main?recursive=1 --jq '.tree[].path' 2>/dev/null || \
gh api repos/{owner}/{repo}/git/trees/master?recursive=1 --jq '.tree[].path'

# Fetch key source files for comparison (limit to 5-8 files per repo)
gh api repos/{owner}/{repo}/contents/{path} --jq '.content' | base64 -d
```

For skills found in Step A, use `skill_view` to read full content including references and scripts.

**What to read:** README, main entry point, core logic files, package.json/pyproject.toml/setup.py for dependencies. Do NOT browser-scrape. Do NOT clone to disk. Use `gh api` exclusively.

### Step D — Compare, Synthesize, and Decide

For each repo/skill, assess on three axes:

| Axis | Question |
|------|----------|
| **Coverage** | Does this repo/skill solve ≥80% of the proposed capability? |
| **Quality** | Is it actively maintained, well-documented, production-ready? |
| **Compatibility** | Can it be wrapped/integrated into an OCAS skill cleanly? (license, language, dependencies) |

**Decision matrix:**

- **≥80% coverage + high quality + compatible** → **WRAP, don't build.** Create the new skill as a thin wrapper/adapter around the existing repo. Credit the source in the skill's `references/` and frontmatter.
- **50-80% coverage** → **Fork/adapt.** Use the repo as a foundation, extend it for the remaining gap. Credit the source.
- **<50% coverage OR incompatible license OR unmaintained** → **Build fresh.** Proceed to Phase 2. Record why existing repos were insufficient.
- **Multiple partial solutions** → **SYNTHESIZE.** This is the most common and most valuable path. Take the best patterns from multiple sources:
  - Architecture from repo A (e.g., the plugin system)
  - Error handling from repo B (e.g., retry + circuit breaker pattern)
  - CLI interface from repo C (e.g., argument parsing + help text conventions)
  - Testing patterns from repo D (e.g., fixture structure, mock strategies)
  - Configuration handling from a skill in the library
  - Combine, restructure, and improve. The result should be greater than the sum of its parts. Credit ALL sources in `references/attribution.md` and frontmatter.

**Synthesis rules:**
1. Every borrowed pattern must be adapted to OCAS conventions — don't copy verbatim, make it native
2. If a pattern is better than what you'd build from scratch, use it — don't reinvent for pride
3. If a pattern is worse than what you'd do, skip it — don't inherit bad design
4. The NEW skill must be a coherent whole, not a Frankenstein — internal consistency matters more than source diversity
5. If you synthesize from ≥3 sources, the result must be meaningfully different from any single source

**Record all findings** in `decisions.jsonl`: which repos/skills were reviewed, their scores, what was borrowed from each, and the final decision (wrap/fork/build/synthesize). This prevents re-researching the same items on future builds.

**Research is complete when:** At least 10 repos/skills have been reviewed OR the search conclusively shows no adequate existing solution. Proceed to Phase 2.

## Phase 2: Classify
Shortcut, workflow, or system?

## Phase 3: Scope
Exact job, explicit non-goals, smallest useful promise.

## Phase 4: Architecture
What goes in SKILL.md vs references vs scripts vs assets?

## Phase 5: Plan
Map the implementation: file structure, dependencies, inter-skill interfaces, cron jobs, journal outputs. Plan before writing.

**Skilllab compliance pre-check (run during Plan, before Build):**
Before writing any files, verify the planned output against skilllab's 10-dimension rubric. Address ALL of the following in the plan:

| Dim | Requirement | Verify |
|-----|-------------|--------|
| D1 | Frontmatter: `name` (lowercase-hyphens, 1-64 chars, matches dir), `description` (1-1024 chars), `license` top-level, `includes:` if refs/scripts exist, `metadata.hermes.tags` + `category`, `triggers:` present | Frontmatter will parse and pass agentskills.io spec |
| D2 | Description follows `[What] [When] [Keywords]. NOT for [Exclusions]` formula. Third-person imperative. Under 1024 chars. | Description triggers correctly, no false activation |
| D3 | SKILL.md body under 500 lines / 5000 tokens. Code ratio <20% (code lines / total lines). No unnecessary background explanations. | Plan splits content: SKILL.md = overview, details in `references/` |
| D4 | Three-layer architecture: metadata → SKILL.md → references. Support file map with "When to read" column. File refs one level deep. Descriptive file names. | Plan includes support file map with conditional triggers |
| D5 | Steps clear, sequential, unambiguous. Checklists (`- [ ]`) for multi-step workflows. Consistent terminology. Concrete examples. | Plan has checklists for any 3+ step procedure |
| D6 | Fragile operations: exact commands. Flexible tasks: direction + defaults. "Why" explained for rigid rules. | Plan marks which instructions are rigid vs flexible, includes "why" |
| D7 | Error handling section or table. Scripts: `--help`, structured output, meaningful exit codes, no interactive prompts. | Plan includes error handling guidance |
| D8 | Progressive disclosure: SKILL.md = navigation, references = detail. Support file map uses conditional language ("Before X", "When Y"). | Every reference file has a conditional trigger in the map |
| D9 | Scripts: self-contained, `--help` with usage/flags/examples, JSON/CSV stdout, exit codes, idempotent where possible, `--dry-run` for destructive ops. | Plan includes script design meeting D9 |
| D10 | All description capabilities covered. Gotchas/Pitfalls section present. Scope is coherent. Procedures generalize. | Plan includes gotchas section |

**If any dimension cannot be met**, adjust the plan before building. Do NOT skip and plan to fix later.

## Phase 6: Build
Write all files according to the plan. Re-check D1 frontmatter and D4 support file map as you write — drift between plan and execution is the #1 cause of post-build skilllab fixes.

## Phase 7: Validate
Routing, structural, usefulness checks.

See `references/package_patterns.md` for package shape guidance and `references/authoring_rules.md` for full authoring standards.