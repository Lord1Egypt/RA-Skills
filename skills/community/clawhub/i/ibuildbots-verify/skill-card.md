## Description:

Run your agent against 5 real prompt-injection attacks and get a local report of what it actually did: credential leak, metric fabrication, false-halt, runaway spend, and log falsification.

This skill is ready for commercial/non-commercial use.

## Publisher:

[weldog](https://clawhub.ai/user/weldog)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent builders use this skill to run a local robustness self-diagnostic against prompt-injection scenarios and review pass/fail behavior from observed agent outputs and files. The local report is for QA and must not be presented as a signed third-party verification badge.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill directs users to clone and run a mutable external GitHub harness that is outside the reviewed package.

Mitigation: Review the cloned repository before execution, pin it to a trusted commit, and run it in a restricted sandbox.

Risk: The harness runs the user's agent as a subprocess and observes outputs, files, logs, timeouts, and local report data.

Mitigation: Run with minimal files, credentials, environment variables, and network access, and set a practical timeout for each pass.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/weldog/skills/ibuildbots-verify)
- [ibuildbots harness repository](https://github.com/Weldog/ibuildbots)
- [ibuildbots Verified tier](https://ibuildbots.dev)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, Markdown, JSON]

**Output Format:** [Markdown guidance with shell commands and a JSON report example]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3 and git; the harness writes a local state.json report.]

## Skill Version(s):

2.1.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
