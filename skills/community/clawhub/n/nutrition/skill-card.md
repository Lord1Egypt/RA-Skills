## Description:

Closes micronutrient gaps and raises diet quality across vitamins, minerals, fiber, supplements, and food-drug interactions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ivangdavila](https://clawhub.ai/user/ivangdavila)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to assess micronutrient adequacy, diet quality, supplement choices, label interpretation, food-drug interactions, and nutrition considerations for diet patterns, life stages, symptoms, labs, and health conditions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can keep sensitive health and nutrition notes as local plaintext under ~/Clawic/data/ and share some health facts with other health-adjacent skills.

Mitigation: Use it only on trusted machines and storage, avoid synced or shared locations when possible, and regularly review or delete saved notes that are no longer needed.

Risk: Portal exports or pasted health records may include sensitive identifiers even when credentials are stripped.

Mitigation: Avoid pasting highly sensitive identifiers unless necessary, and check saved files after use to confirm only intended medical facts were retained.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/ivangdavila/skills/nutrition)
- [Clawic Skill Page](https://clawic.com/skills/nutrition)

## Skill Output:

**Output Type(s):** [text, markdown, guidance, configuration]

**Output Format:** [Markdown guidance with structured local note updates when durable nutrition facts are produced]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May read and update local plaintext nutrition and shared health notes under configured Clawic paths.]

## Skill Version(s):

1.0.2 (source: frontmatter and server release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
