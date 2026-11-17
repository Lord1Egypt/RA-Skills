## Description:

Search, browse, and discover OpenClaw skills from the ClawHub platform with filtering, sorting, recommendations, and detailed skill metadata.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhenstaff](https://clawhub.ai/user/zhenstaff)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to find OpenClaw skills on ClawHub, compare metadata and requirements, and retrieve installation guidance for relevant skills.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The reviewed artifact installs an unpinned global npm package whose package contents were not included in the artifact.

Mitigation: Use an exact audited package version, avoid elevated privileges, and review the npm package source and install scripts before global installation.

Risk: Search queries and skill lookup terms may be sent to ClawHub when the CLI uses the public ClawHub service.

Mitigation: Avoid sensitive query terms and review the current package network behavior before use in restricted environments.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/zhenstaff/skills/openclaw-skill-finder)
- [Project Homepage](https://github.com/ZhenRobotics/openclaw-skill-finder#readme)
- [npm Package](https://www.npmjs.com/package/openclaw-skill-finder)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and optional JSON CLI output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [No API keys were detected in the reviewed evidence.]

## Skill Version(s):

1.0.0 (source: server release metadata and readme, released 2026-03-23)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
