## Description:

This skill helps podcast hosts, interview programs, knowledge creators, and content teams turn authorized podcast or interview material into short-video plans, titles, timestamps, b-roll concepts, AI-HIVE generation commands, and acceptance checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

External creators, marketers, and content teams use this skill to convert authorized long-form podcast or interview assets into reviewable short-video production plans and runnable AI-HIVE workflows. It emphasizes preserving each clip's argument and context while documenting tasks, costs, files, and acceptance checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The AI-HIVE client can forward the user's API key to an arbitrary configured API endpoint.

Mitigation: Use the official AI-HIVE endpoint unless the alternative endpoint is intentionally trusted; avoid setting --base-url, AI_HIVE_BASE_URL, or config base_url casually.

Risk: Selected audio, video, images, or other media may be uploaded to AI-HIVE during generation workflows.

Mitigation: Confirm reuse rights and sensitivity before upload, and use only media the user is authorized to process.

Risk: Generated commands can upload media, start generation jobs, incur cost, download files, or write local outputs.

Mitigation: Review prompts, routes, model choices, output paths, and billable actions before execution; run a small sample before batch jobs.

Risk: Podcast clips or marketing shorts could misrepresent speakers, product claims, or platform compliance if used without review.

Mitigation: Preserve context, mark unverified claims, avoid unauthorized likeness or voice reuse, and keep human review before publication.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wubin1836/skills/podcast-interview-to-shorts-ai-hive)
- [AI-HIVE chat and API access](https://ai-hive.iclip.cn/chat)
- [AI-HIVE API endpoint](https://ai-hive.iclip.cn/api)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with command examples, JSON task records, and file path references]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include AI-HIVE routing mode, model, price snapshot, taskId, status, and downloaded file locations when generation tasks are used.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
