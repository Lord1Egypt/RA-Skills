## Description:

AI-powered auto-repair system for OpenClaw that diagnoses crashes, configuration errors, and model issues, and falls back to iflow-helper when needed.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kosei-echo](https://clawhub.ai/user/kosei-echo)

### License/Terms of Use:

MIT

## Use Case:

Developers and OpenClaw operators use this skill to diagnose gateway crashes, memory search failures, configuration errors, API quota issues, and agent conflicts. It attempts known repairs, records repair history, and falls back to iFlow-assisted manual troubleshooting when automatic repair is not enough.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent monitoring can run with high privileges if installed through system service mechanisms.

Mitigation: Run the watchdog under a least-privilege user account and avoid installing it as root or SYSTEM.

Risk: Generated repair scripts may change or remove OpenClaw configuration and local files.

Mitigation: Use report-only or manual review mode where possible, back up OpenClaw and iFlow configuration first, and inspect each generated script before execution.

Risk: Diagnostic logs and settings files may contain API keys or other credentials.

Mitigation: Redact secrets from logs, settings, and copied error output before sharing them with iFlow or other assistants.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/kosei-echo/skills/openclaw-iflow-doctor)
- [README](artifact/README.md)
- [Installation guide](artifact/INSTALL_GUIDE.md)
- [iFlow authentication guide](artifact/docs/iflow-auth-guide.md)
- [Release notes](artifact/RELEASE.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown and text reports with inline shell commands and generated repair scripts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May generate localized diagnosis reports, repair scripts, configuration checks, and iFlow handoff guidance.]

## Skill Version(s):

1.1.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
