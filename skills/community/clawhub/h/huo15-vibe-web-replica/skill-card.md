## Description:

Creates and guides immersive web replicas and original pages with Three.js, GSAP ScrollTrigger, Lenis smooth scrolling, WebGL effects, and a Vite scaffold.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhaobod1](https://clawhub.ai/user/zhaobod1)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and designers use this skill to analyze target sites or visual goals, scaffold a Vite project, and create code or guidance for immersive Three.js, GSAP, and Lenis web experiences.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated projects rely on npm packages and may use CDN-hosted decoder assets.

Mitigation: Review generated package versions, add a lockfile, and self-host Draco or KTX2 decoder assets before production deployment.

Risk: Immersive WebGL pages can perform poorly on constrained devices if heavy assets or effects are added without testing.

Mitigation: Cap pixel ratio, lazy-load heavy 3D assets, reduce draw calls, and test mobile responsiveness before release.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/zhaobod1/skills/huo15-vibe-web-replica)
- [API Reference](reference.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with code snippets and scaffolded project files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can generate a Vite, Three.js, GSAP, and Lenis project scaffold with supporting templates.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
