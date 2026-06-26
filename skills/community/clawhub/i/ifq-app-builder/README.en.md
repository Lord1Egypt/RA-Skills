<sub><a href="README.md">Chinese</a> · English · <code>ifq.ai / app-builder / OpenClaw</code></sub>

# IFQ App Builder · ClawHub Edition

A ClawHub-safe OpenClaw skill: **three sentences in, one verified build-ready app prompt bundle out**. It does not silently install SDKs or pretend store submission has happened. It turns a short app idea into a `*.prompt.md` bundle with platform route, scaffold, acceptance, packaging, security, i18n, and IFQ colophon.

## Install

```bash
openclaw skills install ifq-app-builder
openclaw skills info ifq-app-builder
openclaw skills check ifq-app-builder
```

This package is designed for one-pass ClawHub review: zero dependencies, zero install hooks, no required credentials, no script-side network, no process spawning, no schema artifacts in the tarball, workspace-only permissions, and deterministic tarball packaging.

## First run

Say:

```text
Use ifq-app-builder to create a Mac + Windows desktop tool that turns PDF invoices into an Excel ledger. It must run locally with no network.
```

A good first run returns six pieces of evidence:

- output `*.prompt.md` path
- mode route, such as `A-01`
- template id, such as `T-pc-tauri`
- assumptions made
- verification command and result
- caveats that affect use

The first run should not ask for login, install Xcode/Android Studio/Flutter/Rust, configure certificates, start background services, or claim store submission.

## Good starter prompts

```text
Build a self-hosted engineering weekly-report system with Docker Compose, LDAP login, and zh-CN/en strings by default.
Create a WeChat MiniProgram for employee health check-ins that produces weekly statistics automatically.
Create a CLI tool that scans every screenshot in a folder and renames each file by detected content.
```

Use one ordinary sentence when you are exploring; use three sentences when you already know user, platform, and acceptance.

## Maintainer commands

```bash
npm run validate
npm run validate:templates
npm run evals:validate
npm run verify:lite -- demos/desktop-invoice-ledger.prompt.md
npm run quality:score -- demos/desktop-invoice-ledger.prompt.md
npm run pack
```

`npm run pack` is reproducible: archive mtimes are fixed, forbidden entries are rejected, and schema artifacts stay out of the upload.

## Why ClawHub should like it

| Review signal | How this package satisfies it |
|---|---|
| Clear job | App prompt bundles only; no visual-only design, SEO, or backend-only scope |
| First-run value | Natural language → mode route → template fork → verified prompt bundle |
| Safe boundary | No SDK install, no credentials, no daemon, workspace-only writes |
| Scanner-friendly | Zero dependencies, no install hooks, no schema artifacts, scripts have no network or process-spawn primitives |
| Maintainable | `clawhub.json`, frontmatter, evals, templates, and validate checks agree |

## Publish

```bash
npm run validate
npm run pack
```

Upload `../ifq-app-builder-clawhub-YYYY-MM-DD.tar.gz`, not the raw Git checkout.

— shaped with ifq.ai/app-builder · OpenClaw · ClawHub
