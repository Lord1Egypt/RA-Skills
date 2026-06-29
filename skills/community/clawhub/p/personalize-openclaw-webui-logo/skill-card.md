## Description: <br>
Personalizes the OpenClaw WebUI favicon by applying bundled logo sets to the control UI assets and optionally installing a startup hook that restores the selected logo after OpenClaw upgrades. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[woohahahaaa](https://clawhub.ai/user/woohahahaaa) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to switch the OpenClaw control-panel browser-tab logo, restore the default logo, update bundled logo sets, or enable an optional guard hook that re-applies the chosen favicon after upgrades. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can overwrite OpenClaw favicon files in the detected control-ui dist directory. <br>
Mitigation: Use it only when intentional favicon customization is desired, and review the target OpenClaw UI directory before applying a logo. <br>
Risk: The optional auto-restore hook runs on OpenClaw startup and can re-apply the last selected favicon after upgrades. <br>
Mitigation: Install the hook only if persistent logo restoration is wanted; otherwise leave it uninstalled and use the one-time apply workflow. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/woohahahaaa/skills/personalize-openclaw-webui-logo) <br>
- [OpenClaw project homepage](https://github.com/openclaw/openclaw) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands and configuration steps] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write favicon assets to the detected OpenClaw control-ui dist directory and may install or remove an optional OpenClaw startup hook when the user chooses that workflow.] <br>

## Skill Version(s): <br>
2.4.2 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
