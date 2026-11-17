## Description:

Helps ecommerce, brand review, and content production teams check AI product images against real references and produce issue lists, risk ratings, remediation guidance, review records, and optional AI-HIVE generation commands.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

External ecommerce design, product operations, brand review, and batch image generation teams use this skill to inspect product images for product fidelity, text, logo, composition, platform sizing, and commercial-risk issues before repair or publication.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles an AI-HIVE API key and can send requests to a configurable endpoint.

Mitigation: Use the default AI-HIVE endpoint, avoid untrusted --base-url or AI_HIVE_BASE_URL values, store the key securely, and rotate the key if it may have been exposed.

Risk: Uploads and generation requests use an external service and may incur billing.

Mitigation: Confirm prompts, model, routing mode, pricing snapshot, and batch size before submission; start with a small sample before batch generation.

Risk: The bundled code focuses on media generation and upload workflows rather than a standalone read-only product-image auditor.

Mitigation: Treat outputs as assisted review artifacts and keep human final review for SKU accuracy, legal claims, brand usage, platform requirements, and printed text.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wubin1836/skills/product-image-quality-check-ai-hive)
- [AI-HIVE chat entry](https://ai-hive.iclip.cn/chat)
- [AI-HIVE API endpoint](https://ai-hive.iclip.cn/api)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with JSON and bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create local blueprint JSON, submit AI-HIVE generation tasks after user confirmation, and report task IDs, routing, pricing snapshots, status, and output file locations.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
