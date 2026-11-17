## Description:

Generate tourism itinerary DOCX by replacing only matched itinerary sections inside a provided Chinese template document.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nnswjlll](https://clawhub.ai/user/nnswjlll)

### License/Terms of Use:


## Use Case:

Travel-agency operators or agent users use this skill to turn simplified Chinese day-by-day route notes into a styled itinerary DOCX while updating schedule, scenic descriptions, meals, and hotels.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The default workflow can remove tables and contract-like sections from the output document.

Mitigation: Use the skill only on copies of templates, run the script with --keep-contract when preserving contract content, and compare the generated DOCX against the original before external use.

Risk: The script is tuned to a specific template layout, so changed paragraph anchors can produce incomplete or misplaced itinerary updates.

Mitigation: Test each new template layout with representative input and manually review all itinerary, table, and terms sections before sharing the result.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/nnswjlll/skills/itinerary-docx-template)
- [Skill instructions](artifact/SKILL.md)
- [Example simplified itinerary input](artifact/tmp_input_2026-03-06.txt)

## Skill Output:

**Output Type(s):** [Files, Shell commands, Guidance]

**Output Format:** [DOCX file plus concise text or Markdown handoff]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a source DOCX template, UTF-8 simplified itinerary text, and the python-docx dependency.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
