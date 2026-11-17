## Description:

This skill helps agents use the Lumi API to repurpose Chinese social videos for TikTok, YouTube, and Instagram with upload, translation, AI dubbing, subtitling, publishing, account, and analytics workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jeffery1995](https://clawhub.ai/user/jeffery1995)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to prepare Lumi API requests for uploading, localizing, dubbing, subtitling, publishing, and monitoring short-form video content across connected social accounts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can automatically publish repurposed videos to linked TikTok, YouTube, and Instagram accounts after processing.

Mitigation: Review the source video, generated localization, caption text, target accounts, and platform visibility before allowing auto-publishing.

Risk: The Lumi API key can allow video upload and processing, connected-account retrieval, analytics access, and publishing actions.

Mitigation: Store LUMI_API_KEY only in the environment, limit access to trusted users, and rotate or revoke the key if account access changes.

Risk: Repurposing third-party videos may create rights, attribution, or platform-policy issues.

Mitigation: Confirm that the user owns or has permission to reuse each source video before starting repurpose or localization workflows.

## Reference(s):

- [Lumi homepage](https://lumipath.cn)
- [Lumi voice catalog](https://lumipath.cn/voices)
- [README.md](artifact/README.md)
- [connections.openapi.json](artifact/references/connections.openapi.json)
- [insights.openapi.json](artifact/references/insights.openapi.json)
- [localization.openapi.json](artifact/references/localization.openapi.json)
- [repurpose.openapi.json](artifact/references/repurpose.openapi.json)
- [social-posts.openapi.json](artifact/references/social-posts.openapi.json)
- [tts.openapi.json](artifact/references/tts.openapi.json)
- [videos.openapi.json](artifact/references/videos.openapi.json)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with curl commands, API request parameters, and status summaries.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires LUMI_API_KEY; workflows may initiate Lumi API calls that upload, process, localize, publish, or inspect social media account data.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
