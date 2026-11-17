## Description:

Provides a paid Juhe birth-chart lookup that returns Chinese calendrical, zodiac, Four Pillars, and five-elements information from a confirmed Gregorian birth date and birth hour.

This skill is ready for commercial/non-commercial use.

## Publisher:

[juhemcp](https://clawhub.ai/user/juhemcp)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to query paid birth-chart, lunar-calendar, zodiac, and five-elements information for a specific Gregorian birth date and birth hour. Agents should use it only after user consent to the paid Alipay workflow and the required data transfer to Juhe.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The documented setup path may run payment tooling with an unpinned `@latest` npm package.

Mitigation: Install only after reviewing the package source and prefer a pinned, reviewed version instead of `@latest`.

Risk: The skill involves paid Alipay flow and sends birth date and birth hour details to Juhe.

Mitigation: Proceed only after clear user consent, collect only the required date and hour fields, and cancel without calling the API when consent or required parameters are missing.

Risk: Birth-chart and five-elements results can be mistaken for reliable decision advice.

Mitigation: Present results as entertainment-only content and avoid medical, financial, legal, career, or relationship recommendations based on the output.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/juhemcp/skills/juhe-birth-eight-a2a)
- [Juhe A2A query endpoint](https://apis.juhe.cn/a2a/query)

## Skill Output:

**Output Type(s):** [API Calls, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown birth-chart report with payment and setup guidance that may include shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses only returned API fields for the final report and includes an entertainment-only disclaimer.]

## Skill Version(s):

1.0.7 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
