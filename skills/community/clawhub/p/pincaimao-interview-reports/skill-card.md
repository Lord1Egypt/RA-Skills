## Description: <br>
Generates Pincaimao interview reports or coaching materials from a job description and interview recording through the Pincaimao API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[pincaimao](https://clawhub.ai/user/pincaimao) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Hiring teams and recruiting agents use this skill to upload an interview recording, pair it with a job description, and receive a readable interview report or coaching material from Pincaimao. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Interview recordings, job descriptions, and related hiring data are sent to Pincaimao for processing. <br>
Mitigation: Confirm the selected files and job description with the user before upload, and share only data intended for Pincaimao processing. <br>
Risk: The Pincaimao API key and returned COS keys are sensitive credentials or access references. <br>
Mitigation: Use a dedicated Pincaimao API key when possible, keep it in the environment, avoid hardcoding it, and avoid exposing returned COS keys. <br>
Risk: The skill relies on a separate pincaimao-basic skill for shared API behavior. <br>
Mitigation: Review pincaimao-basic before allowing the agent to install or load it. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/pincaimao/pincaimao-interview-reports) <br>
- [Pincaimao homepage](https://www.pincaimao.com) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown with optional raw API response code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns a readable summary by default, or the raw Pincaimao API answer when requested.] <br>

## Skill Version(s): <br>
1.0.1 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
