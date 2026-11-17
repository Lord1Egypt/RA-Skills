# Review checklist

Use only the sections relevant to the repository. Record concrete file paths, package names, versions, and dependency paths as evidence.

## Repository and package-manager integrity

- Multiple lockfiles or a lockfile that conflicts with `packageManager` or CI commands.
- Missing lockfile for an application, unexpected lockfile changes, unresolved merge markers, or manifest/lockfile drift.
- Workspace packages omitted from the root configuration or inconsistent dependency policies across packages.
- Unpinned package-manager versions in CI where reproducibility matters.
- Registry overrides, mirrors, scoped registries, patches, overrides, or resolutions that materially change provenance.
- Git, URL, local-path, tarball, alias, or wildcard dependency specifications that need explicit justification.

## Security and supply chain

- Advisories affecting the resolved version, not merely a package name.
- Whether the vulnerable package is direct or transitive and whether it reaches production code.
- Lifecycle scripts (`preinstall`, `install`, `postinstall`, `prepare`) and native builds, especially in newly added or unfamiliar packages.
- Suspicious package names, typosquatting indicators, unexpected maintainership/provenance changes, or registry-source changes. Require external evidence before labeling a package malicious.
- Deprecated packages, compromised releases, missing integrity data, or lockfile entries resolving outside the expected registry.
- Broad overrides or forced resolutions that suppress a security fix or violate peer constraints.
- Secrets or authentication material embedded in registry configuration. Never reproduce secret values in the report.

## Maintenance and compatibility

- Direct dependencies behind supported releases, separating patch/minor updates from majors.
- Runtime, framework, Node.js, TypeScript, peer-dependency, and engine compatibility.
- End-of-life packages or ecosystems, using maintainer documentation or registry metadata as evidence.
- Packages with replacements officially recommended by maintainers.
- Duplicate major versions or large transitive packages that materially affect bundle size, install time, or attack surface.
- Platform-specific or native dependencies that complicate CI, containers, or deployment.

## Necessity and placement

- Runtime packages used only by tests, builds, linting, types, or code generation that could be development dependencies.
- Development packages imported by shipped runtime code.
- Overlapping libraries that solve the same task; explain migration cost before recommending consolidation.
- Apparently unused direct dependencies. Mark these `needs verification` unless framework, plugin, dynamic-import, and configuration usage have been checked.
- Missing peer dependencies or peers incorrectly duplicated as regular dependencies.

## Scripts and execution surface

- Root and workspace scripts that download or execute remote code, use `curl | sh`, invoke package runners without pinned versions, weaken TLS, or expose credentials.
- `pre*` and `post*` hooks that execute implicitly around common commands.
- CI commands that install without a frozen/immutable lockfile.
- Release or publish scripts with destructive actions or broad credentials.

## Evidence quality

Strong evidence combines at least two relevant sources, such as the resolved lockfile entry plus an advisory and a reachable dependency path. Lower confidence when only registry age, download counts, repository activity, heuristic unused checks, or a single audit tool supports the claim.
