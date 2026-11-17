## Description:

This end-of-life OpenClaw skill retains MiniMax music generation workflows for reference and provides local audio analysis and linting helpers that do not require MiniMax.

This skill is ready for commercial/non-commercial use.

## Publisher:

[luischarro](https://clawhub.ai/user/luischarro)

### License/Terms of Use:

MIT-0

## Use Case:

Music creators and developers can use the remaining local tools to analyze audio and lint music requests or lyrics. The documented MiniMax generation workflows are end of life and should not be used for generation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Workflows may send recordings, lyrics, prompts, or drafts to MiniMax without a clear consent checkpoint.

Mitigation: Review privacy implications and obtain permission before uploading sensitive, private, or third-party material.

Risk: The security scan is incomplete, so its suspicious verdict does not establish malicious intent or cover every component.

Mitigation: Review and scan the skill before installation, including components that were only partially inspected.

## Reference(s):

- [README.md — status and local tools](README.md)
- [Setup and preflight](references/setup-and-preflight.md)
- [Audio emotion analysis](references/emotion-analysis.md)
- [MiniMax generation caveats](references/minimax-generation-caveats.md)
- [Publisher source page](https://github.com/LuisCharro/skills/tree/main/publish/music-craft-minimax)

## Skill Output:

**Output Type(s):** [Analysis, JSON, Text, Shell commands, Guidance]

**Output Format:** [Markdown guidance, shell commands, JSON analysis reports, and text prompts or lyrics]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs depend on the selected local analysis or lint helper; MiniMax-generated audio is unavailable through this end-of-life skill.]

## Skill Version(s):

1.7.1 (source: SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
