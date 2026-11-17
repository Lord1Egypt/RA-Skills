## Description:

Professional health assistant with medical report analysis, evidence-based supplement recommendations, machine learning personalization, external API integration, quality verification, local health report storage, interaction checking, and wellness guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sunnyhot](https://clawhub.ai/user/sunnyhot)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to organize health profiles, medications, health records, symptoms, nutrition, supplements, first aid, travel health, and wellness planning. Outputs should be treated as informational support, not diagnosis or a substitute for professional medical care.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release bundles named health reports that may contain sensitive personal data.

Mitigation: Require the publisher to remove the reports or prove they are synthetic before installation or redistribution.

Risk: The skill stores health profiles, medications, reminders, and records in local plaintext JSON files.

Mitigation: Restrict local file permissions, document retention and deletion behavior, and avoid storing unnecessary personal or medical data.

Risk: The skill can direct health-related supplement or medical queries to third-party services.

Mitigation: Ask for user consent before sending health-related queries externally and avoid transmitting identifying health details unless necessary.

Risk: Medical and supplement guidance may be incorrect or inappropriate for abnormal reports, medications, pregnancy, serious symptoms, or emergencies.

Mitigation: Present outputs as informational only, recommend professional medical review for personal decisions, and route emergency symptoms to emergency services.

## Reference(s):

- [Health Assistant ClawHub Release](https://clawhub.ai/sunnyhot/skills/health-assistant-pro)
- [Common Health Conditions Reference](references/common_conditions.md)
- [Emergency First Aid Reference](references/first_aid.md)
- [Travel Health Preparation Checklist](references/travel_health.md)
- [Examine.com Supplement Research Apify Actor](https://apify.com/hanamira/examine-com-supplement-research)
- [ConsumerLab API](https://api.consumerlab.com/)
- [PubMed E-Utilities](https://eutils.ncbi.nlm.nih.gov/entrez/eutils/)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown and structured text with optional JSON examples and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May reference local JSON health records, supplement datasets, API endpoints, and scripts when the agent has access to the artifact.]

## Skill Version(s):

1.5.0 (source: frontmatter, package.json, server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
