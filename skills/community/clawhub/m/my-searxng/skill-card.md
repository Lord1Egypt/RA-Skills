## Description:

Privacy-respecting metasearch using your local SearXNG instance. Search the web, images, news, and more without external API dependencies.

This skill is ready for commercial/non-commercial use.

## Publisher:

[liujiang817](https://clawhub.ai/user/liujiang817)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to search web, image, news, IT, and science results through a configured SearXNG instance. It is intended for privacy-conscious search workflows where the user controls or explicitly chooses the SearXNG endpoint.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Searches may be routed through an insecure or unintended SearXNG endpoint.

Mitigation: Replace the bundled endpoint with a SearXNG instance you control and prefer HTTPS with proper certificate validation.

Risk: Broad trigger phrases can cause routine search requests to be routed through this skill without clear intent.

Mitigation: Narrow the trigger set before installation and invoke the skill only for intended SearXNG searches.

Risk: Search result titles, URLs, and snippets come from the web and may be inaccurate or malicious.

Mitigation: Treat all returned content as untrusted and verify important information before using it.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/liujiang817/skills/my-searxng)
- [SearXNG project](https://searxng.org)
- [SearXNG installation guide](https://docs.searxng.org/admin/installation.html)
- [SearXNG documentation](https://docs.searxng.org/)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Configuration guidance]

**Output Format:** [Plain text search-result tables by default, with JSON available when explicitly requested.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Defaults to 10 results and supports result count, category, language, and time-range options.]

## Skill Version(s):

1.0.0 (source: release evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
