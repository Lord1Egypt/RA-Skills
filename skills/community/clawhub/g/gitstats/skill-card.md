## Description:

Analyze and visualize Git commit time distribution for a repository by date, hour, weekday, branch, and timezone.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wangyendt](https://clawhub.ai/user/wangyendt)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to run gitstats against a Git repository and generate commit activity summaries and charts filtered by branch, date range, and timezone.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Saved chart files may overwrite an existing file at the selected output path.

Mitigation: Choose an explicit output path before running gitstats and check whether the destination file already exists.

Risk: Repository, branch scope, date range, and timezone choices can change the interpretation of commit activity.

Mitigation: Confirm the repository path, branch or all-branches mode, date filters, and timezone before using the generated chart for reporting.

Risk: Large repositories or all-branch analysis may take longer to process.

Mitigation: Use branch and date-range filters when a narrower analysis is sufficient.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with inline shell commands and concise operational guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guidance may include repository paths, date filters, branch selection, timezone settings, and chart output paths.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
