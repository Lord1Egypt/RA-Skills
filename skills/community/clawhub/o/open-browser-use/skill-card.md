## Description:

Platform-neutral guidance for using Open Browser Use, the open-source Chrome automation stack for AI agents.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ifuryst](https://clawhub.ai/user/ifuryst)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to install, verify, troubleshoot, and safely operate Open Browser Use for real Chrome automation through the CLI, MCP server, SDKs, and JSON-RPC methods.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill guides agents through installation of a privileged Chrome automation stack and external release artifacts.

Mitigation: Install only trusted, pinned releases and prefer a Chrome Web Store release when available; use the beta ZIP path only after verifying the release source and checksum.

Risk: Browser automation can expose sensitive Chrome profile data or perform externally visible actions.

Mitigation: Treat the connected Chrome profile as sensitive and obtain user confirmation before history access, clipboard use, file uploads, form submission, purchases, deletion, or actions on logged-in sites.

Risk: Multiple Chrome profiles can lead an agent to act in the wrong browser context.

Mitigation: List connected profiles, ask the user to choose when more than one profile is available, and keep the chosen profile fixed for the task.

## Reference(s):

- [Open Browser Use Installation](references/installation.md)
- [Open Browser Use SDK And Protocol](references/sdk-and-protocol.md)
- [Open Browser Use Troubleshooting](references/troubleshooting.md)
- [Browser Use Documentation](https://docs.browser-use.com)

## Skill Output:

**Output Type(s):** [guidance, markdown, code, shell commands, configuration]

**Output Format:** [Markdown guidance with inline shell commands, SDK examples, and MCP configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include browser session, profile selection, tab lifecycle, file chooser, download, clipboard, and troubleshooting guidance.]

## Skill Version(s):

0.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
