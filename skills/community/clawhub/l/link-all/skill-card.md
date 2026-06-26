## Description: <br>
Link All helps an agent research, select, configure, and test ways to connect external platforms through plugins, CLIs, or APIs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jeandoom](https://clawhub.ai/user/jeandoom) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill when they need an agent to find official connection options for an external service, present choices for confirmation, configure the chosen plugin, CLI, or API approach, and document the successful setup for reuse. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Connecting external services can expose accounts or data if broad OAuth scopes, tokens, or untrusted tools are used. <br>
Mitigation: Confirm each tool and permission scope before use, prefer official plugins or CLIs, and use least-privilege OAuth grants or tokens. <br>
Risk: Generated scripts or saved skills may preserve incorrect setup details or sensitive configuration. <br>
Mitigation: Review generated code and any SKILL.md before saving or running it, and keep secrets in approved credential stores rather than skill text. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown reports with inline commands, configuration steps, and generated scripts when APIs are selected.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires user confirmation before executing a selected linking approach or saving a new skill.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
