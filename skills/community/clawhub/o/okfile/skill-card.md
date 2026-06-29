## Description: <br>
Uploads and publishes files or static site folders to OkFile, with direct links, preview URLs, and multipart support. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[okfilecom](https://clawhub.ai/user/okfilecom) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to upload files, publish static site folders, generate shareable file or preview URLs, and run repeatable OkFile CLI workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Uploaded files, generated links, preview pages, directory listings, and published sites may be externally shareable. <br>
Mitigation: Avoid uploading secrets, regulated data, private personal data, or confidential business files unless appropriate access controls and handling requirements are confirmed. <br>
Risk: Authenticated workflows use an OkFile API key and optional CLI installation from a third-party package source. <br>
Mitigation: Review package provenance before installing the CLI and handle API keys as credentials, including secure storage and rotation where appropriate. <br>


## Reference(s): <br>
- [Server-resolved GitHub source](https://github.com/okfilecom/okfile) <br>
- [OkFile home](https://www.okfile.com/en/) <br>
- [OkFile upload page](https://www.okfile.com/en/upload/) <br>
- [OkFile PyPI package](https://pypi.org/project/okfile/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with API examples, shell commands, and returned URL fields] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce direct file URLs, preview URLs, site URLs, API request examples, and CLI commands.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
