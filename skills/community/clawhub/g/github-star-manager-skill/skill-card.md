## Description:

Manage GitHub stars with AI-powered categorization and cleanup. Use when a user wants to organize their starred repos into GitHub Lists, clean up stale/deprecated stars, export star data for analysis, or get stats about their GitHub stars. Supports semantic categorization via LLM and bulk operations (unstar, add-to-list).

This skill is ready for commercial/non-commercial use.

## Publisher:

[cosformula](https://clawhub.ai/user/cosformula)

### License/Terms of Use:


## Use Case:

Developers and GitHub users use this skill to export starred repositories, organize them into GitHub Lists, identify stale or deprecated projects, and perform confirmed bulk actions through the GitHub CLI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses the authenticated GitHub CLI to read starred repositories and modify GitHub Lists.

Mitigation: Install and run it only when the user is comfortable using the active GitHub CLI login for those account operations, and review proposed list changes before approval.

Risk: Unstarring repositories removes account data from the user's GitHub profile.

Mitigation: Export stars first and require explicit user confirmation before any unstar operation.

Risk: Curated GitHub Lists may expose repository interests if created publicly.

Mitigation: Request private lists when the user does not want curated lists to be public.

## Reference(s):

- [GitHub Classic Tokens](https://github.com/settings/tokens)
- [ClawHub Skill Page](https://clawhub.ai/cosformula/skills/github-star-manager-skill)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration]

**Output Format:** [Markdown with inline bash and JSON command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires an authenticated GitHub CLI session and jq; list modification requires GitHub user scope.]

## Skill Version(s):

0.1.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
