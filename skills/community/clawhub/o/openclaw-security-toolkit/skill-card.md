## Description:

Security guard for OpenClaw users. Audit configs, scan secrets, manage access, and generate security reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hkall](https://clawhub.ai/user/hkall)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw administrators use this skill to audit OpenClaw configuration, scan for exposed secrets, review access settings, rotate tokens, and generate security reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Reports and command output may expose secrets or sensitive local file paths.

Mitigation: Review output locally, avoid shared output paths and JSON reports until raw secret redaction is fixed, and do not paste or share command output.

Risk: Token rotation and hardening commands can modify OpenClaw authentication settings.

Mitigation: Back up ~/.openclaw/openclaw.json, run checks without --fix first, and apply changes only after reviewing the proposed actions.

## Reference(s):

- [OpenClaw Security Best Practices](artifact/references/security-best-practices.md)
- [ClawHub Skill Page](https://clawhub.ai/hkall/skills/openclaw-security-toolkit)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, configuration, guidance]

**Output Format:** [CLI output as terminal text, JSON, or Markdown reports with configuration guidance.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports may include security findings, scores, affected file locations, and recommended actions.]

## Skill Version(s):

1.0.0 (source: server release evidence and CHANGELOG, released 2026-03-11)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
