## Description: <br>
Create high-quality visual designs such as websites, app screens, dashboards, slides, marketing materials, and social media graphics using the Pencil CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gerhardberger](https://clawhub.ai/user/gerhardberger) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, designers, and agent users use this skill to generate and iterate on visual design assets from natural language prompts through the Pencil CLI. It supports setup, authentication, prompt handling, export, and iteration workflows for design files and rendered images. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may prompt an agent to install and run external Pencil CLI tooling. <br>
Mitigation: Require manual approval for npm installs and prefer pinned package versions before running the CLI. <br>
Risk: The skill may involve account login, API credentials, or authenticated CLI sessions. <br>
Mitigation: Approve account login steps manually and avoid exposing credentials in prompts, logs, or generated files. <br>
Risk: The skill may persist fetched skill instructions or write into agent skill directories. <br>
Mitigation: Review CDN-fetched skill files and approve any writes to agent skill directories before making them persistent. <br>
Risk: The skill can create or overwrite local design files during generation and iteration. <br>
Mitigation: Use versioned output filenames such as design-v2.pen and inspect target paths before allowing overwrites. <br>


## Reference(s): <br>
- [Pencil CLI skill file on unpkg](https://unpkg.com/@pencil.dev/cli@latest/SKILL.md) <br>
- [Pencil CLI skill file on jsDelivr](https://cdn.jsdelivr.net/npm/@pencil.dev/cli@latest/SKILL.md) <br>
- [OpenClaw skills documentation](https://docs.openclaw.ai/skills/) <br>
- [ClawHub release page](https://clawhub.ai/gerhardberger/pencil-design) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance, files] <br>
**Output Format:** [Markdown guidance with inline shell commands and generated .pen design files or exported images when the CLI is run] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated design work may create or overwrite local design files; use versioned output filenames for iterations.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
