## Description: <br>
Generates Gemini images through OpenRouter for OpenClaw agents on macOS and sends the generated image through the configured Telegram bot. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[eardori](https://clawhub.ai/user/eardori) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
OpenClaw users and developers use this skill to turn a prompt into an AI-generated image and deliver the result to a configured Telegram destination. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts and generated media are sent to external OpenRouter/Gemini and Telegram services. <br>
Mitigation: Use dedicated low-privilege API and bot tokens, avoid sensitive prompts, and confirm the configured Telegram destination before use. <br>
Risk: The skill downloads image URLs returned by the image-generation API. <br>
Mitigation: Review or patch the URL download handling before deployment and run the skill with restricted network and file access. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/eardori/hana-image-gen-macos) <br>
- [OpenRouter API endpoint](https://openrouter.ai/api/v1/chat/completions) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration] <br>
**Output Format:** [Markdown instructions with shell commands and JSON image path output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires OPENROUTER_API_KEY and TELEGRAM_BOT_TOKEN; sends prompts and generated media to external services.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
