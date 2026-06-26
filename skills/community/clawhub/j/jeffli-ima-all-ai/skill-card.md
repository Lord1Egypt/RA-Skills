## Description: <br>
Ima All Ai provides a unified agent workflow for creating AI images, videos, music, and text-to-speech using KIE and IMA API credentials. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jeffli2002](https://clawhub.ai/user/jeffli2002) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and creative operators use this skill to route prompts, model choices, and optional local media through image, video, music, and speech generation workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts, selected local media, and API credentials may be sent to third-party generation services. <br>
Mitigation: Use scoped or test IMA and KIE keys, avoid sensitive files and prompts, and rotate credentials after evaluation. <br>
Risk: Local generation logs may retain prompts, paths, or operational details. <br>
Mitigation: Review and delete ~/.openclaw/logs/ima_skills/ when local traces should not remain on disk. <br>
Risk: Image-provider, credential, and upload behavior are inconsistently documented in the release evidence. <br>
Mitigation: Inspect the artifact source and security disclosure before use, especially for image tasks that upload local media. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jeffli2002/jeffli-ima-all-ai) <br>
- [IMA Studio](https://imastudio.com) <br>
- [IMA API key page](https://www.imaclaw.ai/imaclaw/apikey) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, JSON, configuration] <br>
**Output Format:** [Markdown guidance with shell commands and JSON result objects containing generated media URLs.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce image, video, music, or speech URLs after calling third-party generation services.] <br>

## Skill Version(s): <br>
1.4.0 (source: SKILL.md frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
