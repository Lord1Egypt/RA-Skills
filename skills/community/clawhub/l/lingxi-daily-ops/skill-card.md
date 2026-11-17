## Description:

Complete daily operations automation for GitHub projects, including automated GitHub interactions, daily report generation, trending watch, and multi-platform social publishing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nima54851](https://clawhub.ai/user/nima54851)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and project maintainers use this skill to automate recurring GitHub operations, monitor trending projects, generate daily Markdown reports, run health checks, and publish operational digests to configured channels.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can automate public GitHub actions under the user's identity and asks for broad GitHub account access.

Mitigation: Use a fine-grained, least-privilege token or GitHub App credential, review target repositories and publishing channels, and require dry-run or manual approval before scheduled runs.

Risk: The documented configuration stores a GitHub token in a local JSON file.

Mitigation: Avoid plaintext token storage where possible and restrict configuration file permissions.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and JSON configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces operational reports, scheduled workflow guidance, trigger commands, and configuration guidance for GitHub and social publishing automation.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
