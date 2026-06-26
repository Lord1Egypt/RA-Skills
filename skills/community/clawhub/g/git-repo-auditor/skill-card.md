## Description: <br>
Audit Git repositories for security issues, large files, sensitive data, and repository health metrics. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Derick001](https://clawhub.ai/user/Derick001) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, security reviewers, and repository maintainers use this skill to audit local Git repositories for committed secrets, large files, sensitive data, and repository health issues. It can produce human-readable or machine-readable reports for local review, compliance checks, and CI workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Audit reports can reveal snippets of secrets or sensitive repository metadata. <br>
Mitigation: Run the tool only on repositories you are allowed to inspect, keep terminal output and report artifacts private, avoid publishing CI logs that contain scan results, and rotate any real credentials it reports. <br>
Risk: Regex-based secret detection can produce false positives or miss some credentials. <br>
Mitigation: Treat findings as review prompts, verify results before remediation, and use custom patterns for repository-specific secret formats. <br>
Risk: Full-history scans can be slow on large repositories. <br>
Mitigation: Use branch, date range, threshold, or check-specific options to narrow scans when working with large histories. <br>


## Reference(s): <br>
- [ClawHub listing](https://clawhub.ai/Derick001/git-repo-auditor) <br>
- [Artifact README](artifact/README.md) <br>
- [Artifact Skill Definition](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, json, csv, guidance] <br>
**Output Format:** [Human-readable terminal reports, JSON reports, CSV reports, and remediation guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports may include repository paths, commit identifiers, filenames, matched secret patterns, issue severity, and suggested remediation steps.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
