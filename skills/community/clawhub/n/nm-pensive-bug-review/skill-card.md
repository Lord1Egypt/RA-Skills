## Description:

Hunts bugs with evidence trails

This skill is ready for commercial/non-commercial use.

## Publisher:

[athola](https://clawhub.ai/user/athola)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to investigate suspected defects, record evidence and severity, prepare minimal fixes, and plan verification. It produces structured review findings and proposed code and test changes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Some paths referenced by the skill were missing from the bundled artifact, and scanner coverage was partial; helper instructions or dependencies may therefore be unavailable.

Mitigation: Check that referenced paths and required dependencies are available before use, and review proposed findings and fixes against the project evidence.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/athola/skills/nm-pensive-bug-review)
- [Homepage listed in Clawdis metadata](https://github.com/athola/claude-night-market/tree/master/plugins/pensive)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Code, Shell commands, Files]

**Output Format:** [Markdown defect reports with code diffs, verification commands, and JSON findings]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes evidence references, severity classification, proposed fixes, and verification steps.]

## Skill Version(s):

1.10.4 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
