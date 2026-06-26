## Description: <br>
Use medical cv resume builder for academic writing workflows that need structured execution, explicit assumptions, and clear output boundaries. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aipoch-ai](https://clawhub.ai/user/aipoch-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to structure medical CVs or resumes from provided education and experience details. It emphasizes explicit assumptions, bounded scope, reproducible output, and fallback handling when inputs are incomplete. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Security evidence flags unresolved scope-boundary issues and overbroad activation language. <br>
Mitigation: Use only for medical CV or resume structuring, refuse out-of-scope academic writing or medical advice requests, and confirm missing required inputs before generation. <br>
Risk: Artifact audit evidence records a stress-case scope-control failure and weak boundary handling. <br>
Mitigation: Require education and experience inputs, state assumptions explicitly, and stop rather than widening the task when the request lacks critical context. <br>
Risk: Packaged execution examples and fallback behavior may need review before deployment. <br>
Mitigation: Run the documented compile and script checks in a sandboxed workspace and review generated outputs before sharing them. <br>


## Reference(s): <br>
- [Medical CV/Resume Builder - References](references/guidelines.md) <br>
- [ClawHub skill page](https://clawhub.ai/aipoch-ai/medical-cv-resume-builder) <br>
- [Publisher profile](https://clawhub.ai/user/aipoch-ai) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, JSON, Code, Shell commands, Guidance] <br>
**Output Format:** [Markdown guidance and JSON containing cv_markdown, sections, and type fields] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces structured CV or resume content from education, experience, and optional type inputs; final outputs should call out assumptions, risks, and unresolved items when relevant.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
