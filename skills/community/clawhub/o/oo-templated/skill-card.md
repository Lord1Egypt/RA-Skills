## Description:

Templated (templated.io). Use this skill for ANY Templated request — reading, creating, updating, and deleting data. Whenever a task involves Templated, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to inspect Templated account data, create renders, and manage templates and renders through a connected OOMOL account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: First-time setup can run unverified installers and enable automatic skill synchronization that affects other agent apps.

Mitigation: Review setup first, separately approve and verify the CLI installation, and disable automatic synchronization if you do not want other agent apps changed.

Risk: Creating or deleting renders changes Templated account data.

Mitigation: Review the exact action and target, and approve it before execution.

## Reference(s):

- [Templated API documentation](https://templated.io/docs/)
- [oo CLI source](https://github.com/oomol-lab/oo-cli)
- [Templated](https://templated.io)
- [ClawHub release page](https://clawhub.ai/oomol/skills/oo-templated)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Guidance]

**Output Format:** [Text responses with JSON payloads and results, plus inline shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Render creation and deletion require user approval; OOMOL mediates connector requests and credentials.]

## Skill Version(s):

1.0.5 (source: frontmatter; server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
