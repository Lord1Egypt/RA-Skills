---
name: init-project-structure
description: "Use when starting a new project from scratch and the user wants the full plan/build/recap/document workflow scaffolded. Creates slim CLAUDE.md, gitignored CLAUDE.local.md, docs/ tree with plans/recaps, TECHNICAL-DOCUMENTATION.md, FUNCTIONAL-SPECIFICATIONS.md, and housekeeping protocol. Asks 2-env vs 3-env topology. Skip for projects that just need slim memory without contracts — use slim-claude-md instead."
version: 2.0.0
author: Alejandro Del Villar
license: MIT
metadata:
  hermes:
    tags: [project-management, project-init, claude-md, documentation, scaffolding]
    related_skills: [slim-claude-md, draft-feature-plan, session-warmup, session-wrapup]
---

# Init Project Structure

Scaffold a brand-new project with the full structured methodology — slim CLAUDE.md, gitignored CLAUDE.local.md, docs/ tree, plans and recaps directories, plus top-level contract docs.

## When to Use

- Starting a new project from scratch
- User wants the plan/build/recap/document cycle working from day one
- Project needs formal contracts (TECHNICAL-DOCUMENTATION.md, FUNCTIONAL-SPECIFICATIONS.md)

## When to Skip (Use slim-claude-md Instead)

- Solo work, prototypes, libraries that don't need formal contracts
- Projects that just need slim memory without the plan/recap overhead

## What This Skill Produces

- **`CLAUDE.md`** — slim router (≤ 300 lines) with hard rules, branch topology, pointer index, common commands, today's state, contracts table, housekeeping protocol, session protocol
- **`CLAUDE.local.md`** — gitignored env file with section headers and `<paste-here>` placeholders
- **`.gitignore`** — entry for `CLAUDE.local.md` (creates `.gitignore` conservatively if absent)
- **`docs/`** tree: `architecture/`, `features/`, `plans/`, `recaps/`, plus optional `pipeline/` and `scripts/`
- **`docs/plans/README.md`** — explains the plan-as-contract convention
- **`TECHNICAL-DOCUMENTATION.md`** — top-level developer-onboarding contract with section scaffolding
- **`FUNCTIONAL-SPECIFICATIONS.md`** — top-level user-flow contract with section scaffolding
- **`docs/STATE-SNAPSHOT.md`**, **`docs/BUSINESS-CONTEXT.md`**, **`docs/TROUBLESHOOTING.md`** — empty stubs with headers

## Composes with slim-claude-md

This skill **uses** `slim-claude-md` templates as its foundation for CLAUDE.md and CLAUDE.local.md structure. Don't duplicate that work. Read templates from the `slim-claude-md` skill's `references/` directory and substitute placeholders, then layer the contract-doc additions.

## Resource Files

| File | When to read |
|------|--------------|
| `slim-claude-md/references/CLAUDE.md.template` | Always — base for project CLAUDE.md |
| `slim-claude-md/references/CLAUDE.local.md.template` | Always — base for project CLAUDE.local.md |
| `slim-claude-md/references/housekeeping-protocol.md` | Always — inlined into CLAUDE.md |
| `references/CLAUDE-template-simple.md` | When user picks 2-env topology |
| `references/CLAUDE-template-full.md` | When user picks 3-env topology |
| `references/TECHNICAL-DOCUMENTATION-template.md` | Always |
| `references/FUNCTIONAL-SPECIFICATIONS-template.md` | Always |
| `references/docs-plans-README-template.md` | Always — written into `docs/plans/README.md` |

---

## Workflow

### 1. Pre-flight checks

```bash
[ -f CLAUDE.md ] && wc -l CLAUDE.md && echo "WARNING: CLAUDE.md already exists" || echo "OK: no CLAUDE.md"
[ -f TECHNICAL-DOCUMENTATION.md ] && echo "WARNING: TECHNICAL-DOCUMENTATION.md already exists" || echo "OK"
[ -f FUNCTIONAL-SPECIFICATIONS.md ] && echo "WARNING: FUNCTIONAL-SPECIFICATIONS.md already exists" || echo "OK"
[ -d .git ] && echo "OK: git repo" || echo "WARNING: not a git repo yet"
```

If any of those exist, **stop** and ask the user whether to overwrite or abort. Never silently overwrite.

**Important — detect existing-code projects with no CLAUDE.md:** A project may have substantial code (1,000+ line files, existing API endpoints, working app) but no `CLAUDE.md` yet. In this case, the pre-flight check says "OK: no CLAUDE.md" but the project is NOT a greenfield startup. Check for existing code:

```bash
# Detect if project has substantial existing code
find . -name "*.py" -o -name "*.js" -o -name "*.ts" -o -name "*.tsx" | head -5 | wc -l
# If >0, this is an EXISTING codebase that needs structure, not a new project
```

If existing code is detected, **ask the user**: "This project already has code. Do you want to (a) scaffold the methodology around the existing codebase, or (b) treat this as a fresh start and archive the old code?" Default to (a) — the methodology should organize what exists, not replace it.

If `.git` is missing, ask whether to `git init` first or abort.

### 2. Gather project facts (one batched question)

Ask:

1. **Project name** (for H1 of CLAUDE.md and TECHNICAL-DOCUMENTATION.md title)
2. **One-line description** (for subtitle and FUNCTIONAL-SPECIFICATIONS.md intro)
3. **Production URL** (if any — leave blank if pre-launch)
4. **Repo URL** (GitHub/GitLab/etc.)
5. **Topology** — pick one of:
   - `simple` — 2 environments (`develop` local → `staging` → `main` production)
   - `full` — 3 environments (`develop` → `staging` → `canary` → `main`)
   - `single-branch` — solo project with just `main` (no separate env)
6. **Hosting platform** (Railway / Vercel / Fly / AWS / self-hosted / other)
7. **Stack** (e.g. "Next.js + Postgres + Redis" or "Python FastAPI + Postgres")
8. **Does this project have a data pipeline or many scripts?** (yes/no)
8. **Does this project have a data pipeline or many scripts?** (yes/no)
9. **Does this project depend on data from another project?** (yes/no) — If yes, specify the source project path and access pattern (e.g., "read-only Postgres role on same instance as `~/Projects/other-repo`"). The CLAUDE.md will get a "Data source" section and a hard rule about read-only access.

If the user wants defaults: `simple` topology, Railway hosting, generic Postgres stack, no pipeline, no scripts directory, no cross-repo dependency.

### 3. Create directory structure

```bash
mkdir -p docs/architecture docs/features docs/plans docs/recaps
# Conditionally:
mkdir -p docs/pipeline docs/scripts   # only if yes to pipeline/scripts
```

**Multi-app projects (API + mobile client):** If the project has both a backend API and a mobile (or separate frontend) app, organize them under `apps/`:

```
apps/api/           # Express / FastAPI / whatever backend
apps/mobile/        # React Native / Flutter mobile app
```

In this case, the methodology scaffolding (CLAUDE.md, docs/, contracts) lives at the repo root. Each app has its own `package.json` and dependency management. Do NOT use npm workspaces for the methodology files — the methodology is repo-level, not per-app. Workspaces can be added later if the apps share code.

**Native mobile apps (no production URL):** When the project has no web frontend, leave `{{PRODUCTION_URL}}` blank in the templates. The CLAUDE.md subtitle should not include a production URL line. The TECHNICAL-DOCUMENTATION.md should note "N/A — mobile app" in the deployment section.

### 4. Write CLAUDE.md

- Read `slim-claude-md/references/CLAUDE.md.template` as base.
- Read `references/CLAUDE-template-simple.md` or `references/CLAUDE-template-full.md` (or skip for `single-branch`) for topology-specific rules.
- Substitute placeholders: `{{PROJECT_NAME}}`, `{{ONE_LINE_DESCRIPTION}}`, `{{PRODUCTION_URL}}`, `{{REPO_URL}}`, `{{DEFAULT_BRANCH}}`, branch table rows.
- Inline housekeeping protocol from `slim-claude-md/references/housekeeping-protocol.md`.
- **Cross-repo dependency**: If the project depends on another project's data (question #9), add a "Data source" section after "Common commands" documenting the dependency, the access pattern (read-only), and a hard rule prohibiting schema changes or writes to that database. Reference the source project's CLAUDE.local.md for connection strings.
- Write to project root.
- **Must be ≤ 300 lines.** If it overshoots, the topology-specific rules block is too verbose — trim.

### 5. Write CLAUDE.local.md

- Read `slim-claude-md/references/CLAUDE.local.md.template`.
- Substitute branch/env structure based on topology pick.
- Leave actual secrets as `<paste-here>` — never invent values.
- Write to project root.

### 6. Update .gitignore

Add `CLAUDE.local.md` to `.gitignore`. If `.gitignore` doesn't exist, create it with that line plus standard ignores for the project's stack (`node_modules/`, `.next/`, `__pycache__/`, `target/`, etc.) — but be conservative and tell the user what was added.

**Pitfall — workspace version conflicts from scaffold boilerplate.** When scaffolding from `create-turbo` or similar generators, inspect every `packages/*/package.json` for version conflicts before writing the workspaces array as `"packages/*"`. A scaffolded `packages/ui/` may declare `"react": "^19.2.0"` which will conflict with your project's React 18 pin during `npm ci`. Even if the package is never imported, npm resolves ALL workspace packages' dependencies. Fix by either:

1. Deleting unused scaffold packages: `rm -rf packages/ui`
2. Explicitly listing workspace packages instead of using a wildcard:
   ```json
   "workspaces": [
     "apps/*",
     "packages/eslint-config",
     "packages/typescript-config"
   ]
   ```
   NOT `"packages/*"` — that picks up every directory in `packages/`, even scaffold boilerplate you'll never use.

After any workspace change, delete `node_modules` + `package-lock.json` and regenerate fresh. Then run the build locally before committing — `npm ci` is stricter than `npm install` about lockfile consistency. The project may already have a `.gitignore` (e.g., Python, Node, generated by a framework). Use `read_file` or `cat` to inspect it first, then append the `CLAUDE.local.md` line at the end. Do not blindly overwrite an existing `.gitignore` — you'll lose important exclusions. If the file already contains `CLAUDE.local.md`, skip this step.

**Pitfall — patch vs. overwrite.** When appending to an existing `.gitignore`, use `patch` (find the last line, append after it) rather than `write_file`. A full overwrite will destroy framework-generated exclusions (e.g., Python's `__pycache__/`, Node's `node_modules/`, generated docs). If you must use `write_file`, first read the entire file and include all existing content.

### 7. Write TECHNICAL-DOCUMENTATION.md

Read `references/TECHNICAL-DOCUMENTATION-template.md`, substitute project facts, write to project root. The template includes section scaffolding (Tech Stack, Architecture, Database Schema, API Reference, Auth, Scripts, Deployment) so the user fills in as the project grows. Each section is intentionally short and references the matching `docs/` file.

**Note on stateless projects:** If the project has no database (e.g., file-upload dashboards, static sites), the template's "Database Schema" section will say "N/A — stateless". This is correct — don't try to invent a schema.

### 8. Write FUNCTIONAL-SPECIFICATIONS.md

Read `references/FUNCTIONAL-SPECIFICATIONS-template.md`, substitute project facts, write to project root. Includes section scaffolding (Authentication, User Flows, Features, Admin, Edge Cases) with the same short-and-link approach.

### 9. Write docs/plans/README.md

Read `references/docs-plans-README-template.md`, write to `docs/plans/README.md`. Explains the plan-as-contract convention, the ISO date filename format (`YYYY-MM-DD-<slug>.md`), plan template structure, and how to use `draft-feature-plan`.

### 10. Write empty stubs

Create placeholder files so docs/ tree pointers in CLAUDE.md aren't broken:

- `docs/STATE-SNAPSHOT.md` — with header explaining it's empty until project has data
- `docs/BUSINESS-CONTEXT.md` — placeholder sections for founder context, target market, revenue model
- `docs/TROUBLESHOOTING.md` — placeholder header
- `docs/architecture/overview.md` — placeholder pointing at project stack and CLAUDE.md
- `.gitkeep` files in empty `docs/features/`, `docs/recaps/`, `docs/plans/`

**Pitfall — stale `docs/recaps/SESSION-RECAP-YYYY-MM-DD.md` pointer:** The base `CLAUDE.md.template` contains a literal placeholder path `docs/recaps/SESSION-RECAP-YYYY-MM-DD.md` in its "Where to find things" section. After you write the real `CLAUDE.md`, grep its pointers and confirm each exists. If this placeholder appears, either (a) remove it from the template before writing, or (b) note it as an expected MISS during verification — it is a template artifact, not a required file.

**Pitfall — `docs/scripts/README.md` for projects with standalone scripts:** If the project has scripts in the repo root (e.g., `.py` files alongside `run.py`), create `docs/scripts/README.md` with a table cataloging them. The user may not have mentioned "scripts" in the initial questions but the files are present. This prevents a broken pointer in CLAUDE.md's "Scripts" section.

### 11. Verify

```bash
wc -l CLAUDE.md                           # should be ≤ 300
git check-ignore -v CLAUDE.local.md       # should match .gitignore line
git status --short                        # CLAUDE.local.md must NOT appear
ls TECHNICAL-DOCUMENTATION.md FUNCTIONAL-SPECIFICATIONS.md
ls docs/plans/README.md

# Walk every docs/ pointer in new CLAUDE.md:
for f in $(grep -oE 'docs/[a-zA-Z0-9_/.-]+\.md' CLAUDE.md); do
  [ -e "$f" ] && echo "OK   $f" || echo "MISS $f"
done
```

**Expected MISS:** `docs/recaps/SESSION-RECAP-YYYY-MM-DD.md` is a literal template placeholder, not a real file. All other MISS lines indicate a bug — fix before handing off.

### 12. Hand off

Tell the user:

- "Project structure scaffolded. CLAUDE.local.md is gitignored and has placeholder sections — fill in actual credentials before any DB or API work."
- "TECHNICAL-DOCUMENTATION.md and FUNCTIONAL-SPECIFICATIONS.md are scaffolded with empty sections. Update them as features ship — the recap workflow will prompt for it."
- "Plans live in `docs/plans/` with ISO date filenames. Use `/plan-feature` (or `draft-feature-plan` skill) before significant work."
- "Recaps live in `docs/recaps/` with ISO date filenames. Use `/recap` (or `write-session-recap` skill) at the end of each session."
- "Don't commit yet — review the scaffold first."

**Do NOT commit.** The user owns the first commit on a new project.

---

## Things to Avoid

1. **Do not invent project facts.** If the user doesn't answer a question, use the documented default.
2. **Do not write any real secrets** in any tracked file. `CLAUDE.local.md` only, and it must be gitignored before writing.
3. **Do not pre-fill TECHNICAL-DOCUMENTATION.md or FUNCTIONAL-SPECIFICATIONS.md with hypothetical content.** Leave sections as scaffolding with `<add-when-implemented>` markers.
4. **Do not create `docs/pipeline/` or `docs/scripts/`** unless the user said the project has those.
5. **Do not set up hooks, GitHub Actions, or CI.** Out of scope.
6. **Do not commit or push.** Always.
7. **Do not assume the project is a specific stack.** Read the user's stack answer and adapt headers accordingly. A Python FastAPI project shouldn't get `prisma migrate` commands.

## Verification Checklist

- [ ] CLAUDE.md written at project root, ≤ 300 lines
- [ ] CLAUDE.local.md written at project root, gitignored
- [ ] `git check-ignore -v CLAUDE.local.md` matches `.gitignore` line
- [ ] `git status --short` does NOT show CLAUDE.local.md
- [ ] `docs/` tree created: architecture/, features/, plans/, recaps/
- [ ] `docs/pipeline/` and `docs/scripts/` only if user confirmed
- [ ] TECHNICAL-DOCUMENTATION.md written at project root
- [ ] FUNCTIONAL-SPECIFICATIONS.md written at project root
- [ ] docs/plans/README.md written
- [ ] All docs/ pointers in CLAUDE.md resolve to existing files
- [ ] Empty stubs created: STATE-SNAPSHOT.md, BUSINESS-CONTEXT.md, TROUBLESHOOTING.md, architecture/overview.md
- [ ] .gitkeep files in empty directories
- [ ] If cross-repo dependency: CLAUDE.md has "Data source" section with read-only hard rule, and CLAUDE.local.md has placeholder for the source's connection string reference
- [ ] If cross-repo dependency: CLAUDE.md has "Data source" section with read-only hard rule, and CLAUDE.local.md has `<!-- reference-source-here -->` placeholder
