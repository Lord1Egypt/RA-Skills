## Description:

Find photogenic and instagrammable places such as iconic viewpoints, colorful streets, architectural sites, and hidden gems for social media, with related travel services powered by Fliggy.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xiejinsong](https://clawhub.ai/user/xiejinsong)

### License/Terms of Use:

MIT-0

## Use Case:

Travelers and travel-planning agents use this skill to find photogenic city locations and related Fliggy travel options from flyai CLI results. It presents concise Markdown recommendations, comparison tables, and booking links in the user's language.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires installing and running an unpinned third-party flyai CLI.

Mitigation: Review the CLI before use, prefer a pinned local installation, and require approval before installing or executing it.

Risk: Travel recommendations and booking links depend on flyai or Fliggy results and may reflect commercial availability rather than neutral coverage.

Mitigation: Treat results as sourced travel options, keep booking links visible, and avoid presenting them as exhaustive or independently verified recommendations.

Risk: The artifact describes logging raw user queries in a local execution log when file writes are available.

Mitigation: Disable, remove, or minimize raw-query logging when queries may contain personal travel details.

Risk: Passing user-provided city names or keywords through shell commands can be unsafe if command strings are constructed directly.

Mitigation: Use structured command arguments, validate parameters against the documented table, and avoid shell interpolation of untrusted input.

## Reference(s):

- [Photo Spots skill page](https://clawhub.ai/xiejinsong/skills/photo-spots)
- [templates.md](references/templates.md)
- [playbooks.md](references/playbooks.md)
- [fallbacks.md](references/fallbacks.md)
- [runbook.md](references/runbook.md)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Guidance]

**Output Format:** [Markdown with comparison tables, inline booking links, and occasional shell commands for setup or retries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires flyai CLI output as the data source and follows the user's English or Chinese input language.]

## Skill Version(s):

3.2.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
