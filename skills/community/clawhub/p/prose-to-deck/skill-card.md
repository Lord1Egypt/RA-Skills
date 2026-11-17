## Description:

Transform articles, essays, transcripts, and other long-form writing into polished single-file HTML presentations with editorial pacing and strong visual storytelling.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yueeli](https://clawhub.ai/user/yueeli)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, writers, and presentation creators use this skill to convert long-form source material into a staged editorial HTML deck with analysis, slide planning, visual direction, build notes, and review checkpoints.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unsafe slug handling can write outside the intended project folder.

Mitigation: Use review mode, keep the default ./projects output root, and avoid untrusted or path-like titles until slug validation is fixed.

Risk: Generated decks may load unverified third-party scripts.

Mitigation: Inspect generated HTML before sharing and confirm any CDN fonts or libraries are acceptable for the deployment environment.

Risk: The skill creates a project directory and multiple local files.

Mitigation: Run it in a workspace where local file creation is expected and review the generated project folder before reuse or distribution.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/yueeli/skills/prose-to-deck)
- [SKILL.md](SKILL.md)
- [Artifact Format - progress.md](references/artifact-progress.md)
- [Artifact Format - 01-analysis.md](references/artifact-analysis.md)
- [Artifact Format - 02-slide-plan.md](references/artifact-slide-plan.md)
- [Artifact Format - 03-visual-direction.md](references/artifact-visual-direction.md)
- [Artifact Format - 04-build-notes.md](references/artifact-build-notes.md)
- [Design System](references/design-system.md)
- [Headline System](references/headline-system.md)
- [Materials Library](references/materials.md)
- [QA Checklist](references/qa-checklist.md)
- [Style Seeds](references/style-seeds.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown stage artifacts plus a single self-contained HTML presentation file]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates a dedicated projects/<slug>-<timestamp>/ folder containing progress.md, analysis, slide plan, visual direction, build notes, and index.html.]

## Skill Version(s):

1.0.3 (source: evidence.release.version and artifact/claw.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
