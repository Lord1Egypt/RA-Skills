## Description: <br>
Continuously captures and applies learnings from errors, user corrections, successful tasks, and periodic reviews to improve agent performance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[keenlycat](https://clawhub.ai/user/keenlycat) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agent operators use this skill to record, search, and review learnings from command failures, user corrections, successful tasks, and insights so future OpenClaw work can avoid repeated mistakes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can persist task details and failed command output in local learning memory, which may include sensitive project data or secrets. <br>
Mitigation: Avoid auto-capturing commands that may expose secrets or sensitive customer or project data, and review captured learnings before retaining them. <br>
Risk: Persistent learning records may remain longer than intended. <br>
Mitigation: Periodically review, edit, or delete ~/.openclaw/workspace/memory/learnings.jsonl according to the user's privacy and retention expectations. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/keenlycat/keenlycat-self-improving-agent) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell command examples and JSONL learning records] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Stores local learning records under ~/.openclaw/workspace/memory/learnings.jsonl when the bundled scripts are used.] <br>

## Skill Version(s): <br>
1.0.1 (source: package.json, release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
