## Description:

Generates markdown digests and CSV exports for GitHub initiative health

This skill is ready for commercial/non-commercial use.

## Publisher:

[athola](https://clawhub.ai/user/athola)

### License/Terms of Use:

MIT-0

## Use Case:

Project and engineering teams use this skill to summarize GitHub initiative progress, surface blockers and risks, and prepare status updates for issues, pull requests, or Discussions. It can also export initiative health metrics as CSV.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The `status` trigger could conflict with a built-in command in the host agent.

Mitigation: Check for a command-name conflict in the target agent before enabling the skill.

Risk: Tracker-derived or GitHub content may be stale or unsuitable for the intended audience when included in a published digest.

Mitigation: Review the source data, linked issues and pull requests, and intended GitHub audience before publishing.

Risk: The security scan was partial because a local reference could not be resolved.

Mitigation: Review the skill and unresolved reference before installation or use.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/athola/skills/nm-minister-github-initiative-pulse)
- [Project homepage](https://github.com/athola/claude-night-market/tree/master/plugins/minister)

## Skill Output:

**Output Type(s):** [Markdown, CSV, Text]

**Output Format:** [Markdown digests and CSV exports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Initiative status summaries, progress metrics, blockers, risks, and milestone information.]

## Skill Version(s):

1.10.3 (source: frontmatter and server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
