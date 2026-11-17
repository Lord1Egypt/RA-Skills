## Description:

GitHub operations skill for creating repositories, pushing code, and managing releases with no user intervention.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yang1002378395-cmyk](https://clawhub.ai/user/yang1002378395-cmyk)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and automation agents use this skill to create GitHub repositories, push project code, update README content, and create GitHub releases using git, curl, and a configured GitHub token.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Fully automatic credentialed GitHub publishing can create public repositories, push commits, create releases, or trigger deployments without adequate review.

Mitigation: Require explicit approval before repository creation, pushes, releases, or deployment-triggering operations.

Risk: GitHub token handling can expose broad credentials or persist them in unsafe locations such as remote URLs.

Mitigation: Use a least-privilege, revocable token in a controlled environment, avoid storing tokens in Git remote URLs, and run from a dedicated checkout.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yang1002378395-cmyk/skills/github-ops-v2)
- [Artifact homepage](https://github.com/openclaw/openclaw)

## Skill Output:

**Output Type(s):** [shell commands, code, configuration, guidance]

**Output Format:** [Markdown with inline bash and API examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires git, curl, and a configured GITHUB_TOKEN.]

## Skill Version(s):

2.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
