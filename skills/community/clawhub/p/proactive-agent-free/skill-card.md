## Description: <br>
Provides a proactive-agent operating pattern that uses persistent context, a write-ahead-log protocol, work buffers, compression recovery, safety guardrails, self-improvement checks, heartbeat routines, and growth loops to help an AI agent anticipate needs and improve task continuity. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users can use this skill as guidance for configuring proactive AI-agent behavior, including context persistence, WAL-style memory updates, compression recovery, validation-before-reporting, and self-improvement guardrails. It is best suited to workflows where persistent memory and supervised proactive behavior are acceptable. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill encourages broad persistent memory of user context without clear consent, retention, or sensitive-data boundaries. <br>
Mitigation: Require explicit user confirmation before storing context, and define what may be stored, retention duration, inspection access, deletion process, and prohibited sensitive-data categories. <br>
Risk: Proactive or heartbeat-driven actions can become too frequent or exceed the user's intended scope. <br>
Mitigation: Use human approval for high-impact actions, set frequency limits, and apply anti-drift checks before allowing autonomous follow-up behavior. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/thcjp/skills/proactive-agent-free) <br>
- [Publisher profile](https://clawhub.ai/user/thcjp) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration] <br>
**Output Format:** [Markdown with tables and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include task status, summaries, configuration steps, recovery guidance, and error-handling notes.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata; artifact frontmatter states 1.0.1) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
