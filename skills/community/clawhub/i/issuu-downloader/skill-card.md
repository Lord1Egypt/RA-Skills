## Description: <br>
Downloads public Issuu documents as high-quality PDF files with retry, proxy, and anti-blocking support. <br>

This skill is for research and development only. <br>

## Publisher: <br>
[zykqyer](https://clawhub.ai/user/zykqyer) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agents and users provide an Issuu document URL to retrieve page images and assemble them into a local PDF. Use only for documents the user is authorized to copy. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill is designed to work around Issuu blocking and may automatically route traffic through local proxies. <br>
Mitigation: Use it only for documents you are authorized to copy, avoid untrusted proxies, and review proxy behavior before running it. <br>
Risk: Automatic proxy probing can make network requests and change routing without an explicit user confirmation step. <br>
Mitigation: Run it in a controlled environment and prefer a version that asks before proxy probing and validates Issuu URLs before making network requests. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/zykqyer/issuu-downloader) <br>


## Skill Output: <br>
**Output Type(s):** [Files, Text] <br>
**Output Format:** [PDF file with a returned file path] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates a downloaded PDF in the configured downloads directory.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
