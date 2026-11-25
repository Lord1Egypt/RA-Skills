## Description:

Helps short-form video marketers analyze a reference clip and adapt its composition and pacing into an original product video using Seedance 2.0 through Qinghu AI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[autoagc](https://clawhub.ai/user/autoagc)

### License/Terms of Use:

MIT-0

## Use Case:

External social commerce and short-form video teams use this skill to analyze a reference clip, adapt its shot structure and pacing to their product, and generate a Seedance 2.0 video. The workflow calls for reviewing the rewritten script before submitting the video task.

### Deployment Geography for Use:

China (Qinghu AI domestic service); workflows also target cross-border e-commerce markets.

## Known Risks and Mitigations:

Risk: The security summary flags unpinned package downloads and instructions that ask users to share an API key in chat; the scan is partial because referenced local paths were missing.

Mitigation: Review the package-install and credential instructions before installing. Keep API keys out of chat and enter them through a protected local method; treat the partial scan as incomplete evidence.

## Reference(s):

- [QHKIT npm package](https://www.npmjs.com/package/@iqinghu/qhkit)
- [ClawHub release page](https://clawhub.ai/autoagc/skills/linkpix-seedance-2-clone)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown script drafts and qhkit command examples with JSON parameters]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include a reference script and rewritten product-video script for user review, plus task status and video result links.]

## Skill Version(s):

0.1.6 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
