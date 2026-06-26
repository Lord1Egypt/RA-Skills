## Description: <br>
GoGlobal guides users through deploying a personal VPS proxy by generating KiwiVM API links, installing 3x-ui, configuring a VLESS+Reality node, and walking through client setup. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[scientificinternet](https://clawhub.ai/user/scientificinternet) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users can use this skill to have an assistant walk them through buying or using a BandwagonHost VPS, deploying 3x-ui, creating a VLESS+Reality node, installing a client, and validating access to international AI services. <br>

### Deployment Geography for Use: <br>
Global, subject to local laws, network rules, and service terms. <br>

## Known Risks and Mitigations: <br>
Risk: The workflow handles powerful VPS control keys and can place those keys inside generated browser links. <br>
Mitigation: Treat generated API links as secrets, avoid sharing screenshots or browser history, and regenerate the KiwiVM API key immediately after setup. <br>
Risk: The workflow can stop or reinstall a VPS, which may erase data or interrupt services. <br>
Mitigation: Review destructive actions before opening control links, confirm reinstall only for the intended server, and back up important data first. <br>
Risk: The workflow installs and configures third-party proxy software and initially exposes the management panel over HTTP. <br>
Mitigation: Review the 3x-ui install source, change the panel password after installation, and enable HTTPS when the setup is complete. <br>
Risk: The security scan describes the skill as a suspicious proxy-deployment workflow with stealth-oriented configuration. <br>
Mitigation: Use it only for a self-controlled VPS and lawful access needs, and confirm compliance with local laws and service terms before deployment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/scientificinternet/goglobal) <br>
- [Publisher profile](https://clawhub.ai/user/scientificinternet) <br>
- [3x-ui upstream project](https://github.com/MHSanaei/3x-ui) <br>
- [BandwagonHost entry point](https://bwh8l.net) <br>
- [Client download guide](https://help.bwh8l.net/index.html) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Chinese Markdown instructions with browser links, status checks, and setup guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generates step-by-step instructions and KiwiVM API links that may embed user-provided VPS control keys; credentials are intended to be redacted from summaries and regenerated after setup.] <br>

## Skill Version(s): <br>
3.3.6 (source: server release evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
