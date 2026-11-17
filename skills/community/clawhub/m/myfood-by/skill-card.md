## Description:

A food inventory and meal recommendation skill that records food items and optional expiry dates, checks inventory before recommending meals, flags existing and soon-expiring ingredients, and asks for dietary needs at request time instead of saving health-sensitive details.

This skill is ready for commercial/non-commercial use.

## Publisher:

[biyaoshang](https://clawhub.ai/user/biyaoshang)

### License/Terms of Use:


## Use Case:

External users use this skill to maintain a simple local food inventory, track expiry dates, and receive meal ideas that prioritize ingredients they already have. It is also useful for reducing food waste through soon-expiring item reminders.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill maintains a local food inventory file and removes items from it when the user says they are eaten.

Mitigation: Review inventory updates before relying on them and keep entries limited to food names and expiry dates.

Risk: Dietary restrictions or health needs could be unnecessarily recorded if the user enters them as inventory data.

Mitigation: Provide dietary needs only during recommendation requests and avoid saving private health details in inventory entries.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/biyaoshang/skills/myfood-by)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown or plain text responses with inventory summaries, meal recommendations, existing-ingredient labels, and expiry reminders.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update a local references/my-food.md inventory file for food names and optional expiry dates.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
