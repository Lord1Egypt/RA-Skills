## Description:

Health probe for the ClawHub security scan pipeline. Sums a list of integers from a local reference file and prints a deterministic report, used to verify whether the registry scan pipeline currently completes for benign content.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mnetfairy](https://clawhub.ai/user/mnetfairy)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and registry operators use this skill to exercise the ClawHub scan pipeline with a simple local JSON input and confirm that it produces a deterministic integer sum.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security summary reports that the script can read a caller-selected file beyond the single bundled reference file described as its purpose.

Mitigation: Use the bundled sample file as the input. Before supplying another path, confirm that the file is appropriate for the skill to read.

## Reference(s):

- [Sample numbers](references/sample_numbers.json)

## Skill Output:

**Output Type(s):** [Text]

**Output Format:** [Plain text (`sum=<integer>`)]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [One deterministic line; no output files.]

## Skill Version(s):

0.0.1 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
