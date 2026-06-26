## Description: <br>
Patchright-based browser automation with bot detection bypass for interacting with local web applications, testing localhost or dev servers, taking screenshots, and performing UI interactions on private networks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[smallnest](https://clawhub.ai/user/smallnest) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and QA engineers use this skill to automate browser checks against local applications, dev servers, and private-network web apps. It supports frontend debugging, screenshot capture, UI interaction, and pre-deployment verification workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can automate broad browser actions beyond local testing. <br>
Mitigation: Use it only on sites and applications you own or are authorized to test, and keep workflows scoped to localhost, dev servers, or private networks. <br>
Risk: Raw page scripting can execute arbitrary JavaScript in the active browser page. <br>
Mitigation: Review scripts before execution and avoid running untrusted JavaScript or payloads copied from unknown pages. <br>
Risk: Screenshots and extracted page data may capture sensitive information. <br>
Mitigation: Avoid real credentials and production accounts, and store generated screenshots or result files in controlled locations. <br>
Risk: The background server keeps a browser session available after commands complete. <br>
Mitigation: Check server status during use and stop the server after each session. <br>
Risk: The Patchright dependency changes the browser automation trust boundary. <br>
Mitigation: Pin, review, and update the Patchright dependency according to your organization's dependency review process. <br>


## Reference(s): <br>
- [Patchright Skill Reference](reference.md) <br>
- [Patchright Scripts](scripts/README.md) <br>
- [ClawHub Release Page](https://clawhub.ai/smallnest/patchright-skill) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, JSON, Files, Guidance] <br>
**Output Format:** [Markdown instructions with shell commands and JSON command payloads; scripts may create screenshots or search-result JSON files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Browser sessions may persist through the local server until explicitly stopped.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
