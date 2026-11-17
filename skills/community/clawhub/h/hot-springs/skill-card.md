## Description:

Find natural hot springs and thermal baths, including outdoor pools, private onsen, medicinal springs, and spa complexes, with related travel services powered by Fliggy.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xiejinsong](https://clawhub.ai/user/xiejinsong)

### License/Terms of Use:

MIT-0

## Use Case:

External users and travel-focused agents use this skill to search for hot springs, thermal baths, and related travel services through flyai CLI results rather than model knowledge.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires installing and using an unpinned global flyai CLI before producing travel results.

Mitigation: Use a pinned, user-approved, isolated CLI installation and verify the CLI version before execution.

Risk: Results are expected to include commercial booking links, which may influence user choices.

Mitigation: Disclose that results are powered by flyai and review booking links before presenting them to users.

Risk: Local execution logs may store raw travel queries.

Mitigation: Disable persistent logging where possible or redact user query details before logs are written.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/xiejinsong/skills/hot-springs)
- [templates.md](references/templates.md)
- [playbooks.md](references/playbooks.md)
- [fallbacks.md](references/fallbacks.md)
- [runbook.md](references/runbook.md)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Guidance]

**Output Format:** [Markdown with booking links and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results are expected to come from flyai CLI output and include booking links when available.]

## Skill Version(s):

3.2.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
