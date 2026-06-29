## Description: <br>
全周期项目发布管控：覆盖版本创建、开发、预发布、发布、验证、运维和下版本规划的 13 步标准流程，支持交互式配置、版本一致性检测、可持续性评分和热更新。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dongjie-oss](https://clawhub.ai/user/dongjie-oss) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and release engineers use this skill to standardize Docker-based GitHub and Alibaba Cloud ACR release workflows, including project setup, version checks, build and publish steps, optional deployment, verification, and next-version planning. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide real release-management actions involving git pushes, tags, Docker builds, ACR publishing, and SSH deployment. <br>
Mitigation: Use explicit release commands and review every proposed git, Docker, ACR, and SSH action before approval. <br>
Risk: Generic trigger words in casual repository discussion could start release-oriented workflows. <br>
Mitigation: Avoid using generic release triggers casually, or clarify that no release, push, tag, registry, or deployment action should be performed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/dongjie-oss/github-acr-release) <br>
- [README.md](artifact/README.md) <br>
- [SKILL.md](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands, generated configuration, and script templates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose git push/tag, Docker/ACR, and SSH deployment actions that require user review before execution.] <br>

## Skill Version(s): <br>
2.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
