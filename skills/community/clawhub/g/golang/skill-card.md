## Description:

Records, searches, and exports local Go development notes through shell commands; it does not perform Go builds, tests, linting, or formatting itself.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bytesagain3](https://clawhub.ai/user/bytesagain3)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers can use this skill to keep timestamped local records of Go-related checks, lint notes, formatting notes, code generation notes, and review findings, then search or export those records for later review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill stores development notes in local plaintext logs and exports that may contain sensitive details.

Mitigation: Do not enter secrets, tokens, proprietary source snippets, or sensitive incident details; review generated CSV, JSON, and text exports before sharing.

Risk: The skill is presented as Go build, test, lint, and format tooling, but the security evidence says it records entries rather than executing those Go workflows.

Mitigation: Treat outputs as journal entries and run actual Go build, test, lint, and formatting tools separately before relying on technical results.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/bytesagain3/skills/golang)
- [BytesAgain homepage](https://bytesagain.com)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Files, Configuration, Guidance]

**Output Format:** [Plain text with shell command examples and local log or export files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes plaintext logs and JSON, CSV, or text exports under ~/.local/share/golang/.]

## Skill Version(s):

2.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
