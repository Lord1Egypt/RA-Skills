## Description:

Self-improving agent that never repeats a mistake. Learns from every correction and failure, remembers why, and checks only the relevant lessons before acting. Local-first, open source.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cognicore-dev](https://clawhub.ai/user/cognicore-dev)

### License/Terms of Use:

MIT-0

## Use Case:

Developers using an AI agent can have it check relevant prior lessons before tasks that change a project, then record corrections and failures so the agent can apply them on later tasks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Lesson entries are persisted in a local database and could retain details that should not be kept.

Mitigation: Avoid putting secrets in lessons, review entries with `cognicore lesson list`, and remove unwanted entries with `cognicore lesson forget` or delete the documented database.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/cognicore-dev/skills/never-twice)
- [Never Twice project documentation link](https://github.com/cognicore-dev/cognicore-env/tree/main/skills/never-twice)
- [CogniCore lesson storage code](https://github.com/cognicore-dev/cognicore-env/blob/main/cognicore/lessons.py)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Text]

**Output Format:** [Markdown instructions with inline shell commands and returned lesson text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Lesson checks return up to three relevant entries and may return no output when none match.]

## Skill Version(s):

1.0.1 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
