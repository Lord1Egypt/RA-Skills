## Description:

Generates Chinese-language entertainment lottery-number recommendations for 双色球 or 大乐透 by deriving Meihua Yishu hexagrams from the current hour and mapping them to lottery numbers.

This skill is ready for commercial/non-commercial use.

## Publisher:

[eamonnn101](https://clawhub.ai/user/eamonnn101)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill for Chinese-language entertainment lottery-number generation based on Meihua Yishu time divination. The skill is intended to present the result as random entertainment with a gambling-risk disclaimer, not as financial advice or a prediction.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Users may treat lottery-number output as financial advice or as a reliable prediction.

Mitigation: Present the output as random entertainment, include the skill's disclaimer, and keep spending guidance conservative.

Risk: The skill may activate on broad Chinese number-picking phrases.

Mitigation: Confirm the user wants entertainment lottery-number generation and ask for 双色球 or 大乐透 when the lottery type is unclear.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/eamonnn101/skills/lottery-divination)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Chinese Markdown response with lottery numbers, brief divination notes, and a disclaimer; the local script emits JSON before the agent formats it.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [For the same lottery type within the same hour, outputs are deterministic because the skill uses the current hour as the generation seed.]

## Skill Version(s):

1.0.1 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
