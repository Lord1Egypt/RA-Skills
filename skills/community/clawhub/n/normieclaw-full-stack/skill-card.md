## Description:

Every NormieClaw skill in one download. 34 production-tested OpenClaw skills covering productivity, finance, health, education, content creation, and more.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nollio](https://clawhub.ai/user/nollio)

### License/Terms of Use:

NormieClaw License Agreement

## Use Case:

External users install this bundle to give an OpenClaw-compatible agent access to a broad set of productivity, finance, health, education, content, career, home, security, and business workflows. Users can copy individual subskills into their agent environment or install the full collection.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The bundle includes broad persistent data handling across many subskills, including finance, health, legal, memory, and indexing workflows.

Mitigation: Install only the subskills needed for the intended use case, scope or disable passive memory and indexing, and review local data retention before use.

Risk: The security evidence reports a real code-injection flaw in a legal-document script.

Mitigation: Do not run the Legal Docs contract scanner on untrusted filenames until the script is patched and re-reviewed.

Risk: Several subskills include scheduled jobs or setup scripts that may run shell, npx, or npm commands.

Mitigation: Review scheduled jobs before enabling them and pin dashboard setup tools before running package-manager commands.

## Reference(s):

- [ClawHub listing](https://clawhub.ai/nollio/skills/normieclaw-full-stack)
- [NormieClaw license terms](https://normieclaw.ai/license)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with optional code, shell commands, configuration files, reports, templates, and dashboard specifications depending on the selected subskill.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs vary by subskill and may involve local files, scripts, schedules, or generated reports.]

## Skill Version(s):

1.0.0 (source: server release metadata, created 2026-03-30)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
