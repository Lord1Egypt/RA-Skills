## Description: <br>
Analyzes form fields on a live webpage using browser automation when the user provides an online URL. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[EvalGitHub](https://clawhub.ai/user/EvalGitHub) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, QA engineers, and product teams use this skill to inspect an online page and summarize the page's form fields by type and total count. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Browser access may load authenticated, internal, or sensitive pages if the user provides them. <br>
Mitigation: Use trusted URLs where possible, avoid localhost, internal, or sensitive sites unless intended, and prefer a separate browser profile for pages requiring login. <br>
Risk: Dynamic, hidden, collapsed, or tabbed form sections can lead to incomplete field counts. <br>
Mitigation: Wait for single-page applications to finish loading and expand relevant tabs or sections before relying on the count. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance] <br>
**Output Format:** [Markdown table with totals and notes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Counts visible or discoverable form fields by category and may include observations about page structure.] <br>

## Skill Version(s): <br>
0.0.1 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
