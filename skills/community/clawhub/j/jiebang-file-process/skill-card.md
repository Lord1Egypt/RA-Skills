## Description: <br>
A file-processing skill that calculates MD5, SHA1, and SHA256 hashes and performs Base64 and URL encoding or decoding for text and file-content checks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jiebang-tools](https://clawhub.ai/user/jiebang-tools) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users can use this skill to hash text, check file-content hashes, or convert text with Base64 and URL encoding workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: User-provided text or file content is sent to the external jiebang.site API. <br>
Mitigation: Do not process secrets, tokens, private URLs, proprietary files, or personal data unless the publisher provides clear data-handling disclosure and confirmation before upload. <br>
Risk: The skill uses an admin-style environment credential for API requests. <br>
Mitigation: Deploy only with an approved, least-privilege credential and rotate or revoke it if exposure is suspected. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jiebang-tools/jiebang-file-process) <br>
- [Jiebang API service](https://www.jiebang.site) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON] <br>
**Output Format:** [JSON] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes the processed result and original input when returned by the external API.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
