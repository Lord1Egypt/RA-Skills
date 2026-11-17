## Description:

Searches Marriott Bonvoy hotels on marriott.com.cn, presents hotel, room, and rate options, and can submit a reservation after user confirmation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[qianjunye](https://clawhub.ai/user/qianjunye)

### License/Terms of Use:


## Use Case:

Travelers and booking assistants use this skill to search Marriott hotels in China, compare available rooms and rates, and complete a reservation only after the user confirms the final selection.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill controls a logged-in Marriott browser session and may leave copied cookies, screenshots, booking selections, and confirmation data on disk.

Mitigation: Use a dedicated Marriott-only browser profile, avoid copying a primary Chrome profile, and remove cookies, screenshots, and debug files after use.

Risk: The skill can submit real hotel reservations after the user confirms a selected room and rate.

Mitigation: Manually verify the hotel, room, rate, cancellation policy, total price, dates, guest details, and payment method before approving reservation submission.

Risk: Automated browsing may be blocked or produce stale room and price information.

Mitigation: Treat displayed availability as provisional and retry or verify directly in the browser when access is blocked or results look inconsistent.

## Reference(s):

- [ClawHub Marriott skill page](https://clawhub.ai/qianjunye/skills/marriott)
- [Publisher profile: qianjunye](https://clawhub.ai/user/qianjunye)
- [Marriott China](https://www.marriott.com.cn)
- [Marriott China sign-in](https://www.marriott.com.cn/sign-in.mi)
- [OpenStreetMap Nominatim search](https://nominatim.openstreetmap.org/search)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, guidance]

**Output Format:** [Markdown summaries and tables backed by JSON script results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes hotel search results, room and rate comparisons, booking summaries, confirmation details, and troubleshooting guidance.]

## Skill Version(s):

1.0.0 (source: release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
