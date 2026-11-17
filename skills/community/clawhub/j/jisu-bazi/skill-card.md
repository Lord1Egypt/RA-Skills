## Description:

Generates a Bazi (Four Pillars) chart from birth date/time and city using JisuAPI, returning pillars, Nayin, major luck cycles, and annual luck data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jisuapi](https://clawhub.ai/user/jisuapi)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to turn birth details into Bazi chart data and agent-readable summaries for entertainment and learning reference.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends entered name or alias, city, sex, and birth date/time to JisuAPI with the configured API key.

Mitigation: Use an alias when possible, disclose the external API call, and avoid using the skill in conversations where these personal details should not leave the agent environment.

Risk: The external API key may be exposed or abused if handled carelessly.

Mitigation: Store JISU_API_KEY in the environment, restrict and rotate it where provider controls allow, and avoid logging command lines or outputs that contain credentials.

Risk: Bazi interpretations can be mistaken for decision guidance.

Mitigation: Present results as entertainment and learning reference only, and avoid framing outputs as a basis for financial, medical, legal, employment, or relationship decisions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jisuapi/skills/jisu-bazi)
- [JisuAPI Bazi API documentation](https://www.jisuapi.com/api/bazi/)
- [JisuAPI](https://www.jisuapi.com/)
- [Bazi paipan API endpoint](https://api.jisuapi.com/bazi/paipan)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [JSON data from the helper script, typically summarized as Markdown or plain text by the agent]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3 and JISU_API_KEY; sends user-provided birth details to JisuAPI.]

## Skill Version(s):

1.0.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
