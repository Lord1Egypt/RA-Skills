## Description:

Summarize core safety information from Investigator's Brochures for clinical researchers.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aipoch-ai](https://clawhub.ai/user/aipoch-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Clinical researchers use this skill to extract and summarize Investigator's Brochure safety information, including adverse reactions, contraindications, warnings, interactions, special populations, overdose, and safety update history.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill processes potentially sensitive Investigator's Brochure documents locally.

Mitigation: Use it only with documents suitable for local processing, preferably inside a virtual environment or container.

Risk: Untrusted PDF or DOCX inputs may be large or difficult for parsers to handle predictably.

Mitigation: Add file-size and execution-time limits before production or regulated use.

Risk: Dependency versions are not pinned and evidence notes unnecessary dependency entries.

Mitigation: Pin and audit dependencies, and remove unnecessary docx and dataclasses entries before sensitive deployment.

Risk: Generated safety summaries may be incomplete or inaccurate.

Mitigation: Manually verify summaries before relying on them for clinical, regulatory, or medical decisions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/aipoch-ai/skills/ib-summarizer)

## Skill Output:

**Output Type(s):** [text, markdown, json, files]

**Output Format:** [Markdown, JSON, or plain text safety summary; optionally written to an output file.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports Chinese or English summary language; extracted clinical safety content requires manual verification.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
