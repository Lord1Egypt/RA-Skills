## Description:

Microservice Gen provides command-line workflows for recording, searching, and exporting development activity such as generation, validation, linting, formatting, review, and reporting notes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xueyetianya](https://clawhub.ai/user/xueyetianya)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers can use this skill to capture microservice-related development notes, command inputs, checks, diffs, fixes, reports, and exports during local workflows. Security evidence says the actual package behaves as a local activity journal, so users should evaluate that behavior before relying on advertised generation claims.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Security evidence states that the package is advertised as a Go Zero microservices helper but behaves as a local activity journal.

Mitigation: Review the installed commands and expected outputs before using the skill in a development workflow.

Risk: Security guidance warns that user inputs may be stored locally in plaintext under ~/.local/share/microservice-gen and later exported.

Mitigation: Do not enter secrets, proprietary code, credentials, incident details, or sensitive configuration unless plaintext local retention and export are acceptable.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/xueyetianya/skills/microservice-gen)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance, Configuration]

**Output Format:** [Markdown with inline shell commands and command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include locally retained activity entries and exports in JSON, CSV, or plain text.]

## Skill Version(s):

1.0.0 (source: release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
