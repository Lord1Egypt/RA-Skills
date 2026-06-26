## Description: <br>
Automates E-Pai-Ke restaurant reservation workflows, including login, shop search, wait-status checks, bookings, and cancellations for Kura Sushi and other restaurants that use E-Pai-Ke. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dabendan2](https://clawhub.ai/user/dabendan2) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to manage E-Pai-Ke restaurant reservations: signing in, finding stores, checking wait status, making bookings, and cancelling reservations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill gives an agent access to an E-Pai-Ke account and authority to make or cancel live reservations. <br>
Mitigation: Require the agent to display the restaurant, date, time, party size, and reservation record, then wait for explicit user approval before any final booking or cancellation confirmation. <br>
Risk: Account credentials may be needed for login and could be exposed if stored in plaintext notes. <br>
Mitigation: Avoid plaintext credential storage and provide credentials only through a controlled secret or interactive login flow. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/dabendan2/kura-booking) <br>
- [E-Pai-Ke](https://e-pai-ke.com/) <br>
- [E-Pai-Ke Reservations](https://e-pai-ke.com/reservationA) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Code, Shell commands] <br>
**Output Format:** [Markdown with inline JavaScript and shell-command guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May direct an agent to use browser automation or Playwright for account login, booking, status checks, and cancellation workflows.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
