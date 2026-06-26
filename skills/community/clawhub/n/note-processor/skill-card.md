## Description: <br>
Summarize, extract keywords, search, and list research notes from research-assistant's database to review progress and find insights efficiently. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[johstracke](https://clawhub.ai/user/johstracke) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and researchers use this skill to inspect local research notes, summarize topics, extract frequent keywords, search within a topic, and list topic-level progress without re-reading every note. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Local research-note content from ~/.openclaw/workspace/research_db.json may be displayed in the terminal or agent session. <br>
Mitigation: Use the skill only with notes you are comfortable surfacing, and avoid notes containing secrets, credentials, sensitive personal data, or untrusted instructions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/johstracke/note-processor) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Terminal text output and Markdown command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reads local research notes from ~/.openclaw/workspace/research_db.json and prints requested summaries, keywords, searches, or topic lists.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
