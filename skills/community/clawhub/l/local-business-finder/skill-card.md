## Description:

Find any local business by category and location on Google Maps, including names, phone numbers, emails, websites, ratings, and hours.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gmapsscraper](https://clawhub.ai/user/gmapsscraper)

### License/Terms of Use:

MIT-0

## Use Case:

External users and business operators use this skill to search for local businesses by category and location, confirm credit-consuming searches, and present Google Maps business profiles in a scannable format.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: User-provided business type or location text could be inserted literally into the documented curl JSON payload.

Mitigation: JSON-encode values and pass them to curl without shell interpolation before executing any generated command.

Risk: Business search queries are sent to gmapsscraper.io using the user's API key.

Mitigation: Use only when the user is comfortable sharing the search terms with gmapsscraper.io and understands the credit cost.

## Reference(s):

- [gmapsscraper homepage](https://gmapsscraper.io)
- [ClawHub skill page](https://clawhub.ai/gmapsscraper/skills/local-business-finder)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, API Calls, Markdown, Files]

**Output Format:** [Markdown guidance with bash code blocks and CSV file output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires curl and GMAPS_SCRAPER_API_KEY; searches consume credits and should be confirmed before execution.]

## Skill Version(s):

1.0.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
