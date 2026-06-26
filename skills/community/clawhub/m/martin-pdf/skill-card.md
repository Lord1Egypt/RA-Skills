## Description: <br>
PDF supports PDF document workflows such as reading, extracting text or tables, merging, splitting, rotating, watermarking, form filling, encryption, image extraction, and OCR, while the packaged release also includes broader database, scraping, media-generation, search, summarization, translation, notification, reminder, and voice capabilities. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kirkraman](https://clawhub.ai/user/kirkraman) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Designers, brand teams, ecommerce operators, and agents use this skill for PDF handling and related content workflows. Operators should evaluate it as a broad multi-tool bundle rather than a narrow PDF-only utility. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The release is labeled as a PDF skill but includes broad database, scraping, media generation, notification, reminder, and Discord voice capabilities. <br>
Mitigation: Install only when a broad multi-tool bundle is intended, and review enabled components before use. <br>
Risk: Several bundled components require or can use sensitive credentials such as Supabase service-role keys, Discord bot tokens, and SkillBoss/API keys. <br>
Mitigation: Provide only the credentials needed for the selected component, scope them narrowly, and avoid exposing service-role or bot tokens to workflows that do not need them. <br>
Risk: Database, ComfyUI setup, downloader, scraping, and Discord voice components can create local or external data flows beyond PDF handling. <br>
Mitigation: Run those components only after confirming the requested task, local environment, and external data handling are appropriate. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/kirkraman/martin-pdf) <br>
- [Publisher profile](https://clawhub.ai/user/kirkraman) <br>
- [Skill homepage](https://www.skillboss.co/skills/pdf) <br>
- [ComfyUI repository](https://github.com/comfyanonymous/ComfyUI.git) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files] <br>
**Output Format:** [Markdown guidance with inline code, shell commands, JSON snippets, and generated file references] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Some bundled components can call external APIs, run local scripts, or produce media files when explicitly invoked.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
