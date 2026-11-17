# poe1-build-analyst v0.1.2

## Release date

2026-08-20

## Overview

`poe1-build-analyst` v0.1.2 is a documentation and release-metadata update for the Path of Exile 1 build-analysis skill. This release makes the repository self-describing, aligns the English, Traditional Chinese, and Simplified Chinese README files, and preserves the security-hardened PoB analysis workflow introduced in v0.1.1.

This release is prepared for the public GitHub repository at commit [`73c1385`](https://github.com/qpooqp777/poe1-build-analyst/commit/73c1385). The ClawHub registry remains at v0.1.1 until v0.1.2 is explicitly published there.

## Highlights

### Repository version metadata

A lightweight [`VERSION`](https://github.com/qpooqp777/poe1-build-analyst/blob/master/VERSION) file now records the repository release candidate as `0.1.2`. This provides a simple source-of-truth for repository checks and release automation without introducing an unnecessary package manifest.

### Fully aligned localized documentation

The English [`README.md`](https://github.com/qpooqp777/poe1-build-analyst/blob/master/README.md), Traditional Chinese [`README.zh-TW.md`](https://github.com/qpooqp777/poe1-build-analyst/blob/master/README.zh-TW.md), and Simplified Chinese [`README.zh-CN.md`](https://github.com/qpooqp777/poe1-build-analyst/blob/master/README.zh-CN.md) now contain the same nine primary sections. The localized versions include the endgame character-code command, optional passive-tree research utility, output schema, included resources, references, and repository-version guidance.

### Preserved security baseline from v0.1.1

This release retains the v0.1.1 hardening that removes arbitrary PoB executable selection, restricts execution to the trusted `pob` executable resolved from `PATH`, applies execution timeouts and output-size limits, validates JSON objects, and fails closed on invalid or excessive output. The skill does not upload character data and keeps `pob share --dry-run` separate from public `pobb.in` publication.

## Validation

The release candidate passed the skill-creator validation and Markdown consistency checks. The repository README files have matching primary-section counts, and the GitHub `VERSION` file contains exactly `0.1.2`.

The PoB integration regression test was executed against the ClawHub-installed v0.1.1 package, which contains the same runtime scripts as this v0.1.2 documentation and metadata candidate. Using LuaJIT and the Path of Building Community headless core, the endgame pipeline successfully decoded a PoB character code, preserved the imported build, ran both `pob analyze` and `pob calc`, selected `Vortex`, recognized tree version `3_29`, and returned `status: verified` with 782 official scalar fields.

| Validation area | Result |
| --- | --- |
| Skill structure validation | Passed |
| README language and section parity | Passed; 9 primary sections in each README |
| Repository VERSION metadata | Passed; `0.1.2` |
| PoB character-code decoding | Passed |
| Official `pob analyze` integration | Passed |
| Official `pob calc` integration | Passed |
| Endgame-only workflow contract | Passed; only `stages.endgame` was emitted |
| Public character-data upload | Not performed |

## Compatibility and requirements

The skill requires Python 3 for structural processing. Official PoB calculation requires LuaJIT and a compatible Path of Building Community source tree. The endgame character-code workflow requires a complete PoB character code rather than a short `pobb.in/<id>` URL. When the PoB root, LuaJIT runtime, XML schema, or skill metadata is unavailable, the workflow must report a blocked or failed verification state rather than fabricate metrics.

## Upgrade notes

Users installing from GitHub should verify that `VERSION` reports `0.1.2` and that all three localized README files are present. Users installing from ClawHub should verify the registry version separately: v0.1.2 is not considered published to ClawHub until its version and security audit are visible in the registry.

A public `pobb.in` URL is not created by this release. Character-code generation and public upload remain separate operations, and public sharing requires explicit user confirmation.

## Contributors

Prepared by Manus AI for the `qpooqp777/poe1-build-analyst` repository.

## References

- [GitHub repository](https://github.com/qpooqp777/poe1-build-analyst)
- [ClawHub skill](https://clawhub.ai/qpooqp777/skills/poe1-build-analyst)
- [qpooqp777/pob-cli](https://github.com/qpooqp777/pob-cli)
- [Path of Building Community Fork](https://github.com/PathOfBuildingCommunity/PathOfBuilding)
