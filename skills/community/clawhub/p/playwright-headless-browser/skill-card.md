## Description: <br>
Sets up Playwright-managed Chromium for Clawdbot headless browser automation in WSL/Linux environments, including browser installation, system dependencies, and Clawdbot configuration. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[maverick-software](https://clawhub.ai/user/maverick-software) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill to configure Clawdbot browser tooling for headless Chromium automation on WSL/Linux systems. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Setup may invoke package managers with sudo and download Playwright Chromium. <br>
Mitigation: Review the scripts before running them and execute setup only in an environment where system package changes and browser downloads are acceptable. <br>
Risk: The configured browser uses no-sandbox mode for WSL or container compatibility. <br>
Mitigation: Use no-sandbox only where required by the runtime environment and avoid using that browser configuration for sensitive browsing. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/maverick-software/playwright-headless-browser) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown with inline bash code blocks and script-driven setup instructions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May install Playwright Chromium, install system libraries, and update Clawdbot browser configuration.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
