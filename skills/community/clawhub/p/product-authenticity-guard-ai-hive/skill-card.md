## Description:

Helps ecommerce platforms, merchants, content-generation teams, and product reviewers compare authorized product references with generated assets and produce authenticity differences, repair guidance, and AI-HIVE command workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

External ecommerce teams, merchants, generated-content teams, and product reviewers use this skill to turn product references, specifications, authorized media, channel constraints, and budget limits into an authenticity review and repair plan. When approved, it can also prepare or run AI-HIVE image and video generation, upload, polling, and download commands.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can act as a billable AI-HIVE media-generation client, not only as an authenticity reviewer.

Mitigation: Confirm prompts, model mode, routing, budget, and expected cost before running generation jobs; use small samples before batch work.

Risk: API keys and uploaded media can expose credentials, product data, or unauthorized assets.

Mitigation: Use a limited AI_HIVE_API_KEY, keep keys out of files, logs, and screenshots, and review asset rights before uploading files.

Risk: Authenticity output can be mistaken for physical inspection, legal judgment, or platform approval.

Mitigation: Mark unconfirmed differences for human review and retain product, brand, legal, and platform final checks for high-impact claims.

Risk: Changing the API base URL can route credentials or media to an unintended service.

Mitigation: Keep the default HTTPS AI-HIVE endpoint unless the operator has independently verified the target service.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wubin1836/skills/product-authenticity-guard-ai-hive)
- [AI-HIVE chat](https://ai-hive.iclip.cn/chat)
- [AI-HIVE OpenAPI base endpoint](https://ai-hive.iclip.cn/api)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown response with checklists, prompts, runnable shell commands, JSON task records, and optional media file paths.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include AI-HIVE task IDs, routing choices, pricing snapshots, status, and local download paths when generation tools are used.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
