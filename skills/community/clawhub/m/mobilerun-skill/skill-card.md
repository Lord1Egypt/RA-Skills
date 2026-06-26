## Description: <br>
Mobilerun lets agents control real Android phones through the Mobilerun API, including tapping, swiping, typing, screenshots, UI tree inspection, app management, and AI agent tasks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Mariozada](https://clawhub.ai/user/Mariozada) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use Mobilerun to automate or remotely operate Android devices, either by issuing direct screen-control API calls or delegating multi-step app workflows to the Droidrun Agent. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can observe and control a real Android device, including screenshots, UI tree access, taps, typing, app management, and autonomous tasks. <br>
Mitigation: Use it only on an intended device, prefer a dedicated or low-risk phone, and require explicit confirmation before sensitive app actions, purchases, account changes, app installs or uninstalls, or feedback submission. <br>
Risk: Screenshots, accessibility trees, and device state can contain sensitive personal data. <br>
Mitigation: Share device observations only with the user, avoid logging or revealing sensitive screen/UI data, and never expose the Mobilerun API key. <br>
Risk: Personal-device setup requires sideloading the Droidrun Portal APK and enabling Android Accessibility access. <br>
Mitigation: Verify the APK source before sideloading, disable unknown-sources access after installation, and turn off Accessibility access when Mobilerun is not needed. <br>


## Reference(s): <br>
- [Mobilerun Skill Page](https://clawhub.ai/Mariozada/mobilerun-skill) <br>
- [Mariozada Publisher Profile](https://clawhub.ai/user/Mariozada) <br>
- [Mobilerun Platform API](api.md) <br>
- [Phone Control API Reference](phone-api.md) <br>
- [Mobilerun Setup](setup.md) <br>
- [Mobilerun Plans & Subscriptions](subscription.md) <br>
- [Droidrun Portal](https://droidrun.ai/portal) <br>
- [Droidrun Portal Source](https://github.com/droidrun/droidrun-portal) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, API calls, Guidance] <br>
**Output Format:** [Markdown with inline HTTP and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include Mobilerun API requests, device status summaries, setup guidance, and task progress updates; must not expose API keys or sensitive screenshot/UI-tree data.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
