## Description: <br>
Newton Perspective guides an agent to answer through an Isaac Newton-inspired first-principles reasoning style, using research when current facts are needed and applying documented mental models. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sjj2026](https://clawhub.ai/user/sjj2026) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to frame questions through Newton-style first-principles analysis, inductive reasoning, mathematical precision, simplicity checks, and explicit uncertainty boundaries. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security scan reported a low-confidence clean result because the target skill artifact was not available for direct inspection during that scan. <br>
Mitigation: Review the skill files before sensitive deployment, including declared permissions, install commands, credential handling, network access, filesystem writes, and persistence behavior. <br>
Risk: The skill instructs the agent to research current factual questions, so outputs can depend on the quality and recency of external sources. <br>
Mitigation: Require source review and citations for high-impact factual, commercial, legal, medical, or financial decisions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/sjj2026/newton-perspective) <br>
- [Skill source: SKILL.md](artifact/SKILL.md) <br>
- [Research: Newton writings](artifact/references/research/01-writings.md) <br>
- [Research: Newton conversations](artifact/references/research/02-conversations.md) <br>
- [Research: expression DNA](artifact/references/research/03-expression-dna.md) <br>
- [Research: external views](artifact/references/research/04-external-views.md) <br>
- [Research: decisions](artifact/references/research/05-decisions.md) <br>
- [Research: timeline](artifact/references/research/06-timeline.md) <br>
- [Stanford Encyclopedia of Philosophy: Newton's Principia](https://plato.stanford.edu/entries/newton-principia/) <br>
- [Newton Project](https://www.newtonproject.ox.ac.uk/) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance] <br>
**Output Format:** [Markdown-formatted natural language responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May direct the agent to use web search for current factual questions; does not produce code, files, shell commands, or configuration by default.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
