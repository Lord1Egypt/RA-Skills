## Description:

Guides agents and developers through scanning Git repositories for leaked API keys, passwords, tokens, private keys, certificates, and environment files using tools such as Gitleaks, TruffleHog, and git-secrets.

This skill is ready for commercial/non-commercial use.

## Publisher:

[guohongbin-git](https://clawhub.ai/user/guohongbin-git)

### License/Terms of Use:


## Use Case:

Developers, security engineers, and agent operators use this skill to select and run Git secret-scanning workflows before commits, during CI, across repository history, and during incident response for leaked credentials.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent hooks or scheduled scans can create ongoing automatic execution in local repositories.

Mitigation: Enable hooks or cron jobs only after reviewing the exact commands, paths, and expected execution cadence.

Risk: Privileged or unpinned installs can install unexpected versions or require elevated access.

Mitigation: Pin tool and action versions, prefer package-manager or vendor-documented installs, and avoid sudo installs where practical.

Risk: Git history rewrites and force pushes can disrupt collaborators or lose history during incident response.

Mitigation: Back up repositories, coordinate with the team, rotate exposed credentials first, and treat BFG plus git push --force as a controlled incident-response step.

## Reference(s):

- [Gitleaks releases](https://github.com/gitleaks/gitleaks/releases)
- [TruffleHog releases](https://github.com/trufflesecurity/trufflehog/releases)
- [git-secrets repository](https://github.com/awslabs/git-secrets.git)
- [ClawHub skill page](https://clawhub.ai/guohongbin-git/skills/git-secrets-scanner)
- [ClawHub publisher profile](https://clawhub.ai/user/guohongbin-git)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with bash, YAML, TOML, and plain-text examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes scanner command examples, CI workflow snippets, hook setup guidance, remediation steps, and sample scanner output.]

## Skill Version(s):

1.0.0 (source: package.json, server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
