## Description:

Create knowledge bases, manage project documentation, track requirements, and organize personal knowledge.

This skill is ready for commercial/non-commercial use.

## Publisher:

[codermoray](https://clawhub.ai/user/codermoray)

### License/Terms of Use:

Apache 2.0

## Use Case:

External users and developers use this skill to create local knowledge bases, manage requirement lifecycles, maintain project status notes, and resume work from saved Markdown and YAML records.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent local records and optional hooks can store message or task content.

Mitigation: Confirm the auto_record setting before use, avoid secrets in complex-task prompts, and review or delete local records when needed.

Risk: Shared ZIP imports and exports can expose sensitive project data or introduce untrusted archive content.

Mitigation: Manually review archives before sharing or importing, and treat shared ZIP files as untrusted unless archive path validation has been confirmed.

Risk: Automatic update checks may be unsuitable for strict no-network or no-shell environments.

Mitigation: Disable automatic update checks when a strict no-network or no-shell setup is required.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/codermoray/skills/myknowledge)
- [README](README.md)
- [Quickstart](QUICKSTART.md)
- [Usage Guide](USAGE.md)
- [Privacy Statement](PRIVACY.md)
- [Pitfalls Guide](docs/PITFALLS.md)

## Skill Output:

**Output Type(s):** [Markdown, Files, Configuration, Guidance]

**Output Format:** [Markdown and YAML-backed local knowledge-base records]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces persistent local project notes, requirement records, status summaries, and optional import/export archives.]

## Skill Version(s):

1.4.89 (source: frontmatter, release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
