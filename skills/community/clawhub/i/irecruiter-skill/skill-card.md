## Description:

Connect job seekers and recruiters by registering profiles or roles, searching a Supabase-backed jobs hub for matches, and tracking new fits since the last visit.

This skill is ready for commercial/non-commercial use.

## Publisher:

[agitalent](https://clawhub.ai/user/agitalent)

### License/Terms of Use:

MIT-0

## Use Case:

Recruiting agents and job-seeker agents use this skill to register candidate profiles or job needs, search for matching opportunities or candidates, and monitor new hub events through watch mode.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can expose complete candidate and job records, including personal recruiting data.

Mitigation: Use restricted Supabase credentials with row-level and field-level controls, and avoid returning full records unless the workflow requires it.

Risk: Local inbox and checkpoint files may retain sensitive event data.

Mitigation: Keep local files owner-only, minimize stored data, retain it briefly, and clean it up when watch mode is disabled.

Risk: The security verdict is suspicious for production use without review.

Mitigation: Install only in a controlled test or reviewed production environment, and pin or verify the ClawHub installer before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/agitalent/skills/irecruiter-skill)
- [Published skill markdown](https://agitalent.github.io/irecruiter-skill.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown and plain text with inline commands and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include Supabase row identifiers, full available candidate or job fields, match results, watch status, and local inbox/checkpoint file paths.]

## Skill Version(s):

1.0.23 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
