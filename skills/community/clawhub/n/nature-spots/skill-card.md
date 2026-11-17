## Description:

Find mountains, lakes, waterfalls, national parks, and natural wonders, including trail difficulty, best seasons, photography tips, and travel booking support powered by Fliggy.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xiejinsong](https://clawhub.ai/user/xiejinsong)

### License/Terms of Use:

MIT-0

## Use Case:

External users and travel-planning agents use this skill to find nature-focused attractions for a city and return CLI-sourced options with booking links, seasonal context, and practical notes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill depends on a third-party travel CLI and may send user travel queries to an external service.

Mitigation: Install only after reviewing and approving the FlyAI CLI source and provenance; avoid submitting sensitive travel details unless approved.

Risk: The skill attempts a global CLI install when the dependency is missing.

Mitigation: Use a pinned, locally approved FlyAI CLI installation instead of ad hoc global installation.

Risk: The workflow steers responses toward booking links returned by the CLI.

Mitigation: Validate generated booking links and make sure users understand links come from the external travel provider.

Risk: The artifact describes raw-query execution logging when filesystem writes are available.

Mitigation: Disable or remove raw-query logging, or redact sensitive input before any execution log is written.

Risk: Shell-style command templates can be unsafe if user values are interpolated directly.

Mitigation: Invoke the CLI with argument-safe APIs or strict escaping and parameter validation.

## Reference(s):

- [Templates](references/templates.md)
- [Playbooks](references/playbooks.md)
- [Fallbacks](references/fallbacks.md)
- [Runbook](references/runbook.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown with comparison tables, inline booking links, concise tips, and occasional shell command snippets for CLI setup or retries.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs are expected to be based on flyai CLI results, include booking links when results are shown, and avoid raw JSON.]

## Skill Version(s):

3.2.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
