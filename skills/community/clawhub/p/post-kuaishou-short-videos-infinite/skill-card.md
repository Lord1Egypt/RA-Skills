## Description:

Guides an agent through publishing a short video on the Kuaishou Creator platform, including upload, description, cover, AI-content declaration, download permission, and final publish steps.

This skill is ready for commercial/non-commercial use.

## Publisher:

[infiniteask](https://clawhub.ai/user/infiniteask)

### License/Terms of Use:

MIT-0

## Use Case:

External creators and operators use this skill to help an agent publish prepared short-form video content to Kuaishou Creator Center while applying the requested title, description, tags, cover, AI-generation declaration, and download setting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide an agent to submit a public Kuaishou post and change download permissions without a built-in final confirmation checkpoint.

Mitigation: Before publishing, require the agent to summarize the exact video file, title, description, tags, cover, AI-content declaration, and download setting, then wait for explicit user approval before clicking publish.

Risk: Incorrect selected media or metadata could result in publishing unintended content.

Mitigation: Have the agent confirm the selected file path and all visible form values from the page before any irreversible publish action.

## Reference(s):

- [Kuaishou Creator Center video publishing page](https://cp.kuaishou.com/article/publish/video?tabType=1)
- [ClawHub skill page](https://clawhub.ai/infiniteask/skills/post-kuaishou-short-videos-infinite)

## Skill Output:

**Output Type(s):** [guidance, code, shell commands]

**Output Format:** [Markdown instructions with browser-action guidance and inline Python examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a user-provided video file, title or description, tags, cover preference, AI-content declaration, and download permission choice.]

## Skill Version(s):

1.0.2 (source: server release metadata; artifact frontmatter lists 1.0.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
