## Description: <br>
Offline deterministic daily fortune skill for lucky direction, colors, numbers, items, do/avoid guidance, today/tomorrow/weekly/monthly readings, couple readings, and scenario-specific fortunes in Chinese or English. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jiajiaoy](https://clawhub.ai/user/jiajiaoy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users invoke this skill for offline, deterministic daily fortune-style entertainment, including lucky elements, short-term guidance, couple compatibility, scenario readings, and push-ready daily text. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Optional local profile storage may contain birth dates, partner details, or push-channel IDs on the user's machine. <br>
Mitigation: Save a profile only after explicit user consent, avoid storing sensitive details on shared machines, restrict file permissions when possible, and use the documented delete-profile flow when no longer needed. <br>
Risk: Fortune-style guidance may be mistaken for factual, medical, legal, financial, or investment advice. <br>
Mitigation: Present outputs as folklore and entertainment reference, keep high-stakes guidance bounded, and remind users to use real-world judgment for medical, legal, investment, or similar decisions. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/jiajiaoy/lucky-today) <br>
- [README](README.md) <br>
- [Fortune Rules](references/fortune_rules.md) <br>
- [Output Templates](references/output_templates.md) <br>
- [Scenario Rules](references/scenario_rules.md) <br>
- [Couple Rules](references/couple_rules.md) <br>
- [User Profile Template](references/user_profile_template.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration guidance] <br>
**Output Format:** [Markdown-style bilingual fortune text with structured sections and optional inline shell commands for cron setup] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Prompt-only output; deterministic for the same birth date and query date; optional push output is condensed for channel delivery.] <br>

## Skill Version(s): <br>
0.1.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
