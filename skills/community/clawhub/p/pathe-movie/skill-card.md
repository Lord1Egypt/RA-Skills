## Description:

Looks up Pathé Netherlands movies, posters, descriptions, cinemas, and showtimes through Pathé JSON APIs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[humboldtjs](https://clawhub.ai/user/humboldtjs)

### License/Terms of Use:


## Use Case:

External users and agent operators use this skill to answer Pathé Netherlands movie questions, including title lookup, ratings, descriptions, posters, cinema availability, and showtimes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Movie and cinema queries are sent to Pathé's website.

Mitigation: Avoid sending sensitive or unrelated personal data in movie queries and disclose external network use when appropriate.

Risk: Default cinema behavior is centered on selected Netherlands venues.

Mitigation: Honor explicit user cinema requests when a different location is needed.

Risk: WhatsApp poster delivery may temporarily save public poster images locally.

Mitigation: Use temporary paths only for explicit media requests and clean up downloaded media after use.

## Reference(s):

- [Pathé API Reference](artifact/references/api.md)
- [Pathé JSON API](https://www.pathe.nl/api)

## Skill Output:

**Output Type(s):** [Text, Markdown, Files, Guidance]

**Output Format:** [Plain text or Markdown responses with optional local image file paths for poster delivery.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May temporarily save public poster or still images locally when WhatsApp media delivery is explicitly requested.]

## Skill Version(s):

1.0.0 (source: server release metadata and user changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
