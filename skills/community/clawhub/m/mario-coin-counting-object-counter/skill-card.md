## Description:

Count occurrences of an object in the image using computer vision algorithm.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lnj22](https://clawhub.ai/user/lnj22)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to run a local computer vision helper that counts how many times a provided template object appears in an input image.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The command-line interface advertises denoise and super_resolution tool choices that are not implemented.

Mitigation: Use only --tool count unless the publisher updates the script.

Risk: Object counts depend on image similarity, threshold selection, and deduplication distance.

Mitigation: Tune threshold and dedup_min_dist for representative images and review count results before relying on them.

## Reference(s):


## Skill Output:

**Output Type(s):** [Shell commands, Analysis, Text]

**Output Format:** [Markdown with inline bash command examples and plain-text count output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Runs local image processing on user-provided image files.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
