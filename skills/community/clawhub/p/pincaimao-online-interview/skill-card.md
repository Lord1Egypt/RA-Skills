## Description:

聘才猫（Pincaimao）在线面试 helps agents conduct multi-turn Pincaimao Online Interview API sessions for text or video interviews with custom questions and report callbacks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pincaimao](https://clawhub.ai/user/pincaimao)

### License/Terms of Use:

MIT-0

## Use Case:

External users and recruiting teams use this skill to run text or video AI interview sessions through Pincaimao, preserving conversation context across turns and optionally generating callback reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Applicant resumes, interview answers, videos, and generated reports may contain sensitive candidate data.

Mitigation: Use the skill only when Pincaimao is an approved processor for that data, and share only candidate materials intended for the interview workflow.

Risk: Report callbacks can send sensitive generated reports to a caller-provided URL.

Mitigation: Set url_callback only to an endpoint you control and trust, or omit it when callback delivery is not required.

Risk: The skill depends on pincaimao-basic, but the security evidence flags that dependency as unspecified.

Mitigation: Confirm the source and contents of pincaimao-basic before installing or loading it.

Risk: API keys and returned COS object keys grant access to interview workflow resources.

Mitigation: Keep PCM_ONLINE_INTERVIEW_KEY in the environment, avoid hardcoding it, and treat returned cos_key values as sensitive.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/pincaimao/skills/pincaimao-online-interview)
- [Pincaimao homepage](https://www.pincaimao.com)
- [Pincaimao API base endpoint](https://api.pincaimao.com)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with bash examples, readable interview responses, or raw API response text when requested.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports blocking and streaming response handling; raw output mode preserves API response content.]

## Skill Version(s):

1.0.1 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
