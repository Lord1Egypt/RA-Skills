## Description:

Turns authorized long-form video projects into a Chinese production workflow for up to 30 short-video candidates, including topics, timecodes, hooks, scripts, cover ideas, schedules, runnable commands, and optional AI-HIVE generation steps.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

External creators, marketing teams, ecommerce teams, and video producers use this skill to plan and execute authorized long-video repurposing into short-form content packages. Developers and operators can also use the bundled scripts to create project blueprints, inspect and reformat video assets, and submit optional AI-HIVE generation jobs after parameter review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: API keys may be exposed through command history, logs, screenshots, or an untrusted custom endpoint.

Mitigation: Use environment variables or protected config for credentials, avoid --api-key in shared shells, and keep AI_HIVE_BASE_URL and --base-url on the official HTTPS endpoint unless the alternate server is fully trusted.

Risk: Uploaded media may include copyrighted, private, trademarked, or otherwise unauthorized material.

Mitigation: Use only media the operator is authorized to upload and keep unsupported reference material to abstract structure guidance instead of copying protected expression.

Risk: AI-HIVE generation jobs may incur cost or create unwanted outputs if submitted before review.

Mitigation: Confirm prompts, model mode, routing, price snapshot, and parameters before paid calls; run a small sample before batch generation.

Risk: Generated commercial claims or platform guidance may be inaccurate or unsupported.

Mitigation: Mark unverified claims for human review and do not treat generated text as a substitute for product data, platform rules, legal advice, or performance guarantees.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wubin1836/skills/long-video-to-thirty-shorts-ai-hive)
- [AI-HIVE chat entry point](https://ai-hive.iclip.cn/chat)
- [AI-HIVE API endpoint](https://ai-hive.iclip.cn/api)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with structured sections, inline shell commands, JSON task records, and generated media file paths when jobs are run]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs are intended to be reviewable before any billable AI-HIVE generation call; generated media workflows can include task IDs, pricing snapshots, status records, and downloaded files.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
