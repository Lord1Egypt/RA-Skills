## Description: <br>
Mobilerun helps agents control connected Android devices through the Mobilerun API for screenshots, UI-state inspection, taps, swipes, typing, app management, and optional Droidrun task execution. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[johnmalek312](https://clawhub.ai/user/johnmalek312) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and users with a Mobilerun API key use this skill to automate or remotely operate Android devices, including observing screens, interacting with mobile apps, provisioning supported devices, and troubleshooting setup or billing issues. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can give an agent broad visibility into and control over a connected Android device, including screenshots, UI accessibility data, taps, typing, and app actions. <br>
Mitigation: Use a test phone or cloud device for risky workflows, avoid sensitive apps and screens unless necessary, and review device actions before allowing high-impact changes. <br>
Risk: Sensitive actions such as purchases, messages, account changes, app installs or uninstalls, webhook setup, and feedback submission may not be guarded strongly enough. <br>
Mitigation: Require explicit user confirmation before those actions and revoke the API key, disable Accessibility, or log out of Portal when finished. <br>
Risk: Screenshots and UI trees can expose private personal data from the device. <br>
Mitigation: Share device observations only with the user, do not expose the API key, and minimize collection or display of sensitive screen contents. <br>


## Reference(s): <br>
- [Mobilerun on ClawHub](https://clawhub.ai/johnmalek312/mobile-run) <br>
- [Mobilerun Platform API](api.md) <br>
- [Phone Control API Reference](phone-api.md) <br>
- [Mobilerun Setup](setup.md) <br>
- [Mobilerun Subscription](subscription.md) <br>
- [Droidrun Portal Source](https://github.com/droidrun/droidrun-portal) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, Guidance, Configuration, Text] <br>
**Output Format:** [Markdown with HTTP request examples and JSON payloads] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses MOBILERUN_API_KEY and may return device status, screenshots, UI accessibility data, task identifiers, and setup guidance.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
