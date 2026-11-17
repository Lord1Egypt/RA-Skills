## Description:

Control macOS applications through the Accessibility API via an MCP server to open apps, click buttons, type text, press keys, scroll, and read UI state.

This skill is ready for commercial/non-commercial use.

## Publisher:

[reg2005](https://clawhub.ai/user/reg2005)

### License/Terms of Use:


## Use Case:

Developers and agent operators use this skill to automate native macOS GUI workflows when a task requires desktop interaction instead of a CLI or API. It is intended for opening applications, inspecting visible UI state, and driving clicks, keyboard input, typing, and scrolling.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires installing an unpinned third-party MCP server.

Mitigation: Install only from a trusted source, review or pin the Homebrew dependency before use, and remove the dependency when it is no longer needed.

Risk: The MCP server requires persistent macOS Accessibility permission and can automate desktop applications.

Mitigation: Grant Accessibility only on trusted machines, avoid using it around passwords, financial actions, private messages, or account administration unless explicitly intended, and revoke Accessibility access after use.

Risk: GUI automation can click, type, press keys, and scroll in active applications.

Mitigation: Review visible UI state before actions, keep automation scoped to intended applications, and unregister the mcporter server when no longer needed.

## Reference(s):

- [Mac Compute Use on ClawHub](https://clawhub.ai/reg2005/skills/mac-compute-use)
- [mcp-server-macos-use homepage](https://github.com/mediar-ai/mcp-server-macos-use)
- [Homebrew](https://brew.sh)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands and command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May reference JSON UI traversal files produced by the MCP server under /tmp/macos-use/ during use.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
