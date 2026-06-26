# AGENTS.md

This folder is the ClawHub-safe OpenClaw edition of `ifq-app-builder` (v1.0.1).

## Entry point

Load `SKILL.md` first. For machine-readable marketplace metadata, read `clawhub.json`.

## What this package does

It turns a three-sentence app idea into a verified `*.prompt.md` build bundle across 12 platform modes:

- desktop / macOS / Windows
- iOS / Android / HarmonyOS
- Flutter / React Native Expo
- WeChat MiniProgram
- local self-hosted web / PWA / CLI

## What it must not do

- Do not install platform SDKs.
- Do not ask for signing certificates or store tokens during Tier 0.
- Do not write outside the active workspace.
- Do not claim a package exists unless a build command returned `0` and the artifact exists.
- Do not add dependencies or install hooks to this ClawHub package.

## Local checks

```bash
npm run validate
npm run validate:templates
npm run evals:validate
npm run pack
```

All must pass before publishing to ClawHub. The root repo also tests that two consecutive `npm run pack` outputs are byte-for-byte identical and contain no schema artifacts.
