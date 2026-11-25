## Description:

Diagnoses GitHub Personal Access Token authentication failures by checking command usage, environment propagation, request parameters, and permissions before concluding a token is expired or revoked.

This skill is ready for commercial/non-commercial use.

## Publisher:

[haiyangchenbj](https://clawhub.ai/user/haiyangchenbj)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to diagnose GitHub API and repository access failures by checking token handling, runtime behavior, and authorization before changing credentials.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow reads a personal access token from a local path and sends it to GitHub’s API; the security analysis is partial.

Mitigation: Keep the full token out of command output, logs, and chat; rotate it if exposed, and confirm its value is sent only to the intended GitHub API endpoint.

Risk: A single failed request or runtime can lead to a mistaken conclusion that a token is revoked or expired.

Mitigation: Check environment propagation and validate the same token with an independent client before investigating token state.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/haiyangchenbj/skills/github-pat-debugging)
- [GitHub authenticated user endpoint](https://api.github.com/user)
- [Token Failure Mode Decision Tree](references/token-failure-modes.md)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, API calls, Configuration instructions]

**Output Format:** [Markdown with inline shell, JavaScript, and API examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Troubleshooting steps and verification guidance; never print a full personal access token.]

## Skill Version(s):

1.0.8 (source: SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
