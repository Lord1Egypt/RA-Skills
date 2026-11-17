## Description:

This skill helps agents analyze and reproduce Kuaishou Genius management-yearly actuals API flows, including endpoint mapping, session-aware probing, payload reconstruction, and concise reporting.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhangpei03](https://clawhub.ai/user/zhangpei03)

### License/Terms of Use:

MIT-0

## Use Case:

Authorized developers and engineers use this skill to map Kuaishou Genius Actual budget portal endpoints, replay approved read-only checks with valid sessions, reconstruct required request payloads, and report blockers or limitations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow reuses live corporate login cookies for an internal financial portal.

Mitigation: Use it only with explicit authorization, protect session material, and never paste live SSO cookies into shared terminals, CI logs, tickets, screenshots, or shell history.

Risk: Probing the wrong host or using weak transport settings could expose sensitive session or budget data.

Mitigation: Restrict use to the approved HTTPS host and avoid disabling TLS verification.

Risk: Placeholder POST payloads may not match the current business schema or permission scope.

Mitigation: Treat generated calls as read-only analysis aids and validate payload fields against a fresh browser network capture before use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zhangpei03/skills/kuaishou-genius-actual)
- [Kuaishou Genius base URL](https://genius.corp.kuaishou.com)
- [Kuaishou Genius Actual page](https://genius.corp.kuaishou.com/management-yearly/actual)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands, Python command examples, endpoint tables, and JSON payload guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May reference local helper scripts and sample JSON payloads; requires an authorized live session cookie for probing.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
