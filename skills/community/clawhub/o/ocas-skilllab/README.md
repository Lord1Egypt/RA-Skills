# ⚙️ Skilllab

  <img src="./assets/readme/hero.jpg" width="100%" alt="Skilllab">

>

**Skill name:** `ocas-skilllab`
**Version:** 3.4.2
**Type:** 
**Layer:** software-development
<<<<<<< Updated upstream
**Author:** Indigo Karasu
=======
**Author:** <agent-name>
>>>>>>> Stashed changes

---

## 📖 Overview

>

---

## 🔧 Commands

<<<<<<< Updated upstream
- `ocas-*` — OCAS family, authored by Indigo Karasu (includes library-management meta-skills).
- `util-*` — Utility skills authored by Indigo Karasu.
- `skilllab` — This skill; meta-skill for skill library management.
- **`--all-profiles` discovery bug (2026-07-15):** `find_all_skills(all_profiles=True)` must resolve the profiles dir from `HERMES_ROOT` (`os.path.join(HERMES_ROOT, "profiles")`), NOT `os.path.expanduser("$HERMES_HOME/..")`. Under a profile chroot (`HOME=<hermes-home>/profiles/<profile>/home`) the latter resolves to the *active* profile's home and silently drops every other profile (e.g. `koda` — `koda/ocas-eng-debug` went unscanned). The runner was fixed; verify with `python3 scripts/critique_10khr_runner.py --all-profiles --report-only` and confirm the non-active profiles actually appear.
=======
- `ocas-*` — OCAS family, authored by <agent-name> (includes library-management meta-skills).
- `util-*` — Utility skills authored by <agent-name>.
- `skilllab` — This skill; meta-skill for skill library management.
- **`--all-profiles` discovery bug (2026-07-15):** `find_all_skills(all_profiles=True)` must resolve the profiles dir from `HERMES_ROOT` (`os.path.join(HERMES_ROOT, "profiles")`), NOT `os.path.expanduser("$HERMES_HOME/..")`. Under a profile chroot (`HOME=$HERMES_HOME/../<profile>/home`) the latter resolves to the *active* profile's home and silently drops every other profile (e.g. `koda` — `koda/ocas-eng-debug` went unscanned). The runner was fixed; verify with `python3 scripts/critique_10khr_runner.py --all-profiles --report-only` and confirm the non-active profiles actually appear.
>>>>>>> Stashed changes
- **`secret-scan.sh --working-tree` mode (added 2026-07-15):** full-history scanning blocks legitimate pushes because pre-existing committed doc prose (example credential URLs in `util-github/credential-purge.md`, the scanner's own regex literal in `util-github/scripts/secret_scan.sh`) flags as "secret." For a SYNC gate you only care about NEW secrets in the working tree, so pass `--working-tree` (scans working tree + `.git/config`, skips `git rev-list --all`). The script excludes itself (`secret-scan.sh`/`secret_scan.sh`) from the working-tree grep. Use full mode only for pre-publish audits where history matters.
- `scripts/skill-sync-all.sh` — UNIFIED sync action (SUPERSEDES `skill-sync-push.sh` + `monorepo-sync.sh`): discovers every `ocas-*`/`util-*`/`eng-*` SKILL.md across `indigo`+`koda` profiles by rule (no hard-coded lists), syncs ocas-* as per-skill repos (new names strip `ocas-`), util-*/eng-* into the `utilities`/`eng-skills` monorepos (strips nested `.git`/`.bak`/pycache, sanitizes doc-URL placeholders, secret-gates `--working-tree`), pushes. Drives cron `skill-sync-all` (daily 04:00). `DRY_RUN=1` for a no-op report. Reusable discovery helpers documented in `references/skill-sync-discovery.md`.
- `scripts/secret-scan.sh` — secret gate (full + `--working-tree` modes). Excludes itself. See §7b.

---

## 📊 Outputs

See `SKILL.md` for outputs, journals, and persistence rules.

---

## 📄 Files

| File | Purpose |
|---|---|
| `SKILL.md` | Skill definition |
| `references/` | Supporting documentation |
| `scripts/` | Helper scripts |


## 📚 Documentation

Read `SKILL.md` for operational details, schemas, and validation rules.

Read `references/` for detailed specifications and examples.


---

## 📄 License

MIT License — see `LICENSE` for details.