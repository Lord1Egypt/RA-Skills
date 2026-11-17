## Description:

Generates a unified carousel image set with a cover and interior pages for Xiaohongshu-style posts, knowledge-card carousels, and product-introduction visuals.

This skill is ready for commercial/non-commercial use.

## Publisher:

[meitu](https://clawhub.ai/user/meitu)

### License/Terms of Use:

MIT-0

## Use Case:

External creators, marketing teams, and agents use this skill to produce coordinated carousel poster sets from user-provided or generated copy. It handles preflight checks, prompt preparation, Meitu CLI image generation, refinement, delivery naming, and optional project preference recording.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Shell-style Meitu CLI command templates can create local command-execution risk when prompts or paths come from untrusted input.

Mitigation: Use the skill only in trusted workspaces, review command arguments before execution, avoid untrusted paths or prompt fragments, and prefer a pinned local Meitu CLI installation.

Risk: Project mode can read and write visual workspace preferences and observation memory.

Mitigation: Confirm the intended workspace paths before enabling memory writes and review stored preferences during project use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/meitu/skills/meitu-carousel)
- [Xiaohongshu cover prompt reference](artifact/references/xiaohongshu-cover.md)
- [Memory protocol reference](artifact/references/memory-protocol.md)

## Skill Output:

**Output Type(s):** [Files, Shell commands, Configuration, Guidance, Text]

**Output Format:** [Markdown guidance with inline shell commands, generated prompt text, JSON command responses, and JPEG image files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires the Meitu CLI and MEITU_OPENAPI_ACCESS_KEY / MEITU_OPENAPI_SECRET_KEY credentials; image files are named by date and page type.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
