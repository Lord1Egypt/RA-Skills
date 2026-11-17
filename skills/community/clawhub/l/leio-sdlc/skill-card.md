## Description:

LEIO SDLC runs a multi-agent Software Development Life Cycle pipeline that plans, codes, reviews, audits, verifies, and merges work through an isolated artifact-driven workflow.

This skill is ready for commercial/non-commercial use.

## Publisher:

[leio9511](https://clawhub.ai/user/leio9511)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering teams use this skill to drive a controlled SDLC workflow for a git repository, from PRD audit through planning, coding, review, verification, and merge. It is intended for highly automated repository work where the user can review pipeline configuration and generated artifacts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can change, merge, clean up, or publish repository code.

Mitigation: Use it only in repositories where automated SDLC control is intended, and review branch, merge, cleanup, and publishing settings before running the orchestrator.

Risk: Incorrect control-plane paths or notification settings could expose private work or apply changes in the wrong repository context.

Mitigation: Confirm the target repository, branch, notification channel, global run directory, and any GitHub sync integration before installation and each run.

Risk: Uncommitted code or private work could be lost during automated cleanup paths.

Mitigation: Start from a clean, backed-up git workspace and preserve important local changes before allowing the pipeline to execute cleanup or merge operations.

## Reference(s):

- [LEIO SDLC ClawHub Skill Page](https://clawhub.ai/leio9511/skills/leio-sdlc)
- [README](README.md)
- [Architecture Blueprint](ARCHITECTURE.md)
- [SDLC Skill Self-Validation via CUJs](docs/PRDs/PRD_012_SDLC_CUJ_Testing.md)
- [Triad Coherence Testing for Planner and Coder](docs/PRDs/PRD_023_Triad_Phase2.md)
- [E2E Testing of Triad Consistency](docs/PRDs/PRD_023_Triad_Reviewer.md)
- [Architectural Audit Report v6](docs/Audit_Report_v6.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown, JSON status artifacts, diffs, shell commands, and repository changes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill can produce and update PRD, PR contract, review, verification, log, and state artifacts while coordinating repository operations.]

## Skill Version(s):

1.0.0 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
