## Description: <br>
B2B manufacturing proactive prospecting: search Google Maps for potential customers based on existing client profiles, enrich leads with business details, score and rank them, and output actionable CSV and JSON lead lists with custom sales openers. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[liufx13](https://clawhub.ai/user/liufx13) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Sales, business development, and operations teams use this skill to turn known B2B customers into profiles, find similar businesses, enrich and rank prospects, and generate structured call lists with tailored openers. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can bulk collect and save B2B outreach contact lists. <br>
Mitigation: Confirm the intended geography, industry, sources, and output path before use; secure or delete prospect-data files when they are no longer needed. <br>
Risk: Prospecting workflows can conflict with platform terms, privacy laws, do-not-call rules, or anti-spam obligations. <br>
Mitigation: Review applicable outreach rules before running searches or using call lists, avoid unnecessary personal contacts, and limit collection to data needed for the stated B2B prospecting task. <br>
Risk: Unverified or placeholder prospect details could lead to misleading call lists. <br>
Mitigation: Follow the included data-integrity checklist: preserve raw extraction notes, mark missing fields as unknown or not found, flag placeholder phone numbers, and verify phone numbers before marking prospects ready to call. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/liufx13/prospecting) <br>
- [README](README.md) <br>
- [Customer Profiling](references/profiling.md) <br>
- [Search Strategy](references/search-strategy.md) <br>
- [Google Maps Search](references/maps-search.md) <br>
- [Chain Store Prospecting Strategy](references/chain-strategy.md) <br>
- [Data Integrity Checklist](references/data-integrity-checklist.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, json, csv, shell commands, guidance] <br>
**Output Format:** [Markdown guidance plus structured JSON prospect files, a JSON index, and CSV call-list projections.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Prospect outputs are organized under prospect-data batches with raw extraction logs, candidate JSON, per-prospect JSON records, and call-list CSV exports.] <br>

## Skill Version(s): <br>
1.0.2 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
