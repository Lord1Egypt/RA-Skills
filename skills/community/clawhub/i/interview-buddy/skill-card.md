## Description:

AI-powered mock interview practice with real-time feedback. Use when preparing for job interviews, practicing behavioral questions, doing technical interview prep, conducting mock interviews, or getting interview coaching for any role or industry.

This skill is ready for commercial/non-commercial use.

## Publisher:

[krishnakumarmahadevan-cmd](https://clawhub.ai/user/krishnakumarmahadevan-cmd)

### License/Terms of Use:

MIT-0

## Use Case:

External users and employees use this skill through an OpenClaw agent to practice interviews, receive role-specific questions, and get feedback on answers across behavioral, technical, product, case-study, situational, and leadership formats.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends email, OTP flow details, role and company details, interview answers, and other interview-prep content to ToolWeb.

Mitigation: Use it only with content the user is comfortable sharing with ToolWeb, and avoid confidential employer, customer, project, or proprietary information.

Risk: Successful API calls may consume paid ToolWeb quota.

Mitigation: Confirm user consent before starting an external session or making repeated API calls.

Risk: User-provided interview text is shown in shell command examples.

Mitigation: Serialize request bodies safely before execution instead of interpolating raw user text into shell commands.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/krishnakumarmahadevan-cmd/skills/interview-buddy)
- [Publisher Profile](https://clawhub.ai/user/krishnakumarmahadevan-cmd)
- [ToolWeb Portal](https://portal.toolweb.in)
- [Interview Buddy API Endpoint](https://portal.toolweb.in/apis/tools/interview-buddy)
- [Artifact README](artifact/README.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown-style interview prompts, answer feedback, coaching tips, ratings, and follow-up questions, with shell command examples for API use.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires TOOLWEB_API_KEY and curl; API access may consume ToolWeb quota.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
