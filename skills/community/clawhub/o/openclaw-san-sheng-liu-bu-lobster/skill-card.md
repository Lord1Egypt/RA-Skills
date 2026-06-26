## Description: <br>
Coordinates OpenClaw task decomposition for solo-company workflows by assigning work to subagents, sending Feishu notifications, creating Feishu documents, updating Feishu tables, and consolidating deliverables. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jiebao360](https://clawhub.ai/user/jiebao360) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Solo operators, small teams, founders, content creators, and knowledge-commerce workers use this skill to split content and research work across OpenClaw subagents, coordinate Feishu notifications, track progress, and collect final Markdown and Feishu document deliverables. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Bundled Feishu OpenIDs, chat IDs, base links, app/table tokens, and folder tokens may point to an unintended workspace or recipient set. <br>
Mitigation: Replace every bundled Feishu identifier with approved workspace-specific values before installation or execution. <br>
Risk: The workflow can send Feishu messages, create cloud documents, update tables, and keep spawned subagent sessions. <br>
Mitigation: Require a dry-run inventory of recipients, documents, table records, and subagent sessions before running real tasks. <br>
Risk: Task outputs may include sensitive or private content that is copied into Feishu documents or tables. <br>
Mitigation: Verify Feishu sharing permissions and data handling rules before sending private content to Feishu. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/jiebao360/openclaw-san-sheng-liu-bu-lobster) <br>
- [README](artifact/README.md) <br>
- [Lobster Team Configuration](artifact/config/lobster-team.md) <br>
- [Feishu Document Automation Guide](artifact/docs/auto-create-feishu-doc.md) <br>
- [Task Tracking Guide](artifact/docs/task-tracking.md) <br>
- [Task Templates](artifact/templates/task-templates.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown task plans, Feishu document and table update instructions, configuration tables, and inline command or API-call examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update Feishu cloud documents, Feishu table records, local Markdown files, and persistent subagent sessions when executed in a configured environment.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
