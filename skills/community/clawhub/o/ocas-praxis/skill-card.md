## Description: <br>
Bounded behavioral refinement loop. Records outcomes, extracts micro-lessons from repeated patterns, consolidates them into capped active behavior shifts, applies shifts at runtime, and generates plain-language debriefs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[indigokarasu](https://clawhub.ai/user/indigokarasu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agents and developers use Ocas Praxis to record task outcomes, extract repeated micro-lessons, manage a capped set of active behavior shifts, generate runtime briefs, and produce concise debriefs for review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can persist records about outcomes and behavior changes under ~/openclaw or OCAS_ROOT. <br>
Mitigation: Use it only when persistent local behavior records are intended, configure retention, and periodically review active shifts and journals. <br>
Risk: Untrusted local processes could write BehavioralSignal files into the intake directory and influence proposed lessons or shifts. <br>
Mitigation: Allow only trusted local skills or processes to write intake files and review proposed or active shifts before relying on runtime briefs. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/indigokarasu/ocas-praxis) <br>
- [Praxis data model](references/data_model.md) <br>
- [Praxis lesson extraction rules](references/lesson_rules.md) <br>
- [Praxis runtime rules](references/runtime_rules.md) <br>
- [Praxis debrief templates](references/debrief_templates.md) <br>
- [Praxis journal format](references/journal.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, guidance] <br>
**Output Format:** [Plain text, Markdown, and JSON-shaped records described by the skill references] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local event, lesson, shift, debrief, decision, report, and journal records under the configured OpenClaw data root.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release metadata and skill.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
