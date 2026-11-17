## Description:

Helps suppliers review Chinese government-procurement response materials against procurement-file requirements, producing structured compliance checklists for invalid-response risks, qualification and policy-function items, formatting issues, key deadlines, and related legal-review or challenge workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chesaram](https://clawhub.ai/user/chesaram)

### License/Terms of Use:

MIT-0

## Use Case:

External suppliers and procurement-response teams use this skill before Chinese government-procurement submission deadlines to check response-file completeness, policy-function evidence, signature and seal requirements, submission logistics, and time-sensitive challenge or complaint options. It is advisory and does not replace legal or compliance review.

### Deployment Geography for Use:

China

## Known Risks and Mitigations:

Risk: Generated compliance reports include the author's signature and WeChat feedback prompt.

Mitigation: Review the required footer before deployment and install only if that attribution and feedback channel are acceptable for the intended environment.

Risk: Procurement response materials can contain confidential bid pricing, proprietary response content, or sensitive procurement details.

Mitigation: Avoid sharing confidential materials through the promoted external channel unless the user's organization explicitly permits it.

Risk: Legal and procurement guidance can become stale or may not fit the specific procurement file.

Mitigation: Verify legal references against current official sources and route material decisions through qualified legal or compliance reviewers.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chesaram/skills/govproc-response-compliance-advisor-1-0-1)
- [Publisher profile](https://clawhub.ai/user/chesaram)
- [Compliance signals](references/compliance-signals.md)
- [Legal core](references/legal_core.md)
- [Few-shot calibration cases](references/few_shot.md)
- [FAQ](references/faq.md)
- [Checklist template](templates/checklist-template.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Structured Markdown checklist with risk tables and concise advisory guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs include a project echo, blind-spot warnings, four risk levels, key timeline checks, and an author signature with a WeChat feedback prompt.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact manifest reports 1.0.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
