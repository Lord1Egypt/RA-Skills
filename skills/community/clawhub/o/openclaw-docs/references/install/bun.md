# Bun (Experimental)

Source: https://docs.openclaw.ai/install/bun

[Skip to main content](#content-area)OpenClaw home pageEnglishSearch...⌘KSearch...NavigationOther install methodsBun (Experimental)Get startedInstallChannelsAgentsToolsModelsPlatformsGateway & OpsReferenceHelpInstall overview
InstallInstaller Internals
Other install methods
DockerPodmanNixAnsibleBun (Experimental)
Maintenance
UpdatingMigration GuideUninstall
Hosting and deployment
Fly.ioHetznerGCPmacOS VMsexe.devDeploy on RailwayDeploy on RenderDeploy on Northflank
Advanced
Development Channels
On this page
- [Bun (experimental)](#bun-experimental)
- [Status](#status)
- [Install](#install)
- [Build / Test (Bun)](#build-%2F-test-bun)
- [Bun lifecycle scripts (blocked by default)](#bun-lifecycle-scripts-blocked-by-default)
- [Caveats](#caveats)

​Bun (experimental)
Goal: run this repo with **Bun** (optional, not recommended for WhatsApp/Telegram)
without diverging from pnpm workflows.
⚠️ **Not recommended for Gateway runtime** (WhatsApp/Telegram bugs). Use Node for production.
​Status

- Bun is an optional local runtime for running TypeScript directly (`bun run …`, `bun --watch …`).

- `pnpm` is the default for builds and remains fully supported (and used by some docs tooling).

- Bun cannot use `pnpm-lock.yaml` and will ignore it.

​Install
Default:
Copy```
bun install

```

Note: `bun.lock`/`bun.lockb` are gitignored, so there’s no repo churn either way. If you want *no lockfile writes*:
Copy```
bun install --no-save

```

​Build / Test (Bun)
Copy```
bun run build
bun run vitest run

```

​Bun lifecycle scripts (blocked by default)
Bun may block dependency lifecycle scripts unless explicitly trusted (`bun pm untrusted` / `bun pm trust`).
For this repo, the commonly blocked scripts are not required:

- `@whiskeysockets/baileys` `preinstall`: checks Node major >= 20 (we run Node 22+).

- `protobufjs` `postinstall`: emits warnings about incompatible version schemes (no build artifacts).

If you hit a real runtime issue that requires these scripts, trust them explicitly:
Copy```
bun pm trust @whiskeysockets/baileys protobufjs

```

​Caveats

- Some scripts still hardcode pnpm (e.g. `docs:build`, `ui:*`, `protocol:check`). Run those via pnpm for now.

AnsibleUpdating⌘I