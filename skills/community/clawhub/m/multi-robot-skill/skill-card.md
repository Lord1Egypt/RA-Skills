## Description:

Multi Robot Skill enables AI agents to coordinate multiple robots through perception feedback, dynamic adapters, and parallel scheduling for robotic arms, quadrupeds, and other HTTP API robots.

This skill is ready for commercial/non-commercial use.

## Publisher:

[alan1112223331](https://clawhub.ai/user/alan1112223331)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and robot operators use this skill to let AI agents integrate HTTP API robots, generate adapters, register robots, plan parallel or sequential tasks, execute coordinated workflows, and summarize results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can send live HTTP commands to physical robots without sufficient safety, authorization, endpoint, or failure-handling guardrails.

Mitigation: Use it only in a controlled test network or simulator unless endpoint allowlists, authenticated robot APIs, human confirmation for hazardous actions, per-robot locking, failure-stop behavior for dependent tasks, and timeout or retry enforcement are added.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/alan1112223331/skills/multi-robot-skill)
- [README](artifact/README.md)
- [Usage Guide](artifact/USAGE_GUIDE.md)
- [OpenClaw Integration Guide](artifact/OPENCLAW_INTEGRATION.md)
- [Adapter API Fixes](artifact/ADAPTER_FIXES.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with Python code and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include generated RobotAdapter code, robot registration configuration, task plans, and execution-result summaries.]

## Skill Version(s):

2.0.0 (source: server release metadata and artifact/_meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
