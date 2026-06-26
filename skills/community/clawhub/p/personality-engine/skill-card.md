## Description: <br>
Personality Engine adds editorial voice, selective silence, urgency-aware timing, ambient pings, daily context, and engagement adaptation to proactive OpenClaw agents. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kingmadellc](https://clawhub.ai/user/kingmadellc) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers building proactive OpenClaw agents use this skill to transform trigger outputs into opinionated, rate-aware, context-sensitive messages. It is suited to trading agents, assistants, monitoring agents, and other systems that send alerts or digests. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can send unprompted messages through micro-initiations and proactive trigger handling. <br>
Mitigation: Require explicit user opt-in, provide clear disable controls, and monitor cadence logs and rate limits before deployment. <br>
Risk: The skill stores local interaction history and engagement metrics. <br>
Mitigation: Use separate state directories per user or agent, set retention limits, and provide deletion controls for stored state. <br>
Risk: Stored context summaries may include user interaction patterns that should not be sent to external model APIs without review. <br>
Mitigation: Review integrations that transmit context externally and avoid sharing stored summaries unless the user has approved that data flow. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/kingmadellc/personality-engine) <br>
- [Personality Engine README](README.md) <br>
- [Personality Engine Architecture Overview](references/systems-overview.md) <br>
- [Personality Engine Customization Guide](references/customization.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, code, configuration, guidance] <br>
**Output Format:** [Python objects and strings, with Markdown documentation and Python integration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can schedule, suppress, enrich, or initiate outbound messages and uses local JSON state for daily context, micro-initiation cadence, and engagement metrics.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
