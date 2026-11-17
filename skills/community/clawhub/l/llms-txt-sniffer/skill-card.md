## Description:

Locate and utilize AI-friendly documentation index files (llms.txt, llms-full.txt) or sitemap.xml for documentation URLs to map sites and reduce token use.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jdchi](https://clawhub.ai/user/jdchi)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill when a user provides a public documentation URL and they need to find an AI-friendly llms.txt, llms-full.txt, or sitemap.xml index before reading the site.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The sniffer makes outbound network requests from the user's machine or agent environment.

Mitigation: Run it only for user-provided, trusted public documentation URLs.

Risk: Under-scoped URL validation may allow requests toward internal services or cloud metadata endpoints.

Mitigation: Avoid running it from environments with access to sensitive internal networks unless URL validation and egress controls are hardened.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jdchi/skills/llms-txt-sniffer)
- [Publisher profile](https://clawhub.ai/user/jdchi)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with optional JSON command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Summarizes discovered index structure and may report found_index, type, content_preview, or an error from the sniffer script.]

## Skill Version(s):

1.3.1 (source: openclaw metadata and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
