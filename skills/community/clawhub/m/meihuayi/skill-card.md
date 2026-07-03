## Description: <br>
MeiHuaYi helps agents perform Plum Blossom I Ching divination using time-based or three-digit numeric casting, then structure readings with hexagram analysis and follow-up prompts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sakura7301](https://clawhub.ai/user/sakura7301) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to generate Chinese Plum Blossom I Ching charts, ask for external-observation context, and produce structured divination readings. It is intended as reference or entertainment guidance and should not replace rational review for major decisions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill automatically retains divination questions, readings, conclusions, feedback, and learning notes in local SQLite databases without a documented no-save or delete workflow. <br>
Mitigation: Avoid entering identifying, medical, financial, or third-party details; run the skill in a controlled workspace and manage or remove the local data directory when records should not persist. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/sakura7301/skills/meihuayi) <br>
- [Skill instructions](artifact/SKILL.md) <br>
- [Eight Trigrams correspondence reference](artifact/data/万物类象.md) <br>
- [Three Essentials and Ten Responses reference](artifact/data/三要十应.md) <br>
- [Divination interpretation guide](artifact/data/解卦技巧.md) <br>
- [I Ching JSON data source](https://raw.githubusercontent.com/john-walks-slow/open-iching/master/iching/iching.json) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown-style Chinese divination reading with command-line text output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update local SQLite databases under data/ for divination records and learning notes.] <br>

## Skill Version(s): <br>
1.0.6 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
