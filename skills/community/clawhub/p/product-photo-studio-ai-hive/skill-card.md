## Description:

Helps ecommerce merchants, photography teams, designers, and multi-SKU operators turn product-image requests into reviewable Chinese workflows, prompts, runnable AI-HIVE commands, and delivery checklists for white-background, scene, selling-point, detail, and platform-sized product images.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

External ecommerce and marketing users use this skill to plan and execute product-photo production with authenticity checks, platform-specific variants, and AI-HIVE image-generation commands. It is intended for authorized product assets and reviewable commercial content workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: API keys and generated downloads could be exposed or mishandled if users redirect the client to an untrusted endpoint or unsafe output location.

Mitigation: Use the default AI-HIVE endpoint, avoid base URL overrides unless the destination is fully trusted, use a low-privilege revocable API key, and download outputs into a disposable directory.

Risk: Product imagery workflows can create misleading claims, unauthorized reference use, or content that appears to endorse a product without evidence.

Mitigation: Confirm asset rights, product facts, platform constraints, and review approval before generation; avoid fabricated certifications, effects, testimonials, or official brand endorsement claims.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wubin1836/skills/product-photo-studio-ai-hive)
- [AI-HIVE product entry](https://ai-hive.iclip.cn/chat)
- [AI-HIVE API base endpoint](https://ai-hive.iclip.cn/api)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration guidance, API calls, Files]

**Output Format:** [Markdown guidance with inline shell commands, JSON task records, and generated local files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create blueprint JSON files and download generated image or video outputs after user confirmation of potentially billable AI-HIVE tasks.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
