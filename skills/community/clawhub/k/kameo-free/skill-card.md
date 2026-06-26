## Description: <br>
Generate expressive talking-head videos from static images using Kameo AI, with optional prompt enhancement for facial expression, lip-sync, and motion. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[veya2ztn](https://clawhub.ai/user/veya2ztn) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External creators, developers, and content teams use this skill to turn a portrait or avatar image into a short talking-head video for demos, social media, education, or multilingual presentation content. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends selected images and dialogue to Kameo, and enhanced generation can send images and text to Google Gemini. <br>
Mitigation: Use only images and dialogue approved for those services, and avoid sensitive personal, confidential, or regulated content. <br>
Risk: The artifact includes example API keys and stores credentials in ~/.config/kameo/credentials.json. <br>
Mitigation: Use user-owned API keys, do not rely on bundled examples, keep the credentials file permission-restricted, and delete or rotate stored credentials when no longer needed. <br>
Risk: Security guidance flags unsafe input interpolation in enhanced prompt scripts. <br>
Mitigation: Avoid generate_enhanced.sh and enhance_prompt.sh until the interpolation issue is fixed, or review and harden them before use. <br>
Risk: register.sh accepts account passwords and writes local credentials. <br>
Mitigation: Prefer manual registration or token creation, avoid passing real passwords through shell history, and rotate credentials after testing. <br>


## Reference(s): <br>
- [Kameo](https://kameo.chat) <br>
- [Kameo Public API](https://api.kameo.chat/api/public) <br>
- [Gemini API endpoint used for prompt enhancement](https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash-exp:generateContent) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, API calls, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON API payloads] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May return Kameo CDN video URLs; generated media depends on external API credits, availability, and user-provided images and prompts.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
