## Description:

Pixcli helps agents generate and edit images, videos, voiceovers, music, sound effects, podcasts, and Remotion-based video assemblies through the pixcli CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cohnen](https://clawhub.ai/user/cohnen)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, creative operators, and agent builders use this skill to produce media assets and assemble finished marketing, social, explainer, product, or podcast outputs. It is suited for workflows that need one CLI-backed path for image, video, audio, podcast, and Remotion project generation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts, source media, and generated podcast content may be sent to the pixcli service, and some publishing flows can expose shareable public links.

Mitigation: Avoid confidential or regulated material unless approved for the service, and use private or no-publish options for sensitive media.

Risk: Runtime use depends on npx, npm packages, and remote CLI execution paths that can introduce supply-chain review needs.

Mitigation: Use pinned npm invocations or a reviewed local install in automated environments, and review dependencies before deployment.

Risk: Voice cloning can create consent and impersonation risks.

Mitigation: Use voice cloning only with clear authorization from the voice owner and review generated audio before distribution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/cohnen/skills/pixcli)
- [Pixcli homepage](https://pixcli.hilo.cx)
- [npm package: pixcli](https://www.npmjs.com/package/pixcli)
- [Command reference](references/command-reference.md)
- [Creative guidelines](references/creative-guidelines.md)
- [Prompt cookbook](references/prompt-cookbook.md)
- [Remotion playbook](references/remotion-playbook.md)
- [Template showcase](references/template-showcase.md)
- [Workflow recipes](references/workflow-recipes.md)

## Skill Output:

**Output Type(s):** [Files, JSON, Shell commands, Code, Configuration instructions, Guidance]

**Output Format:** [Markdown guidance with inline shell commands, JSON CLI responses, generated media files, and Remotion project code]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js and npx plus METERKEY_API_KEY; generated assets may be downloaded locally or published through pixcli links depending on command options.]

## Skill Version(s):

3.4.2 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
