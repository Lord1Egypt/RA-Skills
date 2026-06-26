## Description: <br>
Reads and analyzes data from Google Sheets using public API keys or private service-account credentials. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fuco99](https://clawhub.ai/user/fuco99) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, and OpenClaw users use this skill to fetch Google Sheets data, cache recent reads locally, and answer questions about spreadsheet contents in conversation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can fetch spreadsheet contents from Google APIs and cache them locally. <br>
Mitigation: Use restricted API credentials, share only intended sheets, and avoid sensitive spreadsheets unless local caching is acceptable. <br>
Risk: The scanner flagged broad activation and unsafe shell command templates for review. <br>
Mitigation: Review generated commands before execution and avoid untrusted sheet IDs or tab names unless arguments are safely escaped or handled by a native API client. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/fuco99/google-sheets-soha) <br>
- [Publisher profile](https://clawhub.ai/user/fuco99) <br>
- [Homepage from skill metadata](https://github.com/your-username/google-sheets-soha) <br>
- [Repository from skill metadata](https://github.com/your-username/google-sheets-soha) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with tables, inline shell commands, and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create local JSON cache files for fetched sheet data.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata; artifact frontmatter lists 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
