## Description:

AI-powered marketing asset generation workflow that combines DuckDuckGo design inspiration search, Gemini Nano Banana Pro image generation, Feishu Drive cloud storage, and Slack team notifications.

This skill is ready for commercial/non-commercial use.

## Publisher:

[terrycarter1985](https://clawhub.ai/user/terrycarter1985)

### License/Terms of Use:

MIT-0

## Use Case:

Marketing teams and automation developers use this skill to research campaign design inspiration, generate marketing images, upload approved assets to Feishu Drive, and notify collaborators in Slack.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Readable local files may be uploaded to Feishu Drive or Slack if arbitrary file paths are passed to upload methods.

Mitigation: Restrict uploads to the generated asset directory, avoid arbitrary file paths, and require explicit confirmation before sharing files to configured external channels.

Risk: Generated marketing assets may be shared with the wrong Feishu folder or Slack channel if credentials or channel settings are misconfigured.

Mitigation: Use a dedicated workspace, verify destination folder and channel IDs before execution, and keep credentials scoped to the intended marketing workflow.

Risk: Unpinned dependencies may change behavior across installations.

Mitigation: Pin dependency versions during deployment and review updates before reinstalling or running the workflow.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/terrycarter1985/skills/marketing-asset-generator)

## Skill Output:

**Output Type(s):** [Files, Text, Configuration, Guidance]

**Output Format:** [Python result object with generated asset file paths, Feishu links, and inspiration notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires configured Gemini, Feishu, and Slack credentials before use.]

## Skill Version(s):

1.0.0 (source: server release metadata and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
