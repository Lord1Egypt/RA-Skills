## Description: <br>
Password Generator helps an agent generate passwords, passphrases, PINs, API-style tokens, usernames, and password-strength feedback while keeping settings local and not storing actual passwords. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mkpareek0315](https://clawhub.ai/user/mkpareek0315) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill as a local prompt helper for password ideas, passphrases, PINs, API-style token examples, usernames, password-strength feedback, and security tips. It is not a replacement for a trusted password manager or operating-system-backed cryptographic generator for important account passwords, API keys, or production tokens. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Chat-generated passwords, tokens, and strength estimates may not provide the assurance of a dedicated password manager or cryptographic key generator. <br>
Mitigation: Use this skill for password ideas and feedback; use a trusted password manager or OS-backed generator for important account passwords, API keys, and production tokens. <br>
Risk: Strength-checking real current passwords in chat can expose sensitive secrets to the assistant context. <br>
Mitigation: Do not paste real current passwords into chat; test representative examples or use an offline password-audit tool for live credentials. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/mkpareek0315/password-gen-pro) <br>
- [Publisher profile](https://clawhub.ai/user/mkpareek0315) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown responses with generated secret examples, strength analysis, security guidance, and optional local setup commands or settings JSON.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May read and write settings and usage counts under ~/.openclaw/password-generator; does not store generated passwords.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
