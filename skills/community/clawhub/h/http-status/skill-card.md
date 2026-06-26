## Description: <br>
HTTP status code reference that helps agents explain status codes, common causes, and suggested fixes using an offline lookup table. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ToBeWin](https://clawhub.ai/user/ToBeWin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and support engineers use this skill to quickly interpret HTTP response codes during API debugging, including standard, WebDAV, Nginx, Cloudflare, AWS Elastic Load Balancer, and common unofficial codes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security scan reported no suspicious behavior, but noted that full artifact-backed verification was not available in its review workspace. <br>
Mitigation: Review the visible skill description and packaged files before deployment, and install only if they match the expected HTTP status reference. <br>
Risk: HTTP status guidance for unofficial vendor-specific codes can be incomplete or change over time. <br>
Mitigation: For production incidents, confirm vendor-specific codes against the relevant server, proxy, or platform documentation. <br>


## Reference(s): <br>
- [HTTP status code table](references/codes.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown or plain text explanations with status-code summaries, causes, and recommended actions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Offline lookup; no API key, network access, or external dependencies required.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
