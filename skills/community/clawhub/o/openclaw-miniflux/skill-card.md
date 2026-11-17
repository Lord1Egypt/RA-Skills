## Description:

Manage RSS feeds and entries on a Miniflux instance using openclaw-miniflux-mcp for reading, searching, subscription management, category management, OPML import/export, status updates, and bookmarking.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sinhong2011](https://clawhub.ai/user/sinhong2011)

### License/Terms of Use:


## Use Case:

Developers and end users use this skill to connect an agent to a Miniflux RSS reader instance so it can browse feeds, search and read entries, manage categories and subscriptions, import or export OPML, update read status, and toggle bookmarks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks users to run an unpinned native MCP binary that receives Miniflux account credentials and can modify RSS account data.

Mitigation: Prefer read-only mode unless write actions are needed, use a revocable Miniflux API token instead of a password, and pin and verify the MCP binary or Cargo version before use.

Risk: Write operations can delete feeds or categories, import OPML, change entry status in bulk, and alter bookmarks.

Mitigation: Require explicit user confirmation before destructive actions, OPML imports, or large batch status changes.

Risk: Incorrect Miniflux credentials or instance URLs can cause authentication or connection failures.

Mitigation: On 401 or 403 responses, ask the user to check the API token or credentials; on connection errors, ask the user to verify MINIFLUX_URL.

## Reference(s):

- [openclaw-miniflux-mcp GitHub Releases](https://github.com/sinhong2011/openclaw-skill-miniflux/releases)
- [ClawHub Skill Page](https://clawhub.ai/sinhong2011/skills/openclaw-miniflux)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance, API calls]

**Output Format:** [Markdown with JSON configuration and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include MCP tool calls that read or modify Miniflux feeds, entries, categories, bookmarks, and OPML data.]

## Skill Version(s):

0.1.5 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
