## Description: <br>
Weekly Retro analyzes memory logs to identify accomplishments, recurring patterns, friction points, and forward-looking recommendations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[newageinvestments25-byte](https://clawhub.ai/user/newageinvestments25-byte) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to gather weekly memory logs, analyze accomplishments and recurring patterns, and generate a forward-looking retrospective for vault storage and long-term review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads local memory logs and optional workspace context files that may contain sensitive personal or project information. <br>
Mitigation: Check the configured memory, vault, history, SOUL.md, and AGENTS.md paths before running it, avoid storing secrets in those files, and review generated retrospectives before syncing or sharing them. <br>
Risk: Cron integration can run the retrospective automatically on a schedule. <br>
Mitigation: Enable the cron schedule only when automatic weekly runs are intended and the configured output location is appropriate. <br>


## Reference(s): <br>
- [Retrospective Format Reference](references/retro-format.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown retrospective with YAML frontmatter, plus intermediate structured JSON from gather and analysis steps.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Python standard library only; supports optional history tracking and cron-based weekly runs.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
