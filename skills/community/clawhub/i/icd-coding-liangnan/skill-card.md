## Description:

ICD-Coding helps agents answer Chinese ICD-10, ICD-9-CM-3, ICD-O, and CHS-DRG/DIP coding questions, including DRG 2.0 and DRG 3.0 reference lookups.

This skill is ready for commercial/non-commercial use.

## Publisher:

[liangnan](https://clawhub.ai/user/liangnan)

### License/Terms of Use:

MIT-0

## Use Case:

Medical coders, billing teams, and clinical documentation reviewers use this skill for ICD and CHS-DRG reference assistance, diagnosis and procedure code lookup, DRG grouping support, and transition checks between DRG 2.0 and 3.0.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Medical coding or DRG guidance may be incomplete, outdated, or unsuitable for a specific billing context.

Mitigation: Validate outputs against current official policy, local payer rules, clinical documentation, and qualified billing compliance review.

Risk: DRG 2.0 and DRG 3.0 transition differences can change grouping outcomes.

Mitigation: Confirm which DRG version applies and have qualified coding staff review principal diagnosis, principal procedure, and complication selections.

Risk: Lookup matches, fuzzy searches, or no-match results can be misread as final determinations.

Mitigation: Treat lookup output as coding assistance and escalate uncertain cases to manual review.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/liangnan/skills/icd-coding-liangnan)
- [CHS-DRG 3.0 knowledge guide](artifact/docs/DRG3.0_Knowledge.md)
- [CHS-DRG 2.0 to 3.0 changes](artifact/docs/DRG3.0_Changes.md)
- [DRG 3.0 lookup tool](artifact/docs/drg3.0_lookup_tool.py)
- [National Healthcare Security Administration DRG/DIP 3.0 notice](https://www.nhsa.gov.cn/art/2026/9/2/art_104_21975.html)
- [National Healthcare Security Administration ICD-10 query](https://code.nhsa.gov.cn/jbzd/public/dataWesterSearch.html)
- [WHO ICD-10 Browser](https://icd.who.int/browse10/2022/en)
- [WHO ICD-11 Browser](https://icd.who.int/browse/11)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, guidance]

**Output Format:** [Markdown responses with coding references, lookup results, and optional Python or shell snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses local JSON lookup tables; outputs should be reviewed against official policy, clinical context, and billing compliance requirements.]

## Skill Version(s):

2.2.1 (source: server release metadata and target metadata; artifact update text references v2.3.0 content)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
