## Description:

Generate images and videos from React + Tailwind CSS templates using the loopwind CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tomtev](https://clawhub.ai/user/tomtev)

### License/Terms of Use:


## Use Case:

Developers and content teams use this skill to help agents create Loopwind JSX templates, configure project design tokens, validate templates, and render images or videos from React and Tailwind CSS inputs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The documented install flow runs mutable remote code through `curl | bash`.

Mitigation: Review the installer before execution and prefer a versioned package or release with published checksums or signatures.

Risk: The documented agent skill install uses a mutable remote skill URL.

Mitigation: Pin or locally review the skill content before installing it into an agent environment.

Risk: Templates, images, and fonts may be fetched from remote third-party URLs.

Mitigation: Use trusted sources, pin versions where possible, and review remote assets before rendering or sharing outputs.

## Reference(s):

- [Loopwind ClawHub skill page](https://clawhub.ai/tomtev/skills/loopwind)
- [Loopwind installer](https://loopwind.dev/install.sh)
- [Loopwind remote skill](https://loopwind.dev/skill.md)

## Skill Output:

**Output Type(s):** [markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline JSX, JSON, and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May guide agents to create local .loopwind templates and configuration files, then render PNG, JPEG, SVG, GIF, or MP4 outputs through the loopwind CLI.]

## Skill Version(s):

0.25.11 (source: evidence release and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
