## Description: <br>
Enables OpenClaw to use the Gemini web interface for browser-based conversations, login reuse, file and image uploads, drafting, summarization, research support, image generation, and local downloads. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[etherstrings](https://clawhub.ai/user/etherstrings) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill when they need OpenClaw to operate Gemini through a managed browser session rather than the Gemini API or CLI. It supports conversational tasks, file analysis, drafting, summarization, image generation, and downloading Gemini outputs to a stable local directory. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may operate a Gemini web session using login credentials or a TOTP seed when explicitly needed. <br>
Mitigation: Prefer an already authenticated managed OpenClaw browser profile, use Gemini-specific GEMINI_WEB_* variables, avoid command-line secrets when possible, and never echo passwords or TOTP seeds in logs or summaries. <br>
Risk: Google sign-in may present CAPTCHA, device confirmation, account recovery, or suspicious-login checks that are unsafe to automate. <br>
Mitigation: Stop automation and leave the browser ready for the user to complete the challenge manually. <br>
Risk: The TOTP JSON-file option could expose unrelated secrets if pointed at a broad secret store. <br>
Mitigation: Use a Gemini-specific JSON file and key, and do not point the option at unrelated credential stores. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/etherstrings/openclaw-gemini-web) <br>
- [Gemini web interface](https://gemini.google.com/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, files, guidance] <br>
**Output Format:** [Markdown status summaries with optional shell command snippets and downloaded files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Downloads default to ./output/gemini/YYYY-MM-DD/ unless the user provides another location.] <br>

## Skill Version(s): <br>
0.1.5 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
