## Description:

Build a lean pantry restock list from current staples, upcoming meals, and real gaps without overbuying or making dietary assumptions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[harrylabsj](https://clawhub.ai/user/harrylabsj)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to turn a rough pantry inventory, upcoming meals, and household constraints into a lean restock list grouped by store aisle. It helps identify buy-now, check-before-buying, optional, and skip items without making dietary assumptions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill is limited to English and may not serve users who need pantry planning in another language.

Mitigation: Use it for English-language pantry planning unless a reviewer adds localized instructions and validates the output.

Risk: General grocery-list organization requests may activate the skill even when the user has not asked for a full pantry reset.

Mitigation: Confirm the intended scope when the request is broad, then produce only the list structure the user needs.

Risk: Dietary, allergy, religious, medical, or cultural assumptions could lead to unsuitable food suggestions.

Mitigation: Ask for allergies, avoid-list foods, dietary restrictions, and label needs before recommending substitutions, and remind users to check labels when relevant.

Risk: Incomplete pantry inventory, household size, budget, or storage details can cause overbuying or unnecessary items.

Mitigation: Request materially missing details, keep quantities modest by default, and separate must-buy items from optional extras.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/harrylabsj/skills/pantry-staple-reset)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown-style Pantry Reset List with categorized bullets, store aisle groups, and buy/check/skip sections]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Prompt-only; no code execution, network access, credentials, or API calls.]

## Skill Version(s):

1.0.1 (source: server release evidence and skill.json; SKILL.md frontmatter says 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
