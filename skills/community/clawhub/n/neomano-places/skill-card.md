## Description: <br>
Search Google Places (Places API New) for real-world places, businesses, restaurants, and nearby recommendations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[elandivar](https://clawhub.ai/user/elandivar) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to find real-world places, restaurants, businesses, reviews, ratings, addresses, and Google Maps links through Google Places. It supports text search, location bias, open-now filtering, minimum rating filters, and concise ranked recommendations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a Google Places API key and sends place-search queries to Google Places. <br>
Mitigation: Install only in trusted repositories, restrict the key to Places API and by IP where possible, and avoid sending sensitive query or location details unless appropriate. <br>
Risk: Place recommendations can be weak or ambiguous when returned results have limited ratings, reviews, or relevance. <br>
Mitigation: Prefer concrete results with stronger ratings and review counts, and clearly state when results are weak instead of guessing. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/elandivar/neomano-places) <br>
- [Google Places API endpoint](https://places.googleapis.com) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown bullets for user-facing recommendations, with optional JSON from the helper script] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3 and GOOGLE_PLACES_API_KEY; supports query, limit, latitude, longitude, radius, open-now, minimum-rating, and JSON output options.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
