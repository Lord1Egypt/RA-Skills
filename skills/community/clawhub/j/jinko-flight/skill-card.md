## Description:

Guide for using the Jinko CLI (@gojinko/cli), a terminal tool for searching flights, discovering destinations, managing trips, and booking travel.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kevinjinko](https://clawhub.ai/user/kevinjinko)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill when they want agent guidance for running Jinko CLI commands to search flights, compare fares, discover destinations, manage trips, and generate booking checkout links from a terminal.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill guides users to install and run a global npm executable.

Mitigation: Install @gojinko/cli only from a trusted package source and confirm that global executable installation is acceptable for the environment.

Risk: API keys and traveler or contact details can be exposed through command arguments, shell history, terminal recordings, or shared logs.

Mitigation: Prefer OAuth when possible, use JINKO_API_KEY or local configuration for headless use, and avoid pasting real credentials or traveler details into shared shells and logs.

Risk: Booking commands can generate payment checkout links after traveler and trip data are submitted.

Mitigation: Review flight, traveler, contact, trip, and price details before sending booking data or opening a payment checkout URL.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/kevinjinko/skills/jinko-flight)
- [Publisher profile](https://clawhub.ai/user/kevinjinko)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands, command options, JSON examples, and workflow steps.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guidance assumes the jinko and node binaries are available and either OAuth or JINKO_API_KEY authentication is configured.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
