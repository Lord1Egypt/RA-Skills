## Description:

TinyURL (tinyurl.com). Use this skill for ANY TinyURL request — reading, creating, and updating data. Whenever a task involves TinyURL, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Users can list TinyURLs in their connected account and create short links for destination URLs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup instructions can execute unpinned remote software without a separate approval or verification step.

Mitigation: Review and verify the CLI installation separately; require approval before running an installer or changing installed agent skills.

Risk: Creating a short link changes the user's TinyURL account.

Mitigation: Preserve the skill's confirmation requirement and confirm the destination URL before running the create action.

## Reference(s):

- [TinyURL API documentation](https://api.tinyurl.com/)
- [TinyURL](https://tinyurl.com)
- [oo CLI usage reference](https://github.com/oomol-lab/oo-cli)
- [oo CLI installation guide](https://cli.oomol.com/install-guide.md)
- [TinyURL ClawHub release](https://clawhub.ai/oomol/skills/oo-tinyurl)

## Skill Output:

**Output Type(s):** [Text, JSON]

**Output Format:** [Text or JSON action results, including URL listings or a created short link]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results depend on the requested TinyURL action and connected account.]

## Skill Version(s):

1.0.5 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
