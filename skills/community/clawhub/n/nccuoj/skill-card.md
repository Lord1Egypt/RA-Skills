## Description:

Solve competitive programming problems on NCCUOJ by fetching problem statements, writing local solutions, submitting code, and checking results.

This skill is ready for commercial/non-commercial use.

## Publisher:

[andyjjrt](https://clawhub.ai/user/andyjjrt)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, students, and competitive programmers use this skill to retrieve NCCUOJ public or contest problems, create solution files, submit code, and inspect judge results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: NCCUOJ credentials are passed through documented command arguments and may be exposed in shell history, process listings, terminal logs, or shared environments.

Mitigation: Use a dedicated low-value NCCUOJ password, avoid shared or logged environments, and rotate the password if it may have been exposed.

Risk: Session cookies are persisted under .nccuoj/cookies.txt in the active workspace.

Mitigation: Remove .nccuoj/cookies.txt after use and avoid committing or sharing the .nccuoj directory.

Risk: The NCCUOJ_BASE_URL environment variable can change the API destination used by the helper scripts.

Mitigation: Leave NCCUOJ_BASE_URL unset unless deliberately testing, and verify it points only to the real NCCUOJ site before entering credentials.

## Reference(s):

- [NCCUOJ API Reference](references/api.md)
- [NCCUOJ](https://nccuoj.ebg.tw)
- [ClawHub skill page](https://clawhub.ai/andyjjrt/skills/nccuoj)
- [ClawHub publisher profile](https://clawhub.ai/user/andyjjrt)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown, JSON, source code files, and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create .nccuoj problem, solution, and cookie files in the active workspace.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
