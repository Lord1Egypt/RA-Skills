## Description: <br>
Helps users resolve conflicts among multiple goals and limited resources by producing task ordering, trade-off explanations, boundaries, and not-to-do lists. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[52YuanChangXing](https://clawhub.ai/user/52YuanChangXing) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees, planners, and team leads use this skill to turn competing goals, resource limits, and schedule or scope conflicts into a reviewable priority brief. It is intended for planning support, not for replacing personnel performance decisions or inventing resource commitments. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The local helper can read files supplied as input and write a selected output file, so sensitive personal or business data could be copied into the generated report. <br>
Mitigation: Use only intended local input files, review the generated report before sharing it, and redact sensitive data before processing when needed. <br>
Risk: Priority recommendations may be incomplete or misleading when the input omits goals, constraints, stakeholders, or decision authority. <br>
Mitigation: Treat outputs as reviewable planning drafts and confirm missing information before making final trade-off decisions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/52YuanChangXing/priority-conflict-resolver) <br>
- [README](README.md) <br>
- [Structured specification](resources/spec.json) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance, shell commands] <br>
**Output Format:** [Structured Markdown, with optional JSON output from the local helper script] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs are review-first priority and trade-off briefs based on user-provided local input.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
