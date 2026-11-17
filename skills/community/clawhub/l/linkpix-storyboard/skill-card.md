## Description:

Creates video storyboard scripts with shot plans, camera movement, narration, and optional storyboard images for product videos.

This skill is ready for commercial/non-commercial use.

## Publisher:

[autoagc](https://clawhub.ai/user/autoagc)

### License/Terms of Use:

MIT-0

## Use Case:

Creators and marketers use this skill to plan product-video shots and generate a storyboard script, with optional storyboard images.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may install or update qhkit and Node on the user's machine.

Mitigation: Use a controlled environment with Node and qhkit already installed; avoid unpinned npx or latest-version execution where possible.

Risk: The skill may configure a service token on the user's machine.

Mitigation: Provide credentials only through a method you can revoke or remove.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/autoagc/skills/linkpix-storyboard)
- [qhkit package](https://www.npmjs.com/package/@iqinghu/qhkit)

## Skill Output:

**Output Type(s):** [Markdown, Images, Guidance]

**Output Format:** [Storyboard script and shot table, with optional image links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Storyboard images require qhkit and a configured service token; a script-only fallback is available.]

## Skill Version(s):

0.1.8 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
