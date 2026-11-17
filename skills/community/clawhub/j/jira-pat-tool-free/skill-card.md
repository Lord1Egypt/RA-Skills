## Description:

Jira PAT 管理基础版 helps agents manage issues in self-hosted Jira instances with a personal access token, including issue lookup, JQL search, status transitions, comments, field updates, and issue creation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, project maintainers, and individual Jira users use this skill to inspect and update self-hosted Jira issues through an agent when PAT-based Jira API access is needed, including SSO/SAML environments.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can make live Jira changes, including status transitions, comments, field updates, and issue creation.

Mitigation: Use a least-privilege Jira PAT, point it only at the intended Jira instance, and review write actions before execution.

Risk: The security summary says trigger and data-flow guidance are broad or unclear, which may lead to use outside explicit Jira work.

Mitigation: Use the skill only for Jira-related requests and avoid treating it as a general reporting or analytics helper.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thcjp/skills/jira-pat-tool-free)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration guidance, API calls]

**Output Format:** [Markdown with inline shell commands and Jira API results in text, JSON, or CSV]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include Jira issue data and proposed or executed live Jira changes.]

## Skill Version(s):

1.0.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
