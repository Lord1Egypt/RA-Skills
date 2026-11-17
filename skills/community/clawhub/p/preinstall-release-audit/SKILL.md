---
name: "preinstall-release-audit"
description: "Audit public software releases before installation using static artifacts, license checks, endpoint scans, and live distribution verification."
---

# Preinstall release audit

Use when deciding whether to install unfamiliar public software, especially when source, packaged engine, and desktop assets may have different licenses or release paths.

## Procedure

1. Identify each distribution surface: source repository, package registry artifact, release page, installer links, update manifest, and vendor API.
2. Record versions and artifact names before comparing claims. Do not assume the repository tag, package version, and desktop release are identical.
3. Download or obtain the distributable without running its installer or importing its code. Unpack it as data in a temporary location.
4. Read the artifact’s embedded license and metadata. Compare them with repository and template licenses. Report rights per component; never infer engine rights from an openly licensed UI or template.
5. Inspect packaged persistence and configuration code for credential storage location, file-permission handling, and destructive writes.
6. Inspect updater and launcher code for release hosts, package-manager behavior, relaunch behavior, and what constitutes update success.
7. Enumerate hard-coded HTTP(S) endpoints across packaged source. Classify them as loopback, model provider, vendor service, release/update service, or other external destination. Treat this as static evidence, not proof of runtime behavior.
8. Verify advertised installers and manifests live. Follow redirects and record the final HTTP status; an initial redirect does not prove the target asset exists.
9. Separate findings into observed facts, confidence limits, and recommendation. State explicitly what was not executed and what static inspection cannot exclude.
10. Prefer an isolated environment and pinned version for any subsequent trial; installation remains a separate decision.

## Pitfalls

- Repository visibility does not establish that every shipped component is open source.
- A successful first HTTP response can redirect to a missing release asset.
- No suspicious endpoint found statically is not evidence that telemetry or dynamic network behavior is absent.
- Reading source through imports can execute package code; inspect unpacked files as data.
- Update code may treat a zero exit status as success even when no version changed; inspect its success criteria rather than trusting UI wording.

## Verification

Before reporting, confirm all four evidence classes are present: artifact metadata/license, packaged code inspection, endpoint inventory, and final-status checks for advertised downloads or manifests. Cite artifact version and exact file or URL for each material claim. If a class is unavailable, mark that gap instead of filling it by inference.
