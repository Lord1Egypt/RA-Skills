## Description: <br>
URL shortener, QR code generator, and link analytics API. Create short links, generate QR codes, and track click analytics. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[anandrathnas](https://clawhub.ai/user/anandrathnas) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, marketers, and automation agents use this skill to create and manage Jo4 short links, generate QR codes, and retrieve click analytics for shared URLs and campaigns. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can use a Jo4 API key to create and manage short links. <br>
Mitigation: Use a dedicated or revocable JO4_API_KEY and only provide it to agents that need Jo4 access. <br>
Risk: The skill includes operations that update or delete existing short links. <br>
Mitigation: Require clear user confirmation before changing or deleting existing Jo4 links. <br>


## Reference(s): <br>
- [Jo4 Website](https://jo4.io) <br>
- [Jo4 API Documentation](https://jo4-api.jo4.io/swagger-ui/index.html) <br>
- [Jo4 API Keys](https://jo4.io/api-keys) <br>
- [ClawHub Skill Page](https://clawhub.ai/anandrathnas/jo4) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with curl examples and JSON request or response snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Authenticated Jo4 operations require JO4_API_KEY; public anonymous shortening has limited features and no analytics access.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
