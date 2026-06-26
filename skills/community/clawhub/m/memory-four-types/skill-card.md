## Description: <br>
Memory Four Types gives OpenClaw agents a structured way to classify, store, index, and maintain persistent memories as user, feedback, project, and reference Markdown records. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[rickhuang28](https://clawhub.ai/user/rickhuang28) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to keep long-term local memory organized across sessions. It helps agents decide what to remember, where to store it, how to index it, and when to prune or refresh stale entries. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Persistent memory can retain personal, project, or preference details across sessions longer than intended. <br>
Mitigation: Review and prune MEMORY.md, USER.md, SOUL.md, and memory files regularly, and only save context that should persist. <br>
Risk: Secrets or sensitive personal details could be written into local memory files if the agent records raw conversation content. <br>
Mitigation: Follow the skill's sensitive-information checks before writing memory, redact credentials, and avoid saving passwords, API keys, tokens, or unnecessary sensitive details. <br>
Risk: Automated heartbeat, cron, or sub-agent memory maintenance can update stored context without direct user review. <br>
Mitigation: Enable automated maintenance deliberately, review generated memory changes, and keep stale or inaccurate project and reference memories marked or removed. <br>


## Reference(s): <br>
- [ClawHub package page](https://clawhub.ai/rickhuang28/memory-four-types) <br>
- [Memory index template](templates/MEMORY-index.md) <br>
- [User memory template](templates/user-example.md) <br>
- [Feedback memory template](templates/feedback-example.md) <br>
- [Project memory template](templates/project-example.md) <br>
- [Reference memory template](templates/reference-example.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration instructions] <br>
**Output Format:** [Markdown guidance with templates and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local memory organization guidance and Markdown file patterns; no external tools are required.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
