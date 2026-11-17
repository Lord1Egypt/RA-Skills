## Description:

Node.js + TypeScript 项目开发规范和最佳实践指南。用于指导 MagicBox Node 服务的开发、代码风格、目录结构、配置管理、容器部署等方面的规范。

This skill is ready for commercial/non-commercial use.

## Publisher:

[jinchuncheng123](https://clawhub.ai/user/jinchuncheng123)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to get MagicBox Node service guidance for Node.js and TypeScript project structure, code style, configuration management, database conventions, API patterns, container deployment, logging, error handling, and review practices.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Copyable deployment examples include unsafe production patterns such as broad file permissions, an HTTP npm registry, sshd/crond in the application container, ConfigMap database credentials, and permissive CORS.

Mitigation: Review every deployment and configuration snippet before use; replace broad permissions, use trusted HTTPS registries, remove unnecessary daemons, store credentials in Secrets or a secret manager, and restrict CORS to known origins.

Risk: The security verdict is suspicious because the skill is documentation-only but could weaken systems if its examples are followed as production templates.

Mitigation: Treat the skill as rough internal documentation, adapt examples to local security standards, and run normal code, container, and infrastructure review before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jinchuncheng123/skills/magicbox-node-dev)
- [Code style guide](references/code-style.md)
- [Configuration management guide](references/config-management.md)
- [Container deployment guide](references/container-deployment.md)
- [Directory structure guide](references/directory-structure.md)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown with inline code blocks and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Documentation-only guidance for Node.js and TypeScript service development; copyable deployment examples require review before production use.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
