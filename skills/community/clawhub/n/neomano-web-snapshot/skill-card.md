## Description: <br>
Take a screenshot (PNG) of any website in a headless way (no GUI) to verify it's rendering/working. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[elandivar](https://clawhub.ai/user/elandivar) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to run a headless browser screenshot check for a website, uptime visual check, or page-rendering verification. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Setup downloads Playwright and Chromium locally. <br>
Mitigation: Run the bootstrap step only in an approved environment where local dependency and browser downloads are acceptable. <br>
Risk: The tool visits requested URLs from the user's machine. <br>
Mitigation: Avoid capturing sensitive internal sites unless that access and screenshot capture are intended. <br>
Risk: Screenshot files can contain sensitive page content. <br>
Mitigation: Write outputs only to local, non-sensitive paths and handle generated PNG files according to the page content sensitivity. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/elandivar/neomano-web-snapshot) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/elandivar) <br>


## Skill Output: <br>
**Output Type(s):** [Files, Shell commands, Configuration instructions] <br>
**Output Format:** [PNG screenshot file plus terminal path output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports output path, full-page capture, wait time, and timeout options.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
