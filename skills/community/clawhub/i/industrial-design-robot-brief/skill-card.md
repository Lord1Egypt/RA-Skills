## Description:

Finds recent humanoid-robot papers and turns them into Chinese briefs for industrial designers, prioritizing design impact, user experience, and product-definition relevance over pure academic popularity.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhuqing98](https://clawhub.ai/user/zhuqing98)

### License/Terms of Use:

MIT-0

## Use Case:

Industrial designers, UX designers, and product teams use this skill to collect recent humanoid-robot papers, rank them by design relevance, and receive concise Chinese daily briefs. The skill emphasizes verified paper facts, explicit uncertainty markers, and separated design judgments for form, layout, user trust, and product definition.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated content may be appended to an external Feishu document without clear target-document scoping.

Mitigation: Specify the exact Feishu document before use and require approval before each update.

Risk: Implicit invocation could update or prepare content for the wrong briefing workflow.

Mitigation: Review whether implicit invocation should remain enabled for the deployment context.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/zhuqing98/skills/industrial-design-robot-brief)
- [Skill Definition](artifact/SKILL.md)
- [Sources](artifact/references/sources.md)
- [Translator](artifact/references/translator.md)
- [Template](artifact/references/template.md)
- [Formatter](artifact/references/formatter.md)
- [Quality Check](artifact/references/quality-check.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Feishu-compatible Markdown daily brief in Chinese]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Typically selects five recent papers, ranks them by design impact, includes verification notes, and appends the newest daily section below the pinned Feishu header.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
