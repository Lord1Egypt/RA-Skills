## Description:

Convert unstructured documents into LLM-ready structured data, supporting PDF, Word, PPT, and images while extracting paragraphs, formulas, tables, charts, and other elements into Markdown organized in reading order.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sube-py](https://clawhub.ai/user/sube-py)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to parse local documents into Markdown before extracting fields, tables, body text, or other structured content for downstream analysis and validation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uploads a user-selected local document to PaodingAI/PDRouter for parsing.

Mitigation: Use it only with documents approved for that service, and avoid confidential or regulated content unless the service is approved for the data.

Risk: The workflow requires a PD_ROUTER_API_KEY for authentication.

Mitigation: Provide the key through the environment, keep it out of prompts and saved outputs, and rotate it if exposure is suspected.

Risk: Enabling image output can add base64 image data to Markdown and increase data volume.

Mitigation: Leave PDFLUX_INCLUDE_IMAGES disabled unless embedded image data is explicitly needed.

## Reference(s):

- [PDFlux Test ClawHub listing](https://clawhub.ai/sube-py/skills/pdflux-test)
- [PDRouter platform](https://platform.paodingai.com/)

## Skill Output:

**Output Type(s):** [text, markdown, files, shell commands, configuration, guidance]

**Output Format:** [Markdown text printed to stdout, with optional Markdown file output when an output path is provided.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js and PD_ROUTER_API_KEY; image data is excluded unless PDFLUX_INCLUDE_IMAGES is enabled.]

## Skill Version(s):

1.0.3 (source: server release metadata; artifact frontmatter reports 1.0.2)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
