## Description:

Security self-check for OpenClaw deployments that audits configuration and host security settings and reports PASS, WARN, FAIL, or SKIP results.

This skill is ready for commercial/non-commercial use.

## Publisher:

[guoqunabc](https://clawhub.ai/user/guoqunabc)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill to run a quick OpenClaw security audit covering gateway exposure, authentication, channel policies, configuration permissions, plaintext secrets, firewall state, SSH hardening, and exposed ports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security evidence says the bundled audit script can execute attacker-controlled Python from a crafted OpenClaw config.

Mitigation: Run only in manual review contexts as a low-privilege user and inspect openclaw.json before execution.

Risk: The security evidence says important firewall, SSH, or token-strength checks can be falsely reported as safe.

Mitigation: Treat PASS results as advisory and independently verify host firewall, SSH configuration, and token strength before relying on the report.

Risk: The skill includes sudo remediation commands that can affect host access.

Mitigation: Apply remediation as separate administrative steps only after backups, SSH access checks, and explicit user confirmation.

## Reference(s):

- [OpenClaw Security Check on ClawHub](https://clawhub.ai/guoqunabc/skills/openclaw-security-check)
- [Publisher profile: guoqunabc](https://clawhub.ai/user/guoqunabc)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Human-readable audit report or JSON from the bundled shell script, with Markdown guidance for remediation.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports ten security checks with PASS, WARN, FAIL, or SKIP status; optional remediation guidance requires user confirmation.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
