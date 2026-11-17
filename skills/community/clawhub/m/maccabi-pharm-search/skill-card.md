## Description:

Search for medications and check real-time stock availability at Maccabi pharmacies in Israel.

This skill is ready for commercial/non-commercial use.

## Publisher:

[alexpolonsky](https://clawhub.ai/user/alexpolonsky)

### License/Terms of Use:

MIT

## Use Case:

External users and agents use this skill to search Maccabi Pharm medication records, find Largo codes, check pharmacy stock by Israeli city code, and list Maccabi pharmacy branches before visiting.

### Deployment Geography for Use:

Israel

## Known Risks and Mitigations:

Risk: Medication names and city codes are sent to Maccabi's public web service and may reveal health-related interests.

Mitigation: Use the skill only when the user intends to query Maccabi Pharm, and avoid automated checks that expose sensitive medication searches without user approval.

Risk: Stock data may be delayed or inaccurate.

Mitigation: Treat results as planning guidance and confirm availability with the pharmacy before visiting or relying on the stock status.

Risk: The skill runs a Node.js helper installed from a package source.

Mitigation: Install from a pinned or inspected source and avoid running the installer or helper with elevated privileges.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/alexpolonsky/skills/maccabi-pharm-search)
- [Maccabi Pharm public pharmacy service](https://serguide.maccabi4u.co.il/heb/pharmacy/)
- [Agent Skills specification](https://agentskills.io/specification)

## Skill Output:

**Output Type(s):** [text, shell commands, code, guidance]

**Output Format:** [Terminal text and Markdown with inline shell and JavaScript examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Medication names, Largo codes, prescription flags, city codes, pharmacy addresses, phone numbers, distances, and stock summaries may be included.]

## Skill Version(s):

2.0.0 (source: frontmatter and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
