## Description:

Mystilink Ziwei builds Zi Wei Dou Shu twelve-palace charts with major stars and optional Si Hua, then supports Wiki-grounded readings for Zi Wei, twelve-palace, and Si Hua questions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mystilink-ai](https://clawhub.ai/user/mystilink-ai)

### License/Terms of Use:

MIT

## Use Case:

External users and agents use this skill to calculate Zi Wei Dou Shu charts from birth datetime, timezone, and gender, then produce readings that separate chart facts from Wiki-based interpretation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Birth datetime, timezone, gender, and optional location data are sensitive personal inputs.

Mitigation: Collect only the fields needed for chart calculation and avoid sending full birth profiles to the optional Wiki workflow unless the user intentionally requests it.

Risk: Wiki lookup may involve external network use.

Mitigation: Use minimal derived lookup terms for Wiki API requests and keep chart facts separate from interpretation in the response.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mystilink-ai/skills/mystilink-ziwei-skill)
- [Server-resolved GitHub provenance](https://github.com/mystilink-ai/mystilink-ziwei-skill)
- [Mystilink Wiki search API](https://wiki.mystilink.com/api/v1/search?q=life+palace&system=ziwei&locale=en)
- [Mystilink Wiki Ming Gong page API](https://wiki.mystilink.com/api/v1/pages/ziwei.concept.ming-gong?locale=en)
- [ziwei skill reference](references/overview.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance, JSON]

**Output Format:** [Markdown guidance with shell command examples and JSON chart output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires birth datetime, IANA timezone, and gender; optional longitude, Si Hua year, midnight-zi setting, and Wiki API lookup.]

## Skill Version(s):

0.1.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
