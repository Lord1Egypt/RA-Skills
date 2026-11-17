# Skill Library Maintenance

## When to Use This Reference

Use alongside `hermes-config-change-checklist` when working on **bulk skill operations** — auditing, migrating, standardizing, or batch-fixing 5+ skills at once. The main checklist handles single-skill edits; this covers fleet-level work.

---

## Multi-Phase Workflow

### Phase 1: Audit & Categorize

1. **Count and list all skills** — `ls -d ~/.hermes/skills/*/*/SKILL.md | wc -l`
2. **For each skill/source group, categorize every entry** into one of:
   - **Keep** — valuable, should stay
   - **Merge** — content worth keeping but lives in the wrong skill; plan to absorb into an existing umbrella
   - **Delete** — obsolete, superseded by native tooling, or never used
3. **Check for duplicates/overlaps** — does a native Hermes tool already provide the same capability? (e.g. `tavily-search` → `web_search`/`web_extract`; `find-skills` → `skills_list`/`skill_view`)
4. **Document the plan** before executing changes

Completion criterion: every skill has a clear verdict (keep/merge/delete) and the plan is documented.

### Phase 2: Delete Obsolete Skills

Use `skill_manage(action='delete', name=..., absorbed_into=...)`:
- If merging content into another skill, pass that skill's name as `absorbed_into`
- If truly dead with no forwarding target, pass `absorbed_into=""`
- Do NOT delete pinned skills — `skill_manage` will refuse with a message pointing to `hermes curator unpin <name>`

Standard candidates for deletion (check individually — don't bulk-delete blindly):
- Anything replaced by native Hermes tooling (web search, file ops, browser)
- Migration artifacts from other agent ecosystems (OpenClaw config guard, platform-specific wrappers)
- Skills that were only relevant for a specific one-off project

### Phase 3: Standardize Retained Skills

For every kept skill, ensure:

1. **Frontmatter** — every `SKILL.md` must have (validated via Python/YAML):
   ```yaml
   ---
   name: skill-name
   description: Use when <trigger>. <one-line behavior>.
   version: 1.0.0
   license: MIT-0
   metadata:
     openclaw:
       tags: [relevant, tags]
     hermes:
       tags: [relevant, tags]
       related_skills: [other-skills]
   ---
   ```
   - `description` ≤ 1024 chars
   - Starts with `---` at byte 0
   - Non-empty body after closing `---`

2. **Path migration** — replace ecosystem-specific paths with Hermes equivalents:
   | Old | New |
   |---|---|
   | `/root/.openclaw/` | `~/.hermes/` |
   | `/root/.openclaw/.cache/` | `~/.hermes/cache/` |
   | `/root/.openclaw/.secrets` | the agent's own env file (for Hermes: `hermes config env-path`) |
   | `/root/.openclaw/workspace/` | skill-local or `~/.hermes/` |

3. **Secrets/credentials** — remove hardcoded placeholder credentials from scripts:
   - Never use a placeholder string (`YOUR_KEY_HERE`, `wxYOUR_APPID_HERE`) as a real fallback value in shell expressions
   - Safe pattern: `VALUE="${VALUE:-${ENV_VAR:-}}"` (empty string default)
   - Check for empty string, not placeholder match: `[ -z "$VALUE" ]` not `[ "$VALUE" = "PLACEHOLDER" ]`
   - See "Secrets Hygiene Fix" below for the full treatment

4. **related_skills** — add cross-references to relevant upstream skills. E.g. `hanime-pikpak` → `pikpak-gallery-intake`; `wechat-mp-draft` → MCP equivalents.

5. **Remove stale references** — scrub mentions of deleted skills, old plugin names, ecosystem-specific paths.

### Phase 4: Fix & Harden

#### Secrets Hygiene Fix (wechat-mp-draft pattern)

When migrating shell scripts that had placeholder credentials:

```bash
# ❌ BEFORE: placeholder as real fallback
APPID="${APPID:-${WECHAT_APPID:-wxYOUR_APPID_HERE}}"
APPSECRET="${APPSECRET:-${WECHAT_APPSECRET:-YOUR_SECRET_HERE}}"
if [ "$APPID" = "wxYOUR_APPID_HERE" ]; then
    echo "Error: credentials not configured"
fi

# ✅ AFTER: empty string default + empty check
APPID="${APPID:-${WECHAT_APPID:-}}"
APPSECRET="${APPSECRET:-${WECHAT_APPSECRET:-}}"
if [ -z "$APPID" ] || [ -z "$APPSECRET" ]; then
    echo "❌ Error: credentials not configured"
fi
```

Also update template/example files to reference the official Hermes env file shown by `hermes config env-path` instead of ecosystem-specific secret files. If the template previously contained real placeholder values, replace them with environment-variable-only patterns.

#### Stale Skill Reference Cleanup

After deleting skills, scan all remaining SKILL.md files for references to the deleted names:

```python
import re, pathlib
deleted_names = ['skill-a', 'skill-b']  # names you deleted
root = pathlib.Path('~/.hermes/skills').expanduser()
for p in root.rglob('SKILL.md'):
    text = p.read_text()
    for name in deleted_names:
        if name in text:
            print(p, 'mentions', name)
```

Fix `metadata.hermes.related_skills` in SKILL.md frontmatter, plus any inline prose references.

### Phase 5: Verify

1. **Bulk frontmatter validation** — Python script that iterates all SKILL.md, parses YAML, checks required fields:
   ```python
   for p in sorted(root.rglob('SKILL.md')):
       if not text.startswith('---'): issues.append(...)
   ```

2. **Stale reference scan** — regex patterns for deleted skill names, old base paths, placeholder secret values.

3. **Script syntax checks** for all scripts linked by modified skills:
   ```bash
   python3 -m py_compile script.py
   bash -n script.sh
   ```

4. **Hermes load smoke test** — `hermes skills list` and confirm all expected skill names appear.

5. **skill_view confirmation** for a sample of modified skills to verify they load cleanly.

---

## Common Pitfalls

1. **Hardcoded placeholder run-time defaults.** A placeholder like `YOUR_SECRET_HERE` as a shell default isn't harmless — it can silently pass as a "configured" value or leak in error messages. Always use empty-string default with empty-string check.

2. **Forgetting to update `related_skills` after deletion.** If skill A references skill B in `related_skills` and you delete B, `skill_view` output will note the missing reference. Always scan for dangling cross-references.

3. **Incomplete path migration.** A skill's SKILL.md may say `~/.openclaw/...` while its scripts use a different path. Search with `ripgrep` or Python `pathlib` across all files in the skill directory.

4. **Skipping trust-but-verify on subagents.** When delegating bulk audit/search work, verify key outputs (file paths, counts, status) yourself — subagent summaries are self-reports.

5. **Multiple ecosystem paths in one file.** A single file may reference both `openclaw` AND `hermes` paths after partial migration. Scan for both old and new to catch inconsistencies.
