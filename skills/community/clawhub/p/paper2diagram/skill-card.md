## Description:

Paper2diagram helps an agent analyze research paper PDFs, extract methods and structures, produce academic-review-style summaries, and generate paper-style diagrams through configured Gemini and nano_banana gateways.

This skill is ready for commercial/non-commercial use.

## Publisher:

[qbc-oio](https://clawhub.ai/user/qbc-oio)

### License/Terms of Use:

MIT-0

## Use Case:

Researchers, developers, and external users use this skill to ask an agent to analyze local academic PDFs, summarize methods and findings, and produce diagram assets for reports or slides.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The packaged artifact does not include the executable workflow, and the skill tells users to clone and run an unspecified external repository.

Mitigation: Verify the external repository and dependencies before installation or execution, and do not run unreviewed code in a trusted environment.

Risk: PDF content and prompts may be processed by the configured LLM and image gateways.

Mitigation: Use only trusted gateways, avoid confidential or unpublished PDFs unless data-sharing obligations allow it, and keep API keys scoped separately from installation steps.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/qbc-oio/skills/paper2diagram)
- [ClawHub homepage](https://clawhub.ai/)
- [Example Gemini gateway endpoint](https://api.dongli.work/v1beta)
- [Example image gateway endpoint](https://api.dongli.work)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, files]

**Output Format:** [Markdown or structured text with shell commands, image links, and local file paths]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce 3-5 image files under outputs/ and temporary image links from the configured gateway.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
