## Description:

Sift supports web search, research synthesis, fact verification, entity extraction, and URL content extraction for agents that need current web information.

This skill is ready for commercial/non-commercial use.

## Publisher:

[indigokarasu](https://clawhub.ai/user/indigokarasu)

### License/Terms of Use:

MIT

## Use Case:

Developers, operators, and research agents use Sift to search, verify, compare, summarize, and synthesize current web information while escalating through configured search and extraction tiers.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Policy-bypass and anti-bot guidance may encourage access patterns that conflict with site policies or deployment requirements.

Mitigation: Remove policy-bypass and stealth or anti-bot instructions before deployment, and require operator approval for browser automation or blocked-site escalation.

Risk: Person-targeted research workflows can create privacy and profiling concerns.

Mitigation: Separate or block person-focused research unless an approved use case, data handling policy, and human review path are in place.

Risk: Silent self-updates can change behavior after installation.

Mitigation: Disable silent updates and pin reviewed versions in controlled environments.

Risk: Screenshots, generated scripts, logs, journals, and third-party URL forwarding may retain or expose sensitive information.

Mitigation: Define retention limits, storage locations, redaction requirements, and allowed forwarding destinations before use.

## Reference(s):

- [Research workflow](references/research-workflow.md)
- [Search tiers](references/search_tiers.md)
- [Fetch behavior](references/fetch-behavior.md)
- [Webwright integration](references/webwright-integration.md)
- [DonSeTch integration](references/donsetch-integration.md)
- [CSAPI quota](references/csapi-quota.md)
- [Schemas](references/schemas.md)
- [Journal](references/journal.md)
- [Pitfalls](references/pitfalls.md)
- [SearXNG diagnostics](references/searxng-diagnostics.md)
- [VPS search cheat sheet](references/vps-search-cheat-sheet.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown research answers, JSON envelopes, journal records, and shell command guidance.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce local research journals, extracted entities, source records, and Signal payloads when configured.]

## Skill Version(s):

2.3.1 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
