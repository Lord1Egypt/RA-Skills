## Description:

Book hotels with genuine hot spring baths, including natural onsen pools, private hot spring rooms, and Japanese-style ryokan experiences, using FlyAI/Fliggy live travel search and booking links.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xiejinsong](https://clawhub.ai/user/xiejinsong)

### License/Terms of Use:

MIT-0

## Use Case:

External travelers and travel-booking agents use this skill to find hotels with hot spring or onsen features, compare real-time options, and present Markdown booking results backed by FlyAI/Fliggy CLI output.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks the agent to install and run a third-party CLI globally before retrieving travel data.

Mitigation: Review before installing; run in an isolated environment or revise the skill to require explicit install consent and pinned dependencies.

Risk: Shell-style command templates may pass user-supplied travel parameters into CLI calls.

Mitigation: Use safe argument-array execution and validate or quote destination names, dates, budgets, keywords, and other user-provided values.

Risk: The runbook permits persistent logging of raw user travel queries.

Mitigation: Disable persistent logging or redact sensitive itinerary and personal details before storage.

## Reference(s):

- [Parameter and Output Templates](references/templates.md)
- [Onsen Hotel Playbooks](references/playbooks.md)
- [Fallback Recovery Guide](references/fallbacks.md)
- [Execution Runbook](references/runbook.md)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Guidance]

**Output Format:** [Markdown with booking links and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires FlyAI CLI output for hotel data; should not emit raw JSON or fabricated travel results.]

## Skill Version(s):

3.2.1 (source: server release metadata; artifact frontmatter states 3.2.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
