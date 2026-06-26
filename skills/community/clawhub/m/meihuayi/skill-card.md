## Description: <br>
MeiHuaYi generates Mei Hua Yi Shu divination layouts from the current time or a three-digit number and supports structured interpretation with bundled I Ching reference material. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sakura7301](https://clawhub.ai/user/sakura7301) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to create time-based or number-based Mei Hua Yi Shu charts, then organize readings around trigram imagery, body-use relationships, moving lines, and observed context. Readings should be treated as cultural or entertainment-oriented guidance, not as decision-grade advice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can keep local records of user questions, readings, feedback, and learning notes. <br>
Mitigation: Use non-sensitive prompts, avoid personal medical, legal, financial, or relationship details, and manage or remove the local SQLite files when records should not persist. <br>
Risk: The skill conditionally fetches I Ching data from GitHub if the bundled iching.json file is missing. <br>
Mitigation: Keep the bundled iching.json file present for offline use, or block the conditional fetch in stricter environments. <br>
Risk: Divination output may be mistaken for reliable advice on important decisions. <br>
Mitigation: Treat readings as cultural or entertainment-oriented and use qualified professional advice for consequential medical, legal, financial, or safety decisions. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/sakura7301/meihuayi) <br>
- [Eight Trigrams Correspondence Reference](artifact/data/万物类象.md) <br>
- [Three Essentials and Ten Responses Reference](artifact/data/三要十应.md) <br>
- [Divination Interpretation Techniques](artifact/data/解卦技巧.md) <br>
- [I Ching Hexagram Data](artifact/data/iching.json) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown-style Chinese text with CLI examples, divination chart output, structured interpretation guidance, and local recordkeeping summaries.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create local SQLite record and learning-note databases under the skill data directory when recordkeeping commands are used.] <br>

## Skill Version(s): <br>
1.0.5 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
