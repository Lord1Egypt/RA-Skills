## Description:

Build, train, and debug deep learning models with Keras patterns, layer recipes, and training diagnostics.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ivangdavila](https://clawhub.ai/user/ivangdavila)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to build Keras or TensorFlow neural networks, choose architectures and layers, configure training loops and callbacks, and debug model training issues.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may ask the agent to save a broad Keras activation preference into MAIN memory.

Mitigation: Ask the agent not to write Keras activation preferences to MAIN memory; keep any saved Keras preferences only in ~/keras/memory.md after explicit consent.

Risk: Transfer-learning examples may download pretrained weights when imagenet weights are used.

Mitigation: Use weights=None when fully offline operation is required.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ivangdavila/skills/keras)
- [Skill homepage](https://clawic.com/skills/keras)
- [Setup guide](artifact/setup.md)
- [Layer patterns](artifact/layers.md)
- [Training diagnostics](artifact/training.md)
- [Common architectures](artifact/architectures.md)
- [Memory template](artifact/memory-template.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Python/Keras code examples and occasional shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include local preference-file suggestions only after user consent.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
