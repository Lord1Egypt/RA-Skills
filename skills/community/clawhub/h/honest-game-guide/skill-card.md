## Description: <br>
A spoiler-conscious game guide research skill that verifies walkthrough, build, quest, mechanic, and hidden-content answers against multiple public sources before responding. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[skb2026](https://clawhub.ai/user/skb2026) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Players use this skill to ask for game strategy help while reducing hallucinated or spoiler-heavy guidance. The agent checks current public sources with web search and browsing, asks for the player's progress before spoilers, and cites the sources it used. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Game guide answers can still be incomplete, outdated, or misleading if public sources conflict or are stale. <br>
Mitigation: The skill requires cross-checking important claims against independent sources, noting source conflicts, and declining to answer when reliable evidence is insufficient. <br>
Risk: Game questions may include personal information or account details that are unnecessary for guide research. <br>
Mitigation: Users should avoid sharing personal information; the security guidance identifies normal public-source game-guide use as the intended posture. <br>
Risk: Walkthroughs can reveal spoilers before the player is ready. <br>
Mitigation: The skill asks for the user's current progress first and defaults to gradual, no-spoiler hints unless the user explicitly permits spoilers. <br>


## Reference(s): <br>
- [Honest Game Guide on ClawHub](https://clawhub.ai/skb2026/honest-game-guide) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown guide response with cited source links] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires web search and page browsing; asks for player progress before giving potentially spoiler-sensitive details.] <br>

## Skill Version(s): <br>
0.1.1 (source: SKILL.md frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
