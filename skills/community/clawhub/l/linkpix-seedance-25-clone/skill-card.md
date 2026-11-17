## Description:

Guides an agent to adapt a reference short-form video's script for a product and generate a new video through qhkit when a suitable model is available.

This skill is ready for commercial/non-commercial use.

## Publisher:

[autoagc](https://clawhub.ai/user/autoagc)

### License/Terms of Use:

MIT-0

## Use Case:

Short-video creators, agencies, and brand marketers use this skill to analyze a reference video, adapt its pacing and script to their own products, and request a generated marketing video.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installing a third-party CLI introduces dependency risk.

Mitigation: Review the package before installation and prefer pinned or preinstalled dependencies in higher-security environments.

Risk: API credentials may be stored locally or passed through environment variables.

Mitigation: Protect the API key and avoid exposing it in shared commands or output.

Risk: Submitted media and links are sent to iqinghu for processing.

Mitigation: Confirm that the user is comfortable sharing those inputs before submission.

Risk: Generating a video can consume credits.

Mitigation: Check the cost estimate and obtain explicit user approval before generation.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/autoagc/skills/linkpix-seedance-25-clone)
- [qhkit npm package](https://www.npmjs.com/package/@iqinghu/qhkit)
- [iqinghu API keys](https://www.iqinghu.com/workbench/dashboard/api-keys?urlCode=1788417429126)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown with a script comparison, generation instructions, and a video link]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Video generation requires model availability and user confirmation of cost and inputs.]

## Skill Version(s):

0.1.4 (source: server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
