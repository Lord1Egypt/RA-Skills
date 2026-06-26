## Description: <br>
Automates login to China's 12366 tax service platform by controlling Google Chrome, filling credentials, recognizing graphic CAPTCHA challenges, submitting the login form, and preserving browser session state. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[edwn](https://clawhub.ai/user/edwn) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to automate a controlled login flow for an account they are authorized to access on the 12366 tax service platform. It is useful when an agent needs to invoke a browser-based login process using a supplied login URL, username, password, and optional debugging or window-size parameters. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles sensitive account credentials and may expose passwords if they are passed through command histories, logs, or shared terminals. <br>
Mitigation: Use it only on a private machine for accounts you control, avoid putting real passwords in logged shell commands, and prefer secure secret handling where available. <br>
Risk: The skill preserves reusable browser session data in ./chrome_profile. <br>
Mitigation: Remove ./chrome_profile after use when persistent sessions are not needed, and restrict access to the machine and workspace where it runs. <br>
Risk: Automated CAPTCHA and login workflows may be restricted by the target service's terms or operational controls. <br>
Mitigation: Confirm that the tax service permits the intended automated login workflow before deployment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/edwn/gjsw) <br>
- [12366 tax service login](https://12366.chinatax.gov.cn/login) <br>
- [12366 user center login](https://12366.chinatax.gov.cn/usercenter/login/page) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and parameter guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3 and Google Chrome; uses GJSW_LOGIN_URL as the primary environment variable when a login URL is not passed explicitly.] <br>

## Skill Version(s): <br>
1.0.5 (source: server release evidence and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
