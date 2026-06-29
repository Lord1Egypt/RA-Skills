## Description: <br>
Objectively scores meeting quality from a transcript across decision clarity, time efficiency, and participation balance, producing Markdown and HTML reports through an OpenAI-compatible LLM endpoint. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ucsdzehualiu](https://clawhub.ai/user/ucsdzehualiu) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Employees, external teams, and developers use this skill to score completed meeting transcripts, identify unclear decisions, off-topic time, and uneven participation, and generate reviewable reports. It is designed for batch analysis after a transcript has already been created. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Meeting transcripts may contain confidential or regulated information and are sent to the configured LLM endpoint. <br>
Mitigation: Use a trusted local or organization-approved provider for sensitive meetings, and avoid sending confidential, legal, HR, or regulated transcripts to unapproved endpoints. <br>
Risk: LLM-based scoring can be incomplete or misleading when the model output is malformed, the endpoint fails, or the transcript lacks speaker labels. <br>
Mitigation: Treat the score as a review aid, manually verify important decisions and recommendations, and preserve speaker labels or diarization when participation balance matters. <br>
Risk: HTML visualizations may load Chart.js from a CDN by default. <br>
Mitigation: Review report output handling for restricted environments and vendor or bundle visualization dependencies before production use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ucsdzehualiu/skills/meeting-quality-scorer) <br>
- [README](artifact/README.md) <br>
- [Example configuration](artifact/config.example.yaml) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Markdown, Files, Configuration] <br>
**Output Format:** [Markdown report and HTML visualization files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a transcript text file and a configured OpenAI-compatible LLM endpoint; plain transcripts use degraded scoring without participation balance.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
