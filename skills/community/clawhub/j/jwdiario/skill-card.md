## Description:

Jwdiario retrieves the current Spanish daily text from the official Jehovah's Witnesses Watchtower Online Library page and presents the Bible citation, explanation, and source link without translation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[djismgaming](https://clawhub.ai/user/djismgaming)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to fetch and present the current Spanish JW daily text from wol.jw.org/es. The skill is intended for requests such as showing the JW daily text, daily Bible content, or the Spanish text for today.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security scan reports that the shipped Node script invokes shell-based curl even though the skill instructions describe safer web fetching.

Mitigation: Review before installing; prefer removing shell execution or tightly scoping and documenting the fixed public source domain.

Risk: The skill depends on the availability and page structure of wol.jw.org/es, so output can fail or become incomplete if the source page changes.

Mitigation: Validate output against the official page during deployment and keep failures visible to the user instead of silently fabricating daily text.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/djismgaming/skills/jwdiario)
- [Watchtower Online Library Spanish daily text](https://wol.jw.org/es/wol/h/r4/lp-s)
- [Watchtower Online Library Spanish home](https://wol.jw.org/es/)

## Skill Output:

**Output Type(s):** [text, markdown]

**Output Format:** [Markdown text with the daily passage, explanation, and source link]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Spanish-language content is presented from the source without translation.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
