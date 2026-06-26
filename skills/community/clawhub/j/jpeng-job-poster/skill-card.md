## Description: <br>
Post job listings. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jpengcheng523-netizen](https://clawhub.ai/user/jpengcheng523-netizen) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Recruiting and HR operations teams use this skill to automate posting job listings through a command-line workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill is meant to post job listings, but the evidence does not identify the job-posting service, what data is sent, or how a user approves a listing before publication. <br>
Mitigation: Use only after identifying the service behind JOB_API_KEY, inspecting the posting script, and requiring preview plus explicit approval before any listing is published. <br>
Risk: The workflow requires a JOB_API_KEY credential. <br>
Mitigation: Store the key in a secret manager or protected environment variable, scope it to the minimum needed permissions, and rotate it if exposed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jpengcheng523-netizen/jpeng-job-poster) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/jpengcheng523-netizen) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance, JSON] <br>
**Output Format:** [Markdown with inline bash and JSON code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires JOB_API_KEY and input/output paths for the job-posting command.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
