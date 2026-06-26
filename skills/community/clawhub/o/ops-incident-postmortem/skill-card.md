## Description: <br>
Generates structured, blame-free incident postmortem reports from logs, timeline data, and incident metadata. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[charlie-morrison](https://clawhub.ai/user/charlie-morrison) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, SREs, and incident response teams use this skill to draft postmortems, reconstruct timelines from logs and structured incident data, check for blameful language, and produce action-item-focused incident review reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated reports may include sensitive incident details from logs, timelines, and metadata. <br>
Mitigation: Review generated reports before sharing and provide only the incident files and output paths intended for processing. <br>
Risk: The skill reads local input files and can write report files to a requested output path. <br>
Mitigation: Run it only on trusted local incident inputs and choose output paths deliberately. <br>


## Reference(s): <br>
- [Postmortem Templates & Guidelines](artifact/references/templates.md) <br>
- [ClawHub skill page](https://clawhub.ai/charlie-morrison/ops-incident-postmortem) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, HTML, Shell commands, Guidance] <br>
**Output Format:** [Markdown, HTML, JSON, or terminal text reports; may write output files when an output path is provided] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated reports can include incident details, parsed log events, timelines, root cause analysis, impact summaries, lessons learned, and action items.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
