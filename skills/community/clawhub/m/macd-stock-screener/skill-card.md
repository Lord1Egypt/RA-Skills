## Description:

Screens A-share stocks for right-side MACD golden crosses and left-side approaching crosses, then creates CSV and Markdown reports with East Money forum comment summaries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sunsongyeah](https://clawhub.ai/user/sunsongyeah)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agent operators use this skill to scan China A-share markets for MACD-based candidate stocks and generate daily candidate, summary, and forum-comment reports. It supports routine screening workflows and should not be treated as investment advice or a backtest.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill makes outbound requests to public financial and forum data sources and writes local report files.

Mitigation: Run it in a virtual environment, review the requested output path, and confirm before executing broad or vague stock-picking requests.

Risk: Unpinned dependencies can change screening behavior or introduce supply-chain risk.

Mitigation: Pin and review the akshare, pandas, and numpy dependency versions before operational use.

Risk: The generated sentiment report summarizes public comment data and is not robust sentiment scoring.

Mitigation: Treat sentiment output as contextual commentary only and review market conclusions manually.

Risk: MACD signals can lag or produce false positives, especially for left-side approaching-cross candidates.

Mitigation: Use the reports as screening inputs, not trading decisions, and validate candidates with independent analysis.

## Reference(s):


## Skill Output:

**Output Type(s):** [Shell commands, Files, Markdown, Analysis]

**Output Format:** [Terminal text plus local CSV and Markdown report files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes dated local reports under outputs/YYYY-MM-DD by default and supports CLI options for output directory, top-N count, strategy mode, and sentiment collection.]

## Skill Version(s):

1.0.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
