## Description: <br>
ProdShield gives agents conservative execution guardrails for production systems, destructive operations, deployments, dependency installs, credential handling, and supply-chain-sensitive workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[2eux](https://clawhub.ai/user/2eux) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operators, and agent users use this skill to slow down risky execution paths before production changes, destructive commands, deployments, dependency installs, or credential-sensitive git operations. It helps agents ask for confirmation, prefer dry runs, and surface rollback or recovery steps before irreversible actions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Conservative guardrails may add extra confirmation steps before legitimate risky commands. <br>
Mitigation: Use the skill where production, credentials, destructive commands, deployments, or dependency installs need explicit human review. <br>
Risk: Optional scanner, pre-commit hook, or git history rewrite commands can affect a real repository if run without review. <br>
Mitigation: Review proposed commands first, prefer dry runs or backups where available, and confirm repository scope before execution. <br>
Risk: Instruction-only guardrails depend on the host agent following the skill consistently. <br>
Mitigation: Pair the skill with platform controls such as protected branches, secret scanning, approval rules, and least-privilege credentials. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/2eux/prod-shield) <br>
- [ClawHub homepage](https://clawhub.ai) <br>
- [Dangerous Commands Reference](references/dangerous-commands.md) <br>
- [Environment Detection Patterns](references/environment-patterns.md) <br>
- [Git & GitHub Credential Safety Reference](references/git-credential-safety.md) <br>
- [Recovery Playbook](references/recovery-playbook.md) <br>
- [Gitleaks](https://github.com/gitleaks/gitleaks) <br>
- [detect-secrets](https://github.com/Yelp/detect-secrets) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with inline code blocks and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Instruction-only output; no external binaries are required by the skill itself.] <br>

## Skill Version(s): <br>
1.2.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
