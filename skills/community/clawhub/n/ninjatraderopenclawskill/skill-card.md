## Description:

Ninjatrader Dev provides a NinjaTrader 8 NinjaScript development reference for using directives, lifecycle state management, indicators, order management, compile errors, and deployment.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gmdeep](https://clawhub.ai/user/gmdeep)

### License/Terms of Use:

MIT

## Use Case:

Developers and engineers use this skill when creating, validating, migrating, or deploying NinjaTrader 8 NinjaScript strategies and indicators. It helps structure code, avoid common compile errors, and review deployment steps before changes are applied.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill includes SSH/SCP deployment examples that could copy or overwrite NinjaTrader strategy files on a remote machine if used without review.

Mitigation: Replace hostnames and paths with a user-approved destination, confirm the remote identity, check overwrite risk, and keep strategy activation or live trading as a separate approval step.

Risk: NinjaScript strategy or order-management guidance can affect trading behavior if applied directly to live strategies.

Mitigation: Compile and test changes in NinjaTrader 8 before deployment, review generated code manually, and require explicit approval before enabling strategies for live trading.

## Reference(s):

- [Source repository](https://github.com/GMDEEP/NinjatraderOpenClawSkill)
- [ClawHub skill page](https://clawhub.ai/gmdeep/skills/ninjatraderopenclawskill)
- [Publisher profile](https://clawhub.ai/user/gmdeep)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with C# snippets, checklist items, and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires user review before applying generated code, deployment commands, or trading-strategy changes.]

## Skill Version(s):

0.1.1 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
