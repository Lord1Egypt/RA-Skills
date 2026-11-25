## Description:

Scan supplied diff or patch text for secret-looking values in added lines, with findings masked and no network access.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nenadzivotic](https://clawhub.ai/user/nenadzivotic)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill before committing or while reviewing a patch to find secret-looking values in added diff lines and receive masked findings with file and line references.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: ClawScan rates this skill suspicious because it reports inspecting Git metadata beyond the stated patch-only secret scan; the scan is partial, so the evidence is incomplete.

Mitigation: Consider the reported extra Git metadata access before installing. If only a scan of supplied patch lines is needed, wait for complete review or choose a tool whose behavior stays within that scope.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/nenadzivotic/skills/git-history-leak-check-lite)

## Skill Output:

**Output Type(s):** [Analysis, JSON, Guidance]

**Output Format:** [JSON report with file and line references and masked secret fingerprints]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Scans added diff lines only; values are masked; zero findings do not establish that repository history is clean.]

## Skill Version(s):

1.1.0 (source: release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
