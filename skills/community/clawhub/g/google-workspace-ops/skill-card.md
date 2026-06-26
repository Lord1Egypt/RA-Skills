## Description: <br>
Operates across Google Drive, Docs, Sheets, and Slides to find, summarize, edit, migrate, or clean shared documents. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[djc00p](https://clawhub.ai/user/djc00p) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees and operators use this skill to work across Google Workspace assets: locate the right Drive file, inspect its structure, make or recommend precise updates, and summarize follow-up cleanup such as archive or merge candidates. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad Google Workspace credentials could let an agent inspect or modify files beyond the intended task. <br>
Mitigation: Use a least-privilege Google credential limited to the necessary folders and APIs. <br>
Risk: Live edits, archiving, merging, or restructuring could change shared documents incorrectly. <br>
Mitigation: Test on low-risk files first and require the agent to identify the target file and planned changes before making updates. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/djc00p/google-workspace-ops) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown structured as ASSET, CURRENT STATE, ACTION, and FOLLOW-UPS sections] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires GOOGLE_APPLICATION_CREDENTIALS and a least-privilege Google credential for live Workspace operations.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
