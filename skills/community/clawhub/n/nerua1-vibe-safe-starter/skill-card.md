## Description:

Provides a minimal security starter pack for AI-generated code projects, including dependency audit and package vetting scripts for common vulnerability, maintenance, credential, and supply-chain checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nerua1](https://clawhub.ai/user/nerua1)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to add lightweight security checks to AI-generated application projects before installing dependencies or deploying code. It is aimed at quick local and CI-oriented review rather than comprehensive security assurance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The audit helper can modify project state and may rely on local package manager behavior or external tools.

Mitigation: Run it only on a clean git working tree, review any changed files and command output, and avoid elevated privileges.

Risk: A final CLEAN result may be misleading if npm audit, pip-audit, gitleaks, or fallback checks miss vulnerabilities or secrets.

Mitigation: Install and run the underlying security tools directly when possible, manually review their output, and treat this starter as a first-pass check.

Risk: Package vetting uses live registry and vulnerability service responses, so network failures or stale service data can affect results.

Mitigation: Re-run checks before installation and compare results with registry, OSV, and project maintenance information.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/nerua1/skills/nerua1-vibe-safe-starter)
- [ClawHub Publisher Profile](https://clawhub.ai/user/nerua1)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and script output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces human-reviewed setup and audit guidance; results depend on local project files and available security tools.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
