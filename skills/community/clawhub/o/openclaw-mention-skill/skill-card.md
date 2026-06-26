## Description: <br>
Model-agnostic WhatsApp @mention skill for OpenClaw that converts @Name, @Phone, and @LID mentions into clickable WhatsApp mentions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[junwei1213](https://clawhub.ai/user/junwei1213) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to make OpenClaw WhatsApp bots produce clickable group mentions regardless of how the underlying AI model formats @mentions. It patches OpenClaw message handling and maintains local WhatsApp LID mappings used to resolve names, phone numbers, and LIDs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The installer modifies OpenClaw runtime files and restarts the service. <br>
Mitigation: Review install.sh before running it, install only on an OpenClaw system you control, and rely on the generated backups or uninstall.sh to restore patched files if needed. <br>
Risk: The skill stores local WhatsApp identity mappings in LID_CACHE.json and installs mention guidance into OpenClaw memory. <br>
Mitigation: Audit the local mapping and memory files periodically, and remove them manually after uninstall if the mappings should not be retained. <br>
Risk: OpenClaw updates can overwrite the runtime patches. <br>
Mitigation: Re-run the installer after OpenClaw updates and verify that mentions still resolve as expected. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/junwei1213/openclaw-mention-skill) <br>
- [OpenClaw](https://openclaw.ai) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown documentation, shell commands, JavaScript and shell files, and WhatsApp message text with mention metadata] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires node, bash, and python3; targets the OpenClaw WhatsApp channel.] <br>

## Skill Version(s): <br>
1.0.1 (source: ClawHub release metadata; artifact frontmatter lists 1.0.2) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
