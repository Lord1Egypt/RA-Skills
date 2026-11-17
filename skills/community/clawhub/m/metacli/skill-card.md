## Description:

Meta Marketing CLI for authentication lifecycle, Graph API requests, campaign/ad/adset writes, insights reporting, and Instagram publishing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bilalbayram](https://clawhub.ai/user/bilalbayram)

### License/Terms of Use:


## Use Case:

Developers, marketers, and operators use this skill to run Meta ads, Graph API, insights, OAuth setup, and Instagram publishing workflows from terminal commands while keeping a human involved for sensitive authentication and spend-changing actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill installs an unpinned third-party CLI that can handle Meta app secrets and OAuth tokens.

Mitigation: Install only after reviewing the upstream source, prefer a pinned reviewed version or commit, and use least-privilege Meta scopes.

Risk: The skill can perform account-changing actions, including campaign creation, budget changes, and Instagram publishing.

Mitigation: Keep campaigns paused until reviewed, require explicit confirmation for spend-affecting changes, and confirm public posts before execution.

Risk: Commands may include sensitive values such as app secrets, access tokens, redirect URIs, account IDs, or media publishing inputs.

Mitigation: Do not echo secrets in logs or shared outputs, and validate required IDs, redirect URIs, paths, and payload fields before running commands.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/bilalbayram/skills/metacli)
- [metacli GitHub repository](https://github.com/bilalbayram/metacli)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration]

**Output Format:** [Markdown with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May guide JSON or JSONL output from the underlying CLI for automation.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
