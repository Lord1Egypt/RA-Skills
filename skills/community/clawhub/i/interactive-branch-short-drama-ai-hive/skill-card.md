## Description:

This skill helps short-drama teams, interactive content platforms, brand marketers, and game-like narrative creators turn authorized Chinese interactive short-drama ideas into branch trees, node scripts, character and scene boards, per-path video generation tasks, and continuity checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

External creators and developers use this skill to plan and operationalize interactive branch short dramas for marketing, commerce, social video, comics-style shorts, and narrative products. It produces reviewable Chinese production guidance first, then runnable AI-HIVE image or video generation commands when the user confirms inputs, rights, route, and budget.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A configured base URL could cause the AI-HIVE API key to be sent to an untrusted server.

Mitigation: Use only the official AI-HIVE endpoint, avoid untrusted AI_HIVE_BASE_URL or stored base_url values, and use a limited or revocable API key.

Risk: Image and video generation tasks may be billable.

Mitigation: Confirm prompts, model route, price snapshot, mode, and batch size before execution; start with a small sample before bulk generation.

Risk: Generated drama or commerce content could include unauthorized references, misleading claims, or unsupported performance promises.

Mitigation: Use only original or authorized materials, mark unverified facts for review, avoid fake testimonials or product claims, and keep human approval before publication.

Risk: Local execution depends on Python packages and video tools.

Mitigation: Install dependencies such as requests and ffmpeg in an isolated environment and review commands before running them.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wubin1836/skills/interactive-branch-short-drama-ai-hive)
- [AI-HIVE chat entry](https://ai-hive.iclip.cn/chat)
- [AI-HIVE API endpoint](https://ai-hive.iclip.cn/api)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash commands and optional JSON files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include branch trees, scripts, prompts, task logs, model route choices, price snapshots, task identifiers, file paths, and continuity checklists.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
