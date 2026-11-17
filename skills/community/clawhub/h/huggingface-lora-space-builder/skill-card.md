## Description:

Builds and publishes a tailored Gradio demo on Hugging Face Spaces for a user-provided LoRA, including pipeline selection, LoRA-specific UI design, Space files, and private publishing by default.

This skill is ready for commercial/non-commercial use.

## Publisher:

[huggingface](https://clawhub.ai/user/huggingface)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to turn a Hugging Face LoRA into a usable browser demo. It guides them through reading the LoRA and base model cards, choosing the right inference recipe, creating Space files, publishing privately, and smoke-testing the result.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may ask users to expose powerful Hugging Face access tokens while reading private or gated models and publishing Spaces.

Mitigation: Use an existing authenticated Hugging Face session when possible; otherwise use fine-grained, least-privilege tokens and prefer a secure secret store over pasting tokens into chat.

Risk: The skill can deploy mutable external code or browser scripts into a public-facing Space.

Mitigation: Pin Git dependencies to reviewed commit SHAs and vendor or integrity-pin external browser scripts before making the Space public.

Risk: A Space can build successfully but fail at first inference because of an incorrect LoRA weight name, missing dependency, gated-model token issue, or wrong pipeline class.

Mitigation: Run the documented smoke test after publishing, inspect build or runtime logs on failure, and verify custom or Hub components in a browser when the UI depends on them.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/huggingface/skills/huggingface-lora-space-builder)
- [Adapting the demo to the specific LoRA](references/adapting-to-the-lora.md)
- [Tasks: per-task baseline UI patterns](references/tasks.md)
- [ZeroGPU and publishing](references/zerogpu-and-publishing.md)
- [Creative mode: custom HTML/JS UIs in Gradio](references/creative-mode.md)
- [Qwen-Image and Qwen-Image-Edit reference](references/base-models/qwen-image.md)
- [LTX reference](references/base-models/ltx.md)
- [Krea 2 reference](references/base-models/krea-2.md)
- [Hugging Face Spaces GPU documentation](https://huggingface.co/docs/hub/spaces-gpus#community-gpu-grants)
- [Gradio documentation](https://www.gradio.app/docs)
- [Hugging Face diffusers](https://github.com/huggingface/diffusers)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with Python, shell, and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Typically produces Space implementation files such as app.py, requirements.txt, and README.md, then publishing and smoke-test guidance.]

## Skill Version(s):

1.0.10 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
