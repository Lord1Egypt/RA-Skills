## Description: <br>
Scout helps agents conduct structured OSINT research on people, companies, and organizations and produce provenance-backed briefs with cited findings. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[indigokarasu](https://clawhub.ai/user/indigokarasu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use Scout to research a person, company, or organization, resolve identity across public sources, and generate concise markdown briefs with source logs and uncertainty notes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Scout can keep local OSINT records and share confirmed identity findings with other OpenClaw components. <br>
Mitigation: Review the configured storage paths, retention expectations, and signal-sharing path before deployment; limit collection to the stated research goal. <br>
Risk: Scout registers a daily self-updater that can replace skill files from a remote source. <br>
Mitigation: Prefer disabling the cron job or using manual reviewed updates before installing changes. <br>
Risk: OSINT research on people or organizations can expose private or sensitive details. <br>
Mitigation: Keep minimization enabled, suppress private details unless explicitly permitted, and require explicit permission before paid source escalation. <br>


## Reference(s): <br>
- [ClawHub Scout release page](https://clawhub.ai/indigokarasu/ocas-scout) <br>
- [Scout schemas](references/scout_schemas.md) <br>
- [Scout source waterfall](references/scout_source_waterfall.md) <br>
- [Scout brief template](references/scout_brief_template.md) <br>
- [Scout journal format](references/journal.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, shell commands, guidance] <br>
**Output Format:** [Markdown briefs, optional PDF briefs, JSON records, signal files, journals, and status text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Every retained finding is expected to include source provenance with URL, retrieval timestamp, and supporting quote.] <br>

## Skill Version(s): <br>
2.3.0 (source: release evidence and skill.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
