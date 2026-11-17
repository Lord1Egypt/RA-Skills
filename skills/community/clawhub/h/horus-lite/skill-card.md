## Description:

Horus Lite extracts a clean action-item checklist and brief summary from pasted meeting notes or transcripts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[occupythemilkyway](https://clawhub.ai/user/occupythemilkyway)

### License/Terms of Use:

MIT-0

## Use Case:

External users and productivity-focused teams use this skill to turn pasted meeting notes, transcripts, or bullet points into assigned action items and a short meeting summary.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Full meeting notes or transcripts may appear in terminal output or logs.

Mitigation: Avoid confidential transcripts unless that exposure is acceptable, or run the skill in a controlled environment with logging disabled or restricted.

Risk: The setup command installs an unpinned dependency into the system Python environment.

Mitigation: Install dependencies in an isolated virtual environment and pin package versions before operational use.

Risk: The skill output includes promotional upgrade messaging.

Mitigation: Review generated output before sharing it outside the execution context.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/occupythemilkyway/skills/horus-lite)
- [ClawHub metadata homepage](https://clawhub.ai/occupythemilkyway/horus-lite)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, guidance]

**Output Format:** [Markdown action-item checklist and short summary, with inline shell and Python snippets for setup and execution]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires MEETING_NOTES input; prints the full provided notes before asking the agent to extract action items.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
