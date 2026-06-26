## Description: <br>
Creative toolkit for AI agents to generate images, videos, voiceover, music, and sound effects, then assemble polished output via Remotion. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cohnen](https://clawhub.ai/user/cohnen) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, marketers, and creative teams use this skill to plan and run AI media generation workflows, create production assets with pixcli, and assemble finished videos with Remotion templates and rules. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts and media may be sent to a remote AI media service. <br>
Mitigation: Use only approved content and avoid secrets, regulated data, private customer content, or unreleased media unless the use is authorized. <br>
Risk: API keys can be exposed if passed directly on the command line. <br>
Mitigation: Prefer PIXCLI_API_KEY in the environment rather than the --key option. <br>
Risk: Rendering and ffmpeg commands may overwrite local output files. <br>
Mitigation: Review output paths before running render or ffmpeg commands. <br>


## Reference(s): <br>
- [Pixcli homepage](https://pixcli.shellbot.sh) <br>
- [ClawHub release page](https://clawhub.ai/cohnen/pixcli-skill) <br>
- [Command reference](references/command-reference.md) <br>
- [Creative guidelines](references/creative-guidelines.md) <br>
- [Workflow recipes](references/workflow-recipes.md) <br>
- [Prompt cookbook](references/prompt-cookbook.md) <br>
- [Remotion playbook](references/remotion-playbook.md) <br>
- [Template showcase](references/template-showcase.md) <br>
- [Remotion rules index](references/remotion-rules-index.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, files, guidance] <br>
**Output Format:** [Markdown guidance with shell commands, Remotion code snippets, configuration steps, and generated media file paths.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May invoke a remote AI media service through pixcli and may create or overwrite local image, audio, video, and Remotion project files.] <br>

## Skill Version(s): <br>
2.2.0 (source: SKILL.md frontmatter, server release metadata, target metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
