## Description:

Crawl web pages and detect broken links, redirects, and HTTP errors. Use when auditing site links, finding 404 errors, validating URLs before launch.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xueyetianya](https://clawhub.ai/user/xueyetianya)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and site maintainers use this skill to check individual URLs, scan documents for broken links, batch-check addresses, and export link health reports before or after publishing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can make host-network requests to URLs found in scanned content, including private or internal URLs if provided.

Mitigation: Review inputs before scanning, avoid checking private or token-bearing URLs unless intended, and install only in environments where outbound link checks are acceptable.

Risk: The skill persists URL history, reports, exports, and configuration under ~/.link-checker.

Mitigation: Clear ~/.link-checker when URL history should not persist and avoid using sensitive documents as scan inputs.

Risk: Untrusted text could influence what URLs are checked or what configuration changes an agent proposes.

Mitigation: Do not let untrusted content drive configuration changes, and review agent-proposed commands before execution.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/xueyetianya/skills/link-checker)
- [BytesAgain Homepage](https://bytesagain.com)

## Skill Output:

**Output Type(s):** [text, json, shell commands, configuration, files]

**Output Format:** [Terminal text with optional TXT, CSV, or JSON reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Stores check results, history, reports, exports, and configuration under ~/.link-checker.]

## Skill Version(s):

2.1.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
