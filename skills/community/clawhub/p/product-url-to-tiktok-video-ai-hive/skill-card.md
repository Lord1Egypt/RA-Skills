## Description:

Turns product-link TikTok commerce requests into page fact tables, English hooks, UGC scripts, AI-HIVE media-generation commands, vertical video edits, and review checklists.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

External TikTok Shop sellers, cross-border commerce teams, and paid-media operators use this skill to turn product page facts, authorized product media, target markets, audience constraints, and compliance limits into production-ready commerce video plans and assets. Developers can also use the bundled scripts to create project blueprints, call AI-HIVE image or video generation, upload authorized media, poll asynchronous tasks, and perform deterministic short-video edits.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill stores and uses an AI-HIVE API key locally.

Mitigation: Install only if the AI-HIVE service is trusted, use a limited API key when available, keep credentials out of files and logs, and rely on the local config permissions described by the artifact.

Risk: The skill allows a configurable API endpoint through AI_HIVE_BASE_URL or --base-url.

Mitigation: Prefer the default AI-HIVE URL and only set a custom endpoint when it is controlled and trusted.

Risk: Image or video generation can upload user media and may incur cost.

Mitigation: Upload only media the user is authorized to use, review prompts and routing before generation, and confirm billable tasks before submitting them.

Risk: The advertised product-link workflow is only partially implemented and may depend on user-supplied page facts.

Mitigation: Require product facts or accessible page material, mark unverified claims as pending review, and avoid guessing prices, stock, certifications, efficacy, or platform outcomes.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wubin1836/skills/product-url-to-tiktok-video-ai-hive)
- [AI-HIVE chat](https://ai-hive.iclip.cn/chat)
- [AI-HIVE API base URL](https://ai-hive.iclip.cn/api)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, JSON, guidance]

**Output Format:** [Markdown guidance with inline shell commands and optional JSON files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include task records with routing, model, price snapshot, taskId, status, and downloaded file locations after user confirmation for billable generation.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
