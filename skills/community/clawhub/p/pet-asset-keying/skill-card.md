## Description:

Removes backgrounds from illustrated pet-character images and frame sequences, producing transparent PNG cutouts with a model-free outline-based method.

This skill is ready for commercial/non-commercial use.

## Publisher:

[catsmansion](https://clawhub.ai/user/catsmansion)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and illustrators working with anthropomorphic pet-character artwork use this skill to remove flat backgrounds from single images or frame sequences and produce transparent PNG cutouts. Its primary method is best suited to artwork with clear outline art.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Alternative processing paths require extra dependencies and model resources, and the temporal helper has a missing module.

Mitigation: Use line_keying.py for the model-free path and check dependencies before choosing an alternative.

Risk: The self-check report does not automatically stop processing when its hole counts are concerning.

Mitigation: Keep the source images, write outputs to a separate directory, and inspect results manually.

## Reference(s):

- [Line Keying Design Notes](references/LINE_KEYING.md)
- [Pitfalls and Tested Failure Cases](references/PITFALLS.md)
- [ClawHub release page](https://clawhub.ai/catsmansion/skills/pet-asset-keying)

## Skill Output:

**Output Type(s):** [Files, Guidance]

**Output Format:** [Transparent PNG images and concise processing self-check reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Single images or frame sequences; outputs may be cropped around the character.]

## Skill Version(s):

0.1.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
