## Description:

Moses Stamp embeds a MO§ES™ governance stamp in qualifying generated documents, including mode, posture, session ID, action number, and an integrity hash.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sunrisesillneversee](https://clawhub.ai/user/sunrisesillneversee)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and ClawHub users use this skill to add visible provenance stamps to reports, memos, specs, emails, code deliverables, and other documents intended for use outside the conversation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can automatically alter generated deliverables by appending MO§ES™ branding and governance metadata.

Mitigation: Review the exact stamp text and use the skill only for documents where appended governance metadata is expected.

Risk: The stamp tool keeps a local stamp history under ~/.openclaw/governance.

Mitigation: Confirm local logging is acceptable before installation, especially on shared systems or workflows with retention requirements.

Risk: Appending stamps to source code, JSON, configuration, signed files, or externally shared documents can corrupt structure or change the meaning of the file.

Mitigation: Avoid applying the append command to structured, signed, or externally distributed files unless the resulting artifact has been reviewed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/sunrisesillneversee/skills/moses-stamp)
- [ClawHub publisher profile](https://clawhub.ai/user/sunrisesillneversee)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Files]

**Output Format:** [Markdown stamp block or CLI text output, with optional appended file content]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Stamp content includes governance mode, posture, role, session ID, action number, runtime label, and a SHA-256 integrity hash.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
