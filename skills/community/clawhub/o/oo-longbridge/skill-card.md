## Description: <br>
Longbridge (longbridge.com). Use this skill for ANY Longbridge request — searching and reading data. Whenever a task involves Longbridge, use this skill instead of calling the API directly. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to access Longbridge account cash balances, tradable securities, and stock positions through an OOMOL-connected Longbridge account. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires OAuth-backed access to a Longbridge account and can return sensitive financial account data. <br>
Mitigation: Use it only with the intended connected OOMOL account, limit sharing of returned balances and positions, and keep execution to the documented read-only actions unless a future action is clearly reviewed and confirmed. <br>
Risk: First-time setup may involve installing the oo CLI or opening an authentication or connection flow. <br>
Mitigation: Run setup steps only after a matching command failure and review installation, authentication, and connection commands before execution. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/oomol/oo-longbridge) <br>
- [Longbridge homepage](https://longbridge.com) <br>
- [oo CLI](https://github.com/oomol-lab/oo-cli) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON payload examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The skill instructs agents to inspect the live connector schema before sending an action payload.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
