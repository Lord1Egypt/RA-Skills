## Description: <br>
Interact with the Manus AI agent platform through its REST API to create or continue tasks, manage projects and files, poll status, and configure webhooks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[krishbhimani](https://clawhub.ai/user/krishbhimani) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to delegate work to Manus, continue tracked Manus sessions, upload files, manage projects, and inspect task status without accidentally duplicating sessions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a Manus API key and can act through the user's Manus account. <br>
Mitigation: Install only when the publisher and skill are trusted, keep MANUS_API_KEY in environment configuration, and do not expose the key in prompts or files. <br>
Risk: Manus API actions can spend credits, upload files, create public sharing links, use connectors, configure webhooks, or change task visibility. <br>
Mitigation: Explicitly confirm new task creation, uploads, public sharing, connector use, webhook changes, deletion, and visibility-changing actions before execution. <br>
Risk: The local session registry can contain prompts, task IDs, and task URLs. <br>
Mitigation: Add .manus_sessions.json to .gitignore and avoid putting secrets or sensitive content in prompts or uploaded files. <br>


## Reference(s): <br>
- [Manus Skill Release Page](https://clawhub.ai/krishbhimani/manus-skill) <br>
- [Manus API Reference](artifact/references/api-reference.md) <br>
- [Session Management Design](artifact/references/session-management.md) <br>
- [Manus API Base URL](https://api.manus.ai) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with shell commands, Python snippets, and Manus API response summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires MANUS_API_KEY; may create or update .manus_sessions.json and call Manus APIs for tasks, files, projects, and webhooks.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
