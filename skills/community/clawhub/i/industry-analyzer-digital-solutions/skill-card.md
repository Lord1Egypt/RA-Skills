## Description:

Analyzes digital transformation solutions for a given industry across Huawei, Alibaba, Baidu, Tencent, and vertical industry solution providers, including products, positioning, differentiation, and customer examples.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zrxparley](https://clawhub.ai/user/zrxparley)

### License/Terms of Use:

MIT-0

## Use Case:

Industry analysts, consultants, and agent workflows use this skill to produce the digital-solutions step of an industry analysis. It writes a Markdown analysis covering the four major vendors and at least three vertical providers, then updates the analysis session state.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The generated industry analysis may contain outdated or unsupported vendor claims.

Mitigation: Review generated claims and sources before relying on the analysis.

Risk: The skill writes analysis output and session state under the relevant output/{industry-slug} directory.

Mitigation: Run it in the intended workspace and review file changes before publishing or sharing results.

## Reference(s):

- [Major vendors search checklist](references/major-vendors-list.md)
- [ClawHub skill page](https://clawhub.ai/zrxparley/skills/industry-analyzer-digital-solutions)
- [Publisher profile](https://clawhub.ai/user/zrxparley)

## Skill Output:

**Output Type(s):** [text, markdown, configuration]

**Output Format:** [Markdown analysis file plus session state update]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates or updates output/{industry-slug}/03-digital-solutions.md and output/{industry-slug}/session.json.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
