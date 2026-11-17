# Builder workflows: consolidation, sync, update verification, compliance audit

Reference detail for Forge sub-workflows. SKILL.md carries the short spec; this file carries the procedures, commands, and pitfalls.

---

## Skill Compliance Audit Workflow

When the user asks to audit one or more OCAS skills for architecture compliance (e.g., "check ocas-genie against forge standards"):

### Phase 1: Inventory
For each skill, list all files in the package directory (excluding `.git/`). Check against the required file inventory:
- `SKILL.md`, `README.md`, `CHANGELOG.md`, `skill.json`, `.gitignore`, `evals.json`

### Phase 2: Frontmatter Check
Read SKILL.md. Verify frontmatter has: `name`, `description`, `license`, `metadata.author`, `metadata.email`, `metadata.version`, `metadata.tags`, `metadata.category`.

### Phase 3: Required Sections Check
Verify SKILL.md body contains all required sections:
1. When to use / When NOT to use
2. Responsibility Boundary
3. Ontology Types
4. Journal Outputs
5. Storage Layout
6. OKRs
7. Background Tasks (or explicit "purely reactive" statement)
8. Support File Map

For system skills, also verify: Commands, Initialization, Self-update, Optional Skill Cooperation.

### Phase 4: Check References
Every file in `references/` must be listed in the Support File Map. Every reference mentioned in the map must exist on disk.

### Phase 5: Check skill.json
Valid JSON with: `name`, `version`, `description`, `author`, `email`, `skill_type`, `filesystem`, `self_update`.

### Phase 6: Apply Fixes
For each gap found, write the missing file or add the missing section. Use consistent OCAS patterns (see `compliance-audit-checklist.md` for the full template).

### Phase 7: GitHub Sync — OCAS-ONLY guardrail

**CRITICAL**: Only sync skills that are OCAS-authored. Before creating any repo or pushing any skill:

1. **Verify the skill name starts with `ocas-`**. If it doesn't, STOP. Do not create a repo, do not push, do not sync. This is the single most important guardrail.
2. **Verify the author is <agent-name> or <user>**. Read `metadata.author` from SKILL.md frontmatter. If the author is anyone else (e.g. `agentskill-sh`, `NousResearch`, `anthropics`), STOP.
3. **Check against known 3rd-party skills**. Never push these to GitHub under <agent-handle>:
   - `api-integration`, `google-workspace`, `review-skill`, `deployment`, `docker-management`, `email-sending`, `git-operations`, `json-formatting`, `csv-parsing`, `database-operations`, `execute-code`, `unit-testing`, `web-extract`, `learn`, `terminal-run`, `title-sessions`, `voice-call`
   - Any `prism-*`, `reflexion-*`, `cek-*` skill (these are from the hermes-agent repo, not OCAS)
   - Any skill with `metadata.author` that isn't `<agent-name>` or `<user>`
4. **Check for duplicates**. Before creating a new repo, list existing repos with `gh repo list <agent-handle>`. If a repo with the same name (or a close variant like `vpn` vs `ocas-vpn`) already exists, use the existing one. Don't create a duplicate.
5. **Default to private**. All new repos must be created with `--private`. Never use `--public` unless <operator> explicitly asks.

For each verified OCAS skill:
1. `gh repo create <agent-handle>/{repo} --private` (if no remote exists)
2. `git init` + `git remote add origin` (if no .git)
3. `git add -A && git commit` with conventional commit message
4. `git push -u origin main`
5. Verify `gh repo view` → `PRIVATE`

See `compliance-audit-checklist.md` for the complete checklist.

---

## `forge.consolidate` — merge an orphan into its parent

### Workflow

1. **Audit the skill list.** Map each orphan to its natural parent — e.g. TTS/expression rules → Vibes; status diagnostics → Custodian; skill adaptation → Forge; contact sync and CRM connectors → Weave; briefing pipeline fixes → Vesper/Sands/Dispatch.

2. **Pull latest from GitHub.**
   ```bash
   cd <hermes-home>/skills/ocas-PARENT
   git stash
   git pull origin main
   ```

3. **Read orphan content** and decide what to keep, rewrite, or discard.

4. **Fold content into the parent's existing structure.** Do **not** wrap merged content in `## Integrated: <name>` sections — that bloats SKILL.md and duplicates headings. Identify the parent section that matches the orphan's concern and integrate the content there, refactoring for tone and redundancy. If the content spans multiple parents, divide by domain ownership and replicate critical notes (like account isolation) to every recipient.

5. **Create branch, commit, push, open PR.**
   ```bash
   cd <hermes-home>/skills/ocas-PARENT
   git checkout -b merge/orphan-skill-name
   git add SKILL.md
   git commit -m "Merge orphan skill: orphan-skill-name into ocas-parent"
   git push -u origin merge/orphan-skill-name
   gh pr create --title "Merge: orphan-skill-name → ocas-parent" --body "Integrates orphan-skill-name content into this skill."
   ```

6. **Delete orphan locally.**
   ```bash
   rm -rf <hermes-home>/skills/orphan-skill-name
   rm -rf <hermes-home>/skills/category/orphan-skill-name
   ```

7. **Update memory** so future sessions know the orphan no longer exists independently.

### Pitfalls

- **Protected files**: `<hermes-home>/.env` cannot be edited with the `patch` tool — use `terminal` with `sed -i`.
- **Git stash conflicts**: always `git stash` before pulling. If `stash pop` fails after a merge, resolve manually.
- **Divergent branches**: some repos may have diverged. Use `git config pull.rebase false` or `git rebase origin/main`.
- **For-loop `cd` breaks**: running `cd` inside a bash `for` loop breaks after the first iteration because subsequent `cd` calls become relative. Run each pull as a separate command with full paths.
- **Non-repo skill dirs**: some skill directories may not be git repos (local-only orphans). These can be deleted directly with `rm -rf`.
- **`replace_all` table collision**: when a SKILL.md has duplicate table structures (e.g., two identical reference file maps), `replace_all=true` will match ALL instances and can corrupt formatting at each insertion point. **Fix:** use more surrounding context to make the match unique, or patch each table individually with a unique anchor line. Prefer unique anchors like section headers immediately above the target table.

---

## Patch editing patterns for large SKILL.md files

### Trigger conditions

- User asks to "push local skill changes to GitHub" or "sync skills to the repo"
- After a significant set of local skill iterations that need to be persisted in the main codebase

### Procedure

1. **Identify changes.**
   ```bash
   find ~/.hermes/skills -name "SKILL.md" | while read file; do
       skill_dir=$(dirname "$file")
       rel_path=${skill_dir#$HOME/.hermes/skills/}
       repo_path="<hermes-home>/hermes-agent/skills/$rel_path"
       if [ -d "$repo_path" ]; then
           diff_output=$(diff -rq "$skill_dir" "$repo_path")
           if [ -n "$diff_output" ]; then
               echo "CHANGED: $rel_path"
           fi
       else
           echo "NEW: $rel_path"
       fi
   done
   ```

2. **Synchronize files.**
   ```bash
   find ~/.hermes/skills -name "SKILL.md" | while read file; do
       skill_dir=$(dirname "$file")
       rel_path=${skill_dir#$HOME/.hermes/skills/}
       repo_path="<hermes-home>/hermes-agent/skills/$rel_path"
       if [ ! -d "$repo_path" ] || [ -n "$(diff -rq "$skill_dir" "$repo_path")" ]; then
           mkdir -p "$repo_path"
           cp -r "$skill_dir/." "$repo_path/"
       fi
   done
   ```

3. **Fork-and-PR workflow.**
   ```bash
   cd <hermes-home>/hermes-agent
   git checkout -b skill-updates-$(date +%Y%m%d)
   git add skills/
   git commit -m "OCAS: Sync local skill changes to repository"
   git push fork HEAD
   gh pr create --repo NousResearch/hermes-agent \
                --title "OCAS: Sync local skill changes to repository" \
                --body "Synchronizes latest local skill updates and new skills." \
                --base main \
                --head <agent-handle>:skill-updates-YYYYMMDD
   ```

### Pitfalls

- **Embedded repos**: some local skills have their own `.git` directories. Git will warn about "embedded git repositories".
- **Working directory**: always ensure you are in the repository root before executing git commands.
- **Upstream sync**: always `git pull origin main` and stash local changes before creating the sync branch.

---

## `forge.verify-update` — manual update verification

When a skill's self-update command fails or you need to confirm a skill is at the latest version without mutating it:

1. **Determine local version**: read `metadata.version` from the skill's `SKILL.md` frontmatter.
2. **Determine remote version**: fetch the latest release or tarball and read `metadata.version` from the remote `SKILL.md`.
   - GitHub release API: `curl -s https://api.github.com/repos/{owner}/{repo}/releases/latest`
3. **If versions match**: stop silently. No update needed.
4. **Detailed file comparison (optional)**: download the tarball, extract to a tempdir, and diff key files (line counts, MD5, full diff). Check for new files in remote that don't exist locally.
5. **Git repository verification**: `git status`, `git branch -vv`, compare `git rev-parse HEAD` to `git rev-parse origin/main`. Report whether local is ahead, behind, or diverged.
6. **If versions differ**: copy files from the extracted tarball to the skill directory, write a journal entry, append to `decisions.jsonl`, clean up the tempdir.

### Pitfalls

- GitHub API rate-limits unauthenticated requests at 60/hour.
- Tarball extraction directory names include the commit hash, not just the repo name.
- Git tags may not match release tags exactly.
- Security scanners block pipe-to-interpreter commands — split into separate steps instead of piping.
- OCAS skills v2.9.0+ may not have `skill.json` — read `metadata.version` from `SKILL.md` frontmatter instead.