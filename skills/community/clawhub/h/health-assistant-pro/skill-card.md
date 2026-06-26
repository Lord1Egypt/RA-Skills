## Description: <br>
Health Assistant provides informational wellness support with health report analysis, local health record tracking, supplement recommendations, machine-learning personalization, external health research integrations, and quality verification guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sunnyhot](https://clawhub.ai/user/sunnyhot) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to provide informational health tracking support, supplement recommendations, medical report trend summaries, travel health checklists, and triage-oriented guidance while directing serious or personalized medical decisions to healthcare professionals. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles sensitive medical information using local plaintext JSON files. <br>
Mitigation: Avoid storing real personal health records unless the user accepts plaintext local storage; remove or protect files containing sensitive data before sharing the workspace. <br>
Risk: The skill includes emergency, first-aid, medication, supplement, mental-health, legal travel, and veterinary guidance that could be mistaken for professional advice. <br>
Mitigation: Treat responses as informational, verify emergency numbers and crisis resources for the user's location, and direct urgent or individualized decisions to qualified professionals. <br>
Risk: Medication-import, supplement quality, and external research responses may depend on changing regulations, subscriptions, API access, or incomplete evidence. <br>
Mitigation: Confirm current official sources, API availability, and product-specific information before acting on recommendations. <br>


## Reference(s): <br>
- [Common Health Conditions Reference](references/common_conditions.md) <br>
- [Emergency First Aid Reference](references/first_aid.md) <br>
- [Travel Health Preparation Checklist](references/travel_health.md) <br>
- [PubMed E-utilities API](https://eutils.ncbi.nlm.nih.gov/entrez/eutils/) <br>
- [ConsumerLab API](https://api.consumerlab.com/) <br>
- [Examine.com Supplement Research via Apify](https://apify.com/hanamira/examine-com-supplement-research) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with optional JSON records, code snippets, and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May reference local JSON health records and external health research APIs when configured; outputs are informational and require professional review for medical decisions.] <br>

## Skill Version(s): <br>
1.5.0 (source: server release evidence, target metadata, frontmatter, package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
