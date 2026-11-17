## Description:

MeiHuaYi helps agents run Plum Blossom I Ching divination using time-based or three-digit-number casting, then produce structured hexagram analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sakura7301](https://clawhub.ai/user/sakura7301)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use MeiHuaYi to generate a Plum Blossom I Ching chart from the current time or a three-digit number, ask for contextual observations, and produce a staged interpretive reading for reference or entertainment.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Readings, questions, contextual observations, feedback, and derived notes may be stored locally in plaintext databases.

Mitigation: Avoid entering sensitive personal details, use a separate environment, and install only if local plaintext storage is acceptable.

Risk: The skill may use an unverified remote data fallback if the bundled I Ching data file is missing.

Mitigation: Keep the bundled data file present and verified, pin dependencies yourself, and treat fallback data as untrusted.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/sakura7301/skills/meihuayi)
- [八卦万物类象](data/万物类象.md)
- [三要十应](data/三要十应.md)
- [解卦技巧](data/解卦技巧.md)
- [open-iching iching.json fallback](https://raw.githubusercontent.com/john-walks-slow/open-iching/master/iching/iching.json)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown-style Chinese text with command examples, divination chart output, staged interpretation, and local record or feedback guidance.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update local plaintext SQLite databases for divination records and learning notes.]

## Skill Version(s):

1.0.6 (source: SKILL.md frontmatter, _meta.json, and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
