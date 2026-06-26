## Description: <br>
Generates PNG images from text prompts with the MiniMax image-01 model, using either China or global MiniMax API endpoints. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sweesama](https://clawhub.ai/user/sweesama) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to generate one or more images from natural-language prompts, choose a MiniMax region, control aspect ratio, and save PNG outputs locally. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts and generation settings are sent to MiniMax endpoints and may contain sensitive information. <br>
Mitigation: Keep prompts free of confidential, regulated, or personal data unless the intended MiniMax account and region are approved for that use. <br>
Risk: Image generation consumes MiniMax API quota. <br>
Mitigation: Review the requested image count and output directory before running batch generations. <br>
Risk: The MiniMax API key is required for execution. <br>
Mitigation: Store MINIMAX_API_KEY as a secret environment variable and avoid printing or committing it. <br>


## Reference(s): <br>
- [MiniMax China API key page](https://platform.minimaxi.com/user-center/basic-information/interface-key) <br>
- [MiniMax global API key page](https://www.minimax.io/platform/user-center/basic-information/interface-key) <br>
- [Prompt templates](references/prompt_templates.md) <br>
- [ClawHub listing](https://clawhub.ai/sweesama/mz-minimax-img-gen) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, code, files, guidance] <br>
**Output Format:** [Markdown guidance with Python command examples and generated PNG files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs PNG files named minimax_gen_1.png and similar paths; batch generation is capped at 9 images per run.] <br>

## Skill Version(s): <br>
1.3.8 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
