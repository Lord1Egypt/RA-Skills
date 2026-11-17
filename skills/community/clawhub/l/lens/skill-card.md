## Description:

LENS helps an agent learn a user's context, judgment, and writing voice, then apply that profile to requested decisions and writing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[capachow](https://clawhub.ai/user/capachow)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use LENS to capture an individual's context, decision preferences, and voice, then get personalized analysis or writing when they explicitly request it. Interviews and local session distillation can update the profile over time.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: ClawScan reports a schedule-removal policy concern and could not fully inspect three scripts, so its scan cannot establish that the release is safe.

Mitigation: Review the scripts and confirm schedule removals are limited and clearly reported before installation or enabling scheduled runs.

## Reference(s):

- [LENS release on ClawHub](https://clawhub.ai/capachow/skills/lens)
- [Alignment Scales](references/alignment-scales.md)
- [Resolve Protocol](references/resolve-protocol.md)
- [Trinity Definitions](references/trinity-definitions.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Configuration, Guidance]

**Output Format:** [Personalized natural-language responses and local YAML, JSON, and text profile files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Personalized from the user's LENS profile; may update local profile and schedule settings.]

## Skill Version(s):

2.2.1 (source: package.json, server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
