## Description:

Plans multi-city flight itineraries across several stops and uses the flyai CLI to compare leg combinations, optimize total cost, and return booking links.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xiejinsong](https://clawhub.ai/user/xiejinsong)

### License/Terms of Use:

MIT-0

## Use Case:

External travelers and travel-planning agents use this skill to search multi-city, open-jaw, and cheapest-hub itineraries through flyai CLI output and present real-time options with booking links.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may ask the agent to install an unpinned global third-party CLI and includes a sudo fallback.

Mitigation: Use a pinned, user-scoped or sandboxed flyai CLI installation and do not use the sudo fallback unless explicitly reviewed and approved.

Risk: Travel queries and execution details may be persisted locally by the execution log behavior.

Mitigation: Review, disable, or isolate local execution logging before entering sensitive travel details.

Risk: Flight and booking guidance can be misleading if it is not backed by current CLI output.

Mitigation: Require fresh flyai CLI execution and verify every displayed result includes the CLI-provided booking link.

## Reference(s):

- [Parameter and output templates](references/templates.md)
- [Multi-stop playbooks](references/playbooks.md)
- [Fallbacks](references/fallbacks.md)
- [Execution runbook](references/runbook.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown travel results with booking links and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs must be based on flyai CLI results, avoid raw JSON, and include booking links when presenting travel options.]

## Skill Version(s):

3.2.0 (source: frontmatter and ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
