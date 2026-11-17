## Description:

LMS data aggregation and reporting tool for course information management.

This skill is ready for commercial/non-commercial use.

## Publisher:

[acogkr](https://clawhub.ai/user/acogkr)

### License/Terms of Use:


## Use Case:

Students or authorized agents use this skill to collect Hoseo University LMS course data, generate local deadline and attendance summaries, and run explicitly requested lecture playback.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automated lecture playback may update LMS attendance or progress records.

Mitigation: Use only with explicit institutional authorization and require a user-confirmed playback count before running auto_attend.py.

Risk: The skill handles LMS credentials and examples include plaintext credentials and a --pw command-line option.

Mitigation: Avoid passing passwords on the command line, store credentials only in a local file with restrictive permissions, use a low-risk environment, and rotate credentials after unsafe use.

Risk: A default lecture limit of 0 means unlimited playback scope.

Mitigation: Set a concrete --limit-lectures value for each run and confirm the intended course or week bounds before execution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/acogkr/skills/hoseo-lms)
- [Hoseo University LMS](https://learn.hoseo.ac.kr)
- [OpenClaw](https://clawhub.ai)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands, plus local JSON reports and terminal text summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces local files under ~/.config/hoseo_lms and may launch browser-based LMS lecture playback when explicitly requested.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
