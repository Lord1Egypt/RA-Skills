## Description: <br>
Inner Life Dream adds quiet-hours creative exploration for an agent and captures dream-style reflections for later review. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[DKistenev](https://clawhub.ai/user/DKistenev) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent operators use this skill to let an OpenClaw agent generate occasional, freeform reflections during quiet hours and preserve those insights in local memory for later review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Local dream notes and memory updates may preserve sensitive, stale, or misleading reflections if left unreviewed. <br>
Mitigation: Periodically review memory/dreams, memory/inner-state.json, memory/drive.json, and daily-note dream markers. <br>
Risk: Cron or heartbeat execution can create repeated local memory writes beyond the operator's intent. <br>
Mitigation: Keep maxDreamsPerNight and dreamChance conservative, and confirm inner-life-core initialization before enabling scheduled execution. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/DKistenev/inner-life-dream) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with shell command and JSON configuration examples; the runtime script emits a topic string when dreaming should run.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes local dream notes and updates local dream, inner-state, and drive state files when integrated by the agent.] <br>

## Skill Version(s): <br>
1.0.6 (source: server evidence release and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
