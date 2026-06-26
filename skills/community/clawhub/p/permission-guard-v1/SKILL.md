---
name: permission-guard
description: Security watchdog for OpenClaw agents that monitors installed skill behavior, detects unauthorized file access, suspicious outbound network calls, dangerous command patterns, and generates permission audit reports. Use this skill whenever the user asks about agent activity ("what did my agent do", "check what my skill accessed", "monitor agent permissions", "permission report", "activity log", "did my agent do anything weird", "skill behavior audit", "what files did my agent touch"), after installing a new skill to establish a behavior baseline, or when suspicious or unexpected behavior is suspected. Trigger proactively after any skill installation — a first-run baseline check is always worthwhile.
compatibility: Designed for OpenClaw agents (openclaw.ai). Requires shell access for filesystem and network inspection.
allowed-tools: Bash Read Write
---

# Permission Guard

A runtime security watchdog for OpenClaw agents. Its purpose is to give users clear visibility into what their installed skills are actually doing — catching unexpected file access, suspicious network calls, dangerous commands, or behavior that goes beyond a skill's declared purpose.

## Behavior Log

Maintain a running log at `~/.openclaw/permission-guard.log`. Record each notable agent action in this format:

```
[ISO-8601 timestamp] SKILL:[skill-name] ACTION:[file|network|command] TARGET:[path/url/cmd] STATUS:[ok|flagged|blocked]
```

Keep log files under 10MB — rotate monthly by renaming the old file to `permission-guard.log.YYYY-MM`. The log stays local and is never transmitted externally.

## Security Checks

Run all four checks when producing a report, then summarize findings together.

### Check 1 — Sensitive File Access

Look for recent touches to credential and configuration files:

```bash
find ~ -newer ~/.openclaw/last-check -type f 2>/dev/null \
  | grep -E '(\.ssh|\.aws|\.gnupg|\.config/gcloud|\.gitconfig|/etc/passwd|/etc/shadow|Library/Keychains|\.config/google-chrome|\.mozilla)' \
  | head -30
# Update timestamp after check:
touch ~/.openclaw/last-check
```

Flag any match. The risk is concrete: a rogue skill reading `~/.ssh/id_rsa` while appearing to do something routine is a classic credential exfiltration path.

### Check 2 — Outbound Network Connections

Review active and recent connections:

```bash
ss -tnp 2>/dev/null | grep -Ev '(127\.0\.0\.1|::1|LISTEN)'
```

Flag connections to:
- Unrecognized IPs or domains not associated with the skill's declared APIs
- Known data-sharing services (pastebin, webhook.site, file-sharing hosts)
- Any plaintext (non-HTTPS) connection carrying data

### Check 3 — Dangerous Command Patterns

Check the log for commands that signal permission abuse:

```bash
grep -E '(rm\s+-rf|chmod\s+777|curl.+\|\s*(ba)?sh|wget.+\|\s*(ba)?sh|crontab\s+-[el]|useradd|sudo\b)' \
  ~/.openclaw/permission-guard.log 2>/dev/null | tail -20
```

These patterns don't automatically mean malicious intent, but each warrants a prompt explanation to the user before proceeding.

### Check 4 — Behavioral Drift

Compare what a skill actually did against what its name and description promise. The principle: a skill should only do what its declared purpose suggests.

Examples worth flagging:
- A "weather" skill writing to the filesystem
- An "email" skill accessing SSH keys
- A "calendar" skill running arbitrary shell commands
- Any skill POSTing data to a URL not listed in its declared API set

## Output Format

Produce this report structure, omitting sections that have no events:

```
🛡️ Permission Guard — Activity Report
════════════════════════════════════════
Period: [start] → [end]
Skills monitored: [N]

✅ Normal Activity ([X] events)
   [skill-name]: [description of expected action]

⚠️  Flagged — Investigate ([Y] events)
   [skill-name]: accessed [path] — [why this is suspicious]
   [skill-name]: outbound POST to [ip/domain] — [context]

🔴 Critical — Action Required ([Z] events)
   [skill-name]: [credential path] read + outbound connection in same session
   → Run: claw remove [skill-name]

Assessment: [one-sentence summary]
════════════════════════════════════════
```

If everything is clean, say so plainly — unnecessary warnings erode trust in the watchdog over time.

## Critical Violation Response

When the same skill accesses a credential file AND makes an outbound connection in the same session, treat this as a critical violation rather than a routine flag. This combination is the signature pattern of credential exfiltration: access + transmission. Either alone might be incidental; together they constitute a plausible attack.

Steps to take:
1. Surface the alert immediately and prominently — don't bury it in the report
2. Show the user the exact file accessed and the destination of the outbound call
3. Recommend removal: `claw remove [skill-name]`
4. Ask the user whether to proceed with removal or investigate further first — the decision is theirs, not the watchdog's

## First-Run Baseline

After any new skill is installed, capture a baseline before the skill runs for the first time. This makes future behavioral drift detection much more precise.

```bash
mkdir -p ~/.openclaw/baselines
stat ~/.ssh ~/.aws ~/.gnupg ~/.gitconfig 2>/dev/null \
  > ~/.openclaw/baselines/[skill-name]-baseline.txt
touch ~/.openclaw/last-check
```

## Guiding Principles

Alert and recommend — never act unilaterally. Removing a skill is always the user's decision.

When uncertain whether something is a violation, log and flag it rather than ignoring it. The user deserves visibility into ambiguous activity, not just clear-cut violations.

Avoid false positives where possible. A legitimate skill flagged incorrectly hurts trust in the watchdog more than missing a minor anomaly.
