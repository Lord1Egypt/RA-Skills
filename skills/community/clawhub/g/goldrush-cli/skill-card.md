## Description: <br>
GoldRush CLI is a terminal-first blockchain data tool with MCP support for Claude Desktop and Claude Code. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gane5h](https://clawhub.ai/user/gane5h) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, engineers, and AI-agent users use this skill to run GoldRush CLI commands for wallet balances, token searches, gas estimates, DEX pair monitoring, wallet activity streaming, and Claude MCP setup. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow uses the @covalenthq/goldrush-cli npm package and stores a GoldRush API key in the operating system keychain. <br>
Mitigation: Install and authenticate only on trusted machines after confirming the npm package is expected, and run goldrush logout when access is no longer needed. <br>
Risk: Running goldrush install makes GoldRush MCP tools available to Claude Desktop or Claude Code. <br>
Mitigation: Run goldrush install only when MCP access is intended, and remove or disable the MCP configuration when the tool should no longer be available. <br>
Risk: Streaming commands such as new_pairs, ohlcv_pairs, and watch can run continuously and expose live blockchain activity in the terminal or agent context. <br>
Mitigation: Stop streaming sessions when monitoring is complete and avoid streaming wallet activity into shared or untrusted contexts. <br>


## Reference(s): <br>
- [GoldRush CLI overview](references/overview.md) <br>
- [Model Context Protocol](https://modelcontextprotocol.io/) <br>
- [ClawHub skill page](https://clawhub.ai/gane5h/goldrush-cli) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and CLI examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include one-shot CLI queries, MCP setup guidance, and long-running streaming command guidance.] <br>

## Skill Version(s): <br>
3.0.5 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
