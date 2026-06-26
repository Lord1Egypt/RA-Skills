## Description: <br>
Automate Pinterest pin publishing via browser automation with Playwright, including jp.pinterest.com support, single pins, carousels, batch publishing, and reusable cookie sessions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[luoboask](https://clawhub.ai/user/luoboask) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to automate Pinterest content publishing through a browser session, including login reuse, image upload, pin metadata entry, and batch posting workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Reusable Pinterest session cookies can allow continued account access if the local cookie file is exposed. <br>
Mitigation: Run in an isolated environment or dedicated account, restrict access to ~/.config/pinterest/cookies.json, and delete or rotate cookies after use. <br>
Risk: Some scripts can publish live Pinterest posts automatically using configured or hardcoded pin data. <br>
Mitigation: Inspect and edit pin lists before execution, start with scripts that pause for manual review, and verify the target account and board before publishing. <br>
Risk: Anti-detection and proxy guidance may conflict with platform expectations or account safety practices. <br>
Mitigation: Avoid anti-detection and proxy tactics; follow Pinterest account policies and rate limits. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/luoboask/pinterest-browser-publisher) <br>
- [ClawHub listed homepage](https://clawhub.ai/skills/pinterest-browser-publisher) <br>
- [Pinterest browser publishing package documentation](artifact/PACKAGE.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, Code] <br>
**Output Format:** [Markdown instructions with inline shell commands, JavaScript examples, and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces browser automation workflows that can publish live Pinterest content and write session cookies and screenshots on the local machine.] <br>

## Skill Version(s): <br>
1.0.2 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
