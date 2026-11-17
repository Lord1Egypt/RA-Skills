## Description:

Runtime security skill for AI agents covering prompt injection detection, tool call authorization, sensitive data leak prevention, skill security scanning, and one-click backup and restore.

This skill is ready for commercial/non-commercial use.

## Publisher:

[326668808](https://clawhub.ai/user/326668808)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use Openclaw360 to run local security checks on prompts, tool calls, agent outputs, installed skills, audit logs, and backup or restore workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installation fetches executable code from GitHub.

Mitigation: Review the referenced source at the pinned revision before installing, or install it in an isolated virtual environment.

Risk: Security checks process prompts, tool parameters, outputs, Skill files, audit logs, and local backups.

Mitigation: Run the skill only for intended security checks and avoid submitting data that is outside the scope of the review.

Risk: Initialization and security checks create or update local files under ~/.openclaw360/.

Mitigation: Initialize only after user confirmation and review the documented config, identity, audit, and backup paths before use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/326668808/skills/openclaw360)
- [Openclaw360 source repository](https://github.com/milu-ai/openclaw360)
- [Pinned install source](https://github.com/milu-ai/openclaw360.git@5fd69db)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and optional JSON CLI results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Runs local CLI checks and may append audit records under ~/.openclaw360/ when the user asks it to perform security checks.]

## Skill Version(s):

0.1.11 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
