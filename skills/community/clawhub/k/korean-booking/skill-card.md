## Description: <br>
Korean Booking helps users find Korean beauty and medical-aesthetic clinics, review booking options, open BeautsGO clinic, price, and support pages, and submit appointment requests after collecting booking details. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[beautsgo](https://clawhub.ai/user/beautsgo) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users use this skill to search for Korean beauty or medical-aesthetic clinics, get appointment guidance, open relevant BeautsGO pages, and submit booking requests. Agents can use it in multi-turn conversations that collect clinic, party size, appointment time, and contact details before submission. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Appointment submission can send contact information and cosmetic or medical-service intent to BeautsGO. <br>
Mitigation: Collect and submit details only after explicit user intent; verify clinic, date, contact information, and destination domain before submission. <br>
Risk: Browser and command automation can open third-party pages or local browser processes. <br>
Mitigation: Keep browser actions user-visible, restrict use to documented BeautsGO domains, and do not run debug or sync scripts unless their local effects are understood. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/beautsgo/korean-booking) <br>
- [README](README.md) <br>
- [Multi-turn flow documentation](docs/multi-turn-flow.md) <br>
- [Consult automation documentation](docs/consult-automation.md) <br>
- [BeautsGO](https://beautsgo.com) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance, API Calls, Shell commands] <br>
**Output Format:** [Markdown text and status messages for booking guidance, browser-opening actions, and appointment submission results.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports zh, en, ja, and th; may open BeautsGO pages and submit user-provided appointment details to BeautsGO.] <br>

## Skill Version(s): <br>
2.6.8 (source: SKILL.md frontmatter and server release evidence; package.json reports 2.1.7) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
