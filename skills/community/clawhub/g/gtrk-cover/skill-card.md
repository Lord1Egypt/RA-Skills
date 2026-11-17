## Description:

Guides a two-stage video-cover workflow: design diagnosis, bilingual image prompts, and a browser-based workbench for arranging text and exporting PNG covers.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gitruck](https://clawhub.ai/user/gitruck)

### License/Terms of Use:

MIT-0

## Use Case:

Video creators use this skill to plan cover visuals, create bilingual prompts for external image-generation tools, and produce a standalone browser workbench for laying out text and exporting cover PNGs after background images are ready.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill includes unrelated video-project editing guidance and an extra CLI dependency despite describing a cover-only workflow.

Mitigation: Use a cover-only release with the unrelated editing instructions and unused CLI requirement removed; cover generation does not require a cloud API key.

Risk: The browser workbench loads external fonts and JavaScript whose dependencies have not been verified.

Mitigation: Review the external font and html2canvas dependencies before opening the workbench, or use a reviewed local copy when external loading is unsuitable.

Risk: Some referenced supporting materials are missing from the supplied artifact and the CLI implementation is unverified.

Mitigation: Check that the supporting documents and any CLI functionality needed for a separate workflow are available and reviewed before relying on them.

## Reference(s):

- [Cover layout recipes](artifact/references/layout-recipes.md)
- [Image prompt templates](artifact/references/prompt-templates.md)
- [Workbench guide](artifact/references/workbench-guide.md)
- [Cover delivery checklist](artifact/references/checklist.md)
- [Gitruck ClawHub skill page](https://clawhub.ai/gitruck/skills/gtrk-cover)
- [Gitruck CLI homepage (listed in skill metadata)](https://github.com/Gitruck/cli)

## Skill Output:

**Output Type(s):** [Guidance, Text, Markdown, Code]

**Output Format:** [Design guidance and bilingual image prompts in Markdown; a standalone HTML workbench for browser-based layout and PNG export.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill prepares prompts and the workbench; users provide background images, generate images externally, and export PNGs in their browser.]

## Skill Version(s):

1.3.10 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
