## Description: <br>
Sync local workspace directories and files to Notion pages using the notion-sync CLI or programmatic API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kitakitsune0x](https://clawhub.ai/user/kitakitsune0x) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and workspace users use this skill to initialize Notion sync configuration, preview or run directory syncs, manage ignore patterns, and check sync status for local files mirrored into Notion pages. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can upload local files into Notion, including sensitive or proprietary content if the sync root is too broad. <br>
Mitigation: Use a dedicated Notion root page, run notion-sync sync --dry-run first, and add ignore rules for .env files, keys, credentials, private notes, and proprietary files. <br>
Risk: Existing synced Notion page content can be overwritten because file pages are updated in place. <br>
Mitigation: Review the dry-run output and scope the sync directory before running a non-dry-run sync. <br>
Risk: .notion-sync.json stores the Notion token used for synchronization. <br>
Mitigation: Keep .notion-sync.json out of source control and use a token scoped to a dedicated Notion integration and root page. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/kitakitsune0x/openclaw-notion-sync) <br>
- [Notion integrations setup](https://notion.so/my-integrations) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands, TypeScript examples, and JSON configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update .notion-sync.json and may sync local file contents to Notion when the CLI or API is run.] <br>

## Skill Version(s): <br>
0.1.0 (source: package.json and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
