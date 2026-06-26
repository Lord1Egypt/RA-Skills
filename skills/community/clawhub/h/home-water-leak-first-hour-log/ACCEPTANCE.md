# Acceptance Checklist

- [x] SKILL.md has valid YAML frontmatter.
- [x] skill.json is present and valid JSON.
- [x] Version is 1.0.0 and license is MIT-0.
- [x] Language is English only.
- [x] Prompt-only metadata is present: promptOnly true, hasExecutableCode false, requires_api false, no_code_execution true, execution noExec.
- [x] No executable code, scripts, package files, automation hooks, API use, network requirements, or credential handling.
- [x] Safety boundary tells users to avoid standing water near electricity and call emergency help for active flooding, electrical hazards, structural danger, contaminated water, or unsafe conditions.
- [x] Does not provide plumbing, electrical, appliance, or restoration repair instructions.
- [x] Deliverable is a first-hour action log with shutoff checklist, photo checklist, damage notes, contact list, and cleanup timeline.
- [x] Workflow covers locate source, shut off water if safe and known, protect electricity and valuables, document photos, and record cleanup and contacts.
- [x] Slug matches the accepted design: home-water-leak-first-hour-log.

## Clean Scan Evidence

- [x] No secrets, tokens, passwords, API keys, or private keys.
- [x] No executable code, scripts, package.json, or build artifacts.
- [x] No network calls, outbound requests, or external API dependencies.
- [x] No credential handling or environment-variable leakage.
- [x] No binary files, compiled code, or platform-specific executables.
- [x] No temp files, logs, .DS_Store, or editor artifacts.
- [x] Document-only, prompt-only, no execution required.
- [x] Language content is English with no CJK-dominant paragraphs.

## Install-First Success Path

**Input:** User provides leak discovery details (affected rooms, suspected source, whether water is active or stopped, and safety context).

**Steps:**
1. Read the skill metadata and verify document-only, prompt-only safety.
2. Review the workflow: stabilize safety, locate source, shut off water if safe, protect electricity and valuables, document photos, record damage and contacts, build cleanup timeline.
3. Ask for any missing required inputs (shutoff location, contacts, photos taken).
4. Produce the first-hour action log with all 9 required sections.

**Output:** A printable, timestamped first-hour action log with shutoff checklist, photo checklist, damage notes, contact list, and cleanup timeline ready for immediate use with no additional tools, files, or network access.
