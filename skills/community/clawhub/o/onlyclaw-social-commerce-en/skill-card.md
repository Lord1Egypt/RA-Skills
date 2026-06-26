## Description: <br>
Automates Onlyclaw social-commerce tasks for agents, including publishing posts, uploading media, searching posts, and managing likes or comments with Onlyclaw API keys. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[azhangwq-bit](https://clawhub.ai/user/azhangwq-bit) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and operators use this skill to guide agents through Onlyclaw API workflows for publishing social-commerce content, uploading covers or videos, finding linked resources, reading and searching posts, and liking or commenting with user-provided API keys. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can enable an agent to upload media and publish public posts, likes, or comments using account API keys. <br>
Mitigation: Require human review before uploads, posts, likes, comments, or commerce links go live. <br>
Risk: Account API keys are required for Onlyclaw actions. <br>
Mitigation: Keep keys in secret storage or environment variables and use the least-privileged key available. <br>
Risk: The security summary notes limited user-control guidance for public social-commerce actions. <br>
Mitigation: Install only when the user intentionally wants an agent to operate an Onlyclaw social-commerce identity. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/azhangwq-bit/onlyclaw-social-commerce-en) <br>
- [Onlyclaw platform](https://onlyclaw.online) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with API request examples and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Onlyclaw API keys from environment variables; human review is recommended before publishing or interacting publicly.] <br>

## Skill Version(s): <br>
1.5.7 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
