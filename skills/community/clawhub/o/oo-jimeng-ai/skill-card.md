## Description:

Jimeng AI (volcengine.com). Use this skill for ANY Jimeng AI request — reading, creating, and updating data. Whenever a task involves Jimeng AI, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to submit Jimeng image and video generation or upscaling jobs, then check their results through an OOMOL-connected account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Initial CLI setup can execute a changing online installer whose effects were not inspected.

Mitigation: Review the installer, use a verified release, and explicitly approve local changes.

Risk: Generation inputs pass through OOMOL to the connected provider, and submitted jobs may consume credit.

Mitigation: Review prompts and payloads before submission, confirm state-changing jobs, and check expected credit use.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/oomol/skills/oo-jimeng-ai)
- [oo CLI](https://github.com/oomol-lab/oo-cli)
- [Jimeng AI product page](https://www.volcengine.com/product/jimeng)
- [Volcengine API documentation](https://api.volcengine.com/api-docs/?serviceCode=cv&version=2024-06-06)

## Skill Output:

**Output Type(s):** [Shell commands, JSON payloads, API calls, Guidance, Image and video results]

**Output Format:** [Markdown instructions with oo CLI examples and JSON inputs; action results are returned through the connected service.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generation and processing jobs are asynchronous; separate result actions retrieve completed job results.]

## Skill Version(s):

1.0.5 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
