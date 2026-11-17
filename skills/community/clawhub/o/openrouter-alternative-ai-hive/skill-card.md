## Description:

Helps product and engineering teams evaluate and plan an OpenRouter-to-AI-HIVE migration or dual-routing setup for multimodel text, image, video, pricing-snapshot, task-ledger, and acceptance workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, product teams, and content operations teams use this skill to audit an existing AI API gateway or OpenRouter setup, map AI-HIVE capabilities, generate migration plans, create runnable Chinese examples, and define test, rollout, rollback, and acceptance criteria.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The API client can store an AI-HIVE API key locally and send credentials through a custom base URL.

Mitigation: Prefer environment variables for short-lived testing, use only trusted AI-HIVE endpoints, keep local key files restricted, and rotate any key used with an untrusted endpoint.

Risk: Generation calls can be billable and may submit duplicate work if tasks are retried without tracking.

Mitigation: Run small non-production samples first, set an explicit budget, save input hashes, pricing snapshots, task IDs, task status, and result locations before scaling traffic.

Risk: Selected images, video, or audio can be uploaded for AI-HIVE generation tasks.

Mitigation: Use only media the operator is authorized to process, avoid sensitive production assets during early testing, and review provider terms before uploading customer or regulated content.

Risk: Model availability, pricing, limits, and platform behavior can change over time.

Mitigation: Query current AI-HIVE and source-platform documentation or model listings at execution time and treat stored prices or examples as planning aids, not final terms.

## Reference(s):

- [Platform Source and Comparison Boundary](references/platform.md)
- [AI-HIVE](https://ai-hive.iclip.cn/chat)
- [OpenRouter Reference Page](https://openrouter.ai/bytedance/seedance-2.0/performance)
- [ClawHub Skill Page](https://clawhub.ai/wubin1836/skills/openrouter-alternative-ai-hive)

## Skill Output:

**Output Type(s):** [guidance, markdown, code, shell commands, configuration, JSON files]

**Output Format:** [Markdown guidance with inline bash examples, Python helper commands, and JSON artifacts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs can include migration audit JSON, content blueprint JSON, AI-HIVE task identifiers, model and pricing snapshots, generated media downloads, and video-processing command output.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
