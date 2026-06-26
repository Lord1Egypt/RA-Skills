## Description: <br>
LEIO SDLC is a multi-agent Software Development Life Cycle engine for OpenClaw that automates PRD auditing, planning, coding, review, merge, and verification through an isolated artifact-driven pipeline. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[leio9511](https://clawhub.ai/user/leio9511) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering teams use this skill to run a structured multi-agent SDLC workflow over repositories they control, from approved PRDs through micro-PR planning, TDD implementation, review, merge, notifications, and final verification. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can spawn agents that edit and commit code, create and delete branches, merge reviewed changes, and write run artifacts. <br>
Mitigation: Run it only in repositories you control, require an approved PRD before orchestration, and review generated diffs, review reports, and commits before relying on results. <br>
Risk: Deployment scripts can install or update local skills, preserve or modify configuration, install Git hooks, trigger GitHub sync when available, and restart the OpenClaw gateway. <br>
Mitigation: Review deploy.sh, kit-deploy.sh, orchestrator.py, and config/prompts.json before installation; disable GitHub auto-sync, hook installation, or gateway restart behavior when those actions are not desired. <br>
Risk: The pipeline depends on trusted CLI arguments, environment variables, notification channels, and isolated run directories. <br>
Mitigation: Use trusted inputs, pass explicit workdir and global-dir values, keep test mode out of production runs, and monitor generated logs and ACTION_REQUIRED handoffs. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/leio9511/leio-sdlc) <br>
- [README](README.md) <br>
- [Architecture Blueprint](ARCHITECTURE.md) <br>
- [Audit Report v6](docs/Audit_Report_v6.md) <br>
- [SDLC CUJ Testing PRD](docs/PRDs/PRD_012_SDLC_CUJ_Testing.md) <br>
- [Triad Planner and Coder Testing PRD](docs/PRDs/PRD_023_Triad_Phase2.md) <br>
- [Triad Reviewer Testing PRD](docs/PRDs/PRD_023_Triad_Reviewer.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown documents, JSON review and verification reports, code changes, git commits, shell commands, and notification text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces and consumes repository files, PRD files, micro-PR contracts, diffs, review reports, state files, and deployment artifacts during orchestration.] <br>

## Skill Version(s): <br>
1.0.0 (source: SKILL.md frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
