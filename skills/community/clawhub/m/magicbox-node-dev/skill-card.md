## Description: <br>
Node.js + TypeScript 项目开发规范和最佳实践指南，用于指导 MagicBox Node 服务的开发、代码风格、目录结构、配置管理和容器部署。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[JinChunCheng123](https://clawhub.ai/user/JinChunCheng123) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill as a reference guide for building MagicBox Node services with Node.js, TypeScript, TypeORM, Docker, Kubernetes, and consistent project conventions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Deployment examples may include practices that are too permissive for production environments, such as broad file permissions or long-running auxiliary services. <br>
Mitigation: Review and harden container snippets before use; remove sshd and cron unless explicitly required and avoid chmod 777. <br>
Risk: Example package registry and deployment commands may target infrastructure that is not appropriate for the adopter's environment. <br>
Mitigation: Use a trusted HTTPS npm registry and confirm Docker and Kubernetes targets before running commands. <br>
Risk: Configuration examples include database settings that could be mishandled if copied directly. <br>
Mitigation: Store real database passwords in Kubernetes Secrets or a vault rather than ConfigMaps or source-controlled configuration files. <br>


## Reference(s): <br>
- [Skill definition](SKILL.md) <br>
- [Code style guide](references/code-style.md) <br>
- [Configuration management guide](references/config-management.md) <br>
- [Container deployment guide](references/container-deployment.md) <br>
- [Directory structure guide](references/directory-structure.md) <br>
- [ClawHub skill page](https://clawhub.ai/JinChunCheng123/magicbox-node-dev) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown reference guidance with code, shell, JSON, Dockerfile, and YAML examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Documentation-only guidance; snippets should be reviewed and hardened before production use.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
