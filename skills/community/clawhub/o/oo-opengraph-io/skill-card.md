## Description:

OpenGraph.io (opengraph.io). Use this skill for ANY OpenGraph.io request — searching and reading data. Whenever a task involves OpenGraph.io, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to retrieve OpenGraph and social metadata, scrape webpage HTML, extract site metadata, or capture webpage screenshots through OpenGraph.io.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A webpage-reading request can trigger a remote software installer without a separate approval step.

Mitigation: Review the oo CLI before enabling the skill, require approval before running installer commands, and review automatic skill synchronization; the skill documents OO_SKILLS_SYNC_DISABLED as an opt-out.

## Reference(s):

- [OpenGraph.io API documentation](https://www.opengraph.io/docs/api)
- [OpenGraph.io](https://www.opengraph.io)
- [oo CLI repository](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [Shell commands, JSON, HTML, Screenshots]

**Output Format:** [Shell commands with JSON payloads; action results as JSON, HTML, or screenshots]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results vary by selected OpenGraph.io action.]

## Skill Version(s):

1.0.5 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
