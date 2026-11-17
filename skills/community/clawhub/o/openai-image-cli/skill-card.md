## Description:

Generate, edit, and manage images via OpenAI's GPT Image and DALL-E models.

This skill is ready for commercial/non-commercial use.

## Publisher:

[g9pedro](https://clawhub.ai/user/g9pedro)

### License/Terms of Use:


## Use Case:

Developers and agent users use this skill to generate CLI commands and configuration guidance for installing and operating the OpenAI Image CLI to generate, edit, vary, batch, and manage image outputs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill directs users to install an unaudited, unpinned third-party CLI globally.

Mitigation: Inspect the referenced npm and GitHub package before use, and prefer a pinned or locally installed version.

Risk: The referenced CLI handles OpenAI API keys and may process prompts, input images, generated images, and local history.

Mitigation: Use a restricted OpenAI API key with spending limits, avoid confidential prompts or images unless remote processing is acceptable, and clear or locate the CLI history for sensitive work.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/g9pedro/skills/openai-image-cli)
- [npm package](https://www.npmjs.com/package/@versatly/openai-image-cli)
- [GitHub project link from skill documentation](https://github.com/Versatly/openai-image-cli)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with bash commands and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include installation, authentication, generation, editing, variation, batch, configuration, model-listing, and history commands; JSON output mode is available through the referenced CLI.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
