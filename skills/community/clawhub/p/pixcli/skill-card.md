## Description: <br>
Pixcli is a creative-media agent skill that uses the pixcli CLI to generate and edit images, videos, voiceovers, music, sound effects, podcasts, and Remotion-based video assemblies. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cohnen](https://clawhub.ai/user/cohnen) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, creative operators, and external users use this skill to produce AI media assets and assemble polished video or podcast deliverables from prompts and source assets. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts, source assets, and generated content may be sent to pixcli and its backend providers. <br>
Mitigation: Use the skill only with content approved for remote processing, and avoid secrets, regulated data, or sensitive internal material. <br>
Risk: Podcast or media outputs can be published publicly and permanently by default. <br>
Mitigation: Use --private or --no-publish for internal or sensitive outputs, and verify publication settings before sharing links. <br>
Risk: Voice cloning can create unauthorized synthetic speech. <br>
Mitigation: Clone voices only with clear authorization and review generated audio before publication. <br>


## Reference(s): <br>
- [Pixcli homepage](https://pixcli.shellbot.sh) <br>
- [ClawHub skill page](https://clawhub.ai/cohnen/skills/pixcli) <br>
- [Command Reference](references/command-reference.md) <br>
- [Remotion Product Video Playbook](references/remotion-playbook.md) <br>
- [Template Showcase](references/template-showcase.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, files, guidance] <br>
**Output Format:** [Markdown guidance with JSON and shell command snippets; generated media files and Remotion project files when commands are executed.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node.js, npx, and METERKEY_API_KEY; remote generation can send prompts and source assets to pixcli services.] <br>

## Skill Version(s): <br>
3.4.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
