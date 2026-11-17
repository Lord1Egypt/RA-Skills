## Description:

md2wechat helps agents operate the md2wechat CLI to convert Markdown into WeChat Official Account HTML, previews, drafts, image posts, generated covers or infographics, title suggestions, and related article-writing workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[geekjourneyx](https://clawhub.ai/user/geekjourneyx)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, creators, and publishing teams use this skill to guide an agent through WeChat Official Account article formatting, preview, readiness inspection, draft creation, image-post creation, and related md2wechat CLI workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Draft creation, image upload, publishing, or remote image generation can use local credentials and affect a WeChat account or external provider when explicitly requested.

Mitigation: Review the proposed command before approval and allow those actions only when the user has explicitly requested them and required credentials are configured.

Risk: Publishing readiness can be misread if an agent relies on stale checks or legacy booleans.

Mitigation: Use inspect --json and evaluate data.readiness.targets plus data.readiness.blockers before upload or draft actions.

Risk: Article formatting can unintentionally modify source Markdown if generated content is saved in place.

Mitigation: Keep source Markdown read-only by default, write temporary formatted artifacts, and require explicit user confirmation before saving generated Markdown next to the source.

Risk: Title suggestions, advice, and image plans may be recommendations or prompt requests rather than completed publishing decisions.

Mitigation: Treat advisory outputs as recommendation-only and require user confirmation before converting them into final article, image, upload, or draft actions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/geekjourneyx/skills/md2wechat)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON-aware CLI output handling]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May direct the agent to create temporary formatted Markdown artifacts, local previews, drafts, uploads, or image-generation plans only when the user requests those actions and required credentials are configured.]

## Skill Version(s):

3.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
