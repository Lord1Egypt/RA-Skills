## Description:

Use this skill to read, create, and update LoyJoy data through an OOMOL-connected account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

External users can use this skill to inspect LoyJoy processes, views, and knowledge, and to start processes or generate completions when needed.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The LoyJoy workflow can execute changing remote code and introduce broader agent changes without clear user approval.

Mitigation: Review and approve CLI installation separately, including any additional agent skills it installs or updates. Prefer a verified, fixed release, connect only the LoyJoy access needed, keep confirmation enabled for writes, and note that the remote installer contents remain unverified.

## Reference(s):

- [LoyJoy API documentation](https://docs.loyjoy.com/api/)
- [LoyJoy homepage](https://www.loyjoy.com/en/)
- [oo CLI repository](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [Text, JSON]

**Output Format:** [JSON data or generated text returned by LoyJoy]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results depend on the connected LoyJoy tenant and selected action.]

## Skill Version(s):

1.0.4 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
