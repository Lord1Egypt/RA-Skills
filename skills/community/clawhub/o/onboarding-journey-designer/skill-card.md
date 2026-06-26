## Description: <br>
Designs customer or employee onboarding journeys by breaking work into Day 1, Day 7, and Day 30 plans. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[52YuanChangXing](https://clawhub.ai/user/52YuanChangXing) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Customer success, enablement, HR, and product teams use this skill to turn onboarding inputs into reviewable Markdown journey drafts, checklists, milestones, blockers, and metrics. It is suited for customer activation, employee onboarding, and new-user guidance workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The local helper can create or overwrite the file named by --output. <br>
Mitigation: Choose an output path deliberately, use --dry-run or stdout for review first, and avoid pointing the output at important existing files. <br>
Risk: Onboarding materials may include sensitive personal or business information. <br>
Mitigation: Use only files intended to be shared with the skill and redact sensitive data unless it is necessary for the onboarding plan. <br>
Risk: Generated onboarding journeys may be too generic or incomplete for a specific product, role, or customer segment. <br>
Mitigation: Review the draft against the actual product context, fill the listed confirmation items, and adjust milestones and metrics before execution. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/52YuanChangXing/onboarding-journey-designer) <br>
- [README](artifact/README.md) <br>
- [Skill Definition](artifact/SKILL.md) <br>
- [Output Template](artifact/resources/template.md) <br>
- [Structured Specification](artifact/resources/spec.json) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration] <br>
**Output Format:** [Markdown by default, with optional JSON from the helper script] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces reviewable onboarding drafts and can write an output file when the local Python helper is run with --output.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
