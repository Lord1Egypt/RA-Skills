## Description: <br>
Document extraction via SkillBoss API Hub converts PDFs and images to markdown, JSON, or CSV with confidence scoring. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[marjoriebroad](https://clawhub.ai/user/marjoriebroad) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operations teams use this skill to call SkillBoss API Hub for OCR, document conversion, invoice and receipt field extraction, and table extraction from PDFs and images. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Selected documents or document URLs are sent to an external SkillBoss API Hub service for processing, which can create privacy and retention concerns for sensitive data. <br>
Mitigation: Review the provider's privacy and retention terms before use, test with non-sensitive samples first, and prefer redacted files or short-lived scoped URLs when possible. <br>
Risk: The skill requires a sensitive API credential. <br>
Mitigation: Store SKILLBOSS_API_KEY in an environment variable or secret store, avoid committing credentials, rotate keys regularly, and monitor usage. <br>


## Reference(s): <br>
- [SkillBoss API Hub](https://api.heybossai.com) <br>
- [SkillBoss API Docs](https://api.heybossai.com/v1/pilot) <br>
- [ClawHub skill page](https://clawhub.ai/marjoriebroad/mar-docstrange) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, markdown, JSON, CSV] <br>
**Output Format:** [Markdown guidance with curl examples and structured API response formats] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires SKILLBOSS_API_KEY and sends selected documents or document URLs to SkillBoss API Hub.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
