## Description:

A Chinese-language product comparison skill that helps compare features, prices, sales signals, reputation, and user feedback to produce detailed comparison reports and purchase recommendations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[josephyb97](https://clawhub.ai/user/josephyb97)

### License/Terms of Use:

MIT

## Use Case:

External users and shopping researchers use this skill to compare multiple products across price, features, sales signals, reputation, and real-user feedback. It is intended to support purchase decisions, product reviews, and competitive product analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Web search results, seller claims, prices, and review content may be inaccurate, outdated, promotional, or low quality.

Mitigation: Verify prices, source quality, seller claims, and user-review credibility before relying on recommendations.

Risk: Broad Chinese trigger phrases may activate the skill for general recommendation requests beyond product comparison.

Mitigation: Confirm that the user is asking for a product comparison, purchase recommendation, product review, or competitive analysis before applying the workflow.

Risk: External review platforms may be unavailable or incomplete during research.

Mitigation: State unavailable information clearly, avoid fabricating links or findings, and separate official claims from observed user feedback.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/josephyb97/skills/product-compare)
- [Xiaohongshu Explore](https://www.xiaohongshu.com/explore)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Guidance]

**Output Format:** [Markdown comparison report with tables and recommendation bullets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include product comparison tables, source-qualified findings, limitations when information is unavailable, and segmented purchase recommendations.]

## Skill Version(s):

1.0.0 (source: package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
