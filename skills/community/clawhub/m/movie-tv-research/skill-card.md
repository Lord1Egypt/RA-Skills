## Description:

Researches movies and TV shows — metadata, cast/crew, ratings, reviews, streaming availability, and box-office performance — via the Crawlora API across IMDb, TMDB, JustWatch, Letterboxd, Rotten Tomatoes, Metacritic, and Box Office Mojo, returning clean JSON. Use when the user asks about a title's cast, ratings/scores, where to stream it, critic or user reviews, or its box-office numbers.

This skill is ready for commercial/non-commercial use.

## Publisher:

[crawlora-org](https://clawhub.ai/user/crawlora-org)

### License/Terms of Use:

MIT-0

## Use Case:

Agents use this skill to answer requests about movie and TV metadata, cast and crew, ratings and reviews, streaming availability, and box-office results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Using the skill sends requests to Crawlora's external service with a Crawlora API key; the security review had partial scan coverage and medium confidence.

Mitigation: Review the skill and its data handling before use, keep the key in CRAWLORA_API_KEY, and check returned results against the cited source when accuracy matters.

## Reference(s):

- [Endpoint reference](artifact/reference/endpoints.md)
- [Crawlora](https://crawlora.net)
- [ClawHub skill page](https://clawhub.ai/crawlora-org/skills/movie-tv-research)

## Skill Output:

**Output Type(s):** [JSON, Guidance]

**Output Format:** [Normalized JSON containing movie and TV research results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Fields vary by title and source; some results are paginated.]

## Skill Version(s):

1.0.24 (source: server-resolved ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
