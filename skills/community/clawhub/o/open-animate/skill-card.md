## Description:

Open Animate helps agents create professional motion graphics, generate media assets, and render MP4 videos for launches, explainers, social clips, and other visual content.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jacobcwright](https://clawhub.ai/user/jacobcwright)

### License/Terms of Use:

Apache-2.0

## Use Case:

Developers, content creators, and agent operators use this skill to scaffold Open Animate projects, compose Remotion-based animated scenes, generate supporting media assets, preview work, and render finished MP4 videos.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks users to run mutable npm and external skill-install commands.

Mitigation: Use a project sandbox and prefer pinned package versions or a reviewed lockfile before running Open Animate or Remotion tooling.

Risk: Cloud rendering and AI asset-generation commands may send prompts, media, credentials, or business data to external providers.

Mitigation: Avoid confidential inputs unless provider data handling has been reviewed and the project is approved for that use.

## Reference(s):

- [Open Animate homepage](https://open-animate.com)
- [Open Animate ClawHub listing](https://clawhub.ai/jacobcwright/skills/open-animate)
- [Agent Workflow](references/workflow.md)
- [animate.json Reference](references/scene-config.md)
- [Composition Patterns](references/composition-patterns.md)
- [Animation Cookbook](references/animation-cookbook.md)
- [Asset Generation](references/asset-generation.md)
- [Working with Media](references/media-guide.md)

## Skill Output:

**Output Type(s):** [Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with TypeScript, JSON, and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May guide creation of Remotion projects, generated media assets, and rendered MP4 outputs.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
