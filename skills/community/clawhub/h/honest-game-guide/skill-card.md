## Description:

Honest Game Guide helps agents provide no-spoiler game guidance by checking current public guide sources and cross-verifying key walkthrough details before answering.

This skill is ready for commercial/non-commercial use.

## Publisher:

[skb2026](https://clawhub.ai/user/skb2026)

### License/Terms of Use:

MIT-0

## Use Case:

External users and game-focused agents use this skill to research walkthroughs, builds, boss tactics, hidden content, and version-specific game mechanics while minimizing spoilers. It is intended for source-cited guidance that asks the player's current progress before revealing sensitive details.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Game guide details can become stale after patches or vary across guide sites.

Mitigation: The skill requires version labeling, current source checks, and cross-verification across independent trusted sources before presenting key details.

Risk: Walkthrough research can reveal spoilers about bosses, quests, hidden areas, or endings.

Mitigation: The skill asks for the player's current progress first and begins with progressive no-spoiler hints unless the user explicitly permits spoilers.

Risk: The skill browses external public guide sites and may activate on broad game-related requests.

Mitigation: Use it for game-guide tasks where external browsing is expected, and review cited links before relying on or sharing guidance.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/skb2026/skills/honest-game-guide)
- [ClawHub publisher profile](https://clawhub.ai/user/skb2026)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown with citations and source lists]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires web search and browsing for source verification; starts by confirming player progress to reduce spoilers.]

## Skill Version(s):

0.1.1 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
