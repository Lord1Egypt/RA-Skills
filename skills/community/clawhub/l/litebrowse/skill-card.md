## Description:

Extracts and summarizes the most relevant webpage passages for focused, low-token research without loading or summarizing the full page.

This skill is ready for commercial/non-commercial use.

## Publisher:

[agitalent](https://clawhub.ai/user/agitalent)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and research agents use LiteBrowse to inspect long or cluttered webpages by extracting query-relevant passages first, reducing token use before answering from cited blocks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The helper can fetch arbitrary HTTP(S) URLs from the agent host, including destinations the user may not intend to expose.

Mitigation: Use trusted public pages or local HTML copies, avoid internal and private URLs, and run with network egress controls where possible.

Risk: The helper reads response bodies without an evidence-stated download-size cap.

Mitigation: Prefer fixed or reviewed versions that cap download size, validate redirects, and block private destinations before broad deployment.

## Reference(s):

- [LiteBrowse ClawHub Skill Page](https://clawhub.ai/agitalent/skills/litebrowse)
- [LiteBrowse Direct Access Document](https://agitalent.github.io/LiteBrowse.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown guidance with inline shell commands and cited extracted blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses a query, source URL or HTML file, top-k limit, character budget, per-block character budget, timeout, and JSON or text output format.]

## Skill Version(s):

0.1.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
