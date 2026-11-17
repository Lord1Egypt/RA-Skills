## Description:

Meeting Deep-Process helps agents process meeting data across execution, analysis, knowledge capture, speaker profiling, and quality improvement workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wangjiaocheng](https://clawhub.ai/user/wangjiaocheng)

### License/Terms of Use:

MIT-0

## Use Case:

Employees, external collaborators, and developers can use this skill to turn meeting transcripts, recordings, agendas, and participant context into structured meeting reports, decision traces, action follow-up, knowledge entries, speaker profiles, and meeting-quality improvement plans.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can support persistent participant profiling and workplace-sensitive inferences from meeting data.

Mitigation: Use it only with participant notice and authorization; restrict cumulative profiles and sensitive inferences unless an organizational policy explicitly governs them.

Risk: Meeting analysis outputs may influence employment, negotiation, discipline, retention, or other consequential decisions.

Mitigation: Treat outputs as decision support only, require human review, and do not use them as the sole basis for consequential people or business decisions.

Risk: The fallback meeting-data path references broad meeting-tool commands, including recording, transcript, participant, and meeting-control operations.

Mitigation: Limit credentials and command access to the minimum required data retrieval functions; disable meeting-admin actions unless separately authorized.

Risk: Transcripts, recordings, and generated profiles can create retention and privacy exposure.

Mitigation: Apply retention limits, deletion workflows, and explicit removal handling before using the skill with real meetings.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/wangjiaocheng/skills/meeting-deep-process)
- [Publisher Profile](https://clawhub.ai/user/wangjiaocheng)
- [Meeting Deep-Process Task Catalog](references/meeting-deep-process-catalog.md)
- [Meeting Deep-Process Task Requirements](references/meeting-deep-process-requirements.md)
- [Meeting Deep-Process Template Library](references/exemplars.md)
- [tmeet CLI Reference](references/tmeet-cli-reference.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown reports, structured tables, checklists, and occasional shell command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include confidence labels, source-trace annotations, review markers, and degradation notices when meeting data or live transcript streams are unavailable.]

## Skill Version(s):

1.0.5 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
