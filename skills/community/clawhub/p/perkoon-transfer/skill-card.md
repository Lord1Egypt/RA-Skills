## Description: <br>
Perkoon Transfer helps agents move files over Perkoon using MCP, CLI, A2A, or browser automation workflows for agent-to-human, agent-to-agent, and pipeline transfers. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[alex-vy](https://clawhub.ai/user/alex-vy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to send, receive, and monitor Perkoon file transfers from coding agents, shell-capable agents, HTTP-only agents, or browser automation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Optional browser automation commands download and immediately run remote .mjs scripts without pinning or integrity checks. <br>
Mitigation: Prefer the pinned MCP or CLI workflows, and do not run downloaded .mjs scripts unless the current contents from perkoon.com have been reviewed or separately verified. <br>
Risk: File-transfer workflows can expose unintended or sensitive local files if paths are not checked before sending. <br>
Mitigation: Confirm every file path before sending and avoid sensitive directories unless the user explicitly intends to transfer those files. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/alex-vy/perkoon-transfer) <br>
- [Perkoon homepage](https://perkoon.com) <br>
- [Perkoon A2A agent card](https://perkoon.com/.well-known/agent.json) <br>
- [Perkoon integration guide](https://perkoon.com/llms.txt) <br>
- [Perkoon automation docs](https://perkoon.com/automate) <br>
- [Perkoon CLI package](https://www.npmjs.com/package/perkoon) <br>
- [Perkoon MCP package](https://www.npmjs.com/package/@perkoon/mcp) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown instructions with JSON snippets, shell commands, and configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands may produce JSON event streams, session codes, transfer links, and downloaded files when executed.] <br>

## Skill Version(s): <br>
2.0.2 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
