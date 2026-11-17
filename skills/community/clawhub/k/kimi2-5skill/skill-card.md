## Description:

Troubleshoots Kimi 2.5 / OpenClaw image understanding failures, including OCR failures, ignored vision model configuration, and `Unknown model` runtime errors.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jiangwill2023](https://clawhub.ai/user/jiangwill2023)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators maintaining OpenClaw agents use this skill to diagnose and recover Kimi 2.5 image understanding and OCR runtime failures. It guides runtime verification, model configuration checks, targeted provider-block removal, gateway restart, and real-image regression testing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may direct an agent to inspect and modify local OpenClaw model configuration.

Mitigation: Confirm the image-runtime symptom first, back up the affected `models.json`, and review the exact provider block before removal.

Risk: A repair may be incorrectly considered complete if only static configuration is checked.

Mitigation: Require a healthy gateway state and at least one real-image regression test that returns a normal description or OCR result.

## Reference(s):

- [Incident 2026-04-14](references/incident-2026-04-14.md)
- [Recovery Playbook](references/recovery-playbook.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with command and configuration path references]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include OpenClaw runtime checks, local configuration inspection steps, repair guidance, and validation criteria.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
