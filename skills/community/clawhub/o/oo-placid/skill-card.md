## Description:

Use this skill for Placid requests to inspect templates, create and check image generation requests, and delete image requests.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

For users working in Placid, agents can list or inspect templates, submit image-generation requests, check request status, and delete requests.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: First-time setup instructions can lead an agent to run an online installer whose contents have not been verified.

Mitigation: Install a verified, fixed CLI release separately and require approval before running any downloaded installer.

Risk: The skill uses a connected Placid account and includes actions that create or delete image requests.

Mitigation: Keep confirmation prompts enabled for writes and deletions, and review the target and payload before execution.

## Reference(s):

- [Placid](https://placid.app)
- [Placid API documentation](https://placid.app/docs/2.0/rest/authentication)
- [oo CLI project](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [Text, API results, Guidance]

**Output Format:** [Natural-language summaries and structured Placid action results, including JSON data and image URLs.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Image requests may return a handle for later status checks.]

## Skill Version(s):

1.0.5 (source: frontmatter metadata, release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
