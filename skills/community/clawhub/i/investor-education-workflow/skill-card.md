## Description:

Investor Education Workflow helps agents produce investor education content by retrieving maintained knowledge, supplementing with official sources when needed, translating concepts into plain language, marking output intent, and preparing reviewed content for reuse.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lj22503](https://clawhub.ai/user/lj22503)

### License/Terms of Use:

MIT-0

## Use Case:

External investor educators, advisers, and content teams use this skill to draft investor education explanations, articles, cards, voice scripts, video scripts, and WeChat-ready content. It is designed to convert prohibited product-specific or return-prediction requests into educational guidance rather than investment advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad command and write permissions could expose unrelated workspace files or secrets.

Mitigation: Install only in a sandboxed workspace with no unrelated files or secrets exposed, and prefer a version that removes Bash/Exec and scopes Write to the investor-education knowledge directory.

Risk: Customer questions and feedback may be stored in the reusable knowledge base.

Mitigation: Require explicit consent before saving, redact personal or account-specific details, and review changes before they enter reusable knowledge.

Risk: Investor education outputs could be mistaken for investment advice or drift into product recommendations.

Mitigation: Use the skill's compliance conversion protocol for specific recommendations, guaranteed returns, short-term predictions, or delegated-management requests, and add clear investor-education disclaimers.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/lj22503/skills/investor-education-workflow)
- [Five Modules Knowledge Base](artifact/references/five-modules.md)
- [Four Experts Framework](artifact/references/four-experts.md)
- [LLM Wiki Architecture](artifact/references/llm-wiki.md)
- [Investor Education Template](artifact/templates/education-template.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with structured YAML intent parameters and optional knowledge-base file updates.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May prepare plain-language responses, long-form articles, card content, voice scripts, video scripts, WeChat-ready content, and reviewed knowledge-base entries.]

## Skill Version(s):

1.2.0 (source: evidence release and artifact/clawhub.yaml; artifact/SKILL.md frontmatter reports 1.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
