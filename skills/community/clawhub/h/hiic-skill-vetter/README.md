# HIIC-skill-vetter

Practical, business-aware vetting for OpenClaw skills.

This skill helps an agent quickly judge whether a skill is safe to install, with a bias toward **clear conclusions** instead of paranoia theater.

## What it does

It guides the agent to produce a short report covering:
- external access
- sensitive access
- dynamic execution
- privilege escalation
- scope mismatch

And then gives an explicit verdict:
- ✅ SAFE TO INSTALL
- ⚠️ INSTALL WITH CAUTION
- 🛑 HUMAN REVIEW RECOMMENDED

## Philosophy

Many useful skills legitimately need:
- API access
- tokens or cookies
- screenshots or browser state
- scheduled jobs
- cloud/document/social platform integrations

Those capabilities alone do **not** make a skill unsafe.

The real question is whether the implementation is:
- expected for the stated purpose
- explicit
- limited in scope
- free of hidden or suspicious behavior

## Files

- `SKILL.md` — core behavior and decision policy
- `vet_scan.py` — repeatable helper scanner for reviewing skill directories
- `vet-scan.sh` — shell wrapper for the scanner

## Usage

From an OpenClaw session, invoke this skill when you want a fast yes/no style safety review before installing another skill.

If you want to run the helper scanner directly:

```bash
python3 vet_scan.py <skill-dir>
python3 vet_scan.py <skill-dir> --format json
```

## Ideal use cases

- quick install checks
- portfolio-wide skill reviews
- second-opinion risk screening
- filtering out overcautious false positives

## Repository

GitHub: <https://github.com/Waytobetter619/HIIC-skill-vetter>
