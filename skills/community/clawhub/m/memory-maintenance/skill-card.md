## Description:

Intelligent memory management for OpenClaw agents. Reviews daily notes, suggests MEMORY.md updates, maintains directory health, and auto-cleans old files. Recommended for agents with growing memory footprints.

This skill is ready for commercial/non-commercial use.

## Publisher:

[maxlauriehutchinson](https://clawhub.ai/user/maxlauriehutchinson)

### License/Terms of Use:

MIT

## Use Case:

OpenClaw users and agent maintainers use this skill to review daily memory notes, generate MEMORY.md update suggestions, check memory directory health, and manage archival or cleanup workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: OpenClaw memory notes, MEMORY.md, and USER.md content may be sent to Gemini for review.

Mitigation: Install only if that data sharing is acceptable; add redaction or explicit opt-in before remote analysis.

Risk: Automated maintenance can move or delete memory-related files.

Mitigation: Inspect or disable the daily cron cleanup, use dry-run or safe modes first, and validate model-generated file paths before applying changes.

Risk: Scripts may source .env files and expose broader environment secrets than intended.

Mitigation: Review or patch scripts before installation to avoid sourcing .env files or to limit loaded variables to the required Gemini credential.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/maxlauriehutchinson/skills/memory-maintenance)
- [Publisher profile](https://clawhub.ai/user/maxlauriehutchinson)
- [Skill homepage from artifact metadata](https://github.com/MaxLaurieHutchinson/memory-maintenance)

## Skill Output:

**Output Type(s):** [text, markdown, json, shell commands, configuration, guidance]

**Output Format:** [JSON review data, Markdown reports, shell command output, and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces review files under agents/memory and supports dry-run, safe, cleanup, and status workflows.]

## Skill Version(s):

1.0.0 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
