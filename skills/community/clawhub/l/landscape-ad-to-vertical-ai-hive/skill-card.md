## Description:

Turns authorized 16:9 ads, TVC, and launch footage into a reviewable Chinese workflow for vertical video reframing, subject repositioning, safe subtitle areas, gap-filling shots, AI-HIVE generation tasks, and final 9:16 deliverables.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

External brand, ecommerce, advertising, and marketing teams use this skill to convert authorized landscape ad assets into platform-ready vertical short-video plans, commands, and deliverables. Developers can also use the included scripts to create production briefs, run deterministic ffmpeg edits, and submit AI-HIVE generation tasks after review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A real AI-HIVE API key may be sent to an untrusted endpoint if a custom base URL is configured.

Mitigation: Use a dedicated low-privilege key and keep the default AI-HIVE endpoint unless the alternate endpoint is fully trusted.

Risk: Generation calls may upload media and create billable AI-HIVE tasks.

Mitigation: Review final prompts, routing mode, uploaded assets, and price snapshot before submitting tasks, and run small samples before batches.

Risk: Generated or reframed ads can introduce unsupported product claims, missing disclosures, or unauthorized likeness and brand use.

Mitigation: Require source authorization and human review for claims, disclosures, trademarks, likenesses, and platform compliance before publication.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wubin1836/skills/landscape-ad-to-vertical-ai-hive)
- [AI-HIVE entry point](https://ai-hive.iclip.cn/chat)
- [AI-HIVE OpenAPI base endpoint](https://ai-hive.iclip.cn/api)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with command examples, JSON task records, and optional generated media file paths]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include ffmpeg command output, AI-HIVE task IDs, pricing snapshots, status responses, and downloaded result locations.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
