## Description: <br>
Assess whether to escalate models. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[athola](https://clawhub.ai/user/athola) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent orchestrators use this skill to decide when model escalation is justified, document the reason for escalation, and return to a more efficient model after the higher-capability task is complete. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Escalation guidance can lead to unnecessary cost or latency if an agent changes models before investigating the root cause of a task failure. <br>
Mitigation: Require the agent to document the capability gap, scope the escalated subtask, define success, and return to the efficient model promptly. <br>
Risk: The artifact includes operational decision guidance that may be misapplied to high-stakes or security-sensitive work. <br>
Mitigation: Review escalation decisions before acting on them and scan the skill before deployment, consistent with the clean security verdict and reviewer guidance. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/athola/skills/nm-abstract-escalation-governance) <br>
- [Abstract plugin homepage](https://github.com/athola/claude-night-market/tree/master/plugins/abstract) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Configuration] <br>
**Output Format:** [Markdown guidance with YAML configuration examples and decision tables] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports model-escalation decisions; no API keys or credential environment variables were detected in the submitted artifact.] <br>

## Skill Version(s): <br>
1.9.13 (source: server release metadata; artifact frontmatter says 1.9.8) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
