## Description: <br>
Search podcasts, browse episodes, and fetch podcast transcripts from Podfetcher using the bundled Node.js CLI, SDK, or MCP server. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[FloHiwg](https://clawhub.ai/user/FloHiwg) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external agent users use this skill to search podcast shows, inspect episode catalogs, and retrieve transcripts through a CLI, SDK, or MCP server backed by Podfetcher. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Podfetcher API keys could be exposed through command history, shared configuration, or inline command flags. <br>
Mitigation: Prefer PODFETCHER_API_KEY or a secret manager, and avoid putting real keys in shared configs or command history. <br>
Risk: Changing the default API base URL can send podcast queries, transcript requests, and API keys to another endpoint. <br>
Mitigation: Keep the default Podfetcher API URL unless the alternate endpoint is intentionally trusted. <br>
Risk: Transcript fetching may consume quota or create billing impact. <br>
Mitigation: Have agents ask before fetching transcripts when quota or billing matters. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/FloHiwg/podfetcher-tools) <br>
- [Podfetcher homepage](https://podfetcher.com) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Shell commands, Configuration, API Calls] <br>
**Output Format:** [Plain text or JSON podcast search results, episode lists, and transcript content, with Markdown setup guidance in the skill documentation.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires PODFETCHER_API_KEY; transcript fetching can optionally poll until the transcript is ready.] <br>

## Skill Version(s): <br>
0.5.1 (source: frontmatter, package.json, server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
