## Description: <br>
Hotel Booking AI helps agents search hotels, compare live room rates, create bookings, check or cancel orders, and initiate payment after explicit user confirmation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tourmind](https://clawhub.ai/user/tourmind) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users and travel-booking agents use this skill to complete hotel search, room-rate verification, booking creation, payment initiation, booking lookup, and cancellation workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles payments, guest data, and hotel booking actions. <br>
Mitigation: Use it only for explicit booking, payment, lookup, or cancellation requests, and confirm booking references and payment choices before taking irreversible actions. <br>
Risk: A reusable user_key is stored locally and used for authentication. <br>
Mitigation: Treat the user_key like a password, avoid shared machines, and rotate or revoke it if it may have been exposed. <br>
Risk: Booking and credential data are sent to a non-HTTPS endpoint. <br>
Mitigation: Use the skill only when the publisher and booking API are trusted, and avoid untrusted networks. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/tourmind/hotel-booking-ai) <br>
- [B2B Booking Skill - Parameter Reference](references/parameter_guide.md) <br>
- [AgentAuth Dashboard](https://aauth-170125614655.asia-northeast1.run.app/dashboard) <br>


## Skill Output: <br>
**Output Type(s):** [Text, API calls, Guidance] <br>
**Output Format:** [Plain text or Markdown with booking details, API-derived results, and payment links] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a locally stored user_key and live booking API responses; the skill should not fabricate hotel, room, price, or policy data.] <br>

## Skill Version(s): <br>
0.2.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
