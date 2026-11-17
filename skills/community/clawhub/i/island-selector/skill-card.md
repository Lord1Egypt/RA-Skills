## Description:

A Chinese-language island travel assistant that recommends beach destinations from step-by-step traveler preferences and can retrieve Fliggy product links after the selection flow is complete.

This skill is ready for commercial/non-commercial use.

## Publisher:

[amokay](https://clawhub.ai/user/amokay)

### License/Terms of Use:

MIT-0

## Use Case:

External travelers and travel advisors use this skill to collect trip preferences one step at a time, compare island destinations by budget, travel time, season, and activities, and receive two to four matched recommendations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may invoke a locally configured Fliggy CLI using trip text supplied during the conversation.

Mitigation: Use a pinned CLI version when possible, avoid global installation where practical, and invoke the CLI with structured arguments or validated inputs instead of shell-interpolated strings.

Risk: Product-link lookup may depend on local credentials and external Fliggy responses.

Mitigation: Review local credential configuration before enabling product lookup and allow the skill to fall back to destination recommendations when lookup is unavailable or fails.

## Reference(s):

- [全球海岛数据库](references/island-database.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown recommendations with optional product links and inline shell command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May call an optional locally configured flyai-cli after the five-step preference collection flow; falls back to recommendations when the CLI is unavailable or a product lookup fails.]

## Skill Version(s):

1.0.8 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
