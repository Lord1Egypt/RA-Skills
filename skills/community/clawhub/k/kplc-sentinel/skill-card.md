## Description: <br>
Track Kenyan prepaid electricity (KPLC) tokens, predict blackout times, and get proactive low-balance alerts through chat. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lewisawe](https://clawhub.ai/user/lewisawe) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users in Kenyan households use this skill to track prepaid KPLC token purchases, meter readings, remaining power, electricity spending, and planned outages through an OpenClaw chat agent. <br>

### Deployment Geography for Use: <br>
Kenya <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores household electricity, location/area, appliance, budget, and top-up history locally. <br>
Mitigation: Install only if this local data storage is acceptable, and review the stored profile and history before sharing or transferring the skill environment. <br>
Risk: The skill can create persistent reminders or calendar entries and can steer payment handoff flows without clear confirmation rules. <br>
Mitigation: Require explicit user approval before calendar/reminder creation or payment handoff, especially for outage reminders and low-balance top-up flows. <br>
Risk: The reset command clears profile data immediately. <br>
Mitigation: Confirm the user intends to clear profile data before running or routing a reset request. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/lewisawe/kplc-sentinel) <br>
- [KPLC Planned Maintenance Schedule PDF](https://www.kplc.co.ke/storage/01KPWN6FYWZ5Q9MKXJDHW7EG1A.pdf) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Natural-language chat responses derived from JSON action data, with setup and execution commands in Markdown code blocks.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The Python entrypoint emits JSON for the agent; the agent should convert it into concise user-facing guidance rather than exposing raw JSON.] <br>

## Skill Version(s): <br>
1.7.3 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
