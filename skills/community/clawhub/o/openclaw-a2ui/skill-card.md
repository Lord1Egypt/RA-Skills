## Description: <br>
Adds rich HTML card rendering guidance and UI bridge setup instructions for OpenClaw webchat replies. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[suuuy](https://clawhub.ai/user/suuuy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
OpenClaw users and developers use this skill to produce structured responses as single rich HTML cards and to install or troubleshoot the supporting UI bridge when raw HTML rendering is needed. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill installs a privileged OpenClaw UI plugin that changes OpenClaw configuration and control-ui files. <br>
Mitigation: Review the plugin code and configuration changes before installation, and keep the uninstall procedure available to revert openclaw.json and control-ui changes. <br>
Risk: The UI bridge enables raw HTML card rendering and expands browser-rendering boundaries. <br>
Mitigation: Verify the HTML sanitization policy, allow only the tags and attributes needed for trusted cards, and restrict access to the manifest route. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/suuuy/openclaw-a2ui) <br>
- [A2UI component reference](https://a2ui.org/reference/components/) <br>
- [UI configuration schema](references/ui-config-schema.md) <br>
- [HTML templates](references/html-templates.md) <br>
- [HTML card templates](references/html-card-templates.md) <br>
- [Components reference](references/components.md) <br>
- [Templates reference](references/templates.md) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Code, Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown with inline HTML examples and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Structured replies are expected to use a single HTML card with class="a2ui" unless the user requests plain text.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence and changelog) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
