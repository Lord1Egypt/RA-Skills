## Description: <br>
Structured interview assistant that generates STAR interview questions from a job description and optional resume. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wanwan2qq](https://clawhub.ai/user/wanwan2qq) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
HR teams, recruiters, and hiring managers use this skill to turn job descriptions and optional resumes into structured STAR interview questions, scoring rubrics, and candidate-role matching summaries. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill delegates execution to an unpinned global `interview-assistant` executable that is not included in the artifact. <br>
Mitigation: Verify the executable source, version, and behavior before use, or require a pinned package or source release for review. <br>
Risk: Job descriptions and resumes may contain sensitive hiring or candidate information. <br>
Mitigation: Use only in an approved environment and avoid submitting real candidate materials until the executable and data handling behavior have been reviewed. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/wanwan2qq/interview-assistant) <br>
- [Publisher Profile](https://clawhub.ai/user/wanwan2qq) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, guidance] <br>
**Output Format:** [Markdown, JSON, or text from a CLI command] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces interview questions, matching analysis, STAR scoring guidance, and summaries based on user-provided job descriptions and optional resumes.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
