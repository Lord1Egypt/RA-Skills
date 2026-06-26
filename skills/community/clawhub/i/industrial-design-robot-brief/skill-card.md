## Description: <br>
Finds recent humanoid-robot papers and turns them into Chinese briefs for industrial designers, prioritizing design impact, user experience, and product-definition relevance over pure academic popularity. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhuqing98](https://clawhub.ai/user/zhuqing98) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Industrial designers, UX designers, and product teams use this skill to identify recent humanoid-robot papers and receive concise Chinese briefs that connect paper findings to form, packaging, interaction, trust, and product-definition decisions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Briefs may contain unverified paper metadata or design interpretations that go beyond the source paper. <br>
Mitigation: Verify arXiv IDs, DOIs, titles, dates, authors, and numerical claims; mark unknowns explicitly and keep paper facts separate from design judgments. <br>
Risk: The skill may update a shared Feishu document. <br>
Mitigation: Confirm the exact Feishu document and insertion location before granting document access or applying updates. <br>
Risk: A recency-based workflow can select weak or irrelevant papers when the candidate pool is small. <br>
Mitigation: Use approved paper sources, explicit date ranges, and the design-impact criteria; exclude unverified papers from the top set. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zhuqing98/industrial-design-robot-brief) <br>
- [Sources](references/sources.md) <br>
- [Translator](references/translator.md) <br>
- [Template](references/template.md) <br>
- [Formatter](references/formatter.md) <br>
- [Quality Check](references/quality-check.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Chinese Markdown brief with tables, links, ratings, and clearly labeled uncertainty] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Defaults to five recent papers for the prior local day and appends the newest brief to a Feishu document when document access is available.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
