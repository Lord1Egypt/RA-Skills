## Description: <br>
OpenSpec helps agents use @fission-ai/openspec for spec-driven development when implementing non-trivial changes in existing projects. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[juanclaw](https://clawhub.ai/user/juanclaw) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to have agents propose, validate, implement, and archive OpenSpec change folders for non-trivial repository changes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated or archived openspec/ planning files may steer implementation incorrectly if accepted without review. <br>
Mitigation: Use the skill in version-controlled repositories, review generated or archived openspec/ files, and validate OpenSpec changes before implementation or archive. <br>
Risk: Untrusted OpenSpec tool implementations could affect project-local planning files. <br>
Mitigation: Expose OpenSpec tools only from trusted sources in the agent environment. <br>


## Reference(s): <br>
- [OpenSpec workflow patterns](references/workflow.md) <br>
- [OpenSpec ClawHub release](https://clawhub.ai/juanclaw/openspec-skill) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with OpenSpec artifact examples and tool command names] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May guide creation or updates of project-local openspec/ proposal, design, spec, and task files.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
