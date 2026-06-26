## Description: <br>
Use this skill when the user asks about reading highlights, book notes, annotations, or reading history from KOReader; it retrieves KOReader HighlightSync data and presents it in plain language. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[myugan](https://clawhub.ai/user/myugan) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users use this skill to list books, find highlights, view recent annotations, and summarize themes from their KOReader HighlightSync data. It is scoped to reading-history and highlight retrieval workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill claims to be read-only while artifact behavior includes saving setup details and reading preferences to memory files. <br>
Mitigation: Review memory-writing behavior before installation and require clear user consent before storing paths, profile details, or reading preferences. <br>
Risk: The artifact includes a first-run instruction to delete a setup file despite its read-only positioning. <br>
Mitigation: Remove or explicitly gate any file deletion step before deployment. <br>
Risk: The skill accesses local KOReader HighlightSync data that can reveal reading habits and annotations. <br>
Mitigation: Limit access to the intended highlights directory and avoid exposing paths, internal fields, or technical output in user-facing responses. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/myugan/koreader-highlights) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Plain-language responses, with internal shell commands used by the agent] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [User-facing replies are expected to avoid commands, code, JSON, file paths, and technical errors.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
