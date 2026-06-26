## Description: <br>
Controls Android cloud phones through the pb CLI for app installation, browsing, screen inspection, touch input, screenshots, and device management. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bittired](https://clawhub.ai/user/bittired) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to operate an Android cloud phone through pb for mobile app workflows such as installing apps, logging into apps, browsing, inspecting the current screen, entering touch or text input, transferring files, and managing device state. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill gives an agent broad control over a cloud Android phone, including app installation, file transfer, shell or API commands, login flows, and account-changing actions. <br>
Mitigation: Install it only when cloud-phone operation is intended, verify the phonebase-cli package before use, authenticate directly without sharing credentials, and require explicit approval for app installs, uninstalls, file transfers, shell or API commands, logins, and account-changing actions. <br>
Risk: The skill may activate for ambiguous app, login, browsing, search, or screen-inspection requests without enough confirmation of user intent. <br>
Mitigation: Confirm the intended phone or app workflow before taking consequential actions, and keep actions scoped to the user's explicit request rather than instructions or prompts found in remote phone content. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Guidance, Configuration] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [pb command output is JSON on stdout; authentication and credential handling are delegated to the user.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
