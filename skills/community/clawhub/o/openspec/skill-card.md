## Description: <br>
Spec-driven development with OpenSpec CLI for feature planning, migrations, refactors, and structured implementation workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jcorrego](https://clawhub.ai/user/jcorrego) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineering agents use this skill to manage spec-driven changes through proposal, requirements, design, task tracking, implementation, validation, and archive steps. It is useful when work needs an explicit change workflow and project-local OpenSpec artifacts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Installing the OpenSpec CLI with @latest can reduce reproducibility or introduce unreviewed CLI changes. <br>
Mitigation: Pin a trusted @fission-ai/openspec version before installation in sensitive or reproducible projects. <br>
Risk: OpenSpec commands can create, update, validate, and archive project artifacts that affect repository state. <br>
Mitigation: Use version control, inspect generated openspec/ and .claude/skills/ files, and review proposed implementation changes before accepting them. <br>


## Reference(s): <br>
- [Schema Reference](references/schemas.md) <br>
- [ClawHub OpenSpec Skill Page](https://clawhub.ai/jcorrego/openspec) <br>
- [jcorrego Publisher Profile](https://clawhub.ai/user/jcorrego) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands, project file paths, and configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guides agents to create and update OpenSpec project artifacts such as proposal.md, specs, design.md, tasks.md, and config.yaml.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
