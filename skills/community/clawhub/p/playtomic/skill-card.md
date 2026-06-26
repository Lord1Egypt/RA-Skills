## Description: <br>
This skill helps agents guide users through searching, booking, listing, and canceling Playtomic padel court reservations with the padel-tui CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[philipp-eisen](https://clawhub.ai/user/philipp-eisen) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to complete Playtomic padel court booking workflows from a terminal. The skill supports setup checks, interactive authentication, availability search, booking, active match listing, and requested cancellation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Installation commands and downloaded binaries can affect the user's environment. <br>
Mitigation: Confirm installation intent, prefer trusted or verified padel-tui releases, and verify the binary with `padel-tui --version` before use. <br>
Risk: Interactive login creates or retains local Playtomic session access. <br>
Mitigation: Use a trusted terminal, never pass credentials inline, and log out or remove the local session file when account access should no longer persist. <br>
Risk: Booking and cancellation commands can create reservations, charges, or account changes. <br>
Mitigation: Require explicit user intent and review tenant, court, start time, duration, player count, and match ID before running impactful commands. <br>


## Reference(s): <br>
- [Installation Reference](references/INSTALLATION.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/philipp-eisen/playtomic) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration] <br>
**Output Format:** [Markdown with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires interactive authentication and explicit user confirmation for installation, booking, and cancellation actions.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
