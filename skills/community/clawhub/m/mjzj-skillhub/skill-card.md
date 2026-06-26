## Description: <br>
Helps agents search and filter MJZJ SkillHub skills, reuse install guidance, and submit skill publishing applications through the MJZJ APIs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mjzj-tec](https://clawhub.ai/user/mjzj-tec) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and cross-border e-commerce skill publishers use this skill to browse MJZJ SkillHub by label, keyword, price type, popularity, and recency, then follow install guidance or submit a skill for review. Authenticated workflows use MJZJ_API_KEY for publishing applications and temporary cover image uploads. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Authenticated publishing and cover upload workflows require MJZJ_API_KEY. <br>
Mitigation: Configure the key only for intended MJZJ SkillHub workflows, avoid exposing it in prompts or logs, and update it when authorization fails. <br>
Risk: Custom cover uploads send a user-selected file to MJZJ temporary upload storage. <br>
Mitigation: Upload only the intended cover image, verify content type and size before upload, and avoid submitting sensitive files. <br>
Risk: Skill submissions and returned install guidance can affect marketplace content or user setup. <br>
Mitigation: Review labels, price type, source URL, cover path, submission details, and returned install guidance before submitting or following it. <br>


## Reference(s): <br>
- [MJZJ SkillHub](https://skillhub.mjzj.com) <br>
- [MJZJ API key settings](https://mjzj.com/user/agentapikey) <br>
- [Skill label groups API](https://data.mjzj.com/api/skill/groupLabels) <br>
- [Skill search API](https://data.mjzj.com/api/skill/query) <br>
- [Temporary cover upload API](https://data.mjzj.com/api/common/applyUploadTempFile) <br>
- [Skill publishing application API](https://data.mjzj.com/api/skillManage/applyNew) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, API calls, Configuration] <br>
**Output Format:** [Markdown guidance with API endpoint references and curl examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses MJZJ_API_KEY only for authenticated publishing and cover upload workflows.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
