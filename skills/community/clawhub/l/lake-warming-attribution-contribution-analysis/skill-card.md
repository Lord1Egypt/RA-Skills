## Description:

Calculate the relative contribution of different factors to a response variable using R² decomposition.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wu-uk](https://clawhub.ai/user/wu-uk)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, analysts, and researchers use this skill to estimate how much each factor or interpreted category explains variance in a response variable. It guides agents through global factor analysis, R² decomposition, and concise reporting of the dominant contribution.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The example writes to output.csv and may replace a file the user intended to keep.

Mitigation: Choose a task-specific output path or add an existence check before writing the CSV.

Risk: The sample CSV contains only the dominant factor contribution, which can omit details needed for review.

Mitigation: Extend the output logic to write every factor contribution when a complete attribution table is required.

Risk: R² decomposition can produce negative or non-additive contribution values when factors are correlated or suppressor effects are present.

Mitigation: Check multicollinearity, inspect factor loadings, and treat contribution percentages as model diagnostics rather than causal proof.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, code, guidance]

**Output Format:** [Markdown guidance with Python code snippets and CSV output examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The sample output writes a CSV row for the dominant factor only unless extended.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
