## Description:

Create shareable HTML canvases and Mermaid diagram links through the gui.new API, returning live URLs with input sync and state persistence.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dylanfeltus](https://clawhub.ai/user/dylanfeltus)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to publish generated HTML, visual tools, dashboards, forms, tables, and Mermaid diagrams as shareable gui.new links.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: User-provided HTML or Mermaid content is sent to gui.new and resulting canvases are publicly accessible by URL.

Mitigation: Do not use the skill with secrets, private customer data, confidential business content, or material that should not be visible to anyone with the link.

Risk: Hosted canvas links expire and may have free-tier limits on size, edits, and creation rate.

Mitigation: Plan for the documented expiry and rate limits, or use the optional API key only in an appropriate isolated environment.

## Reference(s):

- [gui.new documentation](https://gui.new/docs)
- [gui.new llms.txt](https://gui.new/docs/llms.txt)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration guidance]

**Output Format:** [Markdown with inline code and API command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces public gui.new URLs for submitted HTML or Mermaid content; optional API key enables extended expiry and higher limits.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
