## Description:

Create professional cinematic scripts for AI video generation with character consistency, cinematography guidance, prompt generation, export options, and optional storage integration.

This skill is ready for commercial/non-commercial use.

## Publisher:

[praveenspeaks](https://clawhub.ai/user/praveenspeaks)

### License/Terms of Use:

MIT

## Use Case:

Developers, creators, and agents use this skill to create story contexts, character references, cinematic scripts, AI image and video prompts, and YouTube metadata for animated or comic video projects. It also helps validate era consistency and save project outputs locally or to Google Drive when configured.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill stores story contexts, character details, scripts, and related project state in agent memory.

Mitigation: Install only when memory access is acceptable for the story projects being created, and avoid entering sensitive story or credential material unless the workspace policy permits it.

Risk: The skill can upload generated project files to Google Drive when authorized.

Mitigation: Use a Google OAuth client and scope appropriate to drive.file, review content before upload, and authorize only the storage destination intended for the project.

Risk: The artifact includes bundled example and template skill manifests that could be auto-discovered by downstream tooling.

Mitigation: Remove or ignore bundled example/template skills when redistributing or using automatic skill discovery.

Risk: Development-tooling dependencies may age over time.

Mitigation: Update and review development dependencies before maintaining or republishing the package.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/praveenspeaks/skills/openclawskills)
- [README](artifact/README.md)
- [Skill Definition](artifact/SKILL.md)
- [Cinematic Script Writer README](artifact/skills/cinematic-script-writer/README.md)
- [Storage Example](artifact/skills/cinematic-script-writer/EXAMPLE-STORAGE.md)
- [Consistency Example](artifact/skills/cinematic-script-writer/EXAMPLE-CONSISTENCY.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown, JSON, plain text, and TypeScript-oriented command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can generate scripts, image and video prompts, character and voice guides, YouTube metadata, and organized project files.]

## Skill Version(s):

1.4.0 (source: server release metadata and artifact root frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
