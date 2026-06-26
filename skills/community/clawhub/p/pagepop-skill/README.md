# pagepop-skill

Generic installable PagePop skill package.

This package is the skill layer that can be adapted to different hosts. It should depend on `pagepop-core` for PagePop behavior and keep host-specific instructions outside this directory.

Build output should be generated from templates and written to `dist/`.

## Manifest

`skill-manifest.json` is committed with public-safe `source` defaults so GitHub source installs can run directly.
Release packages overwrite it with a generated manifest rendered from `skill-manifest.template.json`.
Source installs skip release-package update enforcement; update them by pulling the latest GitHub source.

Do not commit generated manifests that contain environment-specific values.

## Local Build

From the repository root:

```bash
python3 scripts/build-skill.py \
  --pagepop_package_version YYYY.MM.DD-rN \
  --pagepop_skill_channel prod
```
