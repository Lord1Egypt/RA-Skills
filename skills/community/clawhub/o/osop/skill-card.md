## Description: <br>
OSOP workflow authoring, validation, risk analysis, and self-optimization for AI agents. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[archie0125](https://clawhub.ai/user/archie0125) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and AI-agent users use this skill to define, validate, review, execute, log, report on, and improve OSOP workflow definitions for multi-step operational tasks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated .osop workflows, .osoplog.yaml logs, and HTML reports may contain task details, system context, failure information, permissions, or secrets-adjacent workflow data. <br>
Mitigation: Treat generated workflow, log, and report files as sensitive artifacts and review their contents before sharing or storing them outside the intended environment. <br>
Risk: Workflow execution plans can include CLI, database, Docker, infrastructure, MCP, or external-service steps that affect real systems. <br>
Mitigation: Review workflows before execution, prefer dry-run mode when available, and require explicit approval gates for medium or higher risk steps. <br>
Risk: Misconfigured local settings or environment variables could point the skill at an untrusted OSOP MCP endpoint or configuration file. <br>
Mitigation: Verify that ~/.osop/config.yaml and OSOP_MCP_URL point to trusted locations before using OSOP workflow support. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/archie0125/osop) <br>
- [OSOP Website](https://osop.ai) <br>
- [OSOP Specification](https://github.com/Archie0125/osop-spec) <br>
- [OSOP Examples](https://github.com/Archie0125/osop-examples) <br>
- [OSOP Visual Editor](https://osop-editor.vercel.app) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance, Files] <br>
**Output Format:** [Markdown guidance with YAML workflow definitions, shell commands, Mermaid diagrams, structured logs, and HTML report guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce .osop workflow files, .osoplog.yaml execution logs, and standalone HTML reports.] <br>

## Skill Version(s): <br>
1.2.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
