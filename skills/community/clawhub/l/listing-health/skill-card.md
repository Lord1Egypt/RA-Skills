## Description:

检查 Amazon Listing 的信息完整度、潜在误解风险和评论证据，并整理有依据的运营诊断建议。

This skill is ready for commercial/non-commercial use.

## Publisher:

[funewa](https://clawhub.ai/user/funewa)

### License/Terms of Use:

MIT-0

## Use Case:

Amazon sellers and operators use the skill to review an ASIN's product detail page and available reviews, identify information gaps or likely misunderstandings, and prepare evidence-based listing health findings. It requires an ARI API key; paid operations follow the skill's quote and confirmation workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Some operations can affect broader account controls or spend service credits during actions described as previews.

Mitigation: Prefer a corrected release with listing-only commands and approval before spending. For this version, enable 'ask before every charge,' request manual collection, and review recurring monitors; do not assume omitting --confirm makes a preview free.

## Reference(s):

- [ARI operations workspace](https://ari.funewa.com/zh/operations)
- [ClawHub skill release](https://clawhub.ai/funewa/skills/listing-health)
- [operation-workflow.md](references/operation-workflow.md)
- [reference.md](references/reference.md)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Guidance]

**Output Format:** [Structured Markdown listing health audit]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Evidence grounded in available product details and review data; review collection is not implicit.]

## Skill Version(s):

1.5.3 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
