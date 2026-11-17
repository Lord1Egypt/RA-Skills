## Description:

面向 magic-api 开发、排障、二开与升版审查的本地源码技能。基于 magic-api、magic-api-plugin、magic-script、magic-api-example 四个仓库整理，强调按问题类型快速定位源码、样例与升级审查资料。

This skill is ready for commercial/non-commercial use.

## Publisher:

[kwin-lv](https://clawhub.ai/user/kwin-lv)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill for Chinese-language guidance when developing, troubleshooting, extending, or upgrade-reviewing magic-api projects. It helps route questions to relevant magic-api, magic-api-plugin, magic-script, and magic-api-example source areas and examples.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may be incomplete when the expected magic-api repositories or referenced local documents are not available with the artifact.

Mitigation: Use it in workspaces that include the referenced magic-api source repositories and local references, and require the agent to state when a supporting file or repository is unavailable.

Risk: Generated troubleshooting or upgrade-review guidance could be wrong if it is not checked against the user's actual magic-api version and project code.

Mitigation: Review recommendations against the local source, configuration, scripts, and target version before applying changes.

## Reference(s):

- [magic-plus ClawHub Skill Page](https://clawhub.ai/kwin-lv/skills/magic-plus)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline code, file paths, configuration snippets, and command suggestions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Chinese-language responses oriented around source navigation, examples, troubleshooting steps, extension guidance, and upgrade-review conclusions.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
