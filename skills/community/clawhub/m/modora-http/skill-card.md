## Description: <br>
Use this skill to analyze PDFs with a remote MoDora HTTP service. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wu-uk](https://clawhub.ai/user/wu-uk) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to upload PDFs to a configured MoDora service, wait for preprocessing, and ask questions about the uploaded document. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: PDF contents and questions are sent to the configured MoDora service. <br>
Mitigation: Use the skill only with a trusted MoDora endpoint and avoid confidential or regulated PDFs unless that endpoint is approved for the data. <br>
Risk: Environment-managed upstream model credentials are used when uploading or asking questions. <br>
Mitigation: Use a dedicated, revocable API key and keep secrets in environment variables instead of settings files. <br>
Risk: Remote service configuration can affect where documents and credentials are sent. <br>
Mitigation: Use HTTPS for non-local endpoints and require explicit approval before running upload or chat commands. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wu-uk/modora-http) <br>
- [Default MoDora service endpoint](https://api.modora.pro) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON responses from helper scripts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uploads require an absolute PDF path, a user-owned non-secret settings JSON file, environment-managed credentials, and explicit approval before remote access.] <br>

## Skill Version(s): <br>
0.1.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
