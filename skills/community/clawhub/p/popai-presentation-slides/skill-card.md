## Description:

Create presentations using the PopAI API from a topic, optional reference files or URLs, and optional PowerPoint templates, with support for follow-up modifications.

This skill is ready for commercial/non-commercial use.

## Publisher:

[popaiofficial](https://clawhub.ai/user/popaiofficial)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to generate and revise presentation decks through PopAI, including decks grounded in uploaded files, templates, or URLs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: API tokens can be exposed if stored in plaintext repository or agent instruction files.

Mitigation: Use a scoped PopAI token, provide it through the POPAI_ACCESS_TOKEN environment variable at runtime, and do not store it in TOOLS.md or any repository file.

Risk: Prompts, URLs, selected files, templates, filenames, and channel information are sent to PopAI and may appear in local execution logs.

Mitigation: Use only data approved for PopAI processing, avoid confidential or regulated documents unless approved, and review selected files and URLs before generation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/popaiofficial/skills/popai-presentation-slides)
- [PopAI publisher profile](https://clawhub.ai/user/popaiofficial)
- [PopAI skill token setup](https://www.popai.pro/popai-skill)
- [PopAI website](https://www.popai.pro)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Files, Configuration guidance]

**Output Format:** [Markdown guidance plus JSON-line progress events and final PPTX, preview image, and web editing URLs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires POPAI_ACCESS_TOKEN; may upload selected local files or templates to PopAI; initial generation typically takes about five minutes.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
