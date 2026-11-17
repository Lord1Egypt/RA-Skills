## Description:

Generates academic figures and scientific diagrams from paper text using a DashScope-powered multi-agent workflow for planning, image generation, and critic refinement.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zdywrnm](https://clawhub.ai/user/zdywrnm)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, researchers, and technical writers use this skill to turn paper methods, captions, and scientific descriptions into candidate diagrams, plots, and publication-style figures.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill directs users to globally install and run an unpinned third-party npm package whose reviewed code is not included.

Mitigation: Review the npm package source and published version before installing, and prefer a pinned or local install when possible.

Risk: Paper text, captions, or unpublished research content may be sent to external DashScope services during figure generation.

Mitigation: Avoid submitting confidential or unpublished paper text unless external DashScope processing is approved for the intended use.

Risk: Credential setup is ambiguous because the skill asks for a DashScope API key but stores it under OPENAI_API_KEY or openai_api_key.

Mitigation: Confirm which API key is required before adding credentials to environment variables or the global config file.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/zdywrnm/skills/paperbanana-dashscope)
- [npm package](https://www.npmjs.com/package/paperbanana-dashscope)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guides an agent to install and use a third-party CLI that generates image files from user-provided paper text and captions.]

## Skill Version(s):

1.0.5 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
