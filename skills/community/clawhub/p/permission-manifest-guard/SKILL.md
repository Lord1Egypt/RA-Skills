---
name: permission-manifest-guard
version: 0.1.0
description: >
  Inspects an OpenClaw skill directory before install or execution,
  translates declared and observed requirements into a human-readable
  permission manifest, and recommends disposition (review, sandbox, or reject)
  when metadata does not match observed behaviour.
capabilities:
  - read_filesystem
---

## When to invoke

Use this skill when you need to understand what permissions a skill requires
before granting trust. Invoke it when:

- **Reviewing a new skill before install** — a skill has been downloaded or
  proposed and you need to know what it accesses before allowing execution.
- **Checking skill permissions** — you want a summary of every
  permission-relevant signal (binaries, network, env vars, file paths, shell
  commands, config files, package managers, risky capabilities).
- **Generating a permission manifest** — you need a human-readable markdown
  report and a machine-parseable JSON manifest for audit or policy decisions.
- **Deciding whether to sandbox or reject a skill** — the skill's observed
  behaviour may exceed its declared capabilities and you need a scored
  recommendation.
- **Auditing a skill's declared vs observed behaviour** — you want to compare
  what SKILL.md claims against what the source code actually does.

If the task does not involve evaluating skill trust, permissions, or install
safety, this skill is not the right tool.

## How to call — CLI

Run the skill from the command line, passing the skill directory as the
sole argument:

```
npx permission-manifest-guard /path/to/skill
```

**Stdout:** The markdown permission manifest (human-readable report).
Pipe or redirect as needed.

**Stderr:** Diagnostic warnings from analysis stages, plus the path to the
written JSON file.

**Side effect:** Writes `permission-manifest.json` into the skill directory.
This file contains the structured manifest for machine consumption.

**Exit code:** 0 on success, 1 on invalid arguments or analysis failure.

## How to call — programmatic

Import `analyzeSkill` and call it with the skill directory path:

```typescript
import { analyzeSkill } from 'permission-manifest-guard';

const result = await analyzeSkill('/path/to/skill');
```

The returned `AnalysisResult` has three fields:

| Field              | Type                 | Description                                    |
|--------------------|----------------------|------------------------------------------------|
| `markdownManifest` | `string`             | Complete markdown permission report.           |
| `jsonManifest`     | `object`             | Structured manifest matching the markdown data.|
| `diagnostics`      | `DiagnosticWarning[]`| Warnings from discovery, extraction, or classification stages. Each entry has `file`, `stage`, `message`, and `error` fields.|

## What to do with the output

The analysis produces a **disposition recommendation** based on how well the
skill's declared metadata matches its observed source-code behaviour. Act on
the recommendation as follows:

- **allow** — Declared capabilities match observed behaviour. No undeclared
  access detected. Install the skill normally.
- **review** — Minor mismatches found (e.g. an undeclared env var or a
  low-severity capability gap). Inspect the mismatches in the manifest before
  proceeding. A human or policy check should confirm intent.
- **sandbox** — Significant undeclared capabilities detected. Install only
  within an isolated execution environment with restricted filesystem, network,
  and process access.
- **reject** — Severe mismatches or dangerous undeclared capabilities.
  Do not install. Flag the skill for further investigation or removal from
  the registry.

The **markdown manifest** is the artifact for humans — include it in review
threads, audit logs, or approval workflows. The **JSON manifest** is for
automated pipelines — feed it to policy engines, dashboards, or gating checks.

If `diagnostics` is non-empty, some files could not be fully analysed.
Treat a skill with analysis warnings more cautiously — incomplete analysis
means the true permission surface may be larger than reported.

## Limitations

- **Static analysis only.** The skill inspects source code and metadata files.
  It does not execute the skill or trace runtime behaviour. Dynamically
  constructed commands, lazy imports, or runtime code generation will not be
  detected.
- **No transitive dependency scanning.** Only files within the skill directory
  are analysed. If the skill depends on external packages that perform
  privileged operations, those will not appear in the manifest.
- **Heuristic extraction.** Binary, domain, env-var, and shell-command
  extraction uses pattern matching. Unusual code patterns may produce false
  positives or false negatives.
- **Single-directory scope.** The tool analyses one skill directory per
  invocation. Multi-skill repositories require separate runs.
