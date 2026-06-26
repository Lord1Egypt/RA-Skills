## Description: <br>
Generate journal club slides with background, critique, and discussion. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aipoch-ai](https://clawhub.ai/user/aipoch-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Students, researchers, and instructors use this skill to create structured journal club presentation outlines for lab meetings, graduate training, literature reviews, and critical appraisal sessions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The packaged script writes to a user-supplied output path and may overwrite an existing file. <br>
Mitigation: Use an output path inside the workspace and avoid names of important existing files. <br>
Risk: Generated academic presentation content can be incomplete or inaccurate if the paper details are incomplete. <br>
Mitigation: Review the generated outline for source faithfulness and accuracy before presenting. <br>
Risk: Incomplete inputs or broad requests can weaken the skill boundary. <br>
Mitigation: Confirm the paper details, audience, time limit, output path, and scope before execution; use the documented fallback path when required inputs are missing. <br>


## Reference(s): <br>
- [Audit Reference](artifact/references/audit-reference.md) <br>
- [ClawHub skill page](https://clawhub.ai/aipoch-ai/journal-club-presenter) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Structured text or Markdown with optional shell commands for validation] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces slide outlines, background context, key figure explanations, critical evaluation points, and discussion questions; the packaged script can also write a local text file.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
