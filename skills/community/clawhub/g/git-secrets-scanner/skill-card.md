## Description: <br>
Guides agents and developers through scanning Git repositories and commits for leaked API keys, passwords, tokens, private keys, certificates, and environment files. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[guohongbin-git](https://clawhub.ai/user/guohongbin-git) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, security engineers, and release reviewers use this skill to choose and run Git secret-scanning tools, configure pre-commit or CI checks, and respond when leaked credentials are found. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Secret scan output can contain live credentials or sensitive repository details. <br>
Mitigation: Redact scan output before sharing it and revoke or rotate any exposed credentials immediately. <br>
Risk: History cleanup and force-push commands can disrupt collaborators or remove needed repository history. <br>
Mitigation: Run destructive cleanup only with backups, explicit approval, and team coordination. <br>
Risk: Installing scanners from untrusted sources can introduce supply-chain risk. <br>
Mitigation: Install referenced tools only from trusted upstream release channels. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/guohongbin-git/git-secrets-scanner) <br>
- [Gitleaks releases](https://github.com/gitleaks/gitleaks/releases) <br>
- [TruffleHog releases](https://github.com/trufflesecurity/trufflehog/releases) <br>
- [git-secrets repository](https://github.com/awslabs/git-secrets.git) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with bash, YAML, and TOML examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Instruction-only guidance; commands require a local Git repository and separately installed scanning tools.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
