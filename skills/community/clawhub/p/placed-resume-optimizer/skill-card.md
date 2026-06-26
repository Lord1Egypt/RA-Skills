## Description: <br>
Placed Resume Optimizer helps users check ATS compatibility, match resumes to job descriptions, analyze resume gaps, and improve resume bullets through the Placed API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ajitsingh25](https://clawhub.ai/user/ajitsingh25) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External job seekers and career advisors use this skill to evaluate resumes against job descriptions, identify ATS and keyword gaps, and request targeted resume improvements through the Placed service. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Resume content, job descriptions, and generated recommendations are sent to the Placed/Exidian service for processing. <br>
Mitigation: Use the skill only when that service is acceptable for the resume data involved, and avoid unnecessary personal or confidential details. <br>
Risk: The default setup stores the Placed API key on disk at ~/.config/placed/credentials. <br>
Mitigation: Use a dedicated revocable API key, keep it session-only when possible, and rotate or remove the key when the skill is no longer used. <br>
Risk: Resume optimization output may be incorrect, overstated, or poorly matched to the user's actual experience. <br>
Mitigation: Review all suggested changes before applying them and keep a master resume copy separate from tailored versions. <br>


## Reference(s): <br>
- [Placed Resume Optimizer API Reference](references/api-guide.md) <br>
- [Placed](https://placed.exidian.tech) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with shell commands and JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Calls the Placed API with a bearer token and may process resume text, job descriptions, and generated resume recommendations.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release evidence; artifact frontmatter is 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
