## Description:

Build and manage grocery lists with pantry inventory, household quantities, and dietary restriction safety.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ivangdavila](https://clawhub.ai/user/ivangdavila)

### License/Terms of Use:


## Use Case:

External users use this skill to keep shopping lists, pantry notes, household quantities, preferred stores, and dietary restrictions organized for grocery trips. It focuses on what to buy and avoids meal planning, purchasing, price lookup, barcode scanning, and receipt scanning.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Local grocery notes can contain household, pantry, store preference, and dietary restriction information.

Mitigation: Keep ~/grocery local and access-controlled, avoid storing medical-level allergy details unless the user accepts that local storage risk, and ask for confirmation before clearing or starting a list fresh.

## Reference(s):

- [Grocery skill page](https://clawhub.ai/ivangdavila/skills/grocery)
- [List operations](artifact/lists.md)
- [Memory setup](artifact/memory-template.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with shopping lists, local file setup commands, and concise guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May use local markdown files under ~/grocery for memory, pantry, store, and purchase-history notes.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
