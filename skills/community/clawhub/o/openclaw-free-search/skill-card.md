## Description:

Openclaw Free Search lets OpenClaw users run web searches without configuring Brave or Perplexity API keys.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yang1002378395-cmyk](https://clawhub.ai/user/yang1002378395-cmyk)

### License/Terms of Use:

MIT-0

## Use Case:

External OpenClaw users and developers use this skill to retrieve web search results when API-key-backed search providers are not configured.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installation instructions use a mutable npx installer, which may execute remote code that differs from the reviewed release.

Mitigation: Prefer a pinned and reviewed installer version, and inspect the package before running the install command.

Risk: Search terms are sent to DuckDuckGo, and third-party query handling is under-disclosed.

Mitigation: Do not use this skill for secrets, private identifiers, confidential prompts, regulated data, or other sensitive queries.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yang1002378395-cmyk/skills/openclaw-free-search)
- [DuckDuckGo Instant Answer API endpoint](https://api.duckduckgo.com/)

## Skill Output:

**Output Type(s):** [text, json, shell commands, guidance]

**Output Format:** [Plain text or JSON search results, with Markdown shell command examples in the skill documentation]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Search results include an optional abstract and up to 10 related topics when returned by the search service.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
