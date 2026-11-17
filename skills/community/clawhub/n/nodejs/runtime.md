# Runtime — Versions, Flags, and Native Modules

Which Node runs the code, how it was configured before your first line executed, and why a compiled dependency that worked yesterday no longer loads.

## Version Policy

Release cadence (stable policy, not a snapshot): a new major every April and October. Even majors enter LTS that October and get roughly 3 years total — 6 months Current, 12 months Active LTS, 18 months Maintenance. Odd majors are Current for ~6 months and then dead; they exist for library authors to test against, not for production.

Live majors as of 2026-07: 24 is Active LTS, 26 is Current (LTS from October 2026), 22 is in Maintenance, 20 reached end of life in April 2026. Re-check `nodejs.org/en/about/previous-releases` before quoting a support date; the cadence above stays true, these four facts do not.

- Upgrade at the LTS boundary, not at the EOL date: skipping to a fresh Current major puts you on a runtime that changes under you every two weeks.
- Pin the runtime in three places or they drift: `engines` in package.json (declares intent, warns on install), a `.nvmrc`/`.node-version` file (developers), and the container base image tag (production). All three should say the same major.
- `engines` is advisory for npm by default; `engine-strict=true` in `.npmrc` makes a mismatch fail the install instead of printing a warning nobody reads.
- Minimum-version claims in code and docs get verified against the Version Gates table in SKILL.md — that table is the single home for those numbers.

## Flags and NODE_OPTIONS

- Flags come from three places and are merged: the command line, the `NODE_OPTIONS` environment variable, and any shebang arguments. `node -p "process.execArgv"` shows what actually applied (→ `commands.md`).
- `NODE_OPTIONS` is inherited by every child process — a debugging flag left in a shell profile silently applies to installs, test runners, and build tools. It also rejects flags that could change the security posture (`--experimental-*` loaders are restricted there).
- Some flags must exist before the process starts and cannot be set from inside: `--max-old-space-size`, `--max-semi-space-size`, `UV_THREADPOOL_SIZE`. Setting them in code changes nothing for the current process.
- `--experimental-*` flags mean "the API may change in a patch release". Fine behind a version pin, expensive when a minor upgrade renames the flag out from under a deploy.
- The permission model (`--permission`, with `--allow-fs-read`, `--allow-fs-write`, `--allow-child-process`, `--allow-worker`) restricts a process's capabilities from the runtime side. It is still experimental as of Node 24 (2026-07): useful as defense in depth, not as the boundary for genuinely untrusted code — that boundary is a separate process or container (→ `security.md`).

## Native Modules (why the binary broke)

A native module is a C/C++ addon compiled against a specific V8/Node ABI, OS, architecture, and libc. Change any one and it stops loading.

| Symptom | Cause | Fix |
|---|---|---|
| `was compiled against a different Node.js version` / `NODE_MODULE_VERSION 115 vs 127` | ABI changed with the Node major | `npm rebuild`, or reinstall after switching versions |
| `invalid ELF header` / `wrong architecture` | Copied `node_modules` between OS or arch (arm64 laptop → amd64 server) | Install inside the target image; never copy the folder |
| `Error relocating ...: symbol not found` on Alpine | Prebuilt binary targets glibc, Alpine ships musl | Use a glibc base image, or build from source with the musl toolchain |
| `node-gyp` fails: missing python/make/g++ | No build toolchain in the image | Install build deps in a builder stage, ship only the compiled output |
| Works in dev, missing in the production image | The prebuild download happened on the host, not in the image | Run the install inside the image; keep the network available to that step or vendor the prebuild |

- N-API (`node-api`) addons are ABI-stable across majors and do not need a rebuild per upgrade — prefer dependencies that ship N-API prebuilds when you have a choice; it removes this entire failure class.
- Multi-stage Docker: compile in a stage with the toolchain, `COPY` the resulting `node_modules` into a slim runtime image. Shipping compilers to production is both size and attack surface (→ `production.md`).
- Cross-architecture CI (arm64 developers, amd64 servers) must build per target architecture; emulation works and is several times slower for compiled code.
- Lockfiles do not capture prebuilt binaries. Two installs of the same lockfile on different platforms produce different bytes on disk — which is why "it's the same lockfile" is not an argument when the container misbehaves.

## Version Managers and Package Manager Pinning

- One version manager per machine (nvm, fnm, volta, asdf). Two of them fighting over PATH produces the most confusing class of "wrong Node" bug, because `which node` and the shell's actual resolution disagree per shell type.
- Global installs live per Node version: switching majors makes globally installed CLIs vanish. Prefer running project tools through the local `node_modules/.bin` (`npm exec`/`npx`, or `node --run`) so the tool version travels with the repository.
- `packageManager` in package.json plus corepack pins which package manager and version runs, so a yarn-era repo does not get a stray `npm install`. Corepack ships with Node but its status has changed across majors — check whether it is enabled on your target before depending on it in CI.
- CI must install the exact runtime version the deploy uses; "latest LTS" in a workflow file changes under you every six months, on someone else's schedule.

## Deprecations and Upgrade Checks

- Run the suite with `--throw-deprecation` on a branch before a major upgrade: it converts warnings into failures with stacks, turning a vague "will break someday" into a finite list.
- `--pending-deprecation` surfaces the deprecations that are not yet warning by default — the next major's breakage, visible today.
- Read the major's changelog for V8 changes, not just Node's API list: regex, `Intl`, and error-message changes arrive through V8 and break tests that assert on exact strings.
- After any upgrade, re-verify the four numeric assumptions the rest of this skill depends on: threadpool size, heap ceiling behavior under the container limit, HTTP server timeout defaults, and unhandled-rejection behavior (all indexed in SKILL.md).
