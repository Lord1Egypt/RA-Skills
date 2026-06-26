## Description: <br>
Learning Loop - GEARS System helps agents set up autonomous cron-based GEARS learning pipelines for mastering complex topics through five-session feedback loops. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sagarmainkar](https://clawhub.ai/user/sagarmainkar) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill when they want an agent to build a structured curriculum, schedule recurring learning sessions, test progress, and synthesize mastered knowledge for a topic with verifiable answers. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can create scheduled autonomous learning jobs that continue after the initial setup. <br>
Mitigation: Before starting a pipeline, review the topic, timing, notification destination, expected duration, and how to pause or remove pending learning-* cron jobs. <br>
Risk: Autonomous research and self-scoring can produce incorrect or misleading learning material. <br>
Mitigation: Use the skill for topics with clear right or wrong answers, review generated curricula and session outputs, and verify important claims against cited sources. <br>


## Reference(s): <br>
- [ClawHub Release Page](https://clawhub.ai/sagarmainkar/learning-loop-skill) <br>
- [OpenClaw](https://openclaw.com) <br>
- [Learning Loop Methodology](references/methodology.md) <br>
- [Playbook Template](references/playbook-template.md) <br>
- [State Schema](references/state-schema.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance, JSON state files, shell command invocations, and cron job configuration.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates per-topic learning artifacts under memory/learning and scheduled agent jobs after user confirmation.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
