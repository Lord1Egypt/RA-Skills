## Description: <br>
Use this when the user wants to install or set up the Scientify research plugin. Adds research-pipeline, literature-survey, idea-generation, arxiv tools, and workspace management. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Springleave](https://clawhub.ai/user/Springleave) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External researchers and developers use this skill to install the Scientify OpenClaw plugin for literature surveys, research planning, implementation support, experiment workflows, and workspace management. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The installer text tells the agent to proceed without asking. <br>
Mitigation: Require explicit user confirmation before installing Scientify or making workspace changes. <br>
Risk: The release evidence reports conflicting installation guidance. <br>
Mitigation: Use the OpenClaw plugin manager path, `openclaw plugins install scientify`, and avoid direct npm installation unless separately reviewed. <br>
Risk: The skill can lead to paper downloads, generated code execution, experiments, or project deletion. <br>
Mitigation: Ask for confirmation before downloads, generated code execution, experiments, or destructive project actions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Springleave/install-scientify) <br>
- [Scientify npm package](https://www.npmjs.com/package/scientify) <br>
- [Scientify GitHub link from artifact](https://github.com/tsingyuai/scientify) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, code, guidance] <br>
**Output Format:** [Markdown with inline shell commands and research workflow guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May guide plugin installation, paper downloads, generated code execution, experiments, and project workspace actions.] <br>

## Skill Version(s): <br>
1.7.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
