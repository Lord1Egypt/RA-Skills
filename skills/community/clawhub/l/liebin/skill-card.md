## Description:

Liebin helps agents confirm a design direction before implementation by collecting real product content, rendering three comparable design variants, capturing structured feedback, documenting the chosen direction in DESIGN.md, and checking the built page against the original intent.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shaohuadavidlee](https://clawhub.ai/user/shaohuadavidlee)

### License/Terms of Use:

MIT-0

## Use Case:

Designers, developers, and agent users use this skill before building landing pages, UI screens, presentations, or visual redesigns when they need a concrete style decision based on real content. The skill is intended to make design tradeoffs reviewable before implementation and to preserve the accepted direction for downstream agents.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Private project information can be exposed if users provide internal URLs, screenshots, local code paths, staging sites, private repositories, or sensitive customer content.

Mitigation: Use only user-approved inputs and avoid private or sensitive sources unless that access is intended for the design task.

Risk: Optional local Node and Playwright helpers can execute scripts and browser checks in the user's environment.

Mitigation: Install from the reviewed ZIP or a trusted repository state, and review commands before running local helper scripts.

Risk: Design references can tempt agents to copy protected brand assets, fonts, images, icons, or long text rather than learning layout and style relationships.

Mitigation: Use references for structure, spacing, rhythm, density, and contrast; replace logos, proprietary media, font files, icons, and copy unless permission or licensing is clear.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/shaohuadavidlee/skills/liebin)
- [Server-resolved source repository](https://github.com/ShaohuaDavidLee/Liebin)
- [Public project site](https://liebin.caojuege.com)
- [Intake reference](references/intake.md)
- [Variant rendering reference](references/variants.md)
- [DESIGN.md reference](references/design-md.md)
- [Verification reference](references/verify.md)
- [Installation guide](docs/skill-install.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance, DESIGN.md content, HTML preview artifacts, local verification reports, and optional shell commands.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create single-file HTML proof pages and verification outputs when the user asks the agent to run the workflow.]

## Skill Version(s):

0.1.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
