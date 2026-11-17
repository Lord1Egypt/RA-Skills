## Description:

Generate graphical abstract layout recommendations based on paper abstracts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aipoch-ai](https://clawhub.ai/user/aipoch-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Researchers, authors, and developers use this skill to turn academic paper abstracts into graphical abstract recommendations, including key concepts, visual elements, layout blueprints, and image-generation prompts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Confidential or embargoed abstracts may be exposed through shell history or process listings when passed directly on the command line.

Mitigation: Provide sensitive abstracts through controlled stdin or files in a protected workspace instead of inline command arguments.

Risk: The skill can write output to a user-specified path.

Mitigation: Keep output paths inside a controlled workspace and review generated files before sharing or publishing them.

Risk: The release includes an unnecessary dataclasses dependency for modern Python environments.

Mitigation: Remove or pin the dependency before using the skill in automated or privileged environments.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/aipoch-ai/skills/graphical-abstract-wizard)

## Skill Output:

**Output Type(s):** [text, markdown, json, guidance]

**Output Format:** [Markdown, JSON, or plain text recommendations with layout blueprints and Midjourney and DALL-E prompts.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can print to stdout or write results to a user-specified output file.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
