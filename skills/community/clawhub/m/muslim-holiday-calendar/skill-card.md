## Description:

Provides a local Islamic holiday calendar lookup for major observances such as Ramadan, Eid al-Fitr, Eid al-Adha, Islamic New Year, Mawlid al-Nabi, and Arafat Day, with bilingual English and Chinese skill documentation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[darbling](https://clawhub.ai/user/darbling)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers can use this skill to ask an agent for command-line guidance or code-oriented assistance with listing stored Islamic holiday dates, finding the next known holiday, checking countdowns, and retrieving basic holiday information. It is suitable for lightweight calendar lookup workflows that can tolerate a static date table.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security summary reports that the release advertises Hijri conversion and Ashura support that the code does not provide.

Mitigation: Describe the skill as a static holiday lookup unless those capabilities are implemented and validated.

Risk: The security guidance says the holiday data is an incomplete static lookup for a few Islamic holidays from 2024-2030.

Mitigation: Check a trusted calendar source before using results for Hijri conversion, Ashura dates, or important observance planning.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/darbling/skills/muslim-holiday-calendar)
- [Publisher profile](https://clawhub.ai/user/darbling)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, guidance]

**Output Format:** [Markdown or plain text with shell command examples and JSON-oriented command output guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The bundled script returns JSON for supported commands and uses a static holiday dataset covering 2024-2030.]

## Skill Version(s):

1.1.0 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
