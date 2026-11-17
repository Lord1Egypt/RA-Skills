## Description:

Find the best beaches and islands for swimming, snorkeling, surfing, and sunbathing, with travel booking support powered by Fliggy.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xiejinsong](https://clawhub.ai/user/xiejinsong)

### License/Terms of Use:

MIT-0

## Use Case:

External users and travel-planning agents use this skill to search for beaches, islands, snorkeling spots, and family beach attractions, then present booking-linked travel results from flyai/Fliggy.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may install a global npm CLI before answering travel requests.

Mitigation: Review and approve the dependency before installation, and prefer a pinned or controlled environment for execution.

Risk: Searches and booking workflows are centered on flyai/Fliggy and may send travel queries to that service.

Mitigation: Use only with queries appropriate for that third-party workflow, and independently verify prices, availability, and booking terms before purchase.

Risk: The artifact describes persistent local execution logs that can contain raw user queries.

Mitigation: Avoid entering sensitive travel details, require explicit logging approval, and review or delete local execution logs after use.

Risk: The security summary flags forced commercial booking output and booking-link requirements.

Mitigation: Treat recommendations as commercial search results, compare alternatives, and do not rely on the skill as the sole source for safety-critical travel decisions.

## Reference(s):

- [Parameter and Output Templates](references/templates.md)
- [Beach and Island Playbooks](references/playbooks.md)
- [Fallbacks for Attraction Search](references/fallbacks.md)
- [Execution Log Runbook](references/runbook.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown travel results with comparison tables, booking links, and inline shell commands when setup or retry steps are needed]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires flyai CLI output for travel data and expects each result to include a booking link.]

## Skill Version(s):

3.2.0 (source: server release metadata; artifact frontmatter says 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
