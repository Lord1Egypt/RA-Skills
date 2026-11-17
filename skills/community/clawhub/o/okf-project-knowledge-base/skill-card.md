## Description:

Durable project knowledge as Git-native OKF bundles (docs/knowledge/, one concept per file, with provenance and trust tiers). Use to record a decision, finding, or rule that must outlive the session. Not session state or agent instructions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tenequm](https://clawhub.ai/user/tenequm)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and project agents use this skill to create, read, and maintain durable project decisions, findings, and rules as repository knowledge that remains useful across sessions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Project notes or agent instructions could introduce incorrect or misleading guidance.

Mitigation: Review changes against their evidence and bundle conventions before committing.

Risk: Sensitive information could be committed to Git and remain in repository history.

Mitigation: Keep secrets and credentials out of Git.

## Reference(s):

- [Open Knowledge Format (OKF)](https://github.com/GoogleCloudPlatform/open-knowledge-format)
- [Skill homepage](https://github.com/tenequm/skills/tree/main/skills/okf-project-knowledge-base)
- [ClawHub skill page](https://clawhub.ai/tenequm/skills/okf-project-knowledge-base)

## Skill Output:

**Output Type(s):** [Markdown, Guidance]

**Output Format:** [Markdown files with YAML frontmatter]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [One concept per file; includes provenance and trust tiers.]

## Skill Version(s):

0.3.1 (source: ClawHub release metadata, frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
