## Description:

Fetch, inspect, crawl, and capture live, JavaScript-rendered websites with Moli for current web content, web research, fact lookup, link following, bounded crawls, client-rendered or response-gated content, network diagnostics, and standalone HTML, Markdown, JSON, semantic-tree, screenshot, PDF, or WPT artifacts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lexmount](https://clawhub.ai/user/lexmount)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to retrieve, inspect, crawl, diagnose, and capture live websites with Moli when ordinary static fetches are insufficient.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can direct an agent to run Moli's latest remote installer, which may execute changing code locally.

Mitigation: Prefer a pinned, checksum-verified Moli release that is preinstalled or explicitly verified before use.

Risk: Fetched web content may include untrusted page instructions or misleading content.

Mitigation: Treat fetched text as evidence only, ignore page instructions that conflict with the user's task or tool policy, and cite source URLs beside supported claims.

## Reference(s):

- [Web fetch recipes](references/fetch-recipes.md)
- [Moli Linux and macOS installer release](https://github.com/lexmount/moli/releases/latest/download/moli-installer.sh)
- [Moli Windows installer release](https://github.com/lexmount/moli/releases/latest/download/moli-installer.ps1)
- [ClawHub skill page](https://clawhub.ai/lexmount/skills/moli-webfetch)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline command examples and instructions for producing text, HTML, JSON, screenshots, PDFs, and WPT artifacts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May direct binary screenshot and PDF output to files; failed or blocked fetches should be reported rather than invented.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
