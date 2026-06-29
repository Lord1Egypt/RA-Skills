## Description: <br>
Delivers files such as reports, PDFs, images, spreadsheets, archives, and code bundles to a paired Claw Butler desktop or mobile client through the client's file.push capability. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhaobod1](https://clawhub.ai/user/zhaobod1) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and end users use this skill when an agent has generated a file that should be delivered to a paired Claw Butler desktop or mobile client. It is especially relevant when normal WebChat file delivery fails, returns a dead link, or cannot carry the file. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A generated file could be delivered to the wrong paired client. <br>
Mitigation: Confirm the intended Claw Butler client before invoking file.push, especially when multiple devices may be available. <br>
Risk: Large-file URL delivery can expose the file outside the chat system. <br>
Mitigation: Use base64 delivery for smaller files when practical; for large files, use an access-controlled or temporary HTTPS URL and only host files intended for that recipient. <br>
Risk: Local paths or internal media links can become dead links for the client. <br>
Mitigation: Send file bytes through contentBase64 or provide a client-accessible HTTPS URL instead of passing local filesystem paths. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zhaobod1/skills/huo15-claw-butler-file-delivery) <br>
- [Publisher profile](https://clawhub.ai/user/zhaobod1) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration] <br>
**Output Format:** [Markdown with inline command examples and JSON parameters] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guides the agent to invoke file.push with either base64 file content for smaller files or an HTTP(S) URL for larger files.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
