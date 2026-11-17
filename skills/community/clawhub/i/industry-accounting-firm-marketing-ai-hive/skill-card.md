## Description:

This skill helps accounting-firm marketers create Chinese image, short-video, and content marketing plans, prompts, AI-HIVE generation tasks, and review checkpoints for approved channels.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

External users and marketing operators use this skill to plan and produce accounting-firm content that builds professional trust, supports lead generation, and prepares reviewable image, video, prompt, and campaign materials. The workflow emphasizes verified business facts, authorized materials, channel-specific formatting, and professional review before publishing or paid generation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can store AI-HIVE API keys locally and may send them to an arbitrary configured API endpoint.

Mitigation: Review before installation, use a dedicated low-privilege AI-HIVE API key, prefer AI_HIVE_API_KEY over local initialization, and do not set --base-url or AI_HIVE_BASE_URL unless the destination is trusted.

Risk: Generated assets may be downloaded or retained in a default local output directory.

Mitigation: Use --no-download or a controlled output directory when generated assets should not persist in Downloads.

Risk: Client, brand, or confidential reference materials may be uploaded during image or video generation.

Mitigation: Upload only materials the user is authorized to use and avoid client or confidential materials unless authorization is confirmed.

Risk: Marketing outputs could contain unverified accounting-service claims, client examples, qualifications, tax-savings claims, or professional conclusions.

Mitigation: Require human review by the appropriate professional, mark uncertain facts as pending verification, avoid fabricated cases or credentials, and do not use generated content as a substitute for legal, financial, contractual, or safety conclusions.

## Reference(s):

- [会计事务所图片视频内容营销行业手册](references/industry-playbook.md)
- [ClawHub skill page](https://clawhub.ai/wubin1836/skills/industry-accounting-firm-marketing-ai-hive)
- [AI-HIVE](https://ai-hive.iclip.cn/chat)
- [AI-HIVE API endpoint](https://ai-hive.iclip.cn/api)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration]

**Output Format:** [Markdown with structured plans, prompts, command examples, JSON task records, and review checklists]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include AI-HIVE task identifiers, model and price snapshots, content review gates, and deterministic video-editing command output.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
