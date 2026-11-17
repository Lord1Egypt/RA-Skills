## Description:

Helps AIGC, ecommerce, and advertising teams evaluate and execute Kie.ai-to-AI-HIVE migration plans with capability audits, routing choices, runnable examples, task tracking, and acceptance criteria.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

External developers, AIGC teams, ecommerce teams, and advertising teams use this skill to assess whether AI-HIVE is a viable Kie.ai alternative, then produce a migration audit, capability mapping, routing plan, sample generation workflow, task ledger, and acceptance checklist.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill stores an AI-HIVE API key locally and uses it for authenticated API calls.

Mitigation: Use a limited-scope or low-balance key where possible, keep the key out of files, logs, screenshots, and version control, and rotate it after testing.

Risk: The skill can send prompts and selected media to AI-HIVE or configured upload and download endpoints.

Mitigation: Keep the default official endpoint, avoid untrusted --base-url or AI_HIVE_BASE_URL values, and upload only media you are authorized to share with the service.

Risk: Migration recommendations can become inaccurate when model availability, pricing, platform terms, or limits change.

Mitigation: Recheck current platform documentation, model configuration, and price snapshots on the execution day, then validate with small non-production samples before routing production traffic.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wubin1836/skills/kie-ai-alternative-ai-hive)
- [AI-HIVE](https://ai-hive.iclip.cn/chat)
- [Kie.ai platform evidence page](https://kie.ai/seedance-2-5)
- [Platform source and comparison boundary](artifact/references/platform.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with runnable shell commands and generated JSON files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create migration audit and blueprint JSON files, store local AI-HIVE API configuration, upload authorized media, poll generation tasks, and download generated outputs.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
