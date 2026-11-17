## Description:

Use this skill when the user wants to discover new LooLoo tokens, inspect token activity, or review current positions from OpenClaw.

This skill is ready for commercial/non-commercial use.

## Publisher:

[looloolol](https://clawhub.ai/user/looloolol)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to scan LooLoo internal-market tokens, review a selected token's recent trades and top holders, and check authenticated wallet positions through OpenClaw.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Wallet-position queries may reveal authenticated account information in the chat.

Mitigation: Use wallet-position lookup only when the user asks for it, summarize narrowly, and keep raw JSON available only when needed.

Risk: Token discovery and activity summaries may be misread as guaranteed returns or financial advice.

Mitigation: Frame results as discovery and execution support, and do not imply guaranteed profits.

Risk: The workflow depends on the bundled openclaw-looloo plugin tools.

Mitigation: Confirm trust in the plugin before installing or using the skill.

## Reference(s):


## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Concise markdown or plain-text summaries, with raw JSON available when needed]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include token activity signals, top-holder summaries, and authenticated wallet-position information returned by the trusted OpenClaw plugin.]

## Skill Version(s):

0.1.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
