## Description:

Search Google Places (Places API New) for real-world places, businesses, restaurants, and nearby recommendations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[elandivar](https://clawhub.ai/user/elandivar)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agent developers use this skill to look up places, restaurants, businesses, addresses, ratings, review counts, and map links from Google Places. It supports practical local recommendations with optional location bias, open-now filtering, and minimum rating filters.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Place queries and provided coordinates are sent to Google and may affect API usage or billing.

Mitigation: Use a restricted Google Places API key and avoid sending sensitive or unnecessary location data.

Risk: The skill depends on external Google Places data and API availability, so results can be incomplete, unavailable, or change over time.

Mitigation: Present outputs as current lookup results, include ratings and address context when available, and avoid guessing when results are weak or ambiguous.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/elandivar/skills/neomano-places)
- [Google Places API endpoint](https://places.googleapis.com)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown bullets or JSON from the bundled place-search script]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires GOOGLE_PLACES_API_KEY and may include place names, ratings, addresses, review counts, and Google Maps links.]

## Skill Version(s):

1.0.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
