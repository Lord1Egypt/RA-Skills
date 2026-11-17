## Description:

Investor pitch deck structure with slide-by-slide framework, visual design rules, and data presentation for fundraising decks, investor presentations, startup pitches, demo days, and grant proposals.

This skill is ready for commercial/non-commercial use.

## Publisher:

[okaris](https://clawhub.ai/user/okaris)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to plan investor-ready pitch decks, apply slide-by-slide visual guidance, and generate example slide backgrounds or charts through inference.sh CLI commands.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup flow asks users to run a mutable remote installer in a shell before logging in.

Mitigation: Prefer a manual or version-pinned installation with independently verified checksums or signatures, then run login only after installation is verified.

Risk: Fundraising decks may contain confidential company, financial, or investor data that could be sent to remote rendering or Python execution services.

Mitigation: Avoid sending confidential fundraising data to remote services unless that handling is approved for the deck.

## Reference(s):

- [Pitch Deck Visuals Skill Page](https://clawhub.ai/okaris/skills/pitch-deck-visuals)
- [inference.sh](https://inference.sh)
- [inference.sh CLI Installer](https://cli.inference.sh)
- [inference.sh CLI Checksums](https://dist.inference.sh/cli/checksums.txt)

## Skill Output:

**Output Type(s):** [Markdown, Code, Shell commands, Guidance]

**Output Format:** [Markdown with inline bash code blocks and visual design guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include CLI commands that generate slide backgrounds, charts, and image assets.]

## Skill Version(s):

0.1.5 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
