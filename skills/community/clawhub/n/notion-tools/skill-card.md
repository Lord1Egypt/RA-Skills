## Description: <br>
Use for tasks that read or modify Notion pages, data sources, or blocks via the Notion API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Jeffreymaomao](https://clawhub.ai/user/Jeffreymaomao) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and workspace operators use this skill to find, read, create, update, trash, restore, and append content in Notion workspaces through the Notion API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Examples and guidance can change live Notion workspace data, including moving pages to trash or restoring them. <br>
Mitigation: Read and inspect target pages or data sources before writes, test destructive examples in a sandbox or disposable pages first, and confirm ambiguous targets with the user. <br>
Risk: A fallback plaintext token file could expose a Notion API key if stored or synced insecurely. <br>
Mitigation: Prefer runtime-provided NOTION_KEY or a secret manager; if using the fallback file, restrict permissions and never commit or echo the token. <br>


## Reference(s): <br>
- [Notion API documentation](https://developers.notion.com) <br>
- [ClawHub skill page](https://clawhub.ai/Jeffreymaomao/notion-tools) <br>
- [Setup](references/setup.md) <br>
- [Examples](references/examples.md) <br>
- [Blocks And Formatting Edge Cases](references/blocks.md) <br>
- [Property Patterns](references/property-patterns.md) <br>
- [Troubleshooting](references/troubleshooting.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, code] <br>
**Output Format:** [Markdown with inline JSON and bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include Notion API request payloads and command snippets; should not expose full API keys.] <br>

## Skill Version(s): <br>
1.0.2 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
