## Description:

Set up and start Infinite Pokemon when a user asks to install, play, or launch the game with their AI assistant.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shellishack](https://clawhub.ai/user/shellishack)

### License/Terms of Use:

MIT No Attribution

## Use Case:

External users and developers use this skill to have an agent obtain, build, and launch the Infinite Pokemon local desktop or browser game from a suitable checkout.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can clone a live GitHub repository and run npm-controlled code from that checkout without pinned commit verification.

Mitigation: Review the checkout before execution, prefer a pinned and reviewed commit or release, avoid elevated privileges, and keep unrelated secrets out of the agent environment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/shellishack/skills/infinite-pokemon)
- [Repository](https://github.com/Shellishack/infinite-pokemon)
- [Repository and getting started](https://github.com/Shellishack/infinite-pokemon#readme)
- [Chinese README](https://github.com/Shellishack/infinite-pokemon/blob/main/README.zh-CN.md)
- [Generation skills](https://github.com/Shellishack/infinite-pokemon/tree/main/skills)
- [Project disclaimer](https://github.com/Shellishack/infinite-pokemon/blob/main/DISCLAIMER.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and setup guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May start a local desktop or browser game process after dependency installation and build steps.]

## Skill Version(s):

0.2.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
