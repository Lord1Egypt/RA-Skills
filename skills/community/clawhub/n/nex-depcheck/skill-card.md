## Description: <br>
Skill dependency checker. Scan Python skills for external dependencies. Verify stdlib-only compliance, check individual files or entire skill directories. No database needed, pure file scanner. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nexaiguy](https://clawhub.ai/user/nexaiguy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and skill publishers use Nex DepCheck to scan Python skill files or directories for external imports before publishing or deployment. It helps verify stdlib-only compliance and identify dependency issues in individual files, a single skill, or a directory of skills. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Directory scans read Python files under the target path provided by the user. <br>
Mitigation: Run scans only against the project, file, or skills directory intended for dependency review. <br>
Risk: Dependency classifications can affect publishing decisions if accepted without review. <br>
Mitigation: Review the reported external imports and rerun the scanner with verbose output when a result affects release readiness. <br>


## Reference(s): <br>
- [Nex AI website](https://nex-ai.be) <br>
- [ClawHub skill page](https://clawhub.ai/nexaiguy/nex-depcheck) <br>
- [Publisher profile](https://clawhub.ai/user/nexaiguy) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Plain text CLI output and Markdown usage guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports import classifications as stdlib, internal, or external; directory scans read Python files under the requested target path.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
