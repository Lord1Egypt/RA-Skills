## Description: <br>
MCP server for the DRAIN payment protocol that lets agents discover providers, open USDC payment channels on Polygon, and call paid services such as LLMs, scraping, image generation, VPN, and more. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kimbo128](https://clawhub.ai/user/kimbo128) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agent users use this skill to connect an MCP client to drain-mcp, fund a dedicated Polygon wallet, and let agents pay per request for third-party services through DRAIN channels. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The local MCP server uses real wallet credentials and paid network services. <br>
Mitigation: Use only a dedicated low-value Polygon wallet, avoid main wallets, and keep deposits small. <br>
Risk: Open payment channels can commit funds until they are closed or expire. <br>
Mitigation: Open channels only with the amount needed for the task and close channels when work is complete. <br>
Risk: Third-party providers receive the request content sent through paid service calls. <br>
Mitigation: Treat selected providers as recipients of request content and send only information intended for that provider. <br>


## Reference(s): <br>
- [ClawHub listing](https://clawhub.ai/kimbo128/hs58) <br>
- [Handshake58 website](https://handshake58.com) <br>
- [Provider directory](https://handshake58.com/directory) <br>
- [drain-mcp package](https://www.npmjs.com/package/drain-mcp) <br>
- [Project repository](https://github.com/kimbo128/DRAIN) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JSON configuration and shell command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires drain-mcp and a local DRAIN_PRIVATE_KEY for wallet-backed MCP actions.] <br>

## Skill Version(s): <br>
4.0.2 (source: frontmatter, release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
