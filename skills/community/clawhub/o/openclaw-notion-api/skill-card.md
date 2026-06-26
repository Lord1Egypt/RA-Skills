## Description: <br>
Notion API guidance for creating and managing pages, data sources, blocks, and image or file uploads. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ionepub](https://clawhub.ai/user/ionepub) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use this skill to prepare Notion API setup steps, curl commands, JSON payloads, and troubleshooting guidance for workspace content operations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Commands can read, create, update, or upload content in a Notion workspace. <br>
Mitigation: Review each generated command before execution and share only the necessary Notion pages or databases with the integration. <br>
Risk: The setup examples store a Notion API token in a local plaintext file. <br>
Mitigation: Protect the token file, prefer a least-privilege Notion integration, and avoid exposing the token in shared logs or transcripts. <br>


## Reference(s): <br>
- [Notion Developers](https://developers.notion.com) <br>
- [ClawHub skill page](https://clawhub.ai/ionepub/openclaw-notion-api) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, code] <br>
**Output Format:** [Markdown with bash commands and JSON payload examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The guidance references Notion API version 2025-09-03 and direct file upload examples for files up to 20MB.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
