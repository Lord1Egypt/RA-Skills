## Description: <br>
Browse, read, and manage Miniflux feed articles. Use when Claude needs to work with RSS/atom feeds via Miniflux - listing unread/new articles, reading article content, marking articles as read, and managing feeds/categories. Provides CLI access with flexible output formats (headlines, summaries, full content). <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[shekohex](https://clawhub.ai/user/shekohex) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agents use this skill to inspect, search, read, and manage articles in a Miniflux RSS/Atom account from the command line. It supports feed browsing, article retrieval, read-status updates, feed/category listing, statistics, and feed refresh workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can access a user's Miniflux account through an API key. <br>
Mitigation: Install only when this account access is acceptable, and prefer MINIFLUX_URL and MINIFLUX_API_KEY environment variables for credentials. <br>
Risk: Providing credentials with CLI flags can save the API key to ~/.local/share/miniflux/config.json. <br>
Mitigation: Use environment variables instead of CLI flags when the API key should not be written to the local config file. <br>
Risk: The mark-read, mark-unread, and refresh commands can modify article state or trigger feed updates, including for multiple items. <br>
Mitigation: Confirm the target article IDs or feed scope before running state-changing or bulk commands. <br>
Risk: The script depends on the miniflux Python package with an unpinned lower-bound dependency. <br>
Mitigation: Pin and review the dependency version in higher-assurance environments. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/shekohex/miniflux) <br>
- [README](artifact/README.md) <br>
- [Skill instructions](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, configuration] <br>
**Output Format:** [CLI output as plain text or JSON, with Markdown instructions and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may include article titles, article content, feed metadata, category lists, read/unread status changes, refresh confirmations, and statistics.] <br>

## Skill Version(s): <br>
0.1.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
