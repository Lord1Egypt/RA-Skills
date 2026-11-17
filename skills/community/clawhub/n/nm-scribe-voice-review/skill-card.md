## Description:

Runs parallel prose and craft review agents against a voice profile

This skill is ready for commercial/non-commercial use.

## Publisher:

[athola](https://clawhub.ai/user/athola)

### License/Terms of Use:

MIT-0

## Use Case:

Writers and content teams use this skill to review generated prose against a voice profile for AI-pattern issues and craft concerns before publishing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A possible conflict with a built-in `review` command could make command selection ambiguous.

Mitigation: Check whether a `review` command is already registered before installing or enabling this skill, and resolve any naming conflict.

Risk: Reference checks were partial, so some local references may be unresolved.

Mitigation: Confirm the referenced commands and dependencies are available and trusted in the target setup before use.

## Reference(s):

- [Scribe plugin homepage (metadata link)](https://github.com/athola/claude-night-market/tree/master/plugins/scribe)
- [ClawHub skill page](https://clawhub.ai/athola/skills/nm-scribe-voice-review)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Files]

**Output Format:** [Markdown findings tables and reviewed prose]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Advisory findings may be presented for user decisions; hard failures may be auto-corrected.]

## Skill Version(s):

1.10.3 (source: skill frontmatter, server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
