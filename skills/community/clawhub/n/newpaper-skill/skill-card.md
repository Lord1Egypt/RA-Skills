## Description:

Converts academic paper PDFs into PowerPoint posters and HTML files using OpenAI-compatible model APIs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[caoxinran102-sys](https://clawhub.ai/user/caoxinran102-sys)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and researchers use this skill to turn a paper PDF, and optionally a logo, into editable poster outputs while the agent handles setup, configuration, and generation commands.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill downloads and runs mutable external code.

Mitigation: Use a disposable workspace or sandbox, inspect the repository before execution, and pin a reviewed revision when possible.

Risk: The workflow installs packages into a Conda environment.

Mitigation: Review dependency changes before installation and avoid running the setup in sensitive host environments.

Risk: Paper contents are sent to the configured model provider.

Mitigation: Avoid sensitive unpublished papers unless the configured provider is trusted for that data.

Risk: The skill stores API credentials in a plaintext .env file.

Mitigation: Prefer environment-injected or temporary credentials and remove plaintext secrets after use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/caoxinran102-sys/skills/newpaper-skill)
- [Paper2Poster arXiv paper](https://arxiv.org/abs/2505.21497)
- [Paper2Poster project page](https://paper2poster.github.io/)
- [Paper2Poster dataset](https://huggingface.co/datasets/Paper2Poster/Paper2Poster)
- [Paper2Poster demo](https://huggingface.co/spaces/camel-ai/Paper2Poster)
- [External repository specified by the skill](https://github.com/caoxinran102-sys/Paper2Poster.git)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Configuration, Files, Guidance]

**Output Format:** [Markdown guidance with shell commands that generate PPTX and HTML poster files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses the supplied paper PDF path and optional logo path; generated files are written under a generated_posters directory.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
