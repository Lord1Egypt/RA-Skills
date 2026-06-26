## Description: <br>
Updates a learner's error log and course map after a completed lesson when the user asks to save or update progress. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yizhan-yao](https://clawhub.ai/user/yizhan-yao) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Learners and study agents use this skill to record completed lessons, update tracked mistakes, and maintain a course progress map in local markdown files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Casual save or end-of-lesson phrases can trigger unintended edits to the learning dashboard files. <br>
Mitigation: Ask the agent to confirm the target files and planned changes before writing when the request is brief or ambiguous. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Text, Guidance] <br>
**Output Format:** [Markdown file edits plus a concise progress summary] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Updates only the named learning dashboard files and avoids outputting full file contents.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release evidence and plugin.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
