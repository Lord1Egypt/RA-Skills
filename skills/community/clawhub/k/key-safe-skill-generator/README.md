# Key‑Safe Skill Generator (Zero‑Exposure Edition)

A documentation‑only meta‑skill that teaches AI agents how to **design, generate and validate** zero‑exposure skills on MGC Blackbox 1.5.4.

It does not run anything itself. It produces skills — and, more importantly, it produces a **specification and a checklist** that make those skills verifiably correct.

---

## What's New in v2.0.0

Repositioned from "a description of MGC features" to "a generation specification with an acceptance checklist".

- **Removed the duplication.** The MCP tool table, the error‑code table and the sealing‑mechanism walkthrough are gone — those are delegated to the upstream spec, loaded live via `mgc_skill`. This skill stays focused on the part the spec cannot give you.
- **Corrected the templates.** The credential read no longer uses the non‑existent `data_field` key, no longer sends `action: "run"` with a config read, and `mgc_run` no longer claims `diff_1` is schema‑required. All three were runtime‑breaking in generated skills.
- **Corrected the sealing example.** 1.5.4 ext keys carry no underscore, the capsule is imported as a whole file via `mgc_save_file`, and `output_dir` is required.
- **Corrected the deletion guidance.** `mgc_delete` exists since 1.5.4, with the string confirmation flag and the user‑approval rule.
- **Three production shapes** — single script, workflow package, sealed delivery package — each with its own requirements.
- **Four layer specifications** — credential, script, workflow package, sealed delivery.
- **An acceptance checklist** (§8) that makes a generated skill objectively verifiable instead of a matter of opinion.
- **A delivery shape decision table** — local, cross‑node p2p, public free mode.
- **Banned patterns named explicitly** — the fatal path check, computed argparse defaults, extension‑less `diff_3`.

---

## What This Skill Does

- Defines what "zero‑exposure" means as a **checkable five‑point contract**
- Specifies each layer a generated skill must satisfy
- Provides a **six‑step generation flow** from operation to validated package
- Provides **corrected templates** — SKILL.md skeleton, local script skeleton, manifest skeleton
- Provides an **acceptance checklist** for validating a generated skill before delivery
- Provides **anti‑patterns** with the correct practice for each

---

## Quick Start

### 1. Install and start MGC

```bash
pip install mgc-blackbox>=1.5.4
mgc
```

REST API at `http://127.0.0.1:57219`, WebUI at `http://127.0.0.1:57218`.

### 2. Load the upstream spec when you need it

```text
Tool: mgc_skill
```

Returns the live MGC skill specification — tool schemas, `ext` field semantics, error codes, sealing internals. Use it as the authority; this skill as the generation rules.

### 3. Follow the six‑step flow

```text
1. Identify the operation          → what the skill does, for whom
2. Design the credential record    → info_type, info_owner, required fields
3. Choose the production shape     → single script / workflow package / sealed
4. Write the script(s)             → using the layer specs
5. Assemble the skill package      → SKILL.md + manifest.json + optional script
6. Validate against the checklist → the acceptance checklist
```

### 4. Validate before delivery

Work through the acceptance checklist in SKILL.md §8. Every item is objectively checkable — a generated skill that passes it will actually run on MGC 1.5.4.

---

## Acceptance Checklist at a Glance

The five points that define the contract (§2.3):

| # | Test |
|---|---|
| 1 | No credential value appears in any file the AI can read |
| 2 | The credential is referenced by `info_owner` only |
| 3 | The credential is fetched at runtime, inside the boundary |
| 4 | The outcome reaches the AI through a result file |
| 5 | No credential value is passed as a runtime parameter |

The full checklist additionally covers the script layer (literal defaults, `parse_known_args`, `RESULT_FILE:` contract, no fatal path check), the workflow package layer (`diff_2` + extension‑bearing `diff_3`, recognised call forms, re‑save rule), the sealed delivery layer (`output_dir`, multi‑line PEM, capsule import, receiver version floor) and package hygiene.

---

## MCP Tools

| Tool | Purpose |
|---|---|
| `mgc_save` | Store a credential or a script |
| `mgc_save_file` | Store a workflow folder; import a sealed capsule or package |
| `mgc_run` | Execute a stored script — required: `info_owner` |
| `mgc_find` | Fuzzy search by `info_owner` / diff fields — no `info_type` filter |
| `mgc_list` | Enumerate entries (metadata only) |
| `mgc_delete` | Delete a credential or script — `confirm_folder_delete="true"` is a **string** and requires explicit user approval |
| `mgc_seal` | Seal a script — required: `info_owner`, `output_dir` |
| `mgc_seal_package` | Seal a workflow package — required: `info_owner`, `diff_2`, `output_dir` |
| `mgc_package` | Export a folder as a plaintext archive |
| `mgc_open_webui` | Open the WebUI for the user to store credentials |
| `mgc_get` | **Restricted** — never for credentials; only the `__NODE_PUB__` lookup |
| `mgc_skill` | Load the upstream MGC specification — the authority on tools and error codes |

> ❌ AI must NOT call `mgc_get` on a credential entry — it returns plaintext and breaks zero‑exposure.

---

## Delivery Shapes

| Shape | Who can run it | Source visible? | Use for |
|---|---|---|---|
| **Local** | The authoring node only | Not to the AI, but stored locally | Single‑node skills |
| **p2p mode** — `mgc_seal(..., ext04=<target PEM>)` | Only the node holding the matching private key | No | Delegating to a specific known node |
| **free mode** — `mgc_seal(...)`, **omit `ext04`** | Any MGC 1.5.4+ node | No | Public distribution, marketplaces, demos |

`output_dir` is required for `mgc_seal` / `mgc_seal_package` / `mgc_package` — there is no desktop fallback since 1.5.4. Omitting `ext04` does not raise an error; it silently produces a free‑mode artefact, so verify `ext09` came back as `p2p mode` when node binding was intended.

Every sealed artefact carries its source identity in `ext07` and its mode in `ext09`. Modifying either — even changing whitespace — makes the artefact unrestorable (`UNSEAL_FAILED`), so a recipient cannot re‑seal the source onward to a third party.

---

## When to Use This Skill

- You are building a new skill that touches a credential — SMTP, API key, SSH key, token, database password
- You are reviewing someone else's zero‑exposure skill against the checklist
- A generated skill fails at runtime and you need to know which contract it broke

## When NOT to Use This Skill

- The upstream MGC behaviour is what you need a reference for → use `mgc_skill`
- You want to **use** a zero‑exposure skill, not build one → use that skill directly
- The operation needs no credential → no zero‑exposure machinery is needed

---

## Security Principles

- No plaintext credentials in AI context, prompts, logs or generated files
- Credentials stored encrypted via MGC, read at runtime over the localhost REST API
- Sensitive operations performed only by local scripts inside the MGC boundary
- The AI receives only a result artefact
- No executable code in this skill (safe for automatic approval)

> **Never auto‑confirm.** `mgc_delete` returns a candidate list when more than one record matches. Present it to the user, ask "Delete all N records?", and only after approval re‑invoke with `confirm_folder_delete="true"`. The AI must never set that flag on its own.

> **Scope of the guarantee.** MGC protects content confidentiality. After unsealing, a script runs with the permissions of the user running it — its runtime behaviour is outside MGC's control.

---

## License

MIT
