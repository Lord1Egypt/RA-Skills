## Description:

Expands a single Amazon seed keyword into related keyword ideas with search volume, trend, PPC bid, and ranking-difficulty metrics across 10 supported marketplaces.

This skill is ready for commercial/non-commercial use.

## Publisher:

[linkfox-ai](https://clawhub.ai/user/linkfox-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External sellers, ecommerce operators, and agents use this skill to expand one Amazon seed keyword into related keywords and compare search volume, trend, PPC bid, relevance, and ranking difficulty metrics. It is suited to Amazon listing research, long-tail keyword discovery, PPC planning, and marketplace-specific keyword analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Keyword research, account identifiers, and related ecommerce context may be sent to LinkFox services.

Mitigation: Use the skill only when that data sharing is acceptable, avoid sensitive customer or account secrets in prompts, and review the request before execution.

Risk: Authentication and onboarding flows may involve API keys, phone/SMS verification, and account setup.

Mitigation: Prefer official self-service account pages, do not expose API keys or verification details in chat or logs, and rotate credentials if they are disclosed.

Risk: Billing, payment, feedback, or endpoint override behavior could create unintended external actions or route data to unexpected services.

Mitigation: Require explicit user consent before payment or feedback actions and verify LINKFOX_* endpoint variables are not overridden before use.

## Reference(s):

- [Jungle Scout Keyword API Reference](references/api.md)
- [LinkFox Authentication and Billing Onboarding](references/onboarding.md)
- [ClawHub Skill Page](https://clawhub.ai/linkfox-ai/skills/linkfox-junglescout-keyword-by-keyword)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration guidance]

**Output Format:** [Markdown tables and summaries, JSON API responses or saved JSON data files, and inline shell commands when setup is needed]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Full API responses may be written to local linkfox data/cache directories; large responses are summarized unless inline output is requested.]

## Skill Version(s):

1.0.8 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
