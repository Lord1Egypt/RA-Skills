# Literature Review Paper Screener — Local Agent Skill

Copyright (c) 2026 ez-hq

## What this is

The local (internet-enabled) layer of the Literature Review Paper Screener. It searches for
literature, collects evidence, builds a **Literature Evidence Package** with Evidence
Availability Levels A–D, submits it to the private Cloud template for screening, then
audits the results and renders Excel Paper Sheet + Reading List outputs.

Full workflow: see `SKILL.md`.

## License

This repository is licensed under the **MIT License** (see `LICENSE`). The MIT License
covers only the local Agent Skill code in this package: search, evidence collection,
validation, and Excel rendering.

## ⚠️ Proprietary Cloud Template — NOT covered by MIT

The **Cloud Template** behind this Paper Screener — the screening instructions, step
definitions, model configuration, and all prompts executed on the LoomLoom / CogFoundry
platform — is **proprietary and confidential**. It is NOT covered by the MIT License and
is NOT distributed in this package. The Cloud template lives only in the private template
registry and must not be reproduced or published from this repository.

Using, modifying, or redistributing the local code under MIT does **not** grant any rights
to the Cloud template or its prompts.
