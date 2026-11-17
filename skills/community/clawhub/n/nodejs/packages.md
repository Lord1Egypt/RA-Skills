# Packages — Versions, Installs, Workspaces, Publishing

## Version Ranges

- `^1.2.3` floats minor versions, but `^0.2.3` floats only patches — pre-1.0, semver treats minor as breaking. Apps: exact versions + committed lockfile. Libraries: ranges — exact deps in a library force duplicate copies into every consumer's tree.
- Prereleases (`1.3.0-beta.1`) do not satisfy `^1.2.0`: ranges never match a prerelease of a different version unless you ask for it explicitly. That is why a beta "isn't picked up" and why one accidentally published beta does not break the world.
- The three dependency fields answer three different questions: `dependencies` (needed at runtime by consumers), `devDependencies` (needed to build or test this repo), `peerDependencies` (must be supplied by the host app, one shared copy — plugins, frameworks, anything with module-level state).
- `optionalDependencies` fail silently when they cannot install, which is right for platform-specific binaries and wrong for anything the code assumes exists.

## Installing

- `npm install` mutates the lockfile whenever package.json allows it; `npm ci` deletes node_modules, installs the lockfile exactly, and fails on any mismatch — the only correct install for CI and production images (SKILL.md rule 6).
- Production images: `npm ci --omit=dev` — devDependencies inflate image size and audit surface for code that never runs.
- The lockfile is a reviewable artifact. A diff that changes a hundred transitive versions in a PR about a typo means someone ran a bare `npm install` on a stale branch; regenerate deliberately rather than merging it.
- Merge conflicts in a lockfile are resolved by regenerating, not by hand-editing: take the incoming package.json, delete the lockfile, install, commit. Hand-merged lockfiles produce trees that exist on no machine.
- Install scripts run arbitrary code from every transitive dependency at install time. `npm ci --ignore-scripts` where the build tolerates it removes the largest supply-chain surface; native modules are the usual reason it cannot (→ `runtime.md`).
- `peerDependencies` auto-install since npm 7 — and auto-conflict; when two majors of one package coexist, `npm ls <pkg>` shows which dependency paths pulled each.
- `overrides` (npm >=8.3) pins a transitive dependency — the surgical fix for a vulnerability three levels deep. `npm audit fix --force` is the sledgehammer: major bumps, silent breakage.

## Auditing and Updating

- Audit triage by path, not count: an advisory in a devDependency that never executes in production is usually noise — check reachability with `npm ls <vuln-pkg>` before scheduling work. A "0 vulnerabilities" badge earned by upgrading unrelated majors is a net loss.
- Update on a rhythm, in small batches, patch and minor first: a monthly batch of 30 patch bumps is one afternoon; a yearly one is a quarter's project. Majors get their own PR each, with the changelog read.
- Distinguish "wanted" from "latest" in `npm outdated`: wanted is what your ranges already allow (a lockfile refresh), latest is a deliberate decision.
- Before adding a dependency, price it: transitive count, install size, last release date, whether it has native code, and whether the same thing is now in core (`fetch`, `parseArgs`, `node:test`, `--env-file`, `structuredClone` all replaced popular packages).
- A dependency that is unmaintained is not automatically a problem — a small, finished, dependency-free package that does one thing is safer than a maintained one with forty transitive deps.

## Workspaces and Monorepos

- Workspaces hoist shared dependencies to the root: a package can import something it never declared and work locally, then fail when published. Verify each publishable package installs alone before release.
- Version internal dependencies exactly (`"@scope/util": "1.4.2"`, not `^`), or a partially published set of packages resolves to a mix of old and new at consumer install time.
- Two versions of the same package in one workspace tree means two module instances — the singleton and `instanceof` failures in `modules.md` show up as "impossible" bugs in tests that pass individually.
- `npm ci` at the root installs every workspace: build a production image from a filtered install (`--workspace=<name> --omit=dev`) or the image carries the whole monorepo's dependencies.

## Publishing

- Know what ships before it ships: `npm pack --dry-run` lists the tarball contents. Prefer the `files` whitelist over `.npmignore` — deny-lists forget files added later, which is how `.env` files and internal notes get published.
- Verify the entry points resolve from a clean install, not from the repo: `npm pack`, install the tarball into an empty project, then import it as both ESM and CJS if you claim both (→ `modules.md`).
- `prepublishOnly` runs only before `npm publish`; `prepare` also runs when someone installs your package from git — put the build in `prepare` if git installs should work.
- Publish with provenance and 2FA on the account; a package with write access from a single unprotected token is a supply-chain incident waiting for a phishing email.
- You cannot unpublish freely after 72 hours. The remedies are `npm deprecate` (a warning on install) and publishing a fixed version; plan the release as if it is permanent, because it is.
- Semver is a promise about *consumers*, not about effort: removing an export, tightening an input type, renaming a subpath in `exports`, or raising the minimum Node version is a major, however small the diff.

## Containers and CI

- Copy `package.json` and the lockfile first, install, then copy the source — otherwise every source edit invalidates the dependency layer and each build reinstalls from scratch (→ `production.md`).
- Never copy `node_modules` from the host: native modules carry the host's OS, arch, and libc (→ `runtime.md`). Install inside the image, multi-stage to drop compilers from the final layer.
- Cache the package manager's store, not `node_modules`: the store is portable across projects and branches, `node_modules` is a resolved tree that goes stale silently.
- Pin the registry explicitly in CI and mirror it if builds must survive a registry outage; a private scope plus a public default is the configuration that leaks internal package names when it is wrong.
