## Description: <br>
ChatBotKit helps an agent operate ChatBotKit resources through an OOMOL-connected account using the `oo` CLI for reading, creating, and updating data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to let an agent inspect and manage ChatBotKit bots, conversations, messages, datasets, files, and account usage through an OOMOL-connected ChatBotKit account. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can read and change ChatBotKit resources through an OOMOL-connected account. <br>
Mitigation: Install it only for agents that should access that account, and require confirmation for write actions that create or update bots, conversations, datasets, records, files, syncs, or uploads. <br>
Risk: Connector actions depend on sensitive credentials managed by the OOMOL connection. <br>
Mitigation: Keep ChatBotKit connected only in the intended OOMOL account and treat authentication or scope errors as setup issues rather than bypassing the connector flow. <br>


## Reference(s): <br>
- [ChatBotKit ClawHub listing](https://clawhub.ai/oomol/oo-chatbotkit) <br>
- [OOMOL publisher profile](https://clawhub.ai/user/oomol) <br>
- [ChatBotKit homepage](https://chatbotkit.com) <br>
- [oo CLI](https://github.com/oomol-lab/oo-cli) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON payloads; connector responses are JSON.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires an installed and authenticated OOMOL `oo` CLI with ChatBotKit connected.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
