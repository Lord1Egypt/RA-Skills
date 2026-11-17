## Description:

Morfeo Academy's Remotion video style guide for creating Remotion videos, stories, and animations with the Morfeo Academy brand.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pauldelavallaz](https://clawhub.ai/user/pauldelavallaz)

### License/Terms of Use:

MIT

## Use Case:

Developers and content creators use this skill to produce Morfeo Academy branded Remotion videos with consistent colors, typography, animation timing, emoji rendering, and brand icon components.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unpinned npm setup commands can install changing dependency versions.

Mitigation: Review and pin npm package versions before running setup commands.

Risk: Apple emoji images are loaded from a third-party CDN during rendering.

Mitigation: Render only where third-party CDN requests are acceptable, or vendor the required emoji assets locally.

## Reference(s):

- [styles.ts](references/styles.ts)
- [AppleEmoji.tsx](references/AppleEmoji.tsx)
- [BrandIcon.tsx](references/BrandIcon.tsx)
- [MorfeoStory-example.tsx](references/MorfeoStory-example.tsx)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown guidance with TypeScript, TSX, and bash snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes Remotion styling conventions, reusable component patterns, and setup commands.]

## Skill Version(s):

1.0.0 (source: package.json and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
