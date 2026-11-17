## Description:

Queries 1688 weekly and monthly bestseller billboard data to help sellers identify hot wholesale products, suppliers, and sourcing opportunities.

This skill is ready for commercial/non-commercial use.

## Publisher:

[linkfox-ai](https://clawhub.ai/user/linkfox-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External sellers, sourcing teams, and cross-border commerce operators use this skill to query 1688 bestseller rankings, compare wholesale suppliers, and research product opportunities.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends ranking queries and authentication credentials to LinkFox-operated services.

Mitigation: Use a dedicated, revocable API key and review what query data is sent before calling the API.

Risk: The skill includes account onboarding and billing flows that can involve phone/SMS registration and payment actions.

Mitigation: Prefer completing account setup and billing directly through trusted LinkFox account pages, and require explicit user approval before starting any payment flow.

Risk: The skill writes full API responses and cached results to local linkfox data/cache directories.

Mitigation: Review, restrict, or clear generated files when product research data should not persist locally.

Risk: The server security verdict is suspicious because account, billing, credential, storage, and automatic feedback behaviors are broader than the core ranking query use case.

Mitigation: Install only after reviewing the security summary and disable or avoid optional flows that are not needed for the task.

## Reference(s):

- [1688 Product Billboard API Reference](artifact/references/api.md)
- [Authentication and Billing Onboarding](artifact/references/onboarding.md)
- [ClawHub Skill Page](https://clawhub.ai/linkfox-ai/skills/linkfox-dld-product-billboard)

## Skill Output:

**Output Type(s):** [API Calls, Markdown, JSON, Files, Shell commands, Guidance]

**Output Format:** [Markdown summaries and tables with JSON result files for full API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes full responses under a local linkfox data directory and may summarize large responses in stdout.]

## Skill Version(s):

1.0.8 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
