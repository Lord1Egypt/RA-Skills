---
name: flutter-release-pipeline
description: Build and package Flutter Android release artifacts (APK/AAB), collect outputs into a single folder, and produce a short release checklist. Use when the user asks to build APK/AAB, prepare a Play Store release, bump version, gather mapping/symbols, or generate a deterministic release folder for sharing.
---

# Flutter Android Release Pipeline

## Workflow

1) **Preflight**
- Confirm `flutter --version` works.
- Confirm project path contains `pubspec.yaml`.

2) **Build** (choose one)
- AAB: `flutter build appbundle --release`
- APK: `flutter build apk --release` (optionally `--split-per-abi`)

3) **Collect artifacts**
Create `out/flutter_release_<timestamp>/` and copy:
- `build/app/outputs/flutter-apk/*.apk` (if APK build)
- `build/app/outputs/bundle/release/*.aab` (if AAB build)
- `build/app/outputs/mapping/release/mapping.txt` (if present)
- `pubspec.yaml` (snapshot)

4) **Report**
- Print paths + sizes + SHA256 for each artifact.
- Print a short checklist (versionCode/versionName sanity, signing, Play Console notes).

## Script
Run (PowerShell):
- `powershell -ExecutionPolicy Bypass -File scripts/flutter_release.ps1 -Project "<path>" -Mode aab|apk -SplitPerAbi:$false`

## Notes
- Avoid changing app code unless explicitly requested.
- If build fails, return the exact error + suggested fix.
