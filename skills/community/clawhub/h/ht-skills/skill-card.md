## Description:

Manages Haotian Library collections, documents, personal garden quotas, RAG document retrieval, image uploads, image groups, image details, and image quota checks for OpenClaw writing and publishing workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[1044197988](https://clawhub.ai/user/1044197988)

### License/Terms of Use:

MIT-0

## Use Case:

External OpenClaw users use this skill to manage their Haotian Library personal garden content, including creating and updating collections and documents, moving documents, uploading images, checking quotas, and retrieving public collection snippets for grounded writing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses a bearer token that can access and modify a user's Haotian Library account content.

Mitigation: Protect the token like a password, avoid committing it to shared files, and rotate it immediately if exposed.

Risk: Agent-initiated write, move, promotion, or image upload actions can change remote user content.

Mitigation: Review the intended target collection, document, quota state, and upload path before allowing write or upload operations.

Risk: An untrusted API endpoint could receive the user's token or content if the service URL is changed.

Mitigation: Keep server_base_url or HT_SKILL_SERVER_URL set to the trusted official HTTPS service.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/1044197988/skills/ht-skills)
- [Haotian Library](https://aiknowledge.cn)
- [Haotian Library public collection catalog](https://aiknowledge.cn/article/66521-%E7%81%8F%E5%A4%A9%E6%96%87%E5%BA%93%E6%96%87%E9%9B%86%E5%AE%8C%E6%95%B4%E7%9B%AE%E5%BD%95%E5%85%AC%E5%BC%80)
- [Default skill API service](https://zzht.tech)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command examples and JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses a configured bearer token to call Haotian Library APIs and returns parsed JSON responses from client scripts.]

## Skill Version(s):

1.1.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
