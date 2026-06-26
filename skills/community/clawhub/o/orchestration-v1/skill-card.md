## Description: <br>
Orchestrate multi-agent teams with defined roles, task lifecycles, handoff protocols, review workflows, async communication, and artifact sharing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhangjun20250818-cyber](https://clawhub.ai/user/zhangjun20250818-cyber) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to coordinate sustained multi-agent workflows, define agent roles, route tasks through review, and manage handoffs through shared artifacts and comments. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The artifact includes under-scoped instructions for sending messages in an external chat and taking a post-send snapshot. <br>
Mitigation: Require human confirmation of the exact recipient or chat, exact message content, authorization to send, and retention or deletion handling for any snapshot before external messages are sent. <br>
Risk: The Justin/Physical Strike section can create operational risk if treated as a general execution protocol. <br>
Mitigation: Tightly control or remove that section before installation when the deployment does not need a human-operated external messaging workflow. <br>


## Reference(s): <br>
- [Team Setup](references/team-setup.md) <br>
- [Task Lifecycle](references/task-lifecycle.md) <br>
- [Communication](references/communication.md) <br>
- [Patterns](references/patterns.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/zhangjun20250818-cyber/orchestration-v1) <br>
- [Publisher Profile](https://clawhub.ai/user/zhangjun20250818-cyber) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Configuration, Shell commands] <br>
**Output Format:** [Markdown guidance with templates, checklists, and inline command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces process guidance for agent roles, task state, handoffs, reviews, and artifact conventions.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
