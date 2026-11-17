## Description:

Health Guide routes Korean health questions across symptom checks, hospital lookup, disease information, drug information, emergency guidance, checkups, vaccination, healthy living, mental health, and beginner medical-system guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sw326](https://clawhub.ai/user/sw326)

### License/Terms of Use:


## Use Case:

External users use this skill for Korea-oriented general health guidance, including symptom triage, hospital-department routing, drug and disease information, emergency escalation, checkups, vaccination, mental health support, and beginner explanations of the medical system.

### Deployment Geography for Use:

South Korea

## Known Risks and Mitigations:

Risk: Users may mistake general health guidance for diagnosis or prescription.

Mitigation: Keep medical disclaimers visible, avoid definitive diagnosis or dosing instructions, and direct persistent or worsening symptoms to a qualified clinician.

Risk: Emergency symptoms may require immediate local help rather than conversational guidance.

Mitigation: Prioritize emergency screening and route urgent Korean contexts to 119 or appropriate local emergency services.

Risk: API-key setup examples could lead users to expose secrets if copied into shared shells or logs.

Mitigation: Store keys in environment variables, an OS secret store, or owner-only files with restrictive permissions; avoid pasting real keys into shell commands.

Risk: Some referenced API scripts are documented as pending implementation or approval.

Mitigation: Use official-source web search fallback when APIs are unavailable and disclose when an answer is web-search based.

## Reference(s):

- [Health Guide ClawHub listing](https://clawhub.ai/sw326/skills/health-guide)
- [Intent Router](references/intent_router.md)
- [Output Templates](references/output_templates.md)
- [Source Tiers](references/source_tiers.md)
- [National Health Information Portal](https://health.kdca.go.kr)
- [MFDS Drug Overview API](https://www.data.go.kr/data/15075057/openapi.do)

## Skill Output:

**Output Type(s):** [text, markdown, guidance, shell commands, configuration]

**Output Format:** [Markdown health guidance with tables, checklists, brief action steps, disclaimers, and occasional setup shell commands.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Flash responses are always produced; deep-dive responses are used on request or for disease, drug, mental-health, checkup, and vaccination intents.]

## Skill Version(s):

1.0.1 (source: server release metadata; artifact frontmatter reports 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
