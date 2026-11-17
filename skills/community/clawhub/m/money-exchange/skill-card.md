## Description:

Checks exchange rates, currency tips, and money-saving strategies for international travel, with expanded travel-service lookup through FlyAI and Fliggy-backed CLI output.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xiejinsong](https://clawhub.ai/user/xiejinsong)

### License/Terms of Use:

MIT-0

## Use Case:

External travelers and travel support agents use this skill to query exchange rates, exchange locations, and local payment methods through FlyAI CLI output. The skill can also route related travel lookups such as flights, hotels, trains, attractions, visas, insurance, car rentals, and itinerary planning.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks agents to install and trust a global third-party FlyAI CLI before producing results.

Mitigation: Review and approve the CLI installation before use, and run the skill only in environments where that dependency is acceptable.

Risk: The skill can persist raw user queries, which may contain travel, payment, or personal details.

Mitigation: Avoid entering sensitive details and disable or review query logging where deployment controls allow it.

Risk: Returned booking links and travel results come from an external CLI workflow.

Mitigation: Validate booking or detail links before acting on them, and do not use results that lack the required detail link.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/xiejinsong/skills/money-exchange)
- [Output Templates](references/templates.md)
- [Currency Exchange Playbooks](references/playbooks.md)
- [Fallbacks](references/fallbacks.md)
- [Execution Runbook](references/runbook.md)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Guidance]

**Output Format:** [Markdown with tables, inline links, and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires FlyAI CLI output for user-facing results and expects booking or detail links for returned items.]

## Skill Version(s):

3.2.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
