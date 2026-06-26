## Description: <br>
Install and configure PeonPing with an opinionated Orc Peon default so completion alerts work with minimal setup. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sal-jim](https://clawhub.ai/user/sal-jim) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent users use this skill to install PeonPing, enable the Orc Peon sound pack, configure volume and notifications, and verify that local completion alerts are working. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can automatically install software on the user's machine. <br>
Mitigation: Confirm the user wants PeonPing installed before running install or setup commands, and prefer the Homebrew installation path. <br>
Risk: The fallback installer pipes an unpinned remote script into a shell. <br>
Mitigation: Do not use the curl-to-bash fallback unless the upstream installer has been reviewed or pinned and the user explicitly approves it. <br>
Risk: The skill changes local audio and notification settings. <br>
Mitigation: Verify the result with `peon preview` and `peon status`, and adjust volume or notifications only according to the user's preference. <br>


## Reference(s): <br>
- [PeonPing website](https://peonping.com) <br>
- [PeonPing GitHub repository](https://github.com/PeonPing/peon-ping) <br>
- [PeonPing upstream README](https://raw.githubusercontent.com/PeonPing/peon-ping/main/README.md) <br>
- [PeonPing upstream installer](https://raw.githubusercontent.com/PeonPing/peon-ping/main/install.sh) <br>
- [ClawHub skill page](https://clawhub.ai/sal-jim/peon-ping-openclaw) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline bash command blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose local installation and notification configuration commands for the user's approval.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
