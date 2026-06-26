# False Positive Appeal Template (VirusTotal / AV vendors)

Subject: False Positive Report – Pengbo Space Skill

Hello Security Team,

We believe this detection is a false positive for our legitimate automation skill.

## Product
- Name: Pengbo Space Skill
- Repository: <repo-url>
- Version: <version>
- SHA256: <sha256>
- Signature: <signature-info>

## Intended behavior
- Calls only `https://pengbo.space/api/v1` for SMM API operations.
- No autostart by default.
- No forced scheduled task creation.
- No remote download-and-execute on first run.
- No generic shell passthrough (only fixed whitelisted commands).

## Security controls
- HTTPS required.
- API host allowlist enforced.
- Audit logs for write actions.
- Release security checks and malware scan pre-gates.

## Repro steps
1. Install and run with `health` or `services` command.
2. Observe only expected API requests to allowed domain.
3. No persistence mechanism is created unless explicitly configured by user.

Please re-evaluate this sample and remove the false-positive label if appropriate.

Thank you.
