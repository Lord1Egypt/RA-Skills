## Description:

Hotel Pricer helps agents search hotel availability and pricing by city, dates, guests, and radius through the Amadeus Self-Service API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jrojas537](https://clawhub.ai/user/jrojas537)

### License/Terms of Use:


## Use Case:

Agents and developers use this skill to retrieve hotel availability and pricing for a city and stay window, returning formatted hotel offer data for travel planning workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Amadeus API keys and secrets may be exposed through command-line arguments, shell history, or plaintext config backups.

Mitigation: Avoid entering production secrets in reusable shell commands, inspect shell history and backups, and rotate Amadeus credentials if exposure is possible.

Risk: Cached OAuth tokens and credentials are stored under ~/.config/hotel-pricer/config.yaml with weak disclosure of local file protections.

Mitigation: Restrict permissions on the config file and prefer a user-local install path so the skill does not require sudo-managed deployment.

## Reference(s):

- [Amadeus for Developers](https://developers.amadeus.com/)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration]

**Output Format:** [JSON]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Amadeus API credentials; hotel search accepts city, check-in date, check-out date, guests, and search radius.]

## Skill Version(s):

1.1.1 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
