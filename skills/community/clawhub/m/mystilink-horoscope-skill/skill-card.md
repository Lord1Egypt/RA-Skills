## Description:

Western natal astrology charting and reading for Mystilink that computes planets, houses, and aspects from birth time and place, then supports interpretation with Wiki terms.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mystilink-ai](https://clawhub.ai/user/mystilink-ai)

### License/Terms of Use:

MIT

## Use Case:

Developers and agent users use this skill to calculate Western natal chart data from birth time and location, then prepare clear astrology interpretations while keeping computed chart data distinct from explanatory content.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Birth date, time, and location can be sensitive personal data.

Mitigation: Use fictional or minimized data when possible, avoid sending raw birth profiles to optional Wiki API calls, and handle generated chart output as sensitive user data.

Risk: The calculator can write output files to user-provided paths.

Mitigation: Review any output path before execution and write only to locations the user intends to create or overwrite.

Risk: Astrology interpretations can be confused with calculated chart facts.

Mitigation: Keep chart data distinct from interpretation text and cite the relevant Mystilink Wiki concepts when using external explanations.

## Reference(s):

- [Server-resolved GitHub provenance](https://github.com/mystilink-ai/mystilink-horoscope-skill)
- [ClawHub skill page](https://clawhub.ai/mystilink-ai/skills/mystilink-horoscope-skill)
- [Mystilink Wiki search API](https://wiki.mystilink.com/api/v1/search?q=ascendant&system=horoscope&locale=en)
- [Mystilink natal chart concept page](https://wiki.mystilink.com/api/v1/pages/horoscope.concept.natal-chart?locale=en)
- [Skill overview reference](references/overview.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, JSON]

**Output Format:** [Markdown guidance with inline shell commands and JSON chart output from the bundled calculator script]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May use a local Python script requiring pyswisseph and optional Mystilink Wiki lookups for interpretation terms.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
