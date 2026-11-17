## Description:

This skill helps packaging design, e-commerce operations, brand review, and AI image teams compare packaging references with candidate media to identify logo, text, layout, barcode-area, net-content, and claim discrepancies, and prepare confirmed AI-HIVE generation or editing commands when needed.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

External brand, packaging, e-commerce, and AI content teams use this skill to produce packaging quality-check workflows, discrepancy reports, evidence notes, repair guidance, and AI-HIVE command plans for authorized product media.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release is flagged suspicious because it presents as a packaging, logo, and text checker while shipping broad AI-HIVE generation, upload, download, and video-editing tools with weak API-key endpoint scoping.

Mitigation: Install only when those AI-HIVE media capabilities are intended; keep the base URL on the official AI-HIVE endpoint and review commands before execution.

Risk: AI-HIVE calls can upload user media and may trigger billable image or video generation.

Mitigation: Use a low-privilege AI-HIVE key, upload only media you are authorized to send, confirm final parameters and routing before generation, and start batch work with small samples.

Risk: Model OCR and generated-media checks can miss packaging, legal, barcode, ingredient, or production-detail errors.

Mitigation: Mark uncertain findings as pending verification and require human or professional review for regulated product, brand, and legal claims.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wubin1836/skills/packaging-logo-text-check-ai-hive)
- [AI-HIVE chat entry](https://ai-hive.iclip.cn/chat)
- [AI-HIVE API endpoint](https://ai-hive.iclip.cn/api)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with structured sections, inline shell commands, and optional JSON task records]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create blueprint JSON, submit AI-HIVE image or video tasks, upload authorized media, poll task status, and download generated assets after user confirmation.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
