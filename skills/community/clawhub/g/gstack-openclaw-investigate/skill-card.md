## Description: <br>
Provides systematic root cause analysis and verified fixes for bugs or errors using a four-phase debugging process without guessing or premature fixes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[garrytan](https://clawhub.ai/user/garrytan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to investigate bugs, stack traces, and unexpected behavior through a disciplined root-cause workflow before implementing a verified fix. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Debugging evidence can contain secrets, customer data, private file paths, or sensitive logs, especially when the workflow uses external search or saved memory reports. <br>
Mitigation: Configure the agent to redact sensitive data before search or saved reports, or disable memory writes when handling private or production code. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/garrytan/gstack-openclaw-investigate) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/garrytan) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, shell commands] <br>
**Output Format:** [Markdown with inline code and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces root-cause hypotheses, verification steps, implementation guidance, and structured debug reports.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
