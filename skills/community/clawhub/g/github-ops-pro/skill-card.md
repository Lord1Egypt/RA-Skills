## Description:

Github Ops helps an agent create GitHub repositories, push code, update repository files, and create releases with a configured GitHub token.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shenghoo123-png](https://clawhub.ai/user/shenghoo123-png)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to automate GitHub repository operations, including repository creation, code pushes, README updates, and release creation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can give an agent broad unattended authority to create repositories, push code, and create releases.

Mitigation: Require explicit approval before repository creation, public pushes, release creation, or deployment-triggering changes.

Risk: Stored GitHub credentials may be used unsafely, including in token-in-URL git remotes.

Mitigation: Use narrowly scoped, revocable GitHub credentials and avoid embedding tokens in git remote URLs.

Risk: Broad add-and-push workflows can publish unintended files or secrets.

Mitigation: Use reviewed file allowlists and secret scanning before commits and pushes.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/shenghoo123-png/skills/github-ops-pro)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash and API examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires git, curl, and GITHUB_TOKEN according to ClawHub metadata.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
