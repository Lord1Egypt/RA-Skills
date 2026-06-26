## Description: <br>
Control macOS applications via Accessibility API through an MCP server to open apps, click buttons, type text, press keys, scroll, and read UI state. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[reg2005](https://clawhub.ai/user/reg2005) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use this skill to automate and inspect native macOS GUI workflows through an MCP server when a CLI or API path is not available. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill gives an agent broad desktop control and screen-reading power on macOS. <br>
Mitigation: Install only when intentional, supervise use in sensitive applications, and avoid exposing passwords or private messages on screen. <br>
Risk: Traversal JSON files may contain UI state or screen content in /tmp/macos-use. <br>
Mitigation: Clear /tmp/macos-use after use. <br>
Risk: Accessibility permission can remain active after the task is complete. <br>
Mitigation: Unregister the mcporter server and revoke Accessibility permission when the skill is no longer needed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/reg2005/mac-compute-use) <br>
- [mcp-server-macos-use upstream project](https://github.com/mediar-ai/mcp-server-macos-use) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance, JSON] <br>
**Output Format:** [Markdown guidance with inline shell commands and MCP tool responses that may include JSON file paths] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires macOS, mcporter, Homebrew installation of mcp-server-macos-use, and Accessibility permission.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
