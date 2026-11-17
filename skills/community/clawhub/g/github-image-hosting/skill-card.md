## Description:

Upload images to img402.dev for embedding in GitHub PRs, issues, and comments.

This skill is ready for commercial/non-commercial use.

## Publisher:

[img402](https://clawhub.ai/user/img402)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to upload screenshots, mockups, diagrams, and other images to img402.dev, then embed the returned public URL in GitHub pull requests, issues, comments, or Markdown.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Uploaded images are sent to a public third-party host and may be reachable by anyone with the URL.

Mitigation: Review and redact images before upload; do not upload secrets, customer data, private repository content, or internal systems.

Risk: The skill can post hosted image URLs into GitHub contexts where they may become broadly visible.

Mitigation: Confirm the target pull request, issue, or comment is appropriate for public image links before posting.

## Reference(s):

- [img402.dev](https://img402.dev)
- [Coinbase Payments MCP](https://docs.cdp.coinbase.com/mcp)
- [Paying x402 APIs](https://img402.dev/blog/paying-x402-apis)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration instructions]

**Output Format:** [Markdown with inline bash code blocks and image markdown snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include public image URLs returned by img402.dev and upload-response metadata such as expiresAt.]

## Skill Version(s):

1.2.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
