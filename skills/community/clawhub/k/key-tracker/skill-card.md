## Description:

Key Tracker helps an agent capture deadlines, open issues, decisions, commitments, progress, dependencies, insights, and stakeholders from work conversations and reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[vincentlau2046-sudo](https://clawhub.ai/user/vincentlau2046-sudo)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill as a Chinese-language work memory aid that detects and records important project facts from conversations and reports, then helps query those records later.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can persist conversation and report excerpts in plaintext local records across sessions.

Mitigation: Treat the .keyrecords directory as sensitive, avoid secrets or regulated data, apply local file permissions, and review or delete records regularly.

Risk: Automatic capture is documented without clear consent, redaction, or deletion controls.

Mitigation: Enable the skill only where local memory capture is expected, and add explicit deletion or redaction practices before use in sensitive workflows.

## Reference(s):

- [Detection Pattern Library](artifact/references/patterns.md)
- [ClawHub Skill Page](https://clawhub.ai/vincentlau2046-sudo/skills/key-tracker)
- [Project Homepage Listed in Artifact](https://github.com/vincentlau2046-sudo/key-tracker)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration]

**Output Format:** [Markdown guidance with JSON record examples and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Documented behavior stores captured records as local plaintext JSON files under .keyrecords.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
