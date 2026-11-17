## Description:

Test that a Cloud Agent environment will work with prebuilt environment builds and recommend any required changes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[eohmig](https://clawhub.ai/user/eohmig)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to review a Cloud Agent environment before enabling prebuilt environment builds, classify setup work across install, start, and terminals, and identify changes needed for build compatibility.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The packaged skill references a workflow file that is not present in the artifact.

Mitigation: Confirm the referenced workflow is available before relying on the skill for complete migration steps.

Risk: Misplacing long-running services or per-boot work in install can cause builds to hang or produce agents without required services.

Mitigation: Review setup commands by lifecycle, keep install idempotent and terminating, and validate with a build plus a fresh-agent smoke test when tools allow.

Risk: Secrets may be exposed if copied into environment files, Dockerfiles, scripts, logs, or chat output during migration.

Mitigation: Use supported environment secret or build-secret mechanisms and avoid printing sensitive values.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/eohmig/skills/migrate-to-builds)

## Skill Output:

**Output Type(s):** [analysis, markdown, configuration, shell commands, guidance]

**Output Format:** [Markdown with concise recommendations and optional inline shell commands or configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include linked environment or build IDs when available.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
