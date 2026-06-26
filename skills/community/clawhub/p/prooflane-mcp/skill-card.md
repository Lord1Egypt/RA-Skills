## Description: <br>
Clone, install, configure, verify, and run Prooflane's repo-native stdio MCP server locally without claiming unavailable hosted or package-registry distribution. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xiaojiou176](https://clawhub.ai/user/xiaojiou176) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and evaluators use this skill to attach an MCP-capable agent to a local Prooflane checkout, verify the repo-native stdio server, and inspect run, report, and proof surfaces through a truthful first-success path. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill directs users to clone a third-party repository and run local setup or start commands. <br>
Mitigation: Review the cloned repository scripts first and run them in a trusted or sandboxed workspace. <br>
Risk: Token-protected HTTP/API automation surfaces may require an automation token. <br>
Mitigation: Provide tokens through secure environment handling, avoid committing them to files, and avoid logging them. <br>
Risk: Users may overstate current distribution by treating publish-ready package shapes or hosted service paths as live. <br>
Mitigation: Keep claims limited to the repo-native stdio MCP server unless fresh evidence proves package publication or hosted availability. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/xiaojiou176/prooflane-mcp) <br>
- [Publisher Profile](https://clawhub.ai/user/xiaojiou176) <br>
- [Canonical Prooflane Repository](https://github.com/xiaojiou176-open/ui-automation-control-plane) <br>
- [OpenHands Extension Pull Request](https://github.com/OpenHands/extensions/pull/161) <br>
- [Install And Attach Prooflane MCP](artifact/references/INSTALL.md) <br>
- [Prooflane MCP Capabilities](artifact/references/CAPABILITIES.md) <br>
- [First-Success Path](artifact/references/DEMO.md) <br>
- [Troubleshooting](artifact/references/TROUBLESHOOTING.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with shell command blocks and JSON MCP configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Keeps output scoped to local repo-native stdio MCP setup, verification, and proof-oriented first-use guidance.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata and artifact manifest.yaml) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
