## Description: <br>
Natural Language Planner turns natural conversation into organized local tasks and projects with Markdown storage and a local Kanban dashboard. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bparticle](https://clawhub.ai/user/bparticle) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Employees, external users, and developers use this skill to capture tasks and projects from conversation, organize them as local Markdown/YAML files, track priorities and deadlines, and view work in a local dashboard. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The unauthenticated dashboard and attachments may expose task data when LAN mode, tunnels, static hosting, or persistent services are enabled. <br>
Mitigation: Keep the dashboard bound to localhost for sensitive work and avoid LAN mode, public tunnels, static hosting, and systemd persistence unless the exposure is understood. <br>
Risk: Conversation-derived tasks may include sensitive information stored in local Markdown files. <br>
Mitigation: Use an appropriate local workspace location and protect filesystem access to planner data. <br>


## Reference(s): <br>
- [Natural Language Planner README](artifact/README.md) <br>
- [Architecture Overview](artifact/ARCHITECTURE.md) <br>
- [Conversation Examples](artifact/examples/conversation_examples.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/bparticle/natural-language-planner) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown responses with inline Python or shell snippets plus local Markdown/YAML task and project files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update local workspace files and start a local unauthenticated dashboard.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
