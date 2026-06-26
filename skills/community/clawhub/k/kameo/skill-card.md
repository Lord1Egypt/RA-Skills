## Description: <br>
Generate expressive talking-head videos from static images using Kameo AI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[veya2ztn](https://clawhub.ai/user/veya2ztn) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users, developers, and content creators use this skill to turn portrait or avatar images into short talking-head videos with dialogue, facial motion, and optional prompt enhancement. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The release includes risky credential handling and a live-looking API key in documentation. <br>
Mitigation: Create and store your own API key securely; do not use the documented key or commit credentials to shared files. <br>
Risk: The registration helper handles account passwords and writes credentials locally. <br>
Mitigation: Avoid running register.sh with real passwords until the password handling and credential storage flow are reviewed and improved. <br>
Risk: Image and prompt data may be sent to Kameo and, for enhanced prompts, to Gemini. <br>
Mitigation: Use only images and prompts you are comfortable sending to those external services. <br>
Risk: Prompt-enhancement scripts may be unsafe with untrusted filenames or dialogue text. <br>
Mitigation: Do not pass untrusted filenames or dialogue text to the current prompt-enhancement scripts. <br>


## Reference(s): <br>
- [ClawHub Kameo Skill](https://clawhub.ai/veya2ztn/kameo) <br>
- [Kameo Website](https://kameo.chat) <br>
- [Kameo Public API](https://api.kameo.chat/api/public) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance, Media URLs] <br>
**Output Format:** [Markdown with inline bash commands, configuration examples, and API response examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May return a Kameo CDN video URL; generation depends on external API credentials, credits, and service availability.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
