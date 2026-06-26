## Description: <br>
Automates Kuaipu system login, CAPTCHA recognition, browser actions, and approval workflow lookup. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chldong](https://clawhub.ai/user/chldong) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees or authorized operators use this skill to automate login to a Kuaipu business system and query pending approval reminders after configuring approved credentials. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles Kuaipu business-system credentials. <br>
Mitigation: Use only approved accounts, protect the .env file, and prefer a low-privilege account where possible. <br>
Risk: The skill saves authenticated page data, screenshots, CAPTCHA images, and cookies locally. <br>
Mitigation: Run on a trusted machine and delete the tmp directory and generated artifacts after each run. <br>
Risk: The wrapper can install Python dependencies at runtime. <br>
Mitigation: Use a dedicated virtual environment with pinned dependencies and install only when the publisher is trusted. <br>
Risk: Automated login, CAPTCHA solving, and approval lookup may be inappropriate without authorization. <br>
Mitigation: Run the skill only where Kuaipu automation and CAPTCHA handling are explicitly permitted. <br>


## Reference(s): <br>
- [Kuaipu Skill on ClawHub](https://clawhub.ai/chldong/kuaipu-skill) <br>
- [chldong publisher profile](https://clawhub.ai/user/chldong) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, files] <br>
**Output Format:** [Plain text console output plus local HTML, screenshot, CAPTCHA, and cookie artifacts.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires configured Kuaipu URL, username, and password values; saves runtime artifacts under tmp/.] <br>

## Skill Version(s): <br>
0.1.0 (source: ClawHub release metadata; artifact frontmatter says 0.2) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
