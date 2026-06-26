## Description: <br>
Browse a Hookify rule catalog for common git, Python, security, workflow, and performance rules. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[athola](https://clawhub.ai/user/athola) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to browse pre-built Hookify rules and choose standard rules to install or adapt in a project. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Installed Hookify rules may persistently change future agent behavior in a project. <br>
Mitigation: Before installation, confirm the source rule file exists, preview the destination under .claude/, and review the rule behavior. <br>
Risk: Project configuration writes can affect future development workflows. <br>
Mitigation: Install only the rules needed for the project and keep installed rules visible for review before relying on them. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/athola/nm-hookify-rule-catalog) <br>
- [Metadata homepage](https://github.com/athola/claude-night-market/tree/master/plugins/hookify) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown with inline shell commands and rule tables] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Documentation-only catalog; rule installation is user-directed and may write persistent project configuration files.] <br>

## Skill Version(s): <br>
1.9.12 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
