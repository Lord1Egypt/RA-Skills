## Description: <br>
Convert .osop and .osoplog.yaml into standalone HTML report with dark mode and expandable nodes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[archie0125](https://clawhub.ai/user/archie0125) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to turn OSOP workflow definitions and execution logs into local, self-contained HTML reports for inspection and sharing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated reports can contain workflow inputs, outputs, reasoning, errors, costs, and operational metadata from OSOP logs. <br>
Mitigation: Review generated HTML before sharing it outside the intended audience. <br>
Risk: The skill reads local OSOP files provided by the user and creates local HTML copies of their contents. <br>
Mitigation: Run it only on files you intend to inspect and store as a report. <br>


## Reference(s): <br>
- [OSOP homepage](https://osop.ai) <br>
- [ClawHub skill page](https://clawhub.ai/archie0125/osop-report) <br>
- [Publisher profile](https://clawhub.ai/user/archie0125) <br>


## Skill Output: <br>
**Output Type(s):** [Files, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Self-contained HTML report file plus a short file-path response] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reads selected .osop and .osoplog.yaml files and writes an HTML report next to the source file or to a requested output path.] <br>

## Skill Version(s): <br>
1.2.0 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
