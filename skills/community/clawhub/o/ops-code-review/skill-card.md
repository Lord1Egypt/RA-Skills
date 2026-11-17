## Description:

Ops Code Review automates SVN-based code review and security scanning for Django/Python, React with TypeScript, and PHP repositories, then prepares findings for Feishu group delivery.

This skill is ready for commercial/non-commercial use.

## Publisher:

[freepengyang](https://clawhub.ai/user/freepengyang)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operations engineers use this skill to run incremental or full repository scans across SVN-managed Django/Python, React with TypeScript, and PHP codebases. It helps identify security and quality findings, produce remediation guidance, and deliver review reports to an approved Feishu group.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: SVN credentials may be handled unsafely during repository access.

Mitigation: Fix the password-in-process-arguments issue before operational use and use a read-only SVN account scoped only to the repositories being scanned.

Risk: Dependency installation can modify the host environment and uses broad, unpinned installers.

Mitigation: Install only after review in a disposable container or dedicated scanning host, and pin dependency versions before routine use.

Risk: Configuration and generated reports can contain internal repository details or delivery identifiers.

Mitigation: Store configuration in a protected user directory instead of /tmp, keep report files access-controlled, and send reports only to an approved Feishu group.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/freepengyang/skills/ops-code-review)
- [Bundled React TypeScript ESLint config](references/eslint.react.ts.js)
- [Composer installer](https://getcomposer.org/installer)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown reports, inline shell commands, and JSON configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports may include repository names, file paths, scanner findings, remediation guidance, and Feishu delivery payloads.]

## Skill Version(s):

1.0.11 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
