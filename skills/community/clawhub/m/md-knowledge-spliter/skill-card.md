## Description: <br>
MdSpliter helps agents split large Markdown knowledge files into topic-based chunks and use an index to retrieve only relevant sections. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Josephyb97](https://clawhub.ai/user/Josephyb97) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agents use this skill to organize large Markdown knowledge bases into smaller thematic files with an INDEX.md, then load only the chunks relevant to a query. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated chunks or INDEX.md entries may misrepresent the source knowledge file. <br>
Mitigation: Confirm the exact knowledge folder and review generated chunks and INDEX.md before relying on them. <br>
Risk: Sensitive documents may become indexed for future agent use if included in the target folder. <br>
Mitigation: Avoid pointing the skill at sensitive documents unless they are intentionally approved for indexing. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Josephyb97/md-knowledge-spliter) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Files, Guidance] <br>
**Output Format:** [Markdown files and indexing guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates topic-based chunks and INDEX.md; recommends chunks under 2KB and avoiding folders such as node_modules, .git, and credentials.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
