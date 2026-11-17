## Description:

Automates login to China's State Taxation Administration 12366 taxpayer service platform using Chrome browser control, form detection, CAPTCHA OCR, retry handling, and persistent browser sessions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[edwn](https://clawhub.ai/user/edwn)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to run local browser automation for 12366 tax-platform login flows when they provide a username, password, and login URL or configure GJSW_LOGIN_URL.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles tax-platform usernames and passwords during local browser automation.

Mitigation: Use it only in a trusted local account or virtual environment and avoid placing real passwords in shell history.

Risk: A user-supplied login URL could direct credentials to the wrong destination.

Mitigation: Use a carefully verified official HTTPS 12366 login URL before running the automation.

Risk: Persistent browser state can retain cookies and login sessions after the run completes.

Mitigation: Remove ./chrome_profile after use if retained cookies or login state are not desired.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/edwn/skills/gjsw)
- [Publisher profile](https://clawhub.ai/user/edwn)
- [12366 login URL](https://12366.chinatax.gov.cn/login)
- [12366 user center login page](https://12366.chinatax.gov.cn/usercenter/login/page)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown with inline bash commands and command-line arguments]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires local Python dependencies, Google Chrome, credentials supplied as command-line arguments, and a login URL supplied with --url or GJSW_LOGIN_URL.]

## Skill Version(s):

1.0.5 (source: server release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
