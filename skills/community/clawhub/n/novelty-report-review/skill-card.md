## Description:

Reviews scientific and technological novelty search reports against GB/T novelty-search guidance, focusing on novelty-point interpretation, search terms and translations, search strategy, literature selection, and conclusion quality.

This skill is ready for commercial/non-commercial use.

## Publisher:

[charliegates309-oss](https://clawhub.ai/user/charliegates309-oss)

### License/Terms of Use:

MIT-0

## Use Case:

External users and report reviewers use this skill to audit novelty search reports for unclear novelty points, incomplete search terms or translations, weak search strategies, literature-selection gaps, and unsupported conclusions. It returns only identified problems and actionable improvements.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Fallback document extraction may turn a user-supplied file path into executable Python.

Mitigation: Use only trusted local report paths, or rewrite extraction commands to pass paths as arguments with validation and safe quoting before execution.

Risk: The skill under-discloses a claimed Baidu Scholar research basis.

Mitigation: Make any external Baidu Scholar checks explicit and user-approved, and record the search date, queries, and sources used.

Risk: Reports may contain sensitive technical or proprietary information.

Mitigation: Use the skill only in environments approved for the report's confidentiality and avoid processing sensitive reports unless that handling is permitted.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/charliegates309-oss/skills/novelty-report-review)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown audit report]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Problems-only review with prioritized fixes and suggested alternative wording or methods.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
