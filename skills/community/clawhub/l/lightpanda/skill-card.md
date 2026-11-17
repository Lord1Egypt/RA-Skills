## Description:

Lightpanda Browser helps agents install and use the Lightpanda headless browser for fast web scraping, content extraction, automation, and Markdown or HTML page dumps.

This skill is ready for commercial/non-commercial use.

## Publisher:

[smseow001](https://clawhub.ai/user/smseow001)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to fetch web pages with Lightpanda, convert page content to Markdown or HTML, and integrate browser-based extraction into scraping, monitoring, or RAG workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill instructs users to download mutable nightly Lightpanda binaries and Docker images without integrity verification.

Mitigation: Prefer a pinned Lightpanda release or Docker image digest and verify publisher-provided checksums or signatures before use.

Risk: Running an unverified browser binary or container can expose local files, credentials, or sensitive mounted directories.

Mitigation: Run Lightpanda in an isolated workspace or container without mounted credentials or sensitive directories until the upstream source and version are trusted.

## Reference(s):

- [ClawHub Lightpanda Browser skill page](https://clawhub.ai/smseow001/skills/lightpanda)
- [Lightpanda nightly Linux binary](https://github.com/lightpanda-io/browser/releases/download/nightly/lightpanda-x86_64-linux)
- [Lightpanda nightly macOS binary](https://github.com/lightpanda-io/browser/releases/download/nightly/lightpanda-aarch64-macos)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with shell command and Python code examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces installation guidance, command examples, and integration snippets; Lightpanda fetch commands may output page content as Markdown or HTML.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
