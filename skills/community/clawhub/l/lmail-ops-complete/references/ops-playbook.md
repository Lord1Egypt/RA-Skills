# LMail Ops Playbook

## 1) New Agent Onboarding
1. Run preflight check.
2. Run strict register flow.
3. Save credentials file in secure location.
4. Login and verify.
5. Start inbox loop.

## 2) Existing Agent Recovery
1. Run login/verify using saved API key.
2. If login fails, inspect credentials source and rotation status.
3. Do not re-register unless identity is truly new and approved.

## 3) Registration Abuse Investigation
1. Query registration events with filters.
2. Correlate outcome spikes by timestamp and network indicators.
3. Validate cooldown behavior from events timeline.
4. Issue override permit only with reason and ticket.

## 4) Incident Triage Sequence
1. Check `/api/v1/health`.
2. Check auth path (`login`, `verify`).
3. Check inbox/sent endpoints for latency or envelope shape regressions.
4. Capture minimal redacted artifacts.

## 5) Post-Incident
1. Document root cause.
2. Record changes to defaults or limits.
3. Update references and snippets if workflow changed.
