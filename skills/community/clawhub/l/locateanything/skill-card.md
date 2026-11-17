## Description:

NVIDIA LocateAnything-3B vision-language grounding model covering inference APIs, data preparation, training, fine-tuning, and evaluation for object detection, visual grounding, GUI recognition, and OCR.

This skill is for research and development only.

## Publisher:

[openlark](https://clawhub.ai/user/openlark)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to work with LocateAnything-3B for vision-language grounding tasks, including detection, point grounding, OCR, GUI element recognition, data preparation, training, and evaluation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installation steps run unpinned external code and dependencies that can change after review.

Mitigation: Install in an isolated virtual environment or container, review upstream repositories first, and pin Eagle, MagiAttention, submodules, and Python dependencies to reviewed commits or locked versions before use with sensitive files or shared infrastructure.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/openlark/skills/locateanything)
- [LocateAnything-3B model](https://huggingface.co/nvidia/LocateAnything-3B)
- [LocateAnything demo](https://huggingface.co/spaces/nvidia/LocateAnything)
- [NVlabs Eagle repository](https://github.com/NVlabs/Eagle)
- [Eagle project page](https://nvlabs.github.io/Eagle/)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown with Python, JSON, JSONL, and bash examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes normalized box and point formats, data recipe examples, training parameters, and evaluation commands.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
