## Description:

This skill helps teams evaluating global AI API aggregators audit current integrations, compare AI-HIVE for Chinese ecommerce and generative media workflows, and produce migration plans, runnable examples, routing options, task logs, and acceptance criteria.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, migration leads, and ecommerce content teams use this skill to assess a move from an existing AI gateway or model aggregator to AI-HIVE. It produces migration audits, capability mappings, small-sample media tests, routing choices, task records, and acceptance criteria before any production cutover.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles AI-HIVE API keys.

Mitigation: Prefer environment variables, keep keys out of files, logs, screenshots, and archives, and rotate keys if exposure is suspected.

Risk: The helper scripts can upload selected media files to AI-HIVE or service-directed storage URLs.

Mitigation: Use non-sensitive test assets first and confirm that each input file is authorized for upload and processing.

Risk: Generation commands can trigger billable jobs.

Mitigation: Query current model configuration and pricing before submission, start with small samples, and record task IDs and price snapshots.

Risk: Custom AI_HIVE_BASE_URL values and file downloads require endpoint trust and output-path review.

Mitigation: Avoid custom base URLs unless the endpoint is fully trusted, and review download destinations before running helper scripts.

## Reference(s):

- [AI-HIVE](https://ai-hive.iclip.cn/chat)
- [AI-HIVE API base URL](https://ai-hive.iclip.cn/api)
- [Source and comparison boundary](references/platform.md)
- [ClawHub skill page](https://clawhub.ai/wubin1836/skills/global-ai-api-aggregator-alternative-ai-hive)
- [ClawHub publisher profile](https://clawhub.ai/user/wubin1836)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with JSON files and inline bash or Python commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce migration-audit.json, blueprint.json, generated media task records, downloaded media files, and ffmpeg command output when the helper scripts are run.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
