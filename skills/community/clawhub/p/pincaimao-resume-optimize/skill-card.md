## Description: <br>
Calls the Pincaimao Resume Optimization API to optimize or rewrite resume content based on a target job description using an authenticated API key. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[pincaimao](https://clawhub.ai/user/pincaimao) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to upload a resume and submit a target job description to Pincaimao so the API can return optimized resume content. It is useful when adapting resume content for a specific role while preserving the ability to inspect the raw API output. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Resume files and job descriptions are sent to Pincaimao's API for processing and uploaded files are stored on Pincaimao COS. <br>
Mitigation: Install only if Pincaimao is trusted to process this data, review the selected resume file path before execution, and avoid submitting data that should not leave the user's environment. <br>
Risk: The skill depends on a separate pincaimao-basic setup for shared upload, authentication, response, and streaming behavior. <br>
Mitigation: Verify the pincaimao-basic dependency before installing or loading it, and use a dedicated API key through PCM_RESUME_OPTIMIZE_KEY. <br>


## Reference(s): <br>
- [Pincaimao homepage](https://www.pincaimao.com) <br>
- [Pincaimao registration and API key access](https://www.pincaimao.com/agents/login?invite_code=uwqc) <br>
- [Pincaimao API endpoint](https://api.pincaimao.com) <br>
- [ClawHub skill page](https://clawhub.ai/pincaimao/pincaimao-resume-optimize) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown or plain text; raw API output may be shown in a code block when requested.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires PCM_RESUME_OPTIMIZE_KEY and sends selected resume files and job descriptions to Pincaimao's API for processing.] <br>

## Skill Version(s): <br>
1.0.1 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
