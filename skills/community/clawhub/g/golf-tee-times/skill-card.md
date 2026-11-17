## Description:

Search for golf tee times and deals near any location. Find cheapest rounds, compare prices across platforms, and get discount tips. Use when asked about golf, tee times, courses, or booking a round.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tag-assistant](https://clawhub.ai/user/tag-assistant)

### License/Terms of Use:


## Use Case:

External users use this skill to find GolfNow tee-time availability, compare prices, identify hot deals or credit-bookable times, and format results for mobile-friendly sharing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill describes booking behavior that can access stored GolfNow credentials, saved payment cards, rewards, loyalty points, and reservation submission.

Mitigation: Use it as a search helper unless the booking flow is removed or tightly gated with explicit user approval for each account, reward, payment, and reservation action.

Risk: The skill can produce tee-time availability and pricing from a reverse-engineered GolfNow API, which may be incomplete or change without notice.

Mitigation: Treat returned availability and prices as advisory and verify them on GolfNow before purchase or reservation.

Risk: The skill describes sending checkout screenshots through Telegram, which can expose personal or payment-adjacent information.

Mitigation: Send screenshots only after explicit user approval and ensure they are scoped to the current user's transaction.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/tag-assistant/skills/golf-tee-times)
- [GolfNow](https://www.golfnow.com)
- [GolfNow tee-time results API endpoint](https://www.golfnow.com/api/tee-times/tee-time-results)
- [Publisher profile](https://clawhub.ai/user/tag-assistant)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Guidance]

**Output Format:** [Markdown, plain text, or JSON tee-time summaries with optional shell command usage]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results are based on facility-specific GolfNow queries and may include prices, times, course details, ratings, and deal indicators.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
