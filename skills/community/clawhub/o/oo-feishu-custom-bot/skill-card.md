## Description: <br>
Helps an agent send Feishu/Lark custom bot webhook messages through an OOMOL-connected account using the oo CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to have an agent send approved Feishu/Lark custom bot messages, including text, image, rich post, interactive card, and shared-chat messages. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill description is broader than the documented actions and could be mistaken for support for reading or updating Feishu data. <br>
Mitigation: Use it only for the documented Feishu/Lark custom bot send-message actions unless the publisher updates the documented action set. <br>
Risk: All documented send actions are write operations that can post unintended content to Feishu/Lark. <br>
Mitigation: Inspect the live connector schema and confirm the exact message payload and effect with the user before execution. <br>
Risk: The skill requires a connected account and sensitive credentials managed through OOMOL. <br>
Mitigation: Install it only for Feishu/Lark custom bot messaging workflows and avoid exposing raw tokens in prompts, files, or command arguments. <br>


## Reference(s): <br>
- [Feishu Custom Bot homepage](https://www.feishu.cn) <br>
- [oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [ClawHub skill page](https://clawhub.ai/oomol/oo-feishu-custom-bot) <br>
- [Publisher profile](https://clawhub.ai/user/oomol) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline bash commands and JSON payload guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires live connector schema inspection before constructing action payloads.] <br>

## Skill Version(s): <br>
1.0.1 (source: server evidence and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
