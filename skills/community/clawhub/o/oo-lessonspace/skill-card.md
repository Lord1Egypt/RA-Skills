## Description:

Manage Lessonspace through an OOMOL-connected account, including creating spaces and reading organization sessions or recording links.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

External users can use this skill to create Lessonspace rooms and read organization sessions or recording links through their connected OOMOL account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: First-time setup can execute remote installer code without separate user approval.

Mitigation: Review the setup, independently verify and pin the CLI release, and approve local installation separately. Review or disable automatic bundled-skill changes.

Risk: Room credentials and recording links may expose access to Lessonspace sessions.

Mitigation: Handle room credentials and recording links carefully and share them only with intended participants.

Risk: Remote installer behavior and backend credential handling were not verified.

Mitigation: Review installation steps before running them and use an independently verified CLI release.

## Reference(s):

- [Lessonspace](https://www.thelessonspace.com)
- [Lessonspace API documentation](https://www.thelessonspace.com/docs/api)
- [oo CLI](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Text]

**Output Format:** [Structured Lessonspace data such as room details, session records, and recording URLs, with concise explanatory text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results depend on the connected Lessonspace account and the selected action.]

## Skill Version(s):

1.0.5 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
