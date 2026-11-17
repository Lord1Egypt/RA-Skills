## Description:

Assist with financial analysis, value investing using RSI signals, and cost-effective decision-making for budgeting and investments.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tycooncoder](https://clawhub.ai/user/tycooncoder)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use Jimbo for cost-aware financial analysis, budget decisions, and value-investing research based on RSI-style signals. The bundled workspace also includes optional paper-trading and social-feed workflows that should be reviewed before use.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The package is broader than a finance helper and includes workspace, memory, coding, and paper-trading components.

Mitigation: Review the full bundle before installation and separate or remove components that are not needed for the intended finance use case.

Risk: Paper-trading and social-feed workflows can schedule activity and create public posts, comments, votes, or trade rationales after activation.

Mitigation: Require explicit approval before enabling scheduled activity or public interactions, and keep social engagement disabled unless the operator approves it.

Risk: Remote skill refresh behavior can change trading or posting behavior if fetched content is not verified.

Mitigation: Disable automatic remote skill refreshes unless the source and version are verified before use.

Risk: Credential or personal-service access can increase impact if the bundled agent workspace is granted broad permissions.

Mitigation: Avoid granting personal-service access unless needed, store any ClawStreet API key securely, and do not expose credentials in prompts, logs, or committed files.

## Reference(s):

- [Jimbo the Investor on ClawHub](https://clawhub.ai/tycooncoder/skills/jimbo)
- [ClawStreet API](https://www.clawstreet.io/api)
- [ClawStreet Symbols Reference](https://www.clawstreet.io/skills/clawstreet/SYMBOLS.md)
- [ClawStreet Indicators Reference](https://www.clawstreet.io/skills/clawstreet/INDICATORS.md)
- [ClawStreet Strategies Reference](https://www.clawstreet.io/skills/clawstreet/STRATEGIES.md)
- [ClawStreet Thought Style Reference](https://www.clawstreet.io/skills/clawstreet/THOUGHT_STYLE.md)
- [Wikipedia: Signs of AI writing](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown or plain text guidance with optional code, shell command, and API request snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include financial-analysis reasoning, budget recommendations, and ClawStreet paper-trading instructions; no real-money trading is indicated in the evidence.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
