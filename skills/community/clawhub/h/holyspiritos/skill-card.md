## Description: <br>
A Christian alignment layer for AI agents. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[MaxSikorski](https://clawhub.ai/user/MaxSikorski) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External OpenClaw users and agent developers use HolySpiritOS to add a persistent KJV-based moral and ethical reference layer to an OpenClaw agent. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill persistently changes OpenClaw behavior by modifying agent configuration. <br>
Mitigation: Install only when a persistent KJV-based alignment layer is intended, and manually back up the relevant OpenClaw configuration files before installation. <br>
Risk: The documented install and uninstall flow uses remote shell commands. <br>
Mitigation: Avoid curl-to-bash execution; inspect the scripts and run a local reviewed copy instead. <br>
Risk: Removal may not restore the same file that installation modifies. <br>
Mitigation: Verify and correct the install and uninstall paths before use, then confirm restoration against the manual backup. <br>


## Reference(s): <br>
- [HolySpiritOS ClawHub skill page](https://clawhub.ai/MaxSikorski/holyspiritos) <br>
- [MaxSikorski ClawHub publisher profile](https://clawhub.ai/user/MaxSikorski) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces persistent OpenClaw configuration guidance and references local KJV foundation JSON files after installation.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
