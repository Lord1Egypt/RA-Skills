## Description: <br>
Guide for OpenClaw setup, configuration, commands, routing, and troubleshooting. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zurbrick](https://clawhub.ai/user/zurbrick) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to answer OpenClaw-specific setup, configuration, routing, command, runtime health, session, agent, and troubleshooting questions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may suggest OpenClaw configuration changes or restarts that affect active gateway, channel, session, agent, or command behavior. <br>
Mitigation: Inspect only the relevant config subtree, prefer minimal changes, run the pre-restart validator when relevant, and verify after restart. <br>
Risk: Troubleshooting can misattribute a failure if ingress, routing, authorization, runtime/provider, and delivery layers are collapsed into one diagnosis. <br>
Mitigation: Use the triage sequence to identify the failing layer and separate verified facts from inferred causes and remaining tests. <br>


## Reference(s): <br>
- [OpenClaw Triage Checklist](references/triage-checklist.md) <br>
- [Skill Design Notes for OpenClaw](references/skill-design-notes.md) <br>
- [OpenClaw Guide Release Page](https://clawhub.ai/zurbrick/openclaw-guide-zurbrick) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration instructions] <br>
**Output Format:** [Markdown with concise diagnostic steps, config paths, commands, and pass/fail/warn status when relevant] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Distinguishes verified facts, inferred causes, and remaining tests.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
