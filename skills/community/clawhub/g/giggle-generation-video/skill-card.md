## Description:

Supports text-to-video and image-to-video generation with configurable model, duration, aspect ratio, resolution, and optional start or end frame references.

This skill is ready for commercial/non-commercial use.

## Publisher:

[patches429](https://clawhub.ai/user/patches429)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users can use this skill to submit text-to-video or image-to-video jobs to the Giggle Generation API, then query task status and receive generated video links.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Authenticated requests may expose the Giggle API key if redirected off-site.

Mitigation: Use a dedicated Giggle API key with limited quota and require same-origin redirect validation or disabled redirects before routine use.

Risk: Prompts, reference images, and generated video links may contain sensitive or private content.

Mitigation: Avoid submitting sensitive prompts or private images, and treat returned signed URLs as temporary private access links.

Risk: The dependency declaration allows future requests versions rather than a pinned, reviewed package.

Mitigation: Pin and review Python dependencies before deploying the skill in a routine or production environment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/patches429/skills/giggle-generation-video)
- [Giggle API service](https://giggle.pro/)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands, JSON task status, and signed video links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires GIGGLE_API_KEY and python3 with requests; generated video links are temporary signed URLs.]

## Skill Version(s):

0.0.10 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
