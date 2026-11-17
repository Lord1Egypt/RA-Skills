## Description:

Turns a search terms report into a deduplicated negative keyword list with the match type, the level to apply it at, and the account limits checked.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rapidworker1](https://clawhub.ai/user/rapidworker1)

### License/Terms of Use:

MIT-0

## Use Case:

US Google Ads account managers and in-house performance marketers can review local search-term CSV exports, identify duplicate queries, and prepare negative-keyword decisions while keeping account changes under human control.

### Deployment Geography for Use:

United States

## Known Risks and Mitigations:

Risk: The advertised YAML quickstart does not match the script's CSV input requirements.

Mitigation: Provide a CSV containing a search_term column and verify the output before relying on it.

Risk: Negative-keyword proposals can exclude valuable or ambiguous queries if applied without review.

Mitigation: Review proposed exclusions and account limits, then upload manually only after human approval.

Risk: Running the script in an existing output directory overwrites duplicates.md.

Mitigation: Choose a dedicated output directory and preserve any reports that must be retained.

Risk: The optional Windows application has not been covered by the bundled script's security assessment.

Mitigation: Perform a separate security review before using the Windows application.

## Reference(s):

- [Google negative keywords reference](references/google-negative-keywords.md)
- [ClawHub release page](https://clawhub.ai/rapidworker1/skills/google-ads-negative-keyword-list)

## Skill Output:

**Output Type(s):** [Markdown, Guidance]

**Output Format:** [Markdown duplicate-term report and review guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The bundled script reads a local CSV with a search_term column and writes duplicates.md; it does not connect to or modify Google Ads.]

## Skill Version(s):

1.0.7 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
