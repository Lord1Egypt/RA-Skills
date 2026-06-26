---
name: hh-openclaw-agent
description: HH OpenClaw Agent is a public ClawHub hh.ru application skill. Use it when the user says "hh openclaw agent", "hh job apply automation", "hh.ru browser application", or wants a reviewed hh.ru application packet with logged-in browser execution and an auditable submission bundle.
version: 1.0.7
homepage: https://github.com/zack-dev-cm/hh-openclaw-agent
license: MIT-0
user-invocable: true
metadata: {"openclaw":{"homepage":"https://github.com/zack-dev-cm/hh-openclaw-agent","skillKey":"hh-openclaw-agent","requires":{"anyBins":["python3","python"]}}}
---

# HH OpenClaw Agent

Search intent: `hh openclaw agent`, `hh.ru apply`, `job application browser automation`, `career submission bundle`

## Goal

Turn one `hh.ru` application run into a reusable submission bundle:

- one machine-readable application packet
- one ordered execution log with evidence
- one structural bundle check
- one shareable markdown report

This skill is for reviewed `hh.ru` browser execution through OpenClaw.
It assumes the browser profile is already authenticated.

## Use This Skill When

- the user wants to prepare and submit an `hh.ru` application through OpenClaw
- a vacancy-specific packet should be reviewed before the live browser write
- the same `hh.ru` response flow needs an auditable run log instead of chat memory
- a blocked or failed submission needs screenshots, exact steps, and a handoff report
- the operator wants one record of approved content and live browser outcome

## Quick Start

1. Initialize the application packet.
   - Use `python3 {baseDir}/scripts/init_hh_application_packet.py --out <json> --packet-id <id> --vacancy-id <id> --vacancy-title <title> --company-name <company> --resume-title <resume> --vacancy-url <url> --apply-url <url> --cover-letter <text>`.
   - Add `--browser-profile`, `--review-status`, `--reviewer`, and repeatable `--blocked-action` fields when needed.

2. Execute the browser flow through OpenClaw.
   - Open the apply URL in a logged-in profile.
   - Record each meaningful browser action with `append_hh_execution_step.py`.
   - Capture screenshots and outcome notes as the run progresses.

3. Keep operator-owned auth and approval gates explicit.
   - If `hh.ru` shows login, CAPTCHA, 2FA, or another auth challenge, stop and let the operator complete it in the same browser profile.
   - Do not live-send a packet that is still `pending` or `rejected`.

4. Check the bundle before sharing or counting it as complete.
   - Use `python3 {baseDir}/scripts/check_hh_submission_bundle.py --manifest <json> --repo-root <repo> --out <json>`.
   - Fix approval-gate issues, missing screenshots, or incomplete failed-step notes before final handoff.

5. Render the report.
   - Use `python3 {baseDir}/scripts/render_hh_submission_report.py --manifest <json> --out <md>`.
   - The default report redacts the cover letter body, keeps only public `https://*.hh.ru/...` URLs, and redacts private artifact paths.
   - Add `--include-sensitive` only when you intentionally need a full-content export.
   - Share the report instead of loose screenshots and manual notes.

## Operating Rules

### Packet rules

- Keep one packet per vacancy response flow.
- The cover letter should stay vacancy-specific.
- Record vacancy URL, apply URL, resume title, and approval state before opening the live form.

### Execution rules

- Use a logged-in OpenClaw browser profile for the live `hh.ru` session.
- Record expected result and actual result for every meaningful step.
- Capture a screenshot for failed or blocked steps and for the final submitted state when possible.
- Keep artifact paths relative so the bundle can move between machines.

### Safety rules

- Do not claim undocumented `hh.ru` write APIs.
- Do not store cookies, secrets, or tokens in notes or artifacts.
- Do not send a live application unless the packet review state is `approved`.
- Treat login, CAPTCHA, passkey, and 2FA as operator-owned interruptions, not background automation.

## Bundled Scripts

- `scripts/init_hh_application_packet.py`
  - Create a machine-readable application packet for one `hh.ru` response flow.
- `scripts/append_hh_execution_step.py`
  - Append one evidence-backed browser execution step to the packet.
- `scripts/check_hh_submission_bundle.py`
  - Validate approval state, execution evidence, and bundle safety before handoff.
- `scripts/render_hh_submission_report.py`
  - Render a concise markdown report from the packet and execution log.
