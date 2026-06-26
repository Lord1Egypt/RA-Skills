## Description: <br>
Enables secure remote access to a browser on your server for manual tasks like logins, 2FA, and captchas via a protected URL. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[felipegoulu](https://clawhub.ai/user/felipegoulu) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and automation agents use Passo when a workflow needs trusted human help inside a server-hosted browser, such as completing logins, 2FA, captchas, or other manual browser actions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill asks users to run an unpinned remote installer. <br>
Mitigation: Review the installer before running it and install only on an isolated disposable server. <br>
Risk: The remote browser may be used for sensitive login, 2FA, or captcha sessions. <br>
Mitigation: Verify the protected email, avoid highly sensitive accounts unless the Passo security model is trusted, and clear sessions after use. <br>
Risk: A browser tunnel can remain available after the assisted task is complete. <br>
Mitigation: Stop the tunnel when finished. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/felipegoulu/passo) <br>
- [Passo Website](https://getpasso.app) <br>
- [Passo Docs](https://getpasso.app/docs) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline bash code blocks and templated access details] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes browser tunnel commands and placeholders for access URL and protected email.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
