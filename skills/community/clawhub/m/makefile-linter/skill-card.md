## Description: <br>
Lint Makefiles for common issues — tabs, .PHONY, unused vars, portability, and best practices. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[charlie-morrison](https://clawhub.ai/user/charlie-morrison) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to inspect Makefiles for common correctness, portability, and maintainability issues before committing changes or enforcing checks in CI. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Reports may include Makefile variable values or command text from files being inspected. <br>
Mitigation: Run the skill only on Makefiles or stdin content intended for inspection, and review or redact JSON and Markdown output before sharing it. <br>
Risk: Lint findings can be incomplete or context-dependent, especially when used to gate CI with strict mode. <br>
Mitigation: Review reported issues before changing build logic or enforcing strict failures in automated workflows. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Text, JSON, Markdown, Shell commands] <br>
**Output Format:** [Text, JSON, or Markdown reports for lint findings, targets, variables, and combined audits.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reads a user-selected Makefile path or stdin and prints reports locally.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence; artifact frontmatter lists 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
