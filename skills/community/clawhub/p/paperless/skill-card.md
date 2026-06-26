## Description: <br>
Interact with Paperless-NGX document management system via ppls CLI. Search, retrieve, upload, and organize documents. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[NickChristensen](https://clawhub.ai/user/NickChristensen) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and automation agents use this skill to search, retrieve, upload, and organize documents in a Paperless-NGX instance through the ppls CLI. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses a Paperless API token that can access the user's document library. <br>
Mitigation: Use a least-privilege token where possible and avoid exposing the token in logs or shared terminals. <br>
Risk: Document uploads, downloads, and metadata updates can affect sensitive files or the wrong document record. <br>
Mitigation: Keep searches narrow and confirm document IDs, file paths, and metadata before upload or update commands. <br>


## Reference(s): <br>
- [ppls CLI repository](https://github.com/NickChristensen/ppls) <br>
- [Paperless-NGX Documentation](https://docs.paperless-ngx.com/) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, text] <br>
**Output Format:** [Markdown with inline bash code blocks and JSON-oriented CLI examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands commonly use --json for parseable Paperless-NGX results.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
