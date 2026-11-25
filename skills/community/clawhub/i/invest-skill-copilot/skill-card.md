## Description:

Guides agents through stock-research workflows spanning company analysis, valuation, screening, industry, policy, macro, sentiment, and market reviews, with specified sourced Markdown and standalone HTML reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chenxyzcyxpp](https://clawhub.ai/user/chenxyzcyxpp)

### License/Terms of Use:

Apache-2.0

## Use Case:

External users can use it to structure stock-research requests, route them to relevant methodologies, and prepare reports with source and data-gap annotations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The advertised research and reporting capabilities do not match the reported executable behavior, and the scan does not establish that the skill performs the advertised analysis.

Mitigation: Review and manually verify the analysis and report workflow before relying on its outputs.

Risk: Catalog synchronization and request routing are identified as concerns in the security guidance.

Mitigation: Check catalog freshness and confirm that the selected methodology matches the user's request before using a report.

Risk: The skill image was not fully inspected.

Mitigation: Review the image before distributing the skill.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/chenxyzcyxpp/skills/invest-skill-copilot)
- [invest-skill methodology repository (listed in the skill)](https://gitee.com/warwickInv/invest-skill)
- [Data discipline](references/data-discipline.md)
- [Methodology map](references/methodology-map.md)
- [Capability catalog](references/capability-catalog.md)

## Skill Output:

**Output Type(s):** [Markdown, HTML, Structured data]

**Output Format:** [Markdown and standalone HTML research reports, with structured result data]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports are specified to include sources, timestamps, data gaps, and an investment disclaimer; HTML is intended to be self-contained and usable offline.]

## Skill Version(s):

1.1.6 (source: SKILL.md frontmatter, server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
