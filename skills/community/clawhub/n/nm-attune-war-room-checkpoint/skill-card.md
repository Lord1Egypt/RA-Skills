## Description: <br>
Assesses decision reversibility and risk at critical checkpoints. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[athola](https://clawhub.ai/user/athola) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent workflow maintainers use this embedded checkpoint to score decision reversibility, decide whether to escalate to War Room deliberation, and return a recommendation or escalation result to the calling command. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may persist review context, sensitive filenames, security-review details, or confidential decision history under local ~/.claude/memory-palace/strategeion paths. <br>
Mitigation: Install only when local workflow decision logging is acceptable, and review or periodically clean the documented local audit-log paths for sensitive projects. <br>
Risk: Checkpoint recommendations or escalation decisions could be incorrect or misleading for high-stakes workflow branches. <br>
Mitigation: Review checkpoint output before acting, scan the skill before deployment, and require confirmation when the response indicates low confidence or escalation. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/athola/nm-attune-war-room-checkpoint) <br>
- [OpenClaw homepage](https://github.com/athola/claude-night-market/tree/master/plugins/attune) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Markdown, Guidance, Configuration] <br>
**Output Format:** [Markdown checkpoint response with structured fields] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes reversibility score, selected mode, escalation decision, recommendation or orders, confidence, and confirmation requirement.] <br>

## Skill Version(s): <br>
1.9.12 (source: server release metadata; artifact frontmatter lists 1.9.8) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
