# Dependency risk review

## Scope and confidence

- Repository/workspaces inspected:
- Package manager and evidence:
- Manifests and lockfiles inspected:
- Local commands run:
- Networked checks run or skipped:
- Limitations and blind spots:

## Executive summary

State the overall risk, the most important action, and whether any confirmed critical/high issue exists. Keep this short.

## Findings

For each actionable finding, use:

### [Severity] Finding title

- **Package/path:** package and direct/transitive path
- **Evidence:** file, resolved version, command result, advisory, or registry metadata
- **Impact:** realistic consequence for this repository
- **Confidence:** confirmed, likely, or needs verification
- **Action:** smallest safe next step
- **Verify:** exact read-only command or check
- **Blast radius:** expected compatibility, runtime, build, or lockfile implications

Order findings by severity, then confidence and reachability. Do not create empty severity sections.

## Upgrade plan

Group compatible changes into:

1. Immediate containment or security fixes.
2. Low-risk patch/minor updates.
3. Major upgrades requiring migration or testing.
4. Cleanup candidates requiring usage verification.

## Clean result

If there are no actionable findings, say so directly. Still document checks performed and blind spots such as skipped registry access, missing installs, private packages, or untested runtime paths.
