## Description:

Generates Xiaohongshu trending topic ideas and content concepts for brand social media operations, content planning, and trend-based marketing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yyobject](https://clawhub.ai/user/yyobject)

### License/Terms of Use:


## Use Case:

Brand social media operators, content planners, and marketing teams use this skill to research Xiaohongshu activity and produce 5-10 data-supported hot topic briefs for campaign planning.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated reports may load mutable third-party JavaScript from the Tailwind CDN.

Mitigation: Remove, pin, or vendor the styling dependency before using reports in controlled or offline environments.

Risk: Derived keywords, brand context, and fallback searches may disclose confidential campaign strategy to ChatDAM or search providers.

Mitigation: Review inputs for sensitivity, obtain approval for outbound data use, and avoid confidential brand or agency material unless those data flows are acceptable.

Risk: Trend and note data can be incomplete or weakly scoped, which may lead to misleading content recommendations.

Mitigation: Require human review of the report, verify data sources, and label recommendations based on assumptions when API evidence is insufficient.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yyobject/skills/hot-topic-ideator)
- [ChatDAM note search API](https://asset.tezign.com/chatdam/api/notes/search?keyword=[ENCODED_KEYWORD])
- [ChatDAM note detail API](https://asset.tezign.com/chatdam/api/notes/detail?noteId=[NOTE_ID])
- [ChatDAM hot trends API](https://asset.tezign.com/chatdam/api/hot-trends?limit=20)
- [Tailwind CSS CDN](https://cdn.tailwindcss.com)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [HTML report content with shell commands and PDF conversion guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces a single-file HTML report intended to be converted to PDF; generated reports may reference Tailwind CSS from a CDN unless adjusted.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
