## Description: <br>
Scores feature worthiness and enforces branch-size limits against overengineering. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[athola](https://clawhub.ai/user/athola) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill during brainstorming, planning, and execution to score proposed work, compare it against backlog priorities, and keep branches within reviewable size limits. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can steer an agent to publish deferred work and reasoning to GitHub. <br>
Mitigation: Require explicit confirmation before creating issues, comments, or Discussions, and review the exact text before posting. <br>
Risk: Deferred-work records may expose sensitive project context in private or public repositories. <br>
Mitigation: Use only in repositories where visibility and permissions are understood, and remove confidential details before creating persistent GitHub records. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/athola/skills/nm-imbue-scope-guard) <br>
- [OpenClaw homepage metadata](https://github.com/athola/claude-night-market/tree/master/plugins/imbue) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands] <br>
**Output Format:** [Markdown with checklists, scoring tables, and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May instruct the agent to create GitHub issues or discussions for deferred work after user review.] <br>

## Skill Version(s): <br>
1.9.13 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
