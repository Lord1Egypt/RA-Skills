## Description: <br>
Taste generates personalized recommendations from real consumption signals by scanning email and calendar data, enriching venues and items, and explaining each suggestion with prior behavior. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[indigokarasu](https://clawhub.ai/user/indigokarasu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External agent users use Taste to create a local, behavior-driven taste profile and generate evidence-backed recommendations, serendipity suggestions, model status summaries, and weekly pattern reports. It is intended for personal recommendation workflows grounded in the user's actual consumption history, not generic search or editorial lists. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can scan sensitive personal email and calendar data. <br>
Mitigation: Require explicit approval for each scan and limit account, date, and source scope before extraction. <br>
Risk: The skill stores derived purchase, reservation, travel, and preference history locally. <br>
Mitigation: Review retention settings and periodically review or delete the stored JSONL data and journals. <br>
Risk: Entity enrichment through Google Maps or web search can expose venue or item context outside the local workspace. <br>
Mitigation: Review items before enrichment and avoid enriching sensitive or private records through external services. <br>
Risk: The documented cron self-update can change installed skill files on a schedule. <br>
Mitigation: Disable the taste:update cron job or require manual approval before running updates. <br>


## Reference(s): <br>
- [README](README.md) <br>
- [Email and Calendar Extraction](references/email_extraction.md) <br>
- [Entity Enrichment](references/enrichment.md) <br>
- [Taste Recommendation Style](references/recommendation_style.md) <br>
- [Taste Schemas](references/schemas.md) <br>
- [Signal Policy](references/signal_policy.md) <br>
- [Strength Model](references/strength_model.md) <br>
- [Journal](references/journal.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, JSON, Files, Shell commands, Configuration] <br>
**Output Format:** [Markdown recommendations and reports, JSON/JSONL state records, and shell commands for setup or self-update tasks.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Recommendations must cite prior consumption evidence, verify novelty and dietary compatibility, and may persist local data and journal files under ~/openclaw/data/ocas-taste/ and ~/openclaw/journals/ocas-taste/.] <br>

## Skill Version(s): <br>
3.0.1 (source: skill.json and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
