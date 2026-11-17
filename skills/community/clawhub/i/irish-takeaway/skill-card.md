## Description:

Find nearby takeaways in Ireland and browse menus via Deliveroo/Just Eat. Uses Google Places API for discovery and browser automation for menu scraping.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cotyledonlab](https://clawhub.ai/user/cotyledonlab)

### License/Terms of Use:


## Use Case:

External users and agents use this skill to find Irish takeaway restaurants by location, cuisine, rating, or open status, then browse menu information from supported delivery platforms.

### Deployment Geography for Use:

Ireland

## Known Risks and Mitigations:

Risk: The skill sends location text and search intent to Google Places, Deliveroo, or Just Eat.

Mitigation: Use only locations and queries that are acceptable to share with those third-party services.

Risk: The skill depends on a Google Places API key and the external goplaces CLI.

Mitigation: Protect the API key, review or pin the goplaces install source, and confirm the dependency before deployment.

## Reference(s):

- [Irish Takeaway Finder ClawHub listing](https://clawhub.ai/cotyledonlab/skills/irish-takeaway)
- [cotyledonlab publisher profile](https://clawhub.ai/user/cotyledonlab)
- [Deliveroo Ireland](https://deliveroo.ie/)
- [Just Eat Ireland](https://www.just-eat.ie/)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown with inline shell commands and structured restaurant or menu summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires goplaces, GOOGLE_PLACES_API_KEY, and browser access for menu browsing.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
