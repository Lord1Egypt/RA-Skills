## Description:

Conductor (conductor.com). Use this skill for ANY Conductor request — searching and reading data. Whenever a task involves Conductor, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and analysts use this skill to search and read data in a Conductor Monitoring account connected through OOMOL, including website pages, statistics, issues, segments, and affected pages.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup instructions allow remote code execution, and CLI skill synchronization may make changes to agent skills.

Mitigation: Install the CLI only through an explicitly approved, verified process, and check its automatic skill synchronization settings.

## Reference(s):

- [Conductor homepage](https://www.conductor.com)
- [Conductor API documentation](https://support.conductor.com/en_US/api-documentation)
- [oo CLI](https://github.com/oomol-lab/oo-cli)
- [ClawHub release page](https://clawhub.ai/oomol/skills/oo-conductor)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Shell commands, Guidance]

**Output Format:** [JSON data returned by Conductor actions, with oo CLI command examples and setup guidance in Markdown]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-oriented website data; action responses include data and execution metadata.]

## Skill Version(s):

1.0.5 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
