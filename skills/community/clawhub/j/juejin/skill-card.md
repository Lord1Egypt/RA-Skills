## Description:

掘金平台自动化操作。支持发布沸点、查询话题列表等功能。

This skill is ready for commercial/non-commercial use.

## Publisher:

[lang50](https://clawhub.ai/user/lang50)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to publish Juejin short posts, check Juejin login status, and choose topic or theme IDs for posts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Juejin cookies are password-equivalent secrets and may be exposed if passed directly in shell history or logs.

Mitigation: Use a secret store or ephemeral environment variable for cookies, avoid logging cookie values, and rotate the Juejin session if exposure is suspected.

Risk: The artifact includes an undocumented EvoMap publisher with a hardcoded bearer secret.

Mitigation: Do not run scripts/publish_to_evomap.py unless intentionally publishing metadata to EvoMap after reviewing the credential model and removing or rotating embedded secrets.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lang50/skills/juejin)
- [Publisher profile](https://clawhub.ai/user/lang50)
- [Juejin](https://juejin.cn)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a Juejin login cookie supplied by the user.]

## Skill Version(s):

1.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
