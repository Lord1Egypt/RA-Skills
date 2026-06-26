## Description: <br>
Recreates the "汤汤好梦" Chinese cat persona for warm, accurate replies, persona-styled message drafting, and opt-in proactive check-ins through supported OpenClaw scheduling or delivery channels. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fengqiufq](https://clawhub.ai/user/fengqiufq) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and OpenClaw operators use this skill to generate Chinese companion-style responses, rewrite messages in the Meow Speech persona, and prepare sparse bedtime or idle-time check-ins when the user has explicitly opted in. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Scheduled check-ins or external-channel delivery could become unwanted if enabled without clear consent or reviewed job settings. <br>
Mitigation: Enable proactive check-ins only after explicit opt-in, then review host-created jobs, delivery channel, frequency caps, quiet windows, and opt-out controls. <br>
Risk: Memory-backed continuity may retain personal preferences or routines beyond what the user intended. <br>
Mitigation: Use only the platform-approved memory store when the user enables memory continuity, and avoid storing extra personal notes. <br>
Risk: Persona-styled responses may prioritize warmth over precision if used for technical or practical tasks. <br>
Mitigation: Keep factual answers accurate and useful while applying the persona style, and use concise structured troubleshooting when needed. <br>


## Reference(s): <br>
- [Install-time activation quickstart](references/activation-quickstart.md) <br>
- [Meow Speech Automation Guide](references/automation-guide.md) <br>
- [Heartbeat Check List](references/heartbeat-checklist.md) <br>
- [Local Auto Task Template (Low-Token)](references/local-automation-template.md) <br>
- [Meow Speech Reference Notes](references/persona-notes.md) <br>
- [Scheduler Templates for Meow Speech](references/scheduler-templates.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Configuration guidance] <br>
**Output Format:** [Chinese natural-language responses and Markdown guidance with optional JSON-like scheduler examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs should stay concise, persona-consistent, and avoid proactive outreach unless the user has opted in.] <br>

## Skill Version(s): <br>
1.3.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
