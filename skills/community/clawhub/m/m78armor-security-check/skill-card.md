## Description: <br>
Read-only local OpenClaw security configuration check and hardening assessment. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[move78ai](https://clawhub.ai/user/move78ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
OpenClaw operators, developers, and administrators use this skill after install or upgrade to review the local OpenClaw configuration for baseline gaps, risky exposure, weak defaults, and drift indicators. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The checker reads local OpenClaw configuration files and may print configuration-derived findings, including masked secret indicators. <br>
Mitigation: Run it only against configuration files intended for audit and treat terminal or CI logs as operationally sensitive. <br>
Risk: Automated runs may show an upgrade prompt or fail a pipeline when high-risk findings are detected. <br>
Mitigation: Use --quiet for CI or pipeline runs and wire the documented exit code behavior into expected automation policy. <br>


## Reference(s): <br>
- [M78Armor Homepage](https://www.m78armor.com) <br>
- [ClawHub Listing Copy](references/clawhub-listing-copy.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration guidance] <br>
**Output Format:** [Markdown and terminal text; JSON when machine-readable output is requested] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Read-only local execution with English or Chinese output and exit code 1 when high-risk findings are detected.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and bundled script VERSION) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
