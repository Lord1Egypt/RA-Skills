## Description: <br>
Create and maintain dedicated archives for each pet, including profiles, daily journals, photos, feeding logs, health records, and care reminders. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[harrylabsj](https://clawhub.ai/user/harrylabsj) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to keep a local-first companion archive for one or more pets, including profiles, daily notes, photos, feeding changes, health records, reminders, searches, and compact summaries. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Pet profiles, photos or photo paths, clinic notes, health records, and reminders may contain sensitive personal context when stored or shared. <br>
Mitigation: Store data locally, use PET_COMPANION_HOME to isolate data on shared machines, and review records before sharing summaries or reports. <br>
Risk: Health notes could be mistaken for veterinary diagnosis or treatment advice. <br>
Mitigation: Use the skill to organize observations only; do not diagnose disease, do not infer missing medication details, and advise prompt veterinary care for urgent symptoms. <br>


## Reference(s): <br>
- [Data Schema](references/data-schema.md) <br>
- [Query Patterns](references/query-patterns.md) <br>
- [Safety Boundaries](references/safety-boundaries.md) <br>
- [Output Template](references/output-template.md) <br>
- [Template Examples](references/template-examples.md) <br>
- [Intents and Prompts](references/intents-and-prompts.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Files, Guidance] <br>
**Output Format:** [Concise natural-language responses, JSON script output, and Markdown records or reports stored locally] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses local storage under the configured pet companion data directory; PET_COMPANION_HOME can isolate data on shared machines.] <br>

## Skill Version(s): <br>
1.1.0 (source: frontmatter, skill metadata, server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
