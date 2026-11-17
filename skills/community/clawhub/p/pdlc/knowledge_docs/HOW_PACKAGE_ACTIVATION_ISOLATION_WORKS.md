# How Package Activation & Isolation Works

**Scope:** Family-wide | **Audience:** Builders, contributors, advanced users

When you install more than one AI-* package into the same workspace, every package's core workflow is always loaded. This document explains how the family keeps those packages from interfering with each other — how you activate the one you want, how the assistant decides which package is "active," and how it refuses to switch packages behind your back.

---

## The Problem It Solves

Each AI-* package (AI-PILC, AI-ADLC, AI-UXD, AI-POLC, AI-DWG, AI-GCE, AI-TGE, AI-PPM, AI-FLO, AI-ILC) installs a core workflow that declares "when the user asks for X, follow me first." With one package installed, that's unambiguous. With several installed in one workspace, two risks appear:

1. **File interference** — could one package overwrite another's output?
2. **Activation interference** — while you are working in one package, could a stray phrase pull a different package into the conversation?

File interference is handled separately by output-folder separation and the ownership model (see Related Documents). This document covers **activation interference** — making sure the right package runs, and only when you mean it to.

---

## Two Layers of Activation

### Layer 1 — Explicit activation keys (deterministic)

Every package has a command-style activation key in the form `_{PKG}_` — the package abbreviation wrapped in single underscores. Typing the key anywhere in a prompt is treated as a **direct order** to activate that package. It wins over everything else immediately, with no guessing and no confirmation.

| Key | Activates | Key | Activates |
|-----|-----------|-----|-----------|
| `_ILC_` | AI-ILC | `_GCE_` | AI-GCE |
| `_PILC_` | AI-PILC | `_TGE_` | AI-TGE |
| `_ADLC_` | AI-ADLC | `_PPM_` | AI-PPM |
| `_UXD_` | AI-UXD | `_FLO_` | AI-FLO |
| `_POLC_` | AI-POLC | `_DWG_` | AI-DWG |

These keys are intentionally distinct from governance **agent shortcuts**, which use a trailing double underscore (for example `IQA__`). A package key (`_PILC_`) and an agent shortcut (`IQA__`) can never be confused for one another.

There is also one family-wide utility key:

| Key | What it does |
|-----|--------------|
| `_ACTIVE_` | Reports which package is currently active and the status of its state marker. Read-only — it never changes anything and never triggers a switch. |

### Layer 2 — Keyword activation (fallback)

If you don't type a key, a package can still activate from the intent of your request — but only for its own tightened scope. For example, AI-ADLC responds to "architecture / system design," while AI-UXD responds to "UX / interface design." Each package explicitly **disclaims** its siblings' keywords, so a request that clearly belongs to one package does not wake the others. When a phrase is genuinely ambiguous across packages (a bare word like "design" or "governance"), the assistant asks which package you mean rather than guessing.

---

## How "Active Package" Is Tracked

Each lifecycle package writes a small state-marker file while it is running — for example `pilc-state.md`, `adlc-state.md`, `uxd-state.md`. A marker whose status is anything other than "complete" means that package's workflow is **in progress**. That marker is how any package can tell, at the start of a turn, whether a sibling is already mid-session.

(Generator-style packages such as AI-DWG and AI-GCE run as one-shot operations rather than long sessions; they still honor the switching rule below so they never hijack an active session.)

---

## The Switching Rule (Non-Negotiable)

A package switch **never** happens without either a direct order or explicit confirmation:

1. **Direct order** — you type an explicit activation key (`_PILC_`, `_ADLC_`, …). The assistant switches immediately.
2. **Otherwise** — if a different package's state marker shows it is active, the assistant does **not** silently take over. It asks first, for example: *"AI-ADLC is currently active. Switch to AI-PILC? (yes / no)"* and proceeds only on an explicit yes.
3. **Ambiguity** — if a request could match more than one installed package by keyword, the assistant asks which to run.
4. **Announce the switch** — whenever a switch actually happens, the **first line** of that response names the now-active package, for example:

   ```
   Active package: AI-PILC
   ```

This means you always know which package is responding, and you are never moved out of an active workflow by accident.

---

## Optional Runtime Reinforcement (Opt-In Hook)

The switching rule above lives in each package's steering, so the assistant follows it as a matter of instruction. For teams that want an extra, mechanical reminder, the family ships an **opt-in** hook: `package-activation-guard`.

- It is a `promptSubmit` hook that re-checks the switching rule on every prompt.
- It ships **disabled** — you turn it on by setting `"enabled": true` or toggling it in the Hooks UI.
- It is family-wide and works regardless of which packages are installed.

Because it fires on every prompt, it is most useful in workspaces where several AI-* packages genuinely coexist; in a single-package workspace it adds little and is best left off.

---

## Worked Example

A workspace has AI-PILC and AI-ADLC installed. You are halfway through initiating a project (`pilc-state.md` shows status "in-progress").

- You type: *"now let's think about the system design."*
  → The assistant sees AI-PILC is active and the request leans toward AI-ADLC. It does **not** switch. It asks: *"AI-PILC is currently active. Switch to AI-ADLC? (yes / no)"*
- You reply *"yes"* (or instead type `_ADLC_`).
  → The assistant switches and opens with `Active package: AI-ADLC`.
- Later you type `_ACTIVE_`.
  → The assistant reports that AI-ADLC is active, with its marker status — and does nothing else.

---

## Related Documents

- [`HOW_STEERING_FILE_LOADING_WORKS.md`](HOW_STEERING_FILE_LOADING_WORKS.md) — why all core workflows are always loaded
- [`HOW_STATE_FILES_WORK.md`](HOW_STATE_FILES_WORK.md) — the markers that signal an active session
- [`HOW_CHAIN_HANDOFF_WORKS.md`](HOW_CHAIN_HANDOFF_WORKS.md) — how one package's output feeds the next
- [`PATTERN_MARKER_FILE_DETECTION.md`](PATTERN_MARKER_FILE_DETECTION.md) — the marker-detection pattern this relies on
- [`HOW_PROVENANCE_TRACKING_WORKS.md`](HOW_PROVENANCE_TRACKING_WORKS.md) — file-level ownership that prevents output overwrite
- [`ANATOMY_OF_A_HOOK.md`](ANATOMY_OF_A_HOOK.md) — structure of the opt-in activation-guard hook
- [`REFERENCE_MAP_MARKERS.md`](REFERENCE_MAP_MARKERS.md) — every package's state-marker filename

---

*Knowledge Document | Created: 2026-06-15 | Author: [Mohammad Maheri](https://www.linkedin.com/in/mohammad-maheri-8399565b)*
