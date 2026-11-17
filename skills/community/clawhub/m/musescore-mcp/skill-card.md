## Description:

Searches MuseScore sheet music, reads score metadata, and helps resolve download or PDF links through a configured musescore-mcp MCP server.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chrischall](https://clawhub.ai/user/chrischall)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and music-focused agents use this skill to search MuseScore scores, inspect score metadata such as license and duration, and route eligible download or PDF workflows through a local MCP server.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks users to run a private MCP server and fetchproxy browser extension.

Mitigation: Install only after trusting the publisher, use project-scoped MCP configuration, and inspect and pin the exact server and extension versions.

Risk: Requests run through a signed-in MuseScore browser tab.

Mitigation: Use a separate browser profile or MuseScore account when possible, and avoid using accounts or sessions with broader access than the workflow requires.

Risk: MuseScore has no public consumer API, so the workflow depends on server-rendered web app data and browser-session behavior.

Mitigation: Run the healthcheck, verify score metadata and download eligibility before relying on results, and expect behavior to change if MuseScore changes its web app.

## Reference(s):

- [fetchproxy browser extension](https://github.com/chrischall/fetchproxy)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, files]

**Output Format:** [Markdown text with MCP setup snippets, score metadata, URLs, and optional local PDF file output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires musescore-mcp, the fetchproxy extension, and a signed-in MuseScore browser tab; PDF file creation depends on the SVG fallback path and rsvg-convert.]

## Skill Version(s):

0.14.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
