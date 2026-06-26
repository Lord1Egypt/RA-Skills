## Description: <br>
Compares old and new policies or procedures and drafts a structured summary of the main changes, business impacts, process impacts, documents to update, training suggestions, and open questions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[52YuanChangXing](https://clawhub.ai/user/52YuanChangXing) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees, compliance teams, operations teams, and developers use this skill to turn old and new policy materials plus affected-team context into reviewable Markdown or JSON change briefs. It is intended for policy, diff, governance, and compliance workflows, not legal determinations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Policy inputs may contain sensitive or personal information. <br>
Mitigation: Use only inputs appropriate for the workspace and redact sensitive material before processing when required. <br>
Risk: The generated brief may omit context or overstate impacts when source materials are incomplete. <br>
Mitigation: Review the output as a draft and resolve the listed open questions before using it for process, documentation, or training changes. <br>
Risk: Running the bundled helper with --output can replace an existing file at the chosen path. <br>
Mitigation: Choose an intentional output path or run with --dry-run/stdout first to inspect the result. <br>
Risk: The skill is not intended to provide legal determinations. <br>
Mitigation: Route legal conclusions or binding compliance interpretations to qualified reviewers. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/52YuanChangXing/policy-delta-watcher) <br>
- [Publisher profile](https://clawhub.ai/user/52YuanChangXing) <br>
- [README.md](artifact/README.md) <br>
- [SKILL.md](artifact/SKILL.md) <br>
- [resources/spec.json](artifact/resources/spec.json) <br>
- [resources/template.md](artifact/resources/template.md) <br>
- [examples/example-input.md](artifact/examples/example-input.md) <br>
- [examples/example-output.md](artifact/examples/example-output.md) <br>
- [tests/smoke-test.md](artifact/tests/smoke-test.md) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, JSON, Text, Files, Shell commands, Guidance] <br>
**Output Format:** [Structured Markdown by default, with optional JSON wrapping from the local script] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The local helper accepts --input, --output, --format, --limit, and --dry-run; using --output may replace an existing file at the selected path.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
