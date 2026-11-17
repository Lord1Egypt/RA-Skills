## Description:

Generates Chinese marketing-calendar campaign concepts from brand information, scores them with a five-part rubric, and writes a visual HTML report.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cocokkxy](https://clawhub.ai/user/cocokkxy)

### License/Terms of Use:

MIT

## Use Case:

Marketing teams and brand planners use this skill to turn a brand name and brand profile into seasonal campaign ideas tied to major calendar moments. It is intended for Chinese-language marketing-calendar planning and produces only activities that meet the skill's minimum scoring threshold.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Incomplete brand information may be supplemented through web search.

Mitigation: Avoid entering confidential brand strategy unless web-based enrichment is acceptable.

Risk: Generated campaign plans may include unsuitable or inaccurate marketing recommendations.

Mitigation: Review the activity concepts, scoring, and HTML report before using them for customer-facing campaigns.

Risk: The skill writes a local file named marketing_calendar_report.html.

Mitigation: Run it in a workspace where creating or replacing that report file is acceptable.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/cocokkxy/skills/marketing-calendar)
- [Skill definition](artifact/SKILL.md)
- [Marketing calendar workflow](artifact/marketing-calendar.md)

## Skill Output:

**Output Type(s):** [text, code, guidance]

**Output Format:** [Plain text campaign concepts plus a local HTML report]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Filters out campaign concepts below the configured minimum score, defaulting to 80.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
