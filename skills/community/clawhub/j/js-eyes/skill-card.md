## Description: <br>
Install, configure, verify, and troubleshoot JS Eyes browser automation for OpenClaw. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[imjszhang](https://clawhub.ai/user/imjszhang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to install or repair the JS Eyes OpenClaw browser automation stack, connect the browser extension, and verify local browser-control workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill enables browser automation that can interact with logged-in tabs and sensitive browser state. <br>
Mitigation: Install only when browser control is intended, keep the server bound to localhost, require the server token, and review consent and audit records. <br>
Risk: Raw JavaScript execution and externally mounted extension skills can increase execution and data-exposure risk. <br>
Mitigation: Keep allowRawEval=false unless needed, limit enabled extension skills and extraSkillDirs, and verify external skill directories where available. <br>
Risk: Automatic native host setup can make local browser integration changes during installation. <br>
Mitigation: Set nativeHost.autoInstall=false or nativeHost.warnOnly=true when operators need to inspect or approve local integration changes first. <br>


## Reference(s): <br>
- [JS Eyes ClawHub page](https://clawhub.ai/imjszhang/js-eyes) <br>
- [JS Eyes GitHub homepage](https://github.com/imjszhang/js-eyes) <br>
- [Security and Network Behavior](artifact/SECURITY.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, Code] <br>
**Output Format:** [Markdown with inline shell commands and JSON snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include local OpenClaw and JS Eyes configuration changes when setup or repair requires them.] <br>

## Skill Version(s): <br>
2.8.2 (source: server release evidence, SKILL.md frontmatter, package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
