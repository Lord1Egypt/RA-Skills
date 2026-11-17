## Description:

BaZi (Four Pillars) charting and reading for Mystilink that computes pillars, luck cycles, and annual pillars from birth data, then supports interpretation with Mystilink Wiki theory.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mystilink-ai](https://clawhub.ai/user/mystilink-ai)

### License/Terms of Use:

MIT

## Use Case:

External users and agent hosts use this skill to compute BaZi charts, DaYun cycles, and LiuNian annual notes from birth profiles, then produce a reading that separates chart facts from interpretation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Birth details can be personal data when used to build chart profiles.

Mitigation: Keep birth profiles local unless the user intentionally includes them in a query or external request.

Risk: Optional Mystilink Wiki lookups may send theory search terms, system, and locale parameters to wiki.mystilink.com.

Mitigation: Use Wiki lookups only when network access is intended, and cite Wiki provenance when theory pages inform an answer.

Risk: Locale fallbacks may produce English or Chinese terminology that needs user-facing clarification.

Mitigation: Name the locale used, explain key translated terms plainly, and prefer the user's requested language when available.

## Reference(s):

- [Server-resolved GitHub import: mystilink-ai/mystilink-bazi-skill](https://github.com/mystilink-ai/mystilink-bazi-skill)
- [ClawHub skill page](https://clawhub.ai/mystilink-ai/skills/mystilink-bazi-skill)
- [Mystilink Wiki search API for BaZi theory](https://wiki.mystilink.com/api/v1/search?q=day+master&system=bazi&locale=en)
- [Mystilink Wiki Ri Zhu concept page](https://wiki.mystilink.com/api/v1/pages/bazi.concept.ri-zhu?locale=en)
- [Overview reference](references/overview.md)
- [Wiki ID reference](references/wiki-ids.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with optional shell commands and JSON chart data from local scripts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include Wiki page IDs and provenance when Mystilink Wiki theory pages are used.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
