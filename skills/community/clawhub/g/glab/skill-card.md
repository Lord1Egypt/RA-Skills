## Description:

GitLab CLI for managing issues, merge requests, CI/CD pipelines, and repositories.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bezkom](https://clawhub.ai/user/bezkom)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to operate GitLab workflows from an agent-assisted command line, including issues, merge requests, CI/CD pipelines, repositories, and self-hosted GitLab instances.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires a GitLab token and can guide state-changing GitLab operations.

Mitigation: Use a narrowly scoped, project-level or read-only token where possible and review proposed commands before execution.

Risk: Bundled scripts may receive unsafe unvalidated numeric inputs.

Mitigation: Validate MR numbers, timeouts, and polling intervals before running scripts, especially when values come from prompts or repository text.

Risk: Troubleshooting guidance can expose tokens or weaken TLS security.

Mitigation: Do not print tokens to the terminal and do not disable TLS verification in an authenticated session.

## Reference(s):

- [glab API Advanced Reference](references/api-advanced.md)
- [glab Commands Detailed Reference](references/commands-detailed.md)
- [glab Troubleshooting Guide](references/troubleshooting.md)
- [GitLab REST API](https://docs.gitlab.com/ee/api/)
- [GitLab CLI Documentation](https://docs.gitlab.com/editor_extensions/gitlab_cli/)
- [ClawHub Skill Page](https://clawhub.ai/bezkom/skills/glab)

## Skill Output:

**Output Type(s):** [guidance, markdown, shell commands, configuration]

**Output Format:** [Markdown with inline bash code blocks and command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose authenticated GitLab CLI and API commands that should be reviewed before execution.]

## Skill Version(s):

1.0.4 (source: server release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
