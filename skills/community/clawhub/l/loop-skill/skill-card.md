## Description:

Loop Skill helps an agent turn repository advancement plans into an unattended coding-agent loop that scans projects, writes or updates plans, dispatches CLI workers, persists sessions, and exposes a dashboard.

This skill is ready for commercial/non-commercial use.

## Publisher:

[handsomestwei](https://clawhub.ai/user/handsomestwei)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering teams use this skill to coordinate unattended progress across one or more repositories by having a controlling agent inspect project materials, create or update advancement plans, and start a persistent loop that dispatches coding CLI workers.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can read selected repositories and write or update planning files.

Mitigation: Run it only against a narrow, intended project root and review generated plans before allowing workers to proceed.

Risk: The skill can start a persistent background loop and dispatch coding CLI workers.

Mitigation: Use it only when unattended worker execution is intended, monitor the dashboard, and stop it with the documented down command when work should pause.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/handsomestwei/skills/loop-skill)
- [GitHub repository](https://github.com/handsomestWei/loop-skill)
- [Server-resolved GitHub import](https://github.com/handsomestWei/loop-skill)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands, planning tables, file paths, and status guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update repository planning files, start a persistent background loop, and report a dashboard URL.]

## Skill Version(s):

0.1.0 (source: server release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
