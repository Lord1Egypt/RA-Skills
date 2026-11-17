## Description:

Creative toolkit for AI agents to generate images, videos, voiceover, music, and sound effects, then assemble polished output via Remotion.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cohnen](https://clawhub.ai/user/cohnen)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, creative teams, and external agents use this skill to generate visual and audio assets with pixcli, then assemble product videos, social ads, explainers, and marketing content with Remotion templates and guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad command and file permissions can modify project files and run local media tooling.

Mitigation: Use the skill in a sandboxed project, review generated commands before execution, and limit exposed environment variables to those required for the workflow.

Risk: Unpinned npm and npx execution can install or run unexpected package versions.

Mitigation: Pin package versions where possible, inspect package manifests, and avoid unreviewed npx commands.

Risk: Generated media prompts or source assets may be sent to third-party processing services.

Mitigation: Do not submit confidential, regulated, or private media unless third-party processing is approved.

## Reference(s):

- [Pixcli homepage](https://pixcli.shellbot.sh)
- [ClawHub skill page](https://clawhub.ai/cohnen/skills/pixcli-skill)
- [Command Reference](references/command-reference.md)
- [Creative Guidelines](references/creative-guidelines.md)
- [Workflow Recipes](references/workflow-recipes.md)
- [Remotion Product Video Playbook](references/remotion-playbook.md)
- [Template Showcase](references/template-showcase.md)
- [Remotion Rules Index](references/remotion-rules-index.md)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Code, Configuration, Files]

**Output Format:** [Markdown guidance with bash commands, TypeScript/Remotion code references, and generated media file paths]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [When executed by an agent, workflows may create image, video, audio, and Remotion project files in the working directory.]

## Skill Version(s):

2.2.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
