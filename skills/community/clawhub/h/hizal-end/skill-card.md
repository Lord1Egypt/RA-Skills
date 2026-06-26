## Description: <br>
Close the agent's context session and consolidate what was learned. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[parkerscobey](https://clawhub.ai/user/parkerscobey) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to close a work session, review surfaced memory chunks, and decide whether to keep, promote, or discard context before going idle or switching tasks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may activate on ordinary wrap-up language and initiate end-of-session memory review without sufficiently explicit intent. <br>
Mitigation: Use it only when ending a session deliberately, and review the returned memory chunks before taking keep, promote, or discard actions. <br>
Risk: Promoting or deleting stored memory can change agent or project context. <br>
Mitigation: Confirm promoted memory is accurate and useful, and delete original context only after verifying the promotion succeeded and the source chunk is no longer needed. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown with inline command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Provides end-session review instructions for memory consolidation decisions.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
