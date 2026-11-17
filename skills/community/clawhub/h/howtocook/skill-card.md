## Description:

基于MCP协议的AI菜谱推荐服务器，提供菜谱查询、分类筛选、智能膳食规划和每日菜单推荐功能。

This skill is ready for commercial/non-commercial use.

## Publisher:

[cainingnk](https://clawhub.ai/user/cainingnk)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to look up recipes, filter by category, retrieve recipe details, and generate meal recommendations or weekly meal plans based on party size, avoided ingredients, and allergies.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks for a Xiaobenyang API key and stores it in a local plaintext .env file.

Mitigation: Use a disposable or tightly scoped key when possible, avoid entering valuable credentials in shared workspaces, and rotate the key if the .env file may have been exposed.

Risk: The publisher should replace plaintext persistence with host-managed secret storage or require explicit consent and restrictive file permissions.

Mitigation: Review credential handling before installation in managed or shared environments.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/cainingnk/skills/howtocook)
- [Xiaobenyang API key portal](https://xiaobenyang.com)

## Skill Output:

**Output Type(s):** [text, markdown, configuration guidance, API calls]

**Output Format:** [Markdown summaries of JSON API results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a Xiaobenyang API key; recipe and meal-plan content depends on upstream API responses.]

## Skill Version(s):

1.0.1 (source: server release metadata; artifact frontmatter says 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
