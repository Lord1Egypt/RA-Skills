## Description:

This skill lets an agent search the web and find images through the Serper API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[twodogegg](https://clawhub.ai/user/twodogegg)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to give an agent current web, news, image, and other Serper-backed search results with links and source metadata.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search queries are sent to Serper.

Mitigation: Use the skill only for queries that are appropriate to share with Serper.

Risk: Persistent shell configuration can expose or spread SERPER_API_KEY handling beyond a single project.

Mitigation: Prefer per-project environment setup or a secrets manager for SERPER_API_KEY instead of permanently writing it into shell startup files.

Risk: Installing by an unpinned source can make later source changes harder to audit.

Mitigation: Pin or verify the installer source before use when deploying in controlled environments.

## Reference(s):

- [Serper API](https://serper.dev)
- [Serper API Response Format](references/api_response.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown summaries with source links, plus JSON from the Serper search script when the agent runs a search.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires SERPER_API_KEY; search terms are sent to Serper.]

## Skill Version(s):

0.1.1 (source: server release metadata, created 2026-03-11)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
