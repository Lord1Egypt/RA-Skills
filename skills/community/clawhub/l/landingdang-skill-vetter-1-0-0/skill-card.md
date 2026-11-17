## Description:

Security-first skill vetting for AI agents before installing skills from ClawHub, GitHub, or other sources.

This skill is ready for commercial/non-commercial use.

## Publisher:

[landingdang](https://clawhub.ai/user/landingdang)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill before installing or running candidate skills to review source reputation, permission scope, suspicious patterns, and overall installation risk.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may prompt an agent to inspect candidate skills and make public GitHub network requests for repository metadata.

Mitigation: Limit review activity to the specific skill being evaluated, use public metadata only, and avoid providing credentials unless a separate trusted workflow explicitly requires them.

Risk: A vetting report can miss malicious behavior if artifact review is incomplete or the source is misidentified.

Mitigation: Review every file in the candidate skill, document permission scope, and require human approval for high-risk findings such as credentials, broad filesystem access, or privileged commands.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/landingdang/skills/landingdang-skill-vetter-1-0-0)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown report with optional inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces a skill vetting report covering source, author, version, metrics, reviewed files, red flags, permissions, risk level, verdict, and notes.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
