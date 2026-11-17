## Description:

Finds discounted local Groupon deals for services and activities such as automotive, wellness, dining, fitness, entertainment, and home services by city and category.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dejimarquis](https://clawhub.ai/user/dejimarquis)

### License/Terms of Use:

MIT

## Use Case:

External users and agents use this skill to search Groupon for local discounts, compare deal options, and summarize prices, discounts, ratings, locations, fine print, and links.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad discount or activity-planning requests may be narrowed to Groupon results even when broader recommendations would be useful.

Mitigation: Ask whether the user wants Groupon-only results or broader options before limiting the search.

Risk: Groupon inventory, prices, availability, and fine print can change or deals can expire.

Mitigation: Check the current listing and fine print before presenting a deal as available or advising a user to purchase.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/dejimarquis/skills/groupon-skill)
- [Artifact README](artifact/README.md)
- [Skill instructions](artifact/skill.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown or plain text deal summaries with Groupon links and extracted deal fields]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include prices, discounts, merchant names, ratings, locations, fine print, and availability notes when found.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
