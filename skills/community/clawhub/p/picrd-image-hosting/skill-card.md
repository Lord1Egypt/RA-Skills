## Description: <br>
Free image hosting via picrd.com - upload screenshots, diagrams, and image files to get permanent, embeddable URLs. No account required. Supports PNG, JPEG, WebP, and GIF up to 10 MB. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[setdemos](https://clawhub.ai/user/setdemos) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, agents, and external users use this skill to upload selected screenshots, diagrams, and image files to picrd.com and receive public URLs for markdown, issues, pull requests, docs, or chat. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Uploaded images may be public, unlisted but link-accessible, or permanent. <br>
Mitigation: Do not upload private screenshots, documents, credentials, or sensitive images; use TTL uploads when appropriate. <br>
Risk: The delete URL is a one-time secret and cannot be recovered later. <br>
Mitigation: Save the delete URL immediately when uploaded content may need to be removed. <br>
Risk: The service limits uploads to 60 per hour per IP address. <br>
Mitigation: Retry later after rate-limit responses and avoid automated bulk upload loops. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/setdemos/picrd-image-hosting) <br>
- [picrd.com documentation](https://picrd.com/docs) <br>
- [picrd.com](https://picrd.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown with curl commands and JSON response examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces upload guidance for public or unlisted image URLs and album workflows; uploads depend on curl and the external picrd.com service.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
