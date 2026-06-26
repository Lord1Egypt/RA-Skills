## Description: <br>
Classifies user memos and appends them to categorized Markdown files under ~/.memo when triggered by /private-secretary or /ps commands. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tristanchenxm](https://clawhub.ai/user/tristanchenxm) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users use this skill as a personal memo assistant to classify notes into categories such as Tech, Work, Life, Inspiration, and Others, then save them as local Markdown entries. It also supports reorganizing existing memos under ~/.memo when the user asks to rearrange them. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Memos are saved as plaintext under ~/.memo. <br>
Mitigation: Use the skill only for notes suitable for local plaintext storage, or store the memo directory in an encrypted location. <br>
Risk: The suggested shell write step can treat memo text as executable shell syntax. <br>
Mitigation: Review commands before execution and replace the write step with a safely quoted file-writing method before using arbitrary pasted content. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/tristanchenxm/memo-assistant) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Files, Guidance] <br>
**Output Format:** [Markdown entries appended to local files with shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes categorized memo files under ~/.memo.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
