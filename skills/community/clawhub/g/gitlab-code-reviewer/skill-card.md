## Description:

Performs structured code reviews on GitLab merge requests by fetching diffs, applying review guidelines, generating engineering feedback, and optionally posting inline comments through the GitLab API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[neuyazvimyi](https://clawhub.ai/user/neuyazvimyi)

### License/Terms of Use:


## Use Case:

Developers and engineering teams use this skill to review GitLab merge request diffs for correctness, security, performance, maintainability, and framework-specific issues. It can provide a severity-grouped review summary and, when explicitly permitted by token scope, post inline MR comments.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may expose a GitLab token to a host derived from the merge request URL.

Mitigation: Use a least-privilege, short-lived token; avoid untrusted or http MR URLs; and validate that the MR host matches the configured GitLab origin before use.

Risk: The skill can post review comments using the user's GitLab account when write scope is available.

Mitigation: Use read_api scope for analysis-only reviews, run the token capability check first, and post comments only after reviewing the generated findings.

## Reference(s):

- [Code Review Guidelines](references/review-guidelines.md)
- [ClawHub skill page](https://clawhub.ai/neuyazvimyi/skills/gitlab-code-reviewer)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown review summary with optional JSON comment payloads and GitLab inline comments]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Inline posting requires a configured GitLab token with write scope; read-only tokens support analysis without posting comments.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
