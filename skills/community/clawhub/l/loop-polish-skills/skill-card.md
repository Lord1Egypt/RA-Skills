## Description:

Loop Polish automates full-stack project startup, integration verification, browser checks, scoring, conservative auto-fixes, regression loops, and report generation when explicitly requested.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lqclf](https://clawhub.ai/user/lqclf)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use Loop Polish as an automated QA and acceptance loop for trusted dev or staging full-stack projects. It is suited for explicitly requested pre-release verification where an agent can start services, test APIs and UI flows, apply limited fixes, and generate a quality report.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow can modify project source code during auto-fix rounds.

Mitigation: Run it only in trusted dev or staging workspaces, review generated diffs before merging, and keep fixes conservative unless broader changes are explicitly approved.

Risk: Database verification may read database configuration and query project data.

Mitigation: Use non-production databases and set db_verify=false when credential access is not acceptable.

Risk: Project startup and browser automation may install dependencies, launch services, or manage local ports.

Mitigation: Use an isolated workspace, pin or preinstall dependencies such as Playwright, and review port conflicts before allowing process termination.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lqclf/skills/loop-polish-skills)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown progress updates, shell commands, code diffs, configuration snippets, and final reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create report files, state files, branches, service processes, and source-code edits during a full run.]

## Skill Version(s):

1.1.2 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
