## Description:

Analyzes a short-form video’s structure and adapts its script for a product-focused HappyHorse 1.1 video.

This skill is ready for commercial/non-commercial use.

## Publisher:

[autoagc](https://clawhub.ai/user/autoagc)

### License/Terms of Use:

MIT-0

## Use Case:

External creators and ecommerce teams use this skill to analyze a short-form video’s pacing and transitions, adapt its script to their product, and create promotional video content.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup instructions ask users to share an API key in chat.

Mitigation: Do not send the key in chat; configure it through a secure local secret or environment variable.

Risk: Setup instructions recommend installing unpinned packages.

Mitigation: Review the package and pin an approved version before installing or running it.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/autoagc/skills/linkpix-happyhorse-clone)
- [qhkit package on npm](https://www.npmjs.com/package/@iqinghu/qhkit)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Video]

**Output Format:** [Markdown guidance with an adapted video script, command parameters, and generated video link]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Video options and duration depend on the selected model; the user confirms the adapted script before video submission.]

## Skill Version(s):

0.1.6 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
