## Description:

Nov Tarot guides agents through Chinese-language Rider-Waite tarot readings, selecting spreads, interpreting cards with psychological framing, handling follow-up draws, and preparing session reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[joe-zhouman](https://clawhub.ai/user/joe-zhouman)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill when they want an agent to conduct a tarot reading, choose an appropriate spread, interpret supplied or agent-drawn cards, and preserve the reading as a report. The skill is framed for reflective guidance and should not be presented as clinical therapy or deterministic fortune-telling.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill records intimate tarot questions and summaries in local session state without clear user-facing consent.

Mitigation: Require explicit consent before storing reading details, disclose the storage location, and provide deletion controls.

Risk: The counseling-like framing could cause users to mistake tarot reflection for clinical mental health support.

Mitigation: State clear non-therapy boundaries and direct crisis, medical, legal, or safety concerns to qualified professionals.

Risk: The skill can generate additional report files and involve another agent context during report compilation.

Mitigation: Ask the user before generating reports or sharing session context with another agent, and show where generated files are written.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/joe-zhouman/skills/nov-tarot)
- [Server-resolved GitHub source](https://github.com/Joe-zhouman/NovTarot/tree/main/nov-tarot)
- [Publisher profile](https://clawhub.ai/user/joe-zhouman)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Conversational text and Markdown with shell command snippets, JSON session records, and optional HTML or PNG report files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create local session records and report artifacts during a reading.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
