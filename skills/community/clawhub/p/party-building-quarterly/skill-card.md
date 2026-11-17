## Description:

Generates Chinese-language quarterly party-building and government affairs summaries by collecting recent Xi Jinping speeches, Qiushi articles, central meetings, and source links into a fixed Markdown report.

This skill is ready for commercial/non-commercial use.

## Publisher:

[whitetin](https://clawhub.ai/user/whitetin)

### License/Terms of Use:

MIT-0

## Use Case:

Employees or analysts preparing Chinese-language party-building reports can use this skill to gather public-source material from official Chinese party and government outlets, summarize quarterly themes, and produce a citation-linked report.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated citations, quoted excerpts, or example links may be stale, future-dated, or otherwise unsuitable for publication.

Mitigation: Review all source links, quotations, dates, and claims against authoritative sources before using the report.

Risk: The skill depends on a separate summarize CLI for Qiushi article summaries, which can affect output completeness or accuracy if unavailable or misconfigured.

Mitigation: Confirm the summarize CLI is installed and review generated summaries before relying on them.

Risk: Chinese-language political reporting is context-sensitive and may require careful terminology and framing.

Mitigation: Have a qualified reviewer check terminology, citations, and conclusions for the intended audience.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/whitetin/skills/party-building-quarterly)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown report with tables, sectioned summaries, source links, quoted excerpts, and keyword lists]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Chinese-language output; expects source-link review and uses a separate summarize CLI for Qiushi article summaries.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
