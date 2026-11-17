## Description:

Diagnoses 3D print failures from symptoms or images, recommends slicer setting fixes, and helps users log and analyze recurring print problems.

This skill is ready for commercial/non-commercial use.

## Publisher:

[newageinvestments25-byte](https://clawhub.ai/user/newageinvestments25-byte)

### License/Terms of Use:

MIT-0

## Use Case:

External users, makers, and 3D printing operators use this skill to diagnose failed prints, compare symptoms against common failure modes, apply slicer setting fixes, and track recurring printer or material problems.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Failure logs and generated reports can contain sensitive printer, material, business, customer, location, or troubleshooting details supplied by the user.

Mitigation: Avoid entering private details in descriptions or notes, and review logs and reports before sharing them.

Risk: Report output paths are user-selected and could overwrite unrelated files.

Mitigation: Choose report output paths deliberately and inspect existing files before writing a report.

Risk: Diagnosis and slicer recommendations may be inaccurate for a specific printer, material, firmware, or environmental condition.

Mitigation: Treat recommendations as starting points, make small controlled changes, and verify settings against the printer and filament manufacturer's guidance.

## Reference(s):

- [3D Print Failure Types](references/failure-types.md)
- [Slicer Setting Fixes by Failure Type](references/slicer-fixes.md)
- [ClawHub Skill Page](https://clawhub.ai/newageinvestments25-byte/skills/print-failure-analyst)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Files, Guidance]

**Output Format:** [Markdown or plain-text diagnostic guidance, optional JSON diagnostic output, and optional Markdown reports.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update a local failure log and write user-selected Markdown report files.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
