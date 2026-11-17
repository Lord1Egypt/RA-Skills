## Description:

Analyze git repository statistics including contributor rankings, lines of code by language, commit frequency by day/hour, monthly activity trends, and file type breakdowns.

This skill is ready for commercial/non-commercial use.

## Publisher:

[johnnywang2001](https://clawhub.ai/user/johnnywang2001)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to inspect local git repositories, summarize contributor activity, count lines of code, and understand commit patterns over time.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Output can disclose contributor names, email addresses, repository paths, and other internal repository details.

Mitigation: Run the skill only on repositories whose history and paths may be summarized, and review text or JSON output before sharing it.

Risk: Line counting can read through tracked symlinks outside the repository boundary.

Mitigation: Avoid running LOC counting on untrusted repositories; use the --no-loc option when repository contents or symlink handling are not trusted.

## Reference(s):


## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Guidance]

**Output Format:** [Plain text report or JSON output, with shell commands for running the analyzer.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results may include repository paths and contributor names and emails from git history.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
