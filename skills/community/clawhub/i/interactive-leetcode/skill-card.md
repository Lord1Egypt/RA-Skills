## Description:

Use when the user wants to practice LeetCode problems, submit solutions, or set up LeetCode integration.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sperekrestova](https://clawhub.ai/user/sperekrestova)

### License/Terms of Use:


## Use Case:

Developers and coding-practice users use this skill to connect a LeetCode MCP server, follow a learning-guided practice flow, retrieve problems and hints, and submit solutions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill installs and runs a third-party npm MCP server via npx.

Mitigation: Ask for user consent before installation, pin a reviewed package version, and install only if the named npm package and publisher are trusted.

Risk: LeetCode authentication stores session cookies locally.

Mitigation: Treat saved cookies as account credentials, use trusted machines, keep owner-only file permissions, and revoke or rotate the LeetCode session if compromise is suspected.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/sperekrestova/skills/interactive-leetcode)
- [npm package: @sperekrestova/interactive-leetcode-mcp](https://www.npmjs.com/package/@sperekrestova/interactive-leetcode-mcp)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline JSON and shell command blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May guide MCP prompt invocation, local workspace setup, LeetCode authentication, and solution submission workflows.]

## Skill Version(s):

1.0.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
