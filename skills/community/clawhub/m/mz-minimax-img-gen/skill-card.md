## Description:

Generates PNG images from Chinese or English text prompts using MiniMax image-01, with China or global endpoint selection, aspect ratio control, batch generation, and optional prompt enhancement.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sweesama](https://clawhub.ai/user/sweesama)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to generate image assets from text prompts through their own MiniMax account and quota. It is suited for producing draft visuals, social images, product concepts, thumbnails, and other prompt-driven PNG outputs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts are sent to MiniMax's external image-generation service.

Mitigation: Avoid including secrets, private personal data, or sensitive business information in image prompts.

Risk: The skill uses the caller's MiniMax API key and image-generation quota.

Mitigation: Store MINIMAX_API_KEY as an environment variable and monitor MiniMax account usage before running batch generations.

Risk: Generated files are named minimax_gen_*.png and may overwrite matching files in the output directory.

Mitigation: Write outputs to a private, task-specific directory where those filenames will not replace important files.

Risk: The helper depends on the Python requests package.

Mitigation: Install dependencies in a virtual environment before use.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/sweesama/skills/mz-minimax-img-gen)
- [MiniMax Image-01 Prompt Templates](references/prompt_templates.md)
- [MiniMax China API key page](https://platform.minimaxi.com/user-center/basic-information/interface-key)
- [MiniMax Global API key page](https://www.minimax.io/platform/user-center/basic-information/interface-key)

## Skill Output:

**Output Type(s):** [shell commands, configuration, files, guidance]

**Output Format:** [Markdown guidance with bash command examples; PNG files written by the MiniMax API helper]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires MINIMAX_API_KEY; supports cn/global regions, aspect ratios, up to 9 images per run, optional prompt enhancement, and caller-selected output directories.]

## Skill Version(s):

1.3.8 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
