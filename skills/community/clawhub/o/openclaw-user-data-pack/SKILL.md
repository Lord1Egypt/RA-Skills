---
name: openclaw-user-data-pack
version: 1.0.5
description: "Agent instructions: pack/apply OpenClaw user data via scripts; overwrite-by-path only. You dry-run first, read EXPORT_MANIFEST.txt, gate optional layers, resolve merge conflicts yourself—never imply scripts merge."
trigger: "OpenClaw backup, export user data, pack workspace, migration zip, 打包 openclaw, 迁移记忆, openclaw 一键导出, 一键应用, 导入 zip, restore openclaw from zip, 新机器恢复 openclaw"
---

# OpenClaw agent: pack and apply user data

**Who reads this:** you are the **OpenClaw agent** (runtime). This file is **not** end-user documentation—it tells **you** what to run, what to say, and what you must never do.

**Language:** reply to the user in **their** language; keep technical identifiers (paths, flags) as in the scripts.

---

## Your job in one sentence

Use `scripts/pack_openclaw.py` and `scripts/apply_openclaw.py` from this skill to export or restore workspace data (and optional layers **only** if the user clearly opts in after you warn them). **You** own preview, collision handling, and consent—the scripts only write files by path.

---

## When the user asks to export (pack)

1. Run `pip install -r requirements.txt` if dependencies may be missing.
2. Run `python scripts/pack_openclaw.py --dry-run` with the same flags you plan for the real pack; show the user what paths would be included.
3. Explain: default pack is **`workspace/`** only. List optional layers (`--managed-skills`, session flags, config snapshot flags) and **do not add any** until the user **separately** approves each, after you give the short risk line (size, transcripts, secrets)—see **Before any real disk write**.
4. Run the real pack: `python scripts/pack_openclaw.py` with **only** approved flags.
5. Give the user the zip path. **Before** they copy or upload it: **you** open/list the zip and read `EXPORT_MANIFEST.txt`; confirm it matches what you promised (paths + layers).

---

## When the user asks to import (apply)

1. If the zip is not clearly from a trusted source or from this skill’s pack layout (`workspace/`, `EXPORT_MANIFEST.txt`, …), **stop** and say why you will not apply it without their confirmation.
2. Run `pip install -r requirements.txt` if needed.
3. Tell the user to **back up** `$OPENCLAW_HOME` (or `%USERPROFILE%\.openclaw`) and the target workspace—or apply to a throwaway copy—unless they **explicitly** accept overwrite risk after you state it once.
4. **You** read `EXPORT_MANIFEST.txt` inside the zip, then run  
   `python scripts/apply_openclaw.py --zip <path> --dry-run`  
   with `--openclaw-home`, `--workspace`, and `--config` as the environment needs. Treat the combined manifest + dry-run output as the write contract.
5. Walk the user through which paths would be created/overwritten. For overlaps on **memory / persona / skills**, follow **Merge and conflicts (your work; not in scripts)**—**do not** run non–dry-run apply on a live workspace until conflicts are resolved or the user **explicitly** chooses full replace for that subtree.
6. Add `--apply-managed-skills`, session flags, or `--apply-config` **only** after separate approval **and** the warnings in **Before any real disk write**.
7. Run apply **without** `--dry-run` only when the above is satisfied. If config was restored, remind: they still need valid auth on this machine; old paths inside `openclaw.json` may be wrong here.
8. Optionally suggest they run `openclaw doctor` in their environment (they execute it, not you).

---

## Before any real disk write (you follow this order)

Skip a step **only** if the user opts out **after** you repeat the concrete risk.

1. **Dry-run first** — pack and apply both support `--dry-run`. The printed paths are what a real run would touch.
2. **Read `EXPORT_MANIFEST.txt` in the zip** — authoritative list of packed paths; pair with apply dry-run to see destination collisions.
3. **Backups** — dry-run does not change disk; it is not a backup. For apply, insist on backup or throwaway target unless they waive.
4. **Optional layers = informed consent, not checkbox theater**
   - **Sessions:** full transcripts, large JSONL, overwrite session dirs. Do not pass pack/apply session flags unless the user understands that.
   - **Config snapshot / `--apply-config`:** keys, tokens, channels, machine-specific paths. Do not enable without that acknowledgment.
5. **Config parse / JSON5** — if resolving workspace from config fails, run `pip install -r requirements.txt` (includes `json5`) or pass `--workspace` explicitly.

---

## What the scripts actually do (so you do not mislead)

- Pack and apply are **filesystem** steps: extract or copy bytes to paths. **No** semantic merge, **no** three-way merge, **no** conflict UI in Python.
- **You** must inspect manifests, diff mentally or with tools, merge text or rename paths, and get **explicit** user decisions. **Never** tell the user the “tool merged” or “resolved” overlapping memory/skills unless **you** did that with their approval.

If you follow previews + consent + collision handling, you can honestly say the flow is transparent; if you skip that, you risk silent data loss.

---

## Safety: what you must assume and say

- Assume the archive may hold sensitive material: persona, `MEMORY.md`, logs, workspace skills; with optional layers, session JSONL and `openclaw.json` (secrets, channels).
- **Do not** pack or encourage packing `~/.openclaw/credentials/`. Apply never writes credentials; tell the user they must re-login / re-pair on a new machine unless they consciously accept copying secrets (you still do not pack credentials via these scripts).
- Warn against putting the zip on untrusted or public storage.
- **Overwrite rule:** same path ⇒ destination file replaced. Same path ≠ same meaning. Only `openclaw.json` gets a `.bak.<timestamp>` when using `--apply-config`; **other paths are not auto-backed up.**

### Merge and conflicts (your work; not in scripts)

- A path is an address, not proof two files are equivalent. Do **not** treat “same path in zip and disk” as safe to overwrite without reading both when the file is memory, persona, or a skill.
- **Memory-style files:** if both sides exist and differ materially, **read** both, merge or present a tight conflict summary, and get **explicit** user direction before non–dry-run apply (or they merge manually / use a temp extract).
- **Skills (`SKILL.md` etc.):** divergent purpose or triggers ⇒ **do not** pick a winner alone; offer keep local / take zip / merge / rename path so both can exist.
- **Heuristic:** dry-run + manifest + “would this path clobber something important?” ⇒ if yes, **merge-or-confirm** unless the user **explicitly** asked to replace that whole subtree.

---

## Pack: default vs optional

| Content | Path inside zip | In default pack? |
|---------|-------------------|------------------|
| Workspace (persona, memory, workspace skills, canvas, etc.) | `workspace/` | yes |
| Managed skills | `managed-skills/` | no — `--managed-skills` |
| Sessions | `sessions/<agentId>/sessions/` | no — session flags + acknowledgement; **large, sensitive, full transcripts** |
| Config snapshot | `config/openclaw.json` | no — config flags + acknowledgement; **secrets, machine paths** |
| Credentials | n/a | **never** |

---

## Apply: default vs optional

Match flags to what is in the zip. If a layer is in the zip but flags are missing, the script warns and skips that layer.

| Content | Action | Default apply? |
|---------|--------|----------------|
| Workspace | Extract `workspace/*` → target workspace | yes, unless `--no-apply-workspace` |
| Managed skills | → `<openclaw-home>/skills/` | no — `--apply-managed-skills` |
| Sessions | → `<openclaw-home>/agents/<id>/sessions/` | no — `--apply-sessions` + `--i-know-restoring-sessions-overwrites` |
| Config | → `<openclaw-home>/openclaw.json` (existing → `.bak.<timestamp>`) | no — `--apply-config` + `--i-know-config-overwrites-secrets` |

---

## Paths (how you resolve them)

- OpenClaw home: `$OPENCLAW_HOME` or `~/.openclaw`; Windows: `%USERPROFILE%\.openclaw`.
- Pack: if `--workspace` omitted, script reads config. Apply: `--workspace` may create the dir; if omitted, config must parse. On a fresh machine, prefer `openclaw onboard` or pass `--workspace` explicitly.
- Run pack and apply in the **same** environment family (e.g. both WSL) so paths mean the same thing.

---

## Examples (you adapt paths for the user’s OS)

Workspace-only apply, dry-run then real:

```bash
python scripts/apply_openclaw.py --zip ./openclaw-user-export-xxx.zip \
  --openclaw-home ~/.openclaw \
  --workspace ~/.openclaw/workspace \
  --dry-run
python scripts/apply_openclaw.py --zip ./openclaw-user-export-xxx.zip \
  --openclaw-home ~/.openclaw \
  --workspace ~/.openclaw/workspace
```

All optional apply layers — **only** after the user approved **each** flag’s risk:

```bash
python scripts/apply_openclaw.py --zip ./export.zip \
  --openclaw-home ~/.openclaw --workspace ~/.openclaw/workspace \
  --apply-managed-skills \
  --apply-sessions --i-know-restoring-sessions-overwrites \
  --apply-config --i-know-config-overwrites-secrets
```

---

## CLI reference (copy-paste skeletons)

**Pack:**

```text
python scripts/pack_openclaw.py [--workspace PATH] [--openclaw-home PATH] [--config PATH]
  [-o FILE.zip] [--exclude-git | --no-exclude-git] [--managed-skills]
  [--sessions --i-know-sessions-are-large-and-sensitive]
  [--config-snapshot --i-know-config-may-contain-secrets]
  [--dry-run] [--manifest-sha256] [--sha256-max-mb N]
```

**Apply:**

```text
python scripts/apply_openclaw.py --zip FILE.zip [--openclaw-home PATH] [--workspace PATH] [--config PATH]
  [--no-apply-workspace] [--apply-managed-skills]
  [--apply-sessions --i-know-restoring-sessions-overwrites]
  [--apply-config --i-know-config-overwrites-secrets]
  [--dry-run]
```

---

## When to activate this skill (trigger hints)

| Intent | Example user phrases |
|--------|----------------------|
| Export | backup workspace, export memory, pack openclaw |
| Import | new PC restore, import zip, apply backup, restore openclaw |
| Chinese | 一键打包, 一键应用, 导入 zip, 迁移 |

---

## Quick commands (you run from skill root)

| Goal | Command |
|------|---------|
| Pack preview | `python scripts/pack_openclaw.py --dry-run` |
| Pack | `python scripts/pack_openclaw.py` |
| Apply preview | `python scripts/apply_openclaw.py --zip x.zip --dry-run` |
| Apply | `python scripts/apply_openclaw.py --zip x.zip` |
| Dependencies | `pip install -r requirements.txt` |
