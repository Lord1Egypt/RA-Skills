## Description:

换热器CAD图纸生成。当用户说"换热器"、"生成换热器图纸"、"做一个换热器"、"heat-exchanger"时使用此 skill。

This skill is ready for commercial/non-commercial use.

## Publisher:

[liv09370](https://clawhub.ai/user/liv09370)

### License/Terms of Use:

MIT-0

## Use Case:

External users and mechanical engineers use this skill to collect heat-exchanger design parameters, submit them to jixietools.com, review calculated values, and create a guest CAD drawing production sheet.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Proprietary CAD or engineering inputs may be sent to jixietools.com.

Mitigation: Use only inputs that are approved for sharing with that third-party service, and get clear user consent before submission.

Risk: Guest links or guest codes may expose job status or generated files to anyone who receives them.

Mitigation: Treat guest URLs and codes as sensitive, share them only with intended recipients, and avoid submitting confidential projects through unauthenticated guest flows.

Risk: User-provided values are inserted into shell command examples for JSON API requests.

Mitigation: Serialize JSON safely when adapting the workflow, and review commands before execution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/liv09370/skills/heat-exchanger)
- [jixietools.com API base URL](https://jixietools.com/api/v1)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, API calls, Guidance]

**Output Format:** [Chinese-language conversational guidance with Markdown tables, inline shell commands, and JSON-shaped API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guides one parameter at a time, preserves the calculation filename across iterations, creates a guest production link, and polls job status.]

## Skill Version(s):

1.0.1 (source: server release metadata; artifact frontmatter says 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
