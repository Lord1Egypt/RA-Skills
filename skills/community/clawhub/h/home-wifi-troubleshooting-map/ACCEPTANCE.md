# Acceptance Criteria - Home Wi-Fi Troubleshooting Map

## Gate Checks

- [x] `SKILL.md` exists and contains a prompt-only workflow.
- [x] `skill.json` is valid JSON and declares `version=1.0.0`, `license=MIT-0`, `language=en`, and `hasExecutableCode=false`.
- [x] File count is exactly 3: `SKILL.md`, `skill.json`, and `ACCEPTANCE.md`.
- [x] Public-facing documentation is English only.
- [x] No executable code, scripts, package files, network calls, APIs, credentials, secrets, or private data are included.
- [x] Trigger scenario, concrete deliverable, workflow, output format, style rules, and safety boundary are explicit.
- [x] The workflow is limited to visible, low-risk observations and support-ready documentation.
- [x] The output includes symptoms, affected devices and rooms, router or modem light observations, outage checks, speed-test notes, likely issue area, support script, and next actions.
- [x] The safety boundary avoids unsafe electrical work, router disassembly, provider box access, wall work, and credential sharing.
- [x] Emergency or unsafe equipment conditions are routed to appropriate professional or emergency help.
- [x] No CJK characters are present.

## Scope

- Prompt-only MVP.
- Local implementation only.
- Not published to ClawHub in this phase.

## Review Status

- Implemented by: OpenClaw / coder
- Date: 2026-05-11
- Status: Ready for cross-review and test.

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

**Input:** User provides Wi-Fi trouble details (symptoms, affected devices/rooms, router/modem model, light colors/patterns, recent changes, speed-test results, outage notices, and safe steps already tried).

**Steps:**
1. Read the skill metadata and verify document-only, prompt-only safety.
2. Review the workflow: capture symptoms, map scope, collect visible device status, check official channels, list safe visible checks, document restart history, identify escalation triggers, prepare support script.
3. Ask for any missing critical inputs (router light status, affected rooms and devices, recent changes).
4. Produce the Home Wi-Fi Troubleshooting Map with all 8 required sections.

**Output:** A visible-diagnostic sheet with current situation, scope map, visible equipment status, safe checks tried, likely issue area, support call script, next actions, and do-not-do list — ready for immediate use with no additional tools, files, or network access.
