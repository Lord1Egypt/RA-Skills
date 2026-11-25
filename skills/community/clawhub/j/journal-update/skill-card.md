## Description:

Updates or creates today's work journal in the current project's docs/journal/, then commits and pushes it. Use when asked to update the journal, log or record today's work, or wrap up a work session. Not for other dated docs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tenequm](https://clawhub.ai/user/tenequm)

### License/Terms of Use:

MIT-0

## Use Case:

Project contributors use this skill to record a work session in the current repository's daily journal, following that journal's existing format and project instructions. When an entry is warranted, it prepares the journal change for commit and push.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security scan could not resolve one local reference, so its evidence is incomplete.

Mitigation: Review the referenced material and assess whether the unresolved reference affects your use before installation.

Risk: The skill directs the agent to commit and push journal changes to the current repository.

Mitigation: Review the journal entry and repository diff, and confirm the intended repository and push before allowing completion.

## Reference(s):


## Skill Output:

**Output Type(s):** [Files, Markdown, Shell commands]

**Output Format:** [A dated Markdown journal entry following the project's existing format]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Updates one session section and the final open-threads block; may commit and push the journal change.]

## Skill Version(s):

0.1.1 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
