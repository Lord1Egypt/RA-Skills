## Description:

Jimeng Video Generator helps agents create audio-enabled videos from text or images through Volcengine's Dreamina API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tel18610240060-collab](https://clawhub.ai/user/tel18610240060-collab)

### License/Terms of Use:


## Use Case:

External creators, content operators, and developers use this skill to generate short-form videos with optional AI-generated ambience, music, or sound effects from text prompts or input images.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts, referenced media, task metadata, and generated videos may be sent to and processed by Volcengine.

Mitigation: Use the skill only with material approved for Volcengine processing, and avoid confidential, regulated, or personal content unless that processing is acceptable.

Risk: API credentials are required for Volcengine access.

Mitigation: Store credentials in the documented credential file or an approved secret store, restrict access, and rotate credentials if exposure is suspected.

Risk: AI-generated audio may not match the intended creative direction or quality bar.

Mitigation: Review generated video and audio before publication, refine audio cues in prompts, or use a silent model with post-production audio when precise sound is required.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/tel18610240060-collab/skills/jimeng-video)
- [Volcengine content generation tasks API](https://ark.cn-beijing.volces.com/api/v3/contents/generations/tasks)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, API calls, markdown]

**Output Format:** [Markdown with bash, curl, and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guides agents through asynchronous video generation, task status checks, and result retrieval.]

## Skill Version(s):

2.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
