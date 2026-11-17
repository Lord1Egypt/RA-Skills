# Standalone Skill Install / Export (import_skill.py / export_skill.py)

WHY: keelwright ships on ClawHub, skills.sh, askill.sh. Agents need to install/export it
without git, without Hermes-specific paths, runtime-agnostic.

---

## export_skill.py — Create Portable ZIP

```bash
# Default export (public files only, no internal/, no backups/)
python scripts/export_skill.py
# → ~/kw-qa/keelwright-export-<ts>.zip

# Custom path
python scripts/export_skill.py -o /tmp/keelwright.zip

# Include internal/ and backups/ (full state)
python scripts/export_skill.py --all

# Include external QA runs (~/kw-qa/) — OPT-IN, warns about local paths
python scripts/export_skill.py --include-runs
```

**ZIP Contents:**
- Skill source (SKILL.md, references/, scripts/, templates/)
- QA methodology (qa-results/README.md only — raw runs gitignored)
- `_MANIFEST.json` — SHA256 of every file (tamper detection on import)
- Optional: external QA runs + CONTEXT-TRANSFER-PROMPT.md (with `--include-runs`)

**Key guards:**
- No absolute paths in manifest (privacy)
- Files > 10MB skipped
- Symlinks not followed

---

## import_skill.py — Install from ZIP / GitHub / Local

```bash
# From local ZIP
python scripts/import_skill.py ~/kw-qa/keelwright-export-20260831T120000Z.zip

# Custom install dir (default: ~/.keelwright/skills/keelwright)
python scripts/import_skill.py ~/kw-qa/keelwright-export-20260831T120000Z.zip --force
```

**Safety (zip-slip guard + post-install checks):**
- Validates all paths stay inside target dir (no `../` escape)
- Verifies `_MANIFEST.json` SHA256 matches
- Runs `build_skill.py --check` after install (confirms layered index intact)
- Optional: runs `runtime_integration_tester.py --self-test` (5 gates)
- Opt-in: `--run-checks` runs `validate_run.py` on any qa-results in zip

---

## Runtime-Agnostic Install Path

Default: `~/.keelwright/skills/keelwright` (NOT `~/.hermes/...`)

Override with env:
```bash
KEELWRIGHT_SKILLS=/custom/path python scripts/import_skill.py <source>
```

**Detected runtimes (bindings/):**
- Hermes desktop: `~/.hermes/skills/` (legacy)
- OpenClaw: `~/.openclaw/skills/` / ClawHub
- Cursor: `.cursor/skills/`
- Codex: `~/.codex/skills/`
- Cline: `~/.cline/skills/`
- Kilo: `~/.kilo/skills/`

`find_skills_dir()` in `import_skill.py` scans all known locations.

---

## Post-Install Verification (ALWAYS RUN)

```bash
cd ~/.keelwright/skills/keelwright
python scripts/build_skill.py --check        # index ↔ full doc sync
python scripts/runtime_integration_tester.py --skill-dir .  # 5 gates
python scripts/defense_health.py              # Web Guard status
```

If any fails → install incomplete, do not use skill until resolved.

---

## Publishing to Registries

| Registry | Artifact | Command |
|----------|----------|---------|
| ClawHub | ZIP from `export_skill.py --all` | Manual upload via ClawHub UI |
| skills.sh | `SKILL.full.md` (single page) | `python scripts/build_skill.py --inplace` → confirm YES → push tag |
| askill.sh | ZIP + manifest | Manual submit |

**skills.sh / askill.sh** display `SKILL.md` as single page → MUST be `SKILL.full.md` (assembled).
Use `python scripts/build_skill.py --inplace` (with YES confirmation) to overwrite index with full doc for publication, then `git tag vX.Y.Z && git push --tags`.