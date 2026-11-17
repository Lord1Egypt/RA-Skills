## Description:

Turns supplied reports, whitepapers, or benchmark studies into grounded interactive digital-human briefing courses with voice-question support.

This skill is ready for commercial/non-commercial use.

## Publisher:

[personwiseai](https://clawhub.ai/user/personwiseai)

### License/Terms of Use:

MIT-0

## Use Case:

Employees, external educators, analysts, and communications teams use this skill to turn supplied report materials into an interactive briefing course that preserves the report's evidence, methods, and limitations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may install or update persistent PersonWise CLI software.

Mitigation: Review install and update prompts before approval, and approve only the intended PersonWise CLI action.

Risk: The workflow uses browser OAuth and may consume existing course credits through account actions.

Mitigation: Sign in only through the browser OAuth flow, use the intended account, and expect course credits to be consumed for created courses.

Risk: Report materials may be uploaded and courses may become accessible beyond the creator if broader access is requested.

Mitigation: Upload only intentionally selected reports and keep courses private unless link access, publication, or Topics submission is explicitly requested.

Risk: Security evidence reports an expired signed service descriptor in the artifact.

Mitigation: Review current trust and update status before use, and rely on current service or CLI validation before business actions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/personwiseai/skills/personwise-report-briefing)
- [PersonWise service](https://personwise.ai)
- [PersonWise CLI release origin](https://releases.personwise.ai/cli/)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with JSON command inputs and structured CLI responses.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces a PersonWise interactive digital-human briefing course from supplied report materials, with status details and the appropriate private or share URL after successful creation.]

## Skill Version(s):

2.1.9 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
