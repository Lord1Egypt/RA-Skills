## Description:

Guides authorized users through capturing and analyzing their own logged-in browser HAR, extracting minimal auth material, mapping a website action's request chain, and turning the known-good workflow into a reusable local script.

This skill is ready for commercial/non-commercial use.

## Publisher:

[stanestane](https://clawhub.ai/user/stanestane)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to reproduce web actions they are already authorized to perform, such as upload, publish, schedule, or queue workflows, when direct authenticated requests are more reliable than browser automation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles live browser-session credentials and HAR files that may grant account access.

Mitigation: Keep HARs and generated auth files local, out of chat, source control, sync folders, logs, and shared workspaces; retain only the minimum auth material needed.

Risk: Generated replay scripts can expose sensitive request data or perform unintended account actions.

Mitigation: Review generated Python before running it, test one item first, and compare failures against the captured HAR instead of guessing.

Risk: Replaying private web calls may violate site terms, break without notice, or trigger rate limits, account locks, or challenges.

Mitigation: Use only workflows the user is authorized to perform, avoid bypass or brute-force behavior, keep batches small, and refresh expired credentials through the normal browser session.

## Reference(s):

- [HAR capture checklist](references/har-capture-checklist.md)
- [Auth materials](references/auth-materials.md)
- [Request analysis patterns](references/request-analysis-patterns.md)
- [Common web flows](references/common-web-flows.md)
- [Safety boundaries](references/safety-boundaries.md)

## Skill Output:

**Output Type(s):** [Guidance, Analysis, Code, Shell commands, Configuration instructions, Files]

**Output Format:** [Markdown guidance with shell command examples and generated Python or JSON files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce local auth-material files, filtered HAR request summaries, request-shape diffs, and first-pass replay scripts for user review.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
