## Description:

OpenClaw Gemini Web lets an agent operate Gemini in a managed browser to reuse or complete login, continue or start Gemini threads, upload files for analysis, ask questions, draft or summarize content, generate images, and save downloads.

This skill is ready for commercial/non-commercial use.

## Publisher:

[etherstrings](https://clawhub.ai/user/etherstrings)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill when they want an agent to work through the Gemini web interface instead of the Gemini API or CLI. It supports browser-based Gemini conversations, file and image uploads, drafting, summarization, research assistance, image generation, and managed download handling.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may use existing Google login credentials and TOTP secrets during managed browser automation.

Mitigation: Keep MFA secrets in controlled environment variables or local secret files, avoid pasting them into chat, and do not echo credentials or TOTP secrets in logs or summaries.

Risk: Files uploaded through the skill are sent to Google's Gemini web service.

Mitigation: Review files before upload and confirm that the user intends those materials to be processed by Gemini.

Risk: Google login flows can present CAPTCHA, device review, phone verification, account recovery, lockout, or policy pages that should not be automated.

Mitigation: Stop automation when those pages appear or when the login flow becomes unclear, leaving the browser ready for user takeover.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/etherstrings/skills/openclaw-gemini-web)
- [Gemini web app](https://gemini.google.com/)
- [Project homepage](https://github.com/Etherstrings/openclaw-gemini-web-skill)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands, browser status notes, file paths, and optional downloaded files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Downloads are saved to a stable local directory when Gemini returns files; otherwise none.]

## Skill Version(s):

0.1.5 (source: server release evidence; artifact frontmatter lists 0.1.4)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
