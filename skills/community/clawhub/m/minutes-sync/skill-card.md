## Description: <br>
Generate structured meeting minutes with Feishu sync for notes, decisions, action items, and shared team follow-up. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[terrycarter1985](https://clawhub.ai/user/terrycarter1985) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees and team collaborators use this skill to turn meeting context into structured minutes, decisions, and follow-up items, then sync the result to a Feishu document. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Meeting content is uploaded to Feishu documents. <br>
Mitigation: Confirm that Feishu sync is intended for the meeting content before using the skill. <br>
Risk: Minutes could sync to the wrong Feishu account, folder, or document owner. <br>
Mitigation: Verify the active Feishu account, target folder, and any ownership-transfer option before first use. <br>
Risk: Sharing options could expose meeting notes to unintended recipients. <br>
Mitigation: Review share targets and permissions before using Feishu sharing options. <br>
Risk: The skill depends on a separate feishu-doc helper skill for sync behavior. <br>
Mitigation: Review and verify the feishu-doc helper skill before relying on automated document creation. <br>


## Reference(s): <br>
- [Feishu sync guide](references/feishu-sync.md) <br>
- [ClawHub skill page](https://clawhub.ai/terrycarter1985/minutes-sync) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown meeting minutes with a Feishu document link and optional shell command for sync] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The generated minutes preserve missing fields as [待补充] and append the Feishu URL after sync.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
