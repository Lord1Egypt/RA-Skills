# README FOR AI

## Purpose

This document is the authoritative implementation and maintenance contract for
the MAGI Strategic Advisor repository. It is written in English so that the
skill can be compiled and maintained consistently by any AI agent.

## Audit Findings and Required Remediation

The repository audit identified these issues and the required resolution:

| Finding | Resolution |
|---|---|
| The skill index used inconsistent filename casing. | Use `SKILL.md` exactly. |
| The routing table referenced prompt files as runtime dependencies. | Route agents to `references/` and `scripts/`; keep `prompts/` human-only. |
| The repository lacked standard governance and editor files. | Include `.editorconfig`, `CODE_OF_CONDUCT.md`, and `SECURITY.md`. |
| The changelog filename did not match the documented path. | Use `CHANGELOG.md` exactly. |
| Code-pattern documentation exposed a forbidden emoji field. | Use text-only status and risk labels. |
| The specification did not clearly separate index, references, and prompts. | Enforce the three-layer architecture below. |

## Non-Negotiable Requirements

1. All compiled skill content, reference content, scripts, and prompt content
   must be written in English.
2. No emoji characters may occur in any repository file used by the skill.
   Use text labels such as `PASS`, `FAIL`, `HIGH`, and `LOW`.
3. `SKILL.md` contains only routing indexes, quick-reference tables, and the
   compact output contract. It must remain below 120 lines.
4. Reusable code templates, schemas, signatures, and implementation patterns
   belong only in `references/method-patterns.md`. Do not duplicate them in
   `SKILL.md`, `README.md`, or prompt files.
5. Files in `prompts/` are standalone, user-facing copy-paste artifacts. They
   must not be automatically invoked by the agent runtime and must not assume
   access to this repository.
6. Every component must follow harness engineering: explicit inputs, outputs,
   side effects, exit codes, deterministic behavior, and independently
   testable boundaries.
7. New work must preserve these design principles: standardized, generic,
   modular, compact, and automated.
8. The repository is licensed under GNU GPL v3. Do not replace or abbreviate
   the full license text in `LICENSE`.

## Required File Tree

The following files are required. Additional files require an update to this
contract and to the relevant indexes.

```text
magi-advisor/
|-- .editorconfig
|-- .gitattributes
|-- .gitignore
|-- CHANGELOG.md
|-- CODE_OF_CONDUCT.md
|-- CONTRIBUTING.md
|-- LICENSE
|-- Makefile
|-- README FOR AI.md
|-- README.md
|-- SECURITY.md
|-- SUPPORT.md
|-- SKILL.md
|-- .github/
|   |-- CODEOWNERS
|   |-- dependabot.yml
|   |-- PULL_REQUEST_TEMPLATE.md
|   |-- ISSUE_TEMPLATE/
|   |   |-- bug_report.yml
|   |   |-- config.yml
|   |   |-- feature_request.yml
|   |-- workflows/
|       |-- ci.yml
|-- references/
|   |-- decision-matrix.md
|   |-- magi-framework.md
|   |-- method-patterns.md
|-- prompts/
|   |-- 01-implement-method.md
|   |-- 02-robustness-checks.md
|-- scripts/
|   |-- risk-matrix-gen.py
|   |-- validate-project.py
|   |-- weighted-scoring.py
```

## Responsibility Boundaries

| Layer | Files | Responsibility |
|---|---|---|
| Runtime index | `SKILL.md` | Trigger detection, routing, quick references, output contract |
| Runtime knowledge | `references/` | Framework definitions, matrices, schemas, and implementation patterns |
| Executable tools | `scripts/` | Deterministic calculations and command-line interfaces |
| User artifacts | `prompts/` | Portable prompts that a user can paste into any AI chat |
| Repository governance | Root standard files | Licensing, contribution, security, community, editor, and project metadata |

## SKILL.md Contract

`SKILL.md` must contain these sections in this order:

1. `Trigger Conditions`
2. `Capability Index`
3. `Quick-Reference: Output Format`
4. `Quick-Reference: Voting Rules`
5. `Quick-Reference: Veto Conditions`
6. `File Routing Map`

It must not contain implementation code, long procedures, prompt bodies, or
references to prompt files as agent-auto-invocation targets. Detailed content
must be loaded progressively from `references/`.

## references/method-patterns.md Contract

This file is the single source of truth for:

- Data schemas and validation rules
- Function and class signatures
- Runnable implementation templates
- CLI flags and exit-code contracts
- Extension patterns for personas, risk domains, and output formats

Each pattern must document parameters, return values, side effects, errors,
and a minimal verification example. Scripts may implement these patterns, but
their behavior must remain aligned with this reference.

## prompts/ Dual-Mode Contract

The two prompt files have a separate user-facing mode:

| File | Required placeholders | Purpose |
|---|---|---|
| `01-implement-method.md` | `{{SCENARIO}}`, `{{METHOD}}`, `{{CONSTRAINTS}}` | Implement a decision method from a scenario |
| `02-robustness-checks.md` | `{{DECISION}}`, `{{CONTEXT}}`, `{{FOCUS_AREAS}}` | Red-team an existing decision or plan |

Each prompt must be self-contained, portable, dependency-free, and written in
plain Markdown. It must define context, instructions, expected output, and
customization notes. It must not require the target AI to read `SKILL.md`,
`references/`, or `scripts/`.

## Harness Engineering Contract

Every executable module must define:

- Accepted input types and validation behavior
- Stable output shape and formatting
- Side effects and generated files
- Exit codes for success, input errors, and runtime errors
- Standard-library dependencies, unless an approved dependency is documented

Core logic must be deterministic for identical input. Avoid timestamps,
randomness, hidden environment state, and implicit network access. Functions
must be importable and testable without invoking the CLI.

## Standardization Checklist

Before accepting a change, verify:

- Headings, tables, naming, and status labels follow repository conventions.
- Generic logic uses parameters instead of industry-specific assumptions.
- Each file has one responsibility and references are independently readable.
- `SKILL.md` remains compact and detailed material is progressively disclosed.
- Scripts expose `argparse` CLIs and return non-zero exit codes on errors.
- `scripts/validate-project.py` passes before a release is created.
- All text is English and contains no emoji characters.
- All paths in documentation use the exact case-sensitive names in the tree.
- Root GitHub-standard files remain present and linked where appropriate.

## Maintenance Workflow

1. Update the relevant reference or script before changing the index.
2. Keep reusable templates in `references/method-patterns.md`.
3. Keep user-copyable prompts independent from runtime routing.
4. Update `SKILL.md`, `README.md`, `CONTRIBUTING.md`, and `CHANGELOG.md`
   when a public file or behavior changes.
5. Review the complete tree and run the existing script checks before merging.
6. Run `python scripts/validate-project.py` before creating a release.

When a new module is needed, place it in the narrowest appropriate layer,
document its interface, add its routing entry, and update this contract only
when the public structure changes.
