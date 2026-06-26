## Description: <br>
Analyzes a software project and generates Docker build and deployment files, Compose workflows, configuration templates, and containerization documentation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhuyifeiruichuang](https://clawhub.ai/user/zhuyifeiruichuang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and platform engineers use this skill to inspect existing projects and produce a deploy/ workspace with Dockerfiles, Docker Compose files, scripts, configuration templates, and documentation for Docker-based builds and deployments. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated deployment artifacts may copy real configuration secrets into deploy/.env or deploy/config. <br>
Mitigation: Inspect generated files, remove secrets, and add sensitive deploy paths to .gitignore before committing. <br>
Risk: Generated Docker and Compose commands can build and run project-controlled code. <br>
Mitigation: Review generated Dockerfiles, shell scripts, and Compose files before running them, and use the skill only on trusted projects. <br>
Risk: Generated containers may default to running as root. <br>
Mitigation: Change generated Dockerfiles to use a non-root user when root is not required. <br>


## Reference(s): <br>
- [project-containerize ClawHub page](https://clawhub.ai/zhuyifeiruichuang/project-containerize) <br>
- [Publisher profile](https://clawhub.ai/user/zhuyifeiruichuang) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance plus generated Dockerfiles, Compose YAML, shell scripts, and configuration templates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces project-local deploy/ artifacts for human review before execution.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
