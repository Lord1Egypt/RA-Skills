## Description: <br>
Complete MoltMarkets trading agent setup with autonomous trader, market creator, and resolution crons. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[shirtlessfounder](https://clawhub.ai/user/shirtlessfounder) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to configure an autonomous MoltMarkets agent that can trade, create markets, resolve markets, and maintain memory files for learning loops. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Autonomous recurring jobs can make real MoltMarkets account changes, including trades, market creation, comments, and resolutions. <br>
Mitigation: Use a low-balance or test account, review each cron definition before enabling it, and keep notifications or logs enabled. <br>
Risk: Stored MoltMarkets credentials can authorize account actions if exposed or reused outside the intended environment. <br>
Mitigation: Protect the credentials file and restrict the API key where the platform allows it. <br>
Risk: Automatic market resolution can produce incorrect or hard-to-reverse outcomes. <br>
Mitigation: Avoid enabling automatic resolution unless the user accepts that risk and has reviewed the resolution criteria and oracle behavior. <br>


## Reference(s): <br>
- [MoltMarkets Trading Agent on ClawHub](https://clawhub.ai/shirtlessfounder/moltmarkets-trading) <br>
- [MoltMarkets API Reference](references/api-reference.md) <br>
- [Cron Job Definitions](references/cron-definitions.md) <br>
- [Kelly Criterion Guide](references/kelly-formula.md) <br>
- [Memory File Templates](references/memory-templates.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline shell, JavaScript, and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces setup instructions, cron definitions, memory templates, and configuration guidance for autonomous MoltMarkets agents.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
