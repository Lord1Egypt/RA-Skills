## Description: <br>
Multi Agent Project Collaboration Factory helps developers scaffold and run a configurable multi-agent workflow for project planning, research, architecture, implementation, and testing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ninetyhe-90](https://clawhub.ai/user/ninetyhe-90) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and builders use this skill to decompose an internet project into specialist agent workstreams, generate a project scaffold, and guide requirements, research, architecture, implementation, and testing outputs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The generator creates and may replace a local project scaffold in the current working directory. <br>
Mitigation: Run it from the intended parent directory, choose a fresh project name, and do not approve overwrite prompts unless the existing directory is backed up or disposable. <br>
Risk: Broad or incorrect project configuration can steer downstream agents toward unsuitable implementation work. <br>
Mitigation: Review PROJECT_CONFIG.yaml and the generated execution guide before asking agents to produce or modify code. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ninetyhe-90/multi-agent-project-builder) <br>
- [Publisher profile](https://clawhub.ai/user/ninetyhe-90) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance, YAML configuration, generated project files, and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates a local project scaffold with configurable agent roles, workflow phases, and output directories.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
