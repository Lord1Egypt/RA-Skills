## Description:

Upload and manage files through Polsia's Cloudflare R2 proxy with authenticated API requests.

This skill is ready for commercial/non-commercial use.

## Publisher:

[agentlevier](https://clawhub.ai/user/agentlevier)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to upload and manage images, videos, audio, and documents through Polsia's authenticated Cloudflare R2 proxy.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Uploaded files leave the local environment and are stored through Polsia's Cloudflare R2/CDN setup.

Mitigation: Avoid uploading sensitive or regulated files unless Polsia's retention, sharing, and CDN access policies are acceptable for the intended use.

Risk: The skill requires an API key for remote upload requests.

Mitigation: Provide POLSIA_API_KEY only through the runtime environment or a secret manager, and avoid logging bearer tokens or request headers.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/agentlevier/skills/polsia-r2-proxy)
- [Polsia R2 proxy API endpoint](https://polsia.com/api/proxy/r2)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline code, shell commands, and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses POLSIA_API_KEY for authenticated requests; supports upload metadata including file id, key, URL, filename, MIME type, size, and creation time.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
