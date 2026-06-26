## Description: <br>
Security audit for multi-tenant OpenClaw Telegram bots that checks workspace isolation, filesystem sandboxing, session scoping, auth separation, error leaking, and other multi-user security concerns. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[PHY041](https://clawhub.ai/user/PHY041) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and security reviewers use this skill to audit public or multi-user OpenClaw Telegram bot deployments for tenant isolation, session scoping, auth separation, error handling, and related deployment risks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Audit snippets may inspect or help modify local bot configuration and examples discuss sensitive auth/profile files. <br>
Mitigation: Run remediation steps only in intended bot repositories, review changes before deploying, and avoid exposing sensitive auth/profile files. <br>
Risk: The skill is a documentation-style audit aid rather than a runtime security boundary. <br>
Mitigation: Use it as review guidance alongside deployment review and scanning; rely on platform isolation controls for enforcement. <br>


## Reference(s): <br>
- [OpenClaw Gateway Security](https://docs.openclaw.ai/gateway/security) <br>
- [Canlah AI homepage](https://canlah.ai) <br>
- [ClawHub skill release](https://clawhub.ai/PHY041/phy-openclaw-multibot-audit) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration] <br>
**Output Format:** [Markdown checklist with inline code and shell command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes PASS/FAIL/N/A audit items and remediation examples for OpenClaw bot deployments.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata and SKILL.md metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
