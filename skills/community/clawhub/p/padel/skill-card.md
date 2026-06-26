## Description: <br>
Helps agents search, book, list, and cancel Playtomic padel court reservations through the padel-tui terminal CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[philipp-eisen](https://clawhub.ai/user/philipp-eisen) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to automate Playtomic padel court workflows from a terminal, including availability search, booking, active match listing, and cancellation after explicit confirmation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can install or run an external CLI. <br>
Mitigation: Ask for explicit approval before installation and use the existing local binary when installation is declined. <br>
Risk: Authentication creates a local session file. <br>
Mitigation: Use only the interactive terminal login flow and keep the local session file private. <br>
Risk: Booking or cancellation commands can affect real reservations. <br>
Mitigation: Confirm venue, time, duration, player count, or match ID before running booking or cancellation commands. <br>


## Reference(s): <br>
- [Installation Reference](references/INSTALLATION.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands that install, authenticate, book, or cancel should be presented for explicit user confirmation before execution.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
