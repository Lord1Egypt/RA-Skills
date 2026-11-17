## Description:

Prosperity Investing Framework guides an agent through a cyclical growth stock analysis workflow covering industry lifecycle, four-wave timing, stock classification, selection discipline, and report archiving.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pcchris1995](https://clawhub.ai/user/pcchris1995)

### License/Terms of Use:

MIT-0

## Use Case:

External users can use this skill to apply an opinionated stock-analysis framework for industry-cycle screening, candidate stock classification, buy/sell discipline, and structured research-report processing. The workflow is educational and analytical, not personalized financial advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can update persistent investment tracking files and stock pools.

Mitigation: Require explicit user confirmation before any file write, stock-pool change, or tracking-record update.

Risk: External reports, links, or user-provided research can influence investment analysis.

Mitigation: Confirm before processing external material and preserve source filenames, URLs, and dates in generated analysis.

Risk: The framework uses trading language that could be mistaken for personalized financial advice.

Mitigation: Present outputs as educational analysis, require user review, and avoid treating generated conclusions as investment instructions.

## Reference(s):

- [Detailed Framework](artifact/references/detailed-framework.md)
- [Four Waves](artifact/references/four-waves.md)
- [Lifecycle Rules](artifact/references/lifecycle-rules.md)
- [Selection Criteria](artifact/references/selection-criteria.md)
- [Quarter-One Rule](artifact/references/quarter-one-rule.md)
- [Case Studies](artifact/references/case-studies.md)
- [Stock Classification](artifact/references/stock-classification.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance, configuration]

**Output Format:** [Markdown analysis with tables, checklists, structured conclusions, and optional local investment tracking updates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Chinese-language framework content; persistent investment file or stock-pool changes should require explicit user confirmation.]

## Skill Version(s):

1.1.1 (source: server release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
