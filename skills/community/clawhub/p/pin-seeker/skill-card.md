## Description:

Find golf tee times, hot deals, and cheapest rounds by city, ZIP, or course name.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rkrishnakumar](https://clawhub.ai/user/rkrishnakumar)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to search public GolfNow tee-time inventory by natural-language location, date, party size, and course preferences, then present a shortlist with GolfNow links for the user to book separately.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Tee-time searches send details such as location, date, party size, and timezone to Pin Seeker's hosted service.

Mitigation: Only send the details needed for the search and avoid including unrelated personal or sensitive information.

Risk: Search results are not reservations and may be mistaken for a booked or held tee time.

Mitigation: Present results as availability links only, state that Pin Seeker cannot reserve times, and direct the user to complete booking on GolfNow.

Risk: The skill depends on a hosted API and current third-party tee-time inventory.

Mitigation: Report API failures or missing results plainly and avoid fabricating availability, prices, or booking status.

## Reference(s):

- [Pin Seeker Agent Homepage](https://pinseeker.xyz/agents.html)
- [Pin Seeker ClawHub Skill Page](https://clawhub.ai/rkrishnakumar/skills/pin-seeker)
- [Pin Seeker Hosted Search API](https://pinseeker.xyz/api/agent/search)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown/text shortlist with course, time, price, available spots, and GolfNow links; the hosted API returns JSON with a text field for agent replies.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results are informational only and do not book, hold, reserve, or pay for tee times.]

## Skill Version(s):

1.0.5 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
