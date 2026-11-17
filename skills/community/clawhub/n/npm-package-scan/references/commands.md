# Read-only command guide

Choose commands for the detected package manager and version. Check `--help` when syntax may differ. Do not install a missing tool just to complete the review.

## Discover files

```bash
rg --files -g 'package.json' -g 'package-lock.json' -g 'npm-shrinkwrap.json' \
  -g 'pnpm-lock.yaml' -g 'pnpm-workspace.yaml' -g 'yarn.lock' \
  -g '.yarnrc.yml' -g '.npmrc' -g 'bun.lock' -g 'bun.lockb' \
  -g '!node_modules' -g '!dist' -g '!build' -g '!.git'
```

If `rg` is unavailable, use the environment's file-search facility with equivalent exclusions.

## Local inventory

Run only the command matching the repository's package manager:

```bash
npm ls --all --json
pnpm list --depth Infinity --json
yarn list --json
bun pm ls --all
```

Installed-tree commands may fail or be incomplete when dependencies are not installed. The lockfile remains the source of resolved-version evidence.

Useful targeted dependency paths:

```bash
npm explain <package>
pnpm why <package>
yarn why <package>
bun pm why <package>
```

## Registry-backed checks

These commands may send dependency metadata to a registry. State that before running them. Prefer JSON or machine-readable output, save noisy output outside the repository when possible, and do not include credentials in logs.

```bash
npm audit --ignore-scripts --json
npm outdated --json

pnpm audit --json
pnpm outdated --format json

# Yarn Berry / modern Yarn
yarn npm audit --json
yarn outdated --json

bun audit
bun outdated
```

Package-manager versions differ. If a command is unsupported, report that limitation instead of substituting a mutating command. For private registries, confirm that the existing project configuration is intended for the check; do not rewrite registry settings.

## Safe lockfile consistency checks

When the repository's documented workflow supports it, a frozen/immutable install can reveal manifest drift, but it may write `node_modules`, use the network, and execute tooling. Do not run it during a read-only review unless the user authorizes those effects. Suitable commands for CI recommendations include:

```bash
npm ci --ignore-scripts
pnpm install --frozen-lockfile --ignore-scripts
yarn install --immutable --mode=skip-builds
bun install --frozen-lockfile --ignore-scripts
```

## Avoid during review

Do not run automatic remediation or implicit execution commands such as:

```text
npm audit fix [--force]
pnpm audit --fix
yarn npm audit --fix
npx <untrusted-package>
```

Also avoid fresh installs, lockfile regeneration, cache cleaning, deduplication, or package-manager migration unless explicitly requested.
