## Description:

Analyze images using browser and vision capabilities.

This skill is ready for commercial/non-commercial use.

## Publisher:

[litiao1224](https://clawhub.ai/user/litiao1224)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and agents use this skill to open accessible image URLs in a browser, capture page snapshots, and analyze image content with vision capabilities.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Opening remote image URLs can disclose normal network metadata to the image host and may expose private or untrusted links.

Mitigation: Use trusted, non-sensitive image links when possible, and avoid opening private URLs unless disclosure to the host is acceptable.

Risk: The workflow depends on browser tooling, complete Playwright support, and reachable image URLs.

Mitigation: Confirm the browser environment is available and test target image URLs before relying on the analysis workflow.

Risk: The documentation is currently Chinese-only, which may increase operator error for non-Chinese readers.

Mitigation: Have operators review a translated copy or confirm each browser action before use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/litiao1224/skills/image-analysis-litiao)
- [Publisher profile](https://clawhub.ai/user/litiao1224)

## Skill Output:

**Output Type(s):** [guidance, shell commands, markdown]

**Output Format:** [Markdown with inline browser commands and image-analysis guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires browser tooling, complete Playwright support, and reachable image URLs.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
